import base64
import json
import os
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus
)
from winrt.windows.storage.streams import Buffer, InputStreamOptions
import asyncio
from PIL import Image
import io
from datetime import timedelta
from typing import Optional, Tuple


class MediaPlayerController:
    def __init__(self):
        self.session = None
        self.all_sessions = []
    
    async def initialize(self):
        try:
            manager = await SessionManager.request_async()
            self.all_sessions = manager.get_sessions()
            if self.all_sessions and self.all_sessions.size > 0:
                self.session = await self.get_best_session()
                return True
            return False
        except:
            return False
    
    async def get_best_session(self):
        if not self.all_sessions:
            return None
            
        playing_sessions = []
        paused_sessions = []
        
        for session in self.all_sessions:
            try:
                status = session.get_playback_info().playback_status
                if status == GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING:
                    playing_sessions.append(session)
                else:
                    paused_sessions.append(session)
            except:
                continue
        
        # Prioritize playing sessions
        if playing_sessions:
            return playing_sessions[0]
            
        # Keep current if exists
        if self.session:
            current_id = self.session.source_app_user_model_id
            for session in self.all_sessions:
                if session.source_app_user_model_id == current_id:
                    return self.session
        
        return paused_sessions[0] if paused_sessions else self.all_sessions[0]

    async def get_current_track_info(self) -> Optional[dict]:
        if not self.session:
            return None
        try:
            info = await self.session.try_get_media_properties_async()
            if not info:
                return None
            timeline = self.session.get_timeline_properties()
            return {
                'title': info.title or "Unknown",
                'artist': info.artist or "Unknown",
                'album': info.album_title or "Unknown",
                'position': self._format_timedelta(timeline.position),
                'duration': self._format_timedelta(timeline.end_time),
                'playback_status': self.session.get_playback_info().playback_status.name,
                'session_id': self.session.source_app_user_model_id
            }
        except:
            return None

    async def get_current_cover_base64(self) -> Optional[str]:
        if not self.session:
            return None
        try:
            media_info = await self.session.try_get_media_properties_async()
            if not media_info or not media_info.thumbnail:
                return None
            stream = await media_info.thumbnail.open_read_async()
            buffer = Buffer(stream.size)
            await stream.read_async(buffer, stream.size, InputStreamOptions.READ_AHEAD)
            data = bytes(buffer)
            stream.close()
            image = Image.open(io.BytesIO(data))
            if image.mode == "RGBA":
                image = image.convert("RGB")
            byte_array = io.BytesIO()
            image.save(byte_array, format="JPEG")
            return base64.b64encode(byte_array.getvalue()).decode('utf-8')
        except:
            return None
    
    def _format_timedelta(self, td: timedelta) -> str:
        total_seconds = int(td.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    async def play(self):
        if self.session:
            await self.session.try_play_async()

    async def pause(self):
        if self.session:
            await self.session.try_pause_async()

    async def toggle_play_pause(self):
        if self.session:
            status = self.session.get_playback_info().playback_status
            if status == GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING:
                await self.pause()
            else:
                await self.play()

    async def next_track(self):
        if self.session:
            await self.session.try_skip_next_async()

    async def previous_track(self):
        if self.session:
            await self.session.try_skip_previous_async()

    async def get_timeline(self) -> Optional[Tuple[float, float]]:
        if not self.session:
            return None
        timeline = self.session.get_timeline_properties()
        return timeline.position.total_seconds(), timeline.end_time.total_seconds()

    async def set_position(self, seconds: float):
        if self.session:
            await self.session.try_change_playback_position_async(int(seconds * 10_000_000))
            
    async def monitor_track_changes(self, change_callback=None, position_callback=None, 
                               playback_state_callback=None, on_nothing=None, interval=0.1):
        if not await self.initialize():
            if on_nothing:
                await on_nothing()
        else:
            if self.session:
                current_track = await self.get_current_track_info()
                current_cover = await self.get_current_cover_base64()
                if current_track and change_callback:
                    await change_callback(current_track, current_cover)
                if current_track and playback_state_callback:
                    await playback_state_callback(current_track['playback_status'] == 'PLAYING')
        
        last_track = None
        last_session_id = None
        last_playback_state = None
        last_cover = None
        
        while True:
            try:
                prev_session_id = self.session.source_app_user_model_id if self.session else None
                await self.initialize()
                new_session_id = self.session.source_app_user_model_id if self.session else None

                if prev_session_id != new_session_id:
                    if on_nothing:
                        await on_nothing()
                    print(f"Session changed: {prev_session_id} -> {new_session_id}")
                    last_track = None
                    last_session_id = None
                    last_playback_state = None
                    last_cover = None
                
                if not self.session:
                    if on_nothing:
                        await on_nothing()
                    await asyncio.sleep(interval)
                    continue

                current_track = await self.get_current_track_info()
                if not current_track:
                    if on_nothing:
                        await on_nothing()
                    await asyncio.sleep(interval)
                    continue
                
                current_cover = await self.get_current_cover_base64()

                if (not last_track or 
                    last_session_id != current_track['session_id'] or
                    current_track['title'] != last_track['title'] or
                    current_track['artist'] != last_track['artist'] or
                    current_cover != last_cover):
                    if change_callback:
                        await change_callback(current_track, current_cover)
                    last_track = current_track
                    last_session_id = current_track['session_id']
                    last_cover = current_cover

                if (last_playback_state != current_track['playback_status'] and 
                    playback_state_callback):
                    await playback_state_callback(current_track['playback_status'] == 'PLAYING')
                    last_playback_state = current_track['playback_status']
                    
            except Exception as e:
                print(f"Error in monitor_track_changes: {e}")
                if "RPC server" in str(e):
                    self.session = None
                    if on_nothing:
                        await on_nothing()
                
            await asyncio.sleep(interval)

