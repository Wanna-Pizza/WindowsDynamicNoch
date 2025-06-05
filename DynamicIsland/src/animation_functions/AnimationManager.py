from convert_frames import convert_frames_to_dict
class AnimationManager:
    """Manages multiple animations for dynamic island"""
    
    def __init__(self, scale_factor=70):
        self.animations = {}
        self.scale_factor = scale_factor
        self.current_animation = None
    
    def load_animation(self, name, file_prefix):
        """Load animation data from file and store it in animations dictionary"""
        self.animations[name] = convert_frames_to_dict(file_prefix)
        return self.animations[name]
    
    def get_animation(self, name):
        """Get animation data by name"""
        return self.animations.get(name)
    
    def set_current_animation(self, name):
        """Set the current animation to use"""
        if name in self.animations:
            self.current_animation = name
            return True
        return False
    
    def get_frame_data(self, name, frame_number):
        """Get specific frame data from named animation"""
        if name in self.animations and frame_number in self.animations[name]:
            frame_data = self.animations[name][frame_number]
            return {
                'width': float(frame_data['y']) * self.scale_factor,
                'height': float(frame_data['z']) * self.scale_factor
            }
        return None
    
    def frame_count(self, name):
        """Get the total number of frames in an animation"""
        if name in self.animations:
            return max(self.animations[name].keys())
        return 0