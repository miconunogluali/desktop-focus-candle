import tkinter as tk
from tkinter import messagebox
import random
import math

class AdvancedDesktopCandle:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Candle")
        
        # Window settings
        self.root.overrideredirect(True)  
        self.root.attributes('-topmost', True)  
        
        # Screen dimensions and positioning
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.width = 70
        self.height = 170
        
        # You can adjust the candle's position according to your screen.
        pos_x = screen_width - self.width +340  
        pos_y = screen_height - self.height +160

        self.root.geometry(f"{self.width}x{self.height}+{pos_x}+{pos_y}")
        
        # Transparency settings
        self.transparent_color = '#000001'
        self.root.config(bg=self.transparent_color)
        self.root.attributes('-transparentcolor', self.transparent_color)

        # --- TIMER SETTINGS ---
        self.total_minutes = random.randint(1, 2)
        self.total_seconds = self.total_minutes * 60
        self.seconds_left = self.total_seconds

        # Candle Melting Variables
        self.base_y = self.height - 10 
        self.max_candle_height = 110 
        self.center_x = self.width // 2
        self.current_top_y = self.base_y - self.max_candle_height

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, 
                                bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack()

        # Color Palette
        self.color_body = "#FDF5E6"    # Candle Wax
        self.color_shadow = "#E0D7C6"  # 3D Shadow
        self.color_pool = "#FFFFF0"    # Melted Top Wax
        self.color_wick = "#222222"    # Candle Wick

        # Drawing elements
        self.body = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.color_body, outline="")
        self.shadow = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.color_shadow, outline="")
        self.top_oval = self.canvas.create_oval(0, 0, 0, 0, fill=self.color_pool, outline=self.color_shadow)
        self.wick = self.canvas.create_line(0, 0, 0, 0, fill=self.color_wick, width=2)
        
        self.outer_flame = self.canvas.create_polygon(0, 0, 0, 0, smooth=True, fill="#FF4500") 
        self.inner_flame = self.canvas.create_polygon(0, 0, 0, 0, smooth=True, fill="#FFD700") 

        # Animation variables
        self.smoke_particles = []
        self.animation_counter = 0

        # Bind right-click to close the application
        self.root.bind("<Button-2>", lambda e: self.root.destroy())
        
        # Initialize loops
        self.update_timer()      # Melting logic
        self.update_animation()  # Flame flicker and smoke logic

    def update_timer(self):
        """Manages the melting of the candle (Runs every 1 second)"""
        if self.seconds_left > 0:
            self.seconds_left -= 1
            
            # Calculate the melting ratio
            ratio = 1.0 - (self.seconds_left / self.total_seconds)
            
            # Update the top Y position based on melting progress
            self.current_top_y = (self.base_y - self.max_candle_height) + (self.max_candle_height * ratio)
            
            self.refresh_drawing()
            self.root.after(1000, self.update_timer)
        else:
            self.finish_effect()

    def refresh_drawing(self):
        """Updates the visual height of the candle"""
        cx = self.center_x
        radius = 25 
        top = self.current_top_y
        bottom = self.base_y
        oval_h = 10 # Perspective oval height

        # Update Body
        self.canvas.coords(self.body, cx - radius, top, cx + radius, bottom)
        # Update Shadow 
        self.canvas.coords(self.shadow, cx, top, cx + radius, bottom)
        # Update Top Wax Pool
        self.canvas.coords(self.top_oval, cx - radius, top - oval_h/2, cx + radius, top + oval_h/2)
        # Update Wick
        self.canvas.coords(self.wick, cx, top, cx, top - 10)

    def update_animation(self):
        """Flame flickering and smoke movement (Approx. 30 FPS)"""
        if self.seconds_left <= 0: return

        self.animation_counter += 0.2
        cx = self.center_x
        wick_tip = self.current_top_y - 5
        
        # Sine wave movements for wind and 'breathing' effect
        wind = math.sin(self.animation_counter) * 1.5
        breath = math.cos(self.animation_counter * 2) * 1.5

        def get_flame_coords(w, h, dy):
            base_y = wick_tip + dy
            tip_y = base_y - h - breath
            mid_y = base_y - (h/3)
            return [
                cx, base_y,                         # Bottom center
                cx - w + (wind * 0.5), mid_y,       # Left bulge
                cx + wind, tip_y,                   # Top tip
                cx + w + (wind * 0.5), mid_y        # Right bulge
            ]

        # Update flame shapes
        self.canvas.coords(self.outer_flame, *get_flame_coords(9, 26, 2))
        self.canvas.coords(self.inner_flame, *get_flame_coords(5, 15, 1))

        # Randomly generate smoke particles
        if random.random() < 0.05:
            self.add_smoke(cx + wind, wick_tip - 25)
            
        self.process_smoke()
        
        self.root.after(30, self.update_animation)

    def add_smoke(self, x, y):
        """Creates a smoke particle"""
        size = random.randint(2, 5)

        # Initial gray smoke
        particle = self.canvas.create_oval(x, y, x + size, y + size, fill="#CCCCCC", outline="")
        self.smoke_particles.append([particle, x, y, 40]) # 40 frames lifespan

    def process_smoke(self):
        """Handles smoke movement and fading"""
        to_remove = []
        for i, p in enumerate(self.smoke_particles):
            obj, x, y, life = p
            if life > 0:
                y -= 1 # Move upwards
                x += math.sin(y/10 + self.animation_counter) * 0.5 # Oscillate
                
                # Fading color calculation
                gray_val = int(180 + (40 - life) * 1.8)
                hex_color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
                
                self.canvas.coords(obj, x, y, x + 4, y + 4)
                self.canvas.itemconfigure(obj, fill=hex_color)
                self.smoke_particles[i][3] -= 1
            else:
                to_remove.append(i)
        
        for i in reversed(to_remove):
            self.canvas.delete(self.smoke_particles[i][0])
            del self.smoke_particles[i]

    def finish_effect(self):
        """Cleanup and notification when timer expires"""
        self.canvas.delete(self.outer_flame)
        self.canvas.delete(self.inner_flame)
        messagebox.showinfo("Well Done", f"Focus session complete! {self.total_minutes} min.")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
  

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = AdvancedDesktopCandle(root)
    root.mainloop()