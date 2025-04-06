import customtkinter
import time
from PIL import Image, ImageTk
import threading
import os
import win32gui

class LoadingScreen(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.geometry("800x800")
        self.configure(fg_color="white")
        self._set_appearance_mode("light")
        
        # Create main frame
        self.frame = customtkinter.CTkFrame(self, fg_color="white")
        self.frame.pack(expand=True, fill="both")

        
        # Load and resize logo
        try:
            self.logo_image = Image.open("logo.png")
            basewidth = 400
            wpercent = (basewidth / float(self.logo_image.size[0]))
            hsize = int((float(self.logo_image.size[1]) * float(wpercent)))
            self.logo_image = self.logo_image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            
            # Create and pack logo label
            self.logo_label = customtkinter.CTkLabel(
                self.frame,
                text="",
                image=self.logo_photo
            )
            self.logo_label.pack(pady=(150, 100))  # Adjusted padding
        except Exception as e:
            # Fallback to text if image loading fails
            self.logo_label = customtkinter.CTkLabel(
                self.frame,
                text="OpenLabel",
                font=("Arial", 48, "bold"),
                text_color="green"
            )
            self.logo_label.pack(pady=(150, 100))  # Adjusted padding
        
        # Create progress bar
        self.progress_bar = customtkinter.CTkProgressBar(
            self.frame,
            width=400,
            height=15,
            corner_radius=10,
            fg_color="#E0E0E0",
            progress_color="green"
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)
        
        # Loading text
        self.loading_label = customtkinter.CTkLabel(
            self.frame,
            text="Loading...",
            font=("Arial", 14),
            text_color="green"
        )
        self.loading_label.pack(pady=(0, 10))
        
        # Center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"600x600+{x}+{y}")
        
        # Remove window decorations
        self.overrideredirect(True)
        self.attributes('-alpha', 0.0)  # Start fully transparent
        
        self.rounded_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=20)
        self.frame = self.rounded_frame
        # Start animations
        self.after(100, self.fade_in_window)

    def fade_in_window(self, alpha=0.0):
        """Fade in the entire window"""
        if alpha < 1.0:
            alpha += 0.1
            self.attributes('-alpha', alpha)
            self.after(50, lambda: self.fade_in_window(alpha))
        else:
            self.after(500, self.start_progress)
            self.make_rounded()

    def make_rounded(self, radius=20):
        #from win32gui import CreateRoundRectRgn, SetWindowRgn

        x,y = 0,0
        w = self.winfo_width()
        h = self.winfo_height()

        region = CreateRoundRectRgn(x, y, w, h, radius, radius)
        SetWindowRgn(self.winfo_id(), region, True)
    def start_progress(self):
        """Start the progress bar animation"""
        self.progress = 0.0
        self.animate_progress()

    def animate_progress(self):
        """Animate the progress bar"""
        if self.progress < 1.0:
            self.progress += 0.01  # Smooth increment
            self.progress_bar.set(self.progress)
            self.after(15, self.animate_progress)
        else:
            self.after(500, self.fade_out_window)

    def fade_out_window(self, alpha=1.0):
        """Fade out the entire window"""
        if alpha > 0:
            alpha -= 0.1
            self.attributes('-alpha', alpha)
            self.after(50, lambda: self.fade_out_window(alpha))
        else:
            self.destroy()  # Close the window

def show_loading_screen():
    app = LoadingScreen()
    app.mainloop()

if __name__ == "__main__":
    show_loading_screen()