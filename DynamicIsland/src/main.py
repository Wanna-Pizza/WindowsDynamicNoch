import asyncio
import time
import flet as ft
import win32gui
import win32con
import ctypes
from ctypes import windll
from functions.media_checker import MediaPlayerController
from dynamic_island.DynamicIslandClass import ControlDynamicIsland

def find_window_by_name(window_name):
    return win32gui.FindWindow(None, window_name)

original_styles = {}

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.init_page()
        self.page.run_task(self.main)
    
    def init_page(self):
        self.page.window.frameless = True
        self.page.window.skip_task_bar = True
        self.page.window.height = 500
        self.page.window.width = 500
        self.page.window.resizable = False
        self.page.title = "Dynamic Island"

        self.page.update()
        time.sleep(1)
        
        self.page.window.always_on_top = True
        self.page.bgcolor = 'transparent'
        self.page.window.bgcolor = 'transparent'
        self.page.padding = 0
        self.page.update()

        self.hwnd = find_window_by_name(self.page.title)
        self.setClickthrough()

    def setClickthrough(self):
        user32 = windll.user32
        gdi32 = windll.gdi32
        screen_width = user32.GetSystemMetrics(0)
        
        win_width = 500
        center_win_x = screen_width // 2
        win_rect_left = center_win_x - win_width // 2

        self.page.window.left = win_rect_left
        self.page.window.top = 0
        self.page.update()

        rect_width, rect_height = 300, 60
        center_x = screen_width // 2
        rect_left = center_x - rect_width // 2
        
        region_left = rect_left - win_rect_left
        region_right = region_left + rect_width
        region = gdi32.CreateRectRgn(region_left, 0, region_right, rect_height)

        try:
            if self.hwnd not in original_styles:
                original_styles[self.hwnd] = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)

            styles = original_styles[self.hwnd]
            styles |= win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOOLWINDOW
            styles &= ~win32con.WS_EX_APPWINDOW
            
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, styles)
            win32gui.SetLayeredWindowAttributes(self.hwnd, 0, 255, win32con.LWA_ALPHA)
            win32gui.SetWindowRgn(self.hwnd, region, True)
            
            user32.SetWindowPos(
                self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
            )
        except Exception as e:
            print(f"Error setting clickthrough: {e}")

    async def main(self):
        self.controller = MediaPlayerController()
        self.app = ControlDynamicIsland(controller_media=self.controller)
        self.page.add(self.app)
        self.page.update()
        
        await self.start_monitoring_sound()

    async def start_monitoring_sound(self):
        async def on_track_change(track_info, cover_base64):
            if cover_base64:
               await self.app.change_track(cover_base64)

        async def on_playback_state_change(is_playing):
            self.app.playing_pause(is_playing)
        
        try:
            await self.controller.monitor_track_changes(
                change_callback=on_track_change,
                playback_state_callback=on_playback_state_change,
                on_nothing=self.app.reset_animation,
                interval=0.05
            )
        except Exception as e:
            print(f"Monitoring stopped due to error: {e}")

if __name__ == "__main__":
    ft.app(target=MainApp,assets_dir="assets")