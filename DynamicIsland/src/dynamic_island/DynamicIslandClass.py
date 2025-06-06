import asyncio
import time
import flet as ft
from animation_functions.AnimationManager import AnimationManager
from layers.DynamicIslandIn import DynamicIislandIn
from layers.music import SoundControl
from functions.media_checker import MediaPlayerController
import base64
import io
from PIL import Image
import numpy as np
from collections import Counter

class DynamicIslandApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER
        self.alignment = ft.alignment.top_center
        self.animation_manager = AnimationManager(scale_factor=70)
        self.animation_manager.load_animation("open", "frames_open")
        self.animation_manager.load_animation("callback", "callback")
        self.animation_manager.load_animation("close", "callback_out")
        self.animation_manager.load_animation("show_side", "show_side")
        self.animation_manager.load_animation("side_hovered", "side_hovered")
        self.animation_manager.load_animation("side_unhovered", "side_unhovered")
        self.animation_manager.set_current_animation("open")
        
        initial_frame = self.animation_manager.get_frame_data("open", 1)
        self.base_height = initial_frame['height']
        self.base_width = initial_frame['width']
        self.height_dynamic = initial_frame['height']
        self.width_dynamic = initial_frame['width']
        self.is_hovered = False
        self.is_playing = False
        self.content = self.__content()
        # self.init_container()
        
    def update_layout(self):
        """Update layout dimensions based on current width/height"""
        self.container.height = self.height_dynamic
        self.container.width = self.width_dynamic
        self.container.update()

    def layout(self):
        """Create the layout for the dynamic island"""
        height = self.height_dynamic
        width = self.width_dynamic
        animate = ft.Animation(duration=2)
        
        self.left = ft.Container(width=height, animate=animate, padding=10)
        self.middle = ft.Container(width=width-(height*2), animate=animate, padding=10)
        self.right = ft.Container(width=height, animate=animate, padding=10)

    def __play_animation(self, name, speed=0.01, start_frame=1, end_frame=None):
        """Play a specific animation by name asynchronously"""
        anim_data = self.animation_manager.get_animation(name)
        if not anim_data:
            print(f"Animation '{name}' not found")
            return False
            
        if end_frame is None:
            end_frame = self.animation_manager.frame_count(name)
        
        for frame_number in range(start_frame, end_frame + 1):
            frame_data = self.animation_manager.get_frame_data(name, frame_number)
            if frame_data:
                self.width_dynamic = frame_data['width']
                self.height_dynamic = frame_data['height']
                self.update_layout()
                time.sleep(0.01)
        return True

    def play_animation(self, name, speed=0.01, start_frame=1, end_frame=None):
            return self.page.run_thread(self.__play_animation,name, speed, start_frame, end_frame)


    async def reset_animation(self):
        """Reset the animation asynchronously"""
        animate = ft.Animation(duration=300, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
        self.container.animate = animate
        self.container.update()
        await asyncio.sleep(0.02)
        self.width_dynamic = self.base_width
        self.height_dynamic = self.base_height
        self.update_layout()
        await self.layer.animate_layer(False)  # Assumes animate_layer is async
        await asyncio.sleep(0.3)
        new_animate = ft.Animation(duration=2, curve=ft.AnimationCurve.EASE_IN)
        self.container.animate = new_animate
        self.container.update()
        return True

    async def show_sound_control(self):
        """Show sound control animation asynchronously"""
        await self.layer.animate_layer(True)  # Assumes animate_layer is async
        await self.play_animation("show_side")

    async def run_animation(self):
        """Run the current animation asynchronously"""
        current_anim = self.animation_manager.current_animation
        if current_anim:
            await self.play_animation(current_anim)

    def __content(self):
        """Initialize the main UI"""
        self.layer = DynamicIislandIn()  # Fixed typo: DynamicIislandIn -> DynamicIslandIn
        self.container = ft.Container(
            width=self.width_dynamic,
            height=self.height_dynamic,
            bgcolor="black",
            shadow=ft.BoxShadow(
                spread_radius=0,blur_radius=20,
                color="blackm,0.2"
            ),
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.only(
                bottom_left=self.height_dynamic/2,
                bottom_right=self.height_dynamic/2
            ), 
            content=self.layer,
            animate=ft.Animation(duration=2)
        )
        return self.container
    
    async def __on_hover(self, e):
        """Handle hover events asynchronously"""
        self.is_hovered = not self.is_hovered
        if self.is_hovered:
            self.play_animation("side_hovered") if self.is_playing else self.play_animation("callback")
        else:
            self.play_animation("side_unhovered") if self.is_playing else self.play_animation("close")

    async def __on_click(self, e):
        """Handle click events asynchronously"""
        self.container.on_hover = None
        self.is_hovered = False
        self.update_layout()
        await asyncio.sleep(0.02)
        self.play_animation("close")
        self.play_animation("open")
        # self.container.on_hover = self.__on_hover
        self.update_layout()
    
    def reset_hover(self):
        """Reset hover state"""
        self.container.on_hover = None
        self.container.update()
    def set_hover(self):
        """Set hover state"""
        self.container.on_hover = self.__on_hover
        self.container.update()

    # def init_container(self):
        self.container.on_hover = self.__on_hover
        # self.container.on_click = self.__on_click
    
    async def init_sound(self):
        """Initialize sound control animation asynchronously"""
        try:
            await asyncio.sleep(0.5)
            await self.layer.animate_layer()  # Assumes animate_layer is async
            await self.play_animation("show_side")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error in init_sound: {e}")

    def get_dominant_color(self, base64_string):
        try:
            img_data = base64.b64decode(base64_string)
            img = Image.open(io.BytesIO(img_data))
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            img = img.resize((100, 100))
            pixels = np.array(img)
            pixels = pixels.reshape(-1, 3)
            
            brightness = 0.299 * pixels[:, 0] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 2]
            
            brightness_threshold = np.percentile(brightness, 90)
            bright_pixels = pixels[brightness >= brightness_threshold]
            
            if len(bright_pixels) == 0:
                count = Counter(map(tuple, pixels))
                most_common_color = count.most_common(1)[0][0]
                hex_color = '#{:02x}{:02x}{:02x}'.format(*most_common_color)
                return hex_color
                
            count = Counter(map(tuple, bright_pixels))
            most_common_bright_color = count.most_common(1)[0][0]
            
            hex_color = '#{:02x}{:02x}{:02x}'.format(*most_common_bright_color)
            return hex_color
            
        except Exception as e:
            print(f"Error extracting dominant color: {e}")
            return "black"  # Default to white on error


class ControlDynamicIsland(DynamicIslandApp):
    def __init__(self,controller_media=None):
        super().__init__()
        self.controller_media: MediaPlayerController = controller_media
        self.content_control: SoundControl = self.layer.content
    
    def init_control_audio(self):
        self.content_control.setup_callbacks(
            on_play=self.controller_media.play,
            on_pause=self.controller_media.pause,
            on_next=self.controller_media.next_track,
            on_prev=self.controller_media.previous_track
        )

    def playing_pause(self,state):
        self.content_control.toggle_functions_play_pause(state)

    
    async def change_track(self, music_cover_base64):
        layer: DynamicIislandIn = self.layer
        print("ABOBA")
        if self.content_control:
            # self.reset_hover()
            await self.reset_animation()
            self.content_control.change_music_cover(music_cover_base64)
            self.page.run_thread(self.play_animation,"show_side")
            await self.layer.change_bgcolor(self.get_dominant_color(music_cover_base64))
            await asyncio.sleep(0.2)
            await layer.animate_layer()
            self.is_playing = True
            # self.set_hover()
    def did_mount(self):
        self.init_control_audio()
        return super().did_mount()