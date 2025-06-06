import base64
import io
import flet as ft
from PIL import Image

class SoundControl(ft.Container):
    """Container for sound control buttons"""

    def __init__(self, music_cover_base64 = None,on_pause=None,on_play=None, on_next=None, on_prev=None):
        super().__init__()
        self.music_cover_base64 = music_cover_base64
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER
        self.is_playing = False
        self.on_pause = on_pause
        self.on_play = on_play
        self.on_next = on_next
        self.on_prev = on_prev
        self.content = self.__content()
       
    
    def setup_callbacks(self, on_play=None, on_next=None, on_prev=None, on_pause=None):
        print(on_play)
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_next = on_next
        self.on_prev = on_prev
        self.content = self.__content()
        self.update()
    
    def toggle_functions_play_pause(self, is_playing):
        if is_playing:
            self.play_pause.content.name = ft.Icons.PAUSE
            self.play_pause.on_click = self.__on_pause
            self.is_playing = False
        else:
            self.play_pause.content.name = ft.Icons.PLAY_ARROW
            self.play_pause.on_click = self.__on_play
            self.is_playing = True
        self.play_pause.update()
    
    
    def __on_play(self, e):
        if self.on_play:
            self.is_playing = True
            self.toggle_functions_play_pause(self.is_playing)
            async def on_play():
                await self.on_play()
            self.page.run_task(on_play)
    def __on_pause(self, e):
        """Callback for pause button click."""
        if self.on_play:
            self.is_playing = False
            self.toggle_functions_play_pause(self.is_playing)
            async def on_pause():
                await self.on_pause()
            self.page.run_task(on_pause)
    def __on_next(self, e):
        """Callback for next button click."""
        if self.on_next:
            async def on_next():
                await self.on_next()
            self.page.run_task(on_next)
    def __on_prev(self, e):
        """Callback for previous button click."""
        if self.on_prev:
            async def on_prev():
                await self.on_prev()
            self.page.run_task(on_prev)


    @staticmethod
    def get_contrast_color(base64_image: str) -> str:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        image = image.convert("RGB")
        width, height = image.size
        
        center_x, center_y = width // 2, height // 2
        
        square_size = 30
        left = max(center_x - square_size // 2, 0)
        top = max(center_y - square_size // 2, 0)
        right = min(center_x + square_size // 2, width)
        bottom = min(center_y + square_size // 2, height)
        
        cropped_image = image.crop((left, top, right, bottom))
        pixels = list(cropped_image.getdata())
        
        avg_pixel = tuple(sum(channel) // len(pixels) for channel in zip(*pixels))
        
        brightness = (avg_pixel[0] * 0.299 + avg_pixel[1] * 0.587 + avg_pixel[2] * 0.114)
        
        color = 'black' if brightness > 150 else 'white,0.8'  # Порог можно настроить
        return color

    
    def change_color_buttons(self, color):
        """Change the color of the control buttons."""
        self.play_pause.content.color = color
        self.next_track.content.color = color
        self.prev_track.content.color = color
        self.next_track.content.update()
        self.prev_track.content.update()
        self.play_pause.content.update()

    def change_music_cover(self, music_cover_base64):
        self.music_cover_base64 = music_cover_base64
        self.music_cover.content = ft.Image(src_base64=self.music_cover_base64)
        self.image_bg_cover.src_base64 = self.music_cover_base64
        self.image_bg_cover.update()
        self.change_color_buttons(self.get_contrast_color(self.music_cover_base64))
        self.music_cover.update()
    
    def __content(self):
        self.music_cover = ft.Container(
            ft.Image(src_base64=self.music_cover_base64),
            alignment=ft.alignment.center_left,
            border_radius=ft.border_radius.only(bottom_left=10)
        )
        self.play_pause = ft.Container(
            ft.Icon(ft.Icons.PAUSE,color="white,0.8"),
            alignment=ft.alignment.center,
            on_click=self.__on_play,
        )
        self.next_track = ft.Container(
            ft.Icon(ft.Icons.SKIP_NEXT,color="white,0.8"),
            alignment=ft.alignment.center,
            on_click=self.__on_next,
        )

        self.prev_track = ft.Container(
            ft.Icon(ft.Icons.SKIP_NEXT,color="white,0.8"),
            scale=-1,
            on_click=self.__on_prev,
        )

        self.image_bg_cover = ft.Image(scale=10)
        self.stack_bg = ft.Stack([
            self.image_bg_cover,
            ft.Container(
                width=500,
                height=500,
                blur=ft.Blur(
                    sigma_x=50,
                    sigma_y=50,
                    tile_mode=ft.BlurTileMode.REPEATED
                ),
            )
        ],alignment=ft.alignment.center)

        self.whole_stack = ft.Stack([
            self.stack_bg,
            
            ft.Container(self.music_cover,padding=4),
            ft.Row([
                self.prev_track,
                self.play_pause,
                self.next_track,    
            ],alignment=ft.MainAxisAlignment.CENTER),

        ])

        return self.whole_stack
