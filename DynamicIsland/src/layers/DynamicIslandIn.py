from layers.music import SoundControl
import flet as ft


class DynamicIislandIn(ft.Container):
    """Container for the dynamic island with animations"""
    def __init__(self):
        super().__init__()
        self.opacity = 0
        self.bgcolor = "black"
        self.animate_param = ft.Animation(duration=300, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
        self.animate_opacity = self.animate_param
        self.animate = self.animate_param
        self.content = SoundControl()
        self.alignment = ft.alignment.center 
    

    async def animate_layer(self, show: bool = True):
        if show:
            self.opacity = 1
        else:
            self.opacity = 0
        self.update()
    
    async def change_bgcolor(self, bgcolor: str):
        self.bgcolor = bgcolor
        self.update()