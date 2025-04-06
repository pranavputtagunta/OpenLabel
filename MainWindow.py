import customtkinter
import json
from Utilities import Frame
import cv2
from PIL import Image, ImageTk, ImageDraw
from SettingsWindow import SettingsWindow
import pywinstyles
import os

from welcome import OpenLabelApp
from loading import LoadingScreen
import backend.process_product_img as processor

import time
# Define the path to your JSON file for user profile
USER_PROFILE_FILE = "backend/user_profile.json"
RESPONSE_JSON_PATH = "backend/response.json"

def open_popup(self):
    # Create the popup window (a CTkToplevel instance)
    popup = customtkinter.CTkToplevel(self)
    popup.title("Profile Settings")
    popup.geometry("400x700")
    popup._set_appearance_mode("light")
    popup.configure(fg_color="white")
    
    # Make the popup modal and ensure it appears above the main window
    popup.transient(self)
    popup.grab_set()
    popup.update_idletasks()

    # Create a frame to hold the content
    frame = customtkinter.CTkFrame(popup, fg_color="white")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title label for the settings popup
    title_label = customtkinter.CTkLabel(
        frame,
        text="Profile Settings",
        font=("Arial", 24, "bold"),
        text_color="green"
    )
    title_label.pack(pady=20)

    # Helper function to create labeled entry fields
    def create_entry_field(label_text, multiline=False, height=40):
        sub_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        sub_frame.pack(fill="x", padx=20, pady=10)
        label = customtkinter.CTkLabel(
            sub_frame,
            text=label_text,
            font=("Arial", 14),
            text_color="green"
        )
        label.pack(anchor="w")
        if multiline:
            widget = customtkinter.CTkTextbox(
                sub_frame,
                height=height,
                corner_radius=10,
                border_width=2,
                border_color="#E0E0E0",
                fg_color="white",
                text_color="black"
            )
        else:
            widget = customtkinter.CTkEntry(
                sub_frame,
                height=height,
                corner_radius=10,
                border_width=2,
                border_color="#E0E0E0",
                fg_color="white",
                text_color="black"
            )
        widget.pack(fill="x", pady=(5, 0))
        return widget

    # Create the entry fields
    name_entry = create_entry_field("Name:")
    diet_entry = create_entry_field("Diet:")
    restrictions_entry = create_entry_field("Restrictions:")
    health_goals_entry = create_entry_field("Health Goals:", multiline=True, height=100)

    # If a user profile already exists, pre-populate the fields
    if hasattr(self, "user_profile") and self.user_profile:
        name_entry.insert(0, self.user_profile.get("name", ""))
        diet_entry.insert(0, self.user_profile.get("diet", ""))
        restrictions_entry.insert(0, self.user_profile.get("food_restrictions", ""))
        health_goals_entry.insert("0.0", self.user_profile.get("goals", ""))

    # Function to update the profile and JSON file when the update button is clicked
    def update_profile():
        updated_profile = {
            "name": name_entry.get(),
            "diet": diet_entry.get(),
            "food_restrictions": restrictions_entry.get(),
            "goals": health_goals_entry.get("0.0", "end").strip()
        }
        # Update the profile in the main window
        self.user_profile = updated_profile
        if hasattr(self, "update_profile_display"):
            self.update_profile_display()

        # Update the JSON file (USER_PROFILE_FILE should be defined elsewhere)
        try:
            with open(USER_PROFILE_FILE, 'w') as f:
                json.dump(updated_profile, f, indent=4)
            print(f"Profile updated and saved to {USER_PROFILE_FILE}")
        except Exception as e:
            print(f"Error updating JSON file: {e}")

        # Close the popup window
        popup.destroy()

    # Create the update button
    update_button = customtkinter.CTkButton(
        frame,
        text="Update Profile",
        command=update_profile,
        fg_color="green",
        hover_color="darkgreen",
        corner_radius=20,
        height=40,
        border_width=2,
        border_color="white"
    )
    update_button.pack(pady=20)

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        import tkinter as tk 
        """
        if tk._default_root is None:
            tk._default_root = self
        """
        
        self.geometry("700x800")
        
        """
        self.transient(master)
        self.grab_set()
        """

        



        #self.grab_set()
        self.title("OpenLabel")

        self._set_appearance_mode("light")
        self.configure(bg="#eeeeee",
                         fg_color="#eeeeee")
        customtkinter.set_default_color_theme("green")

        # Configure main window grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Image Processing State Variables
        self.analyzed = False
        self.frame = None
        self.pause_webcam = False
        self.food_recommender = processor.FoodRecommender(USER_PROFILE_FILE)

# WEBCAMMMMMMMMMMMMMMMMMMMMM
        # This frame uses grid layout and fills the entire window.
        self.webcam_frame = Frame(
            self,
            row_count=1,
            col_count=1,
            row_weight=1,
            col_weight=1,
            corner_radius=40
        )
        self.webcam_frame.grid(row=0, column=0, sticky="nsew")
        self.webcam_label = customtkinter.CTkLabel(
            self.webcam_frame,
            text="",
            font=("Arial", 24),
            fg_color="#eeeeee"
        )
        self.webcam_label.grid(row=0, column=0, sticky="nsew")

        self.cap = cv2.VideoCapture(0)
        self.update_webcam()

        # Wait for window to render so we have dimensions




        



        self.update_idletasks()
        
        self.window_width = 700
        self.window_height = 800
        # ---------------- Description Frame ----------------
        self.description_height = 200
        self.description_width = int(self.window_width * 0.8)
        # Create the description frame with grid layout, rounded corners, and fixed size.
        self.description_frame = Frame(
            self,
            row_count=1,
            col_count=1,
            row_weight=1,
            col_weight=1,
            corner_radius=20,
            width=self.description_width,
            height=self.description_height,
            fg_color="#1d1e1e"
        )
        # Prevent the frame from resizing based on its content.
        self.description_frame.grid_propagate(False)


        # Add a centered description label
        self.description_label = customtkinter.CTkLabel(
            self.description_frame,
            text="Nutrition & Allergen Info",
            font=("Arial", 18),
            text_color="#1d1e1e",
            anchor="center",
            corner_radius=20
        )
        self.description_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", rowspan=1, columnspan=1)


        # Initially, place the description frame off-screen (below the window)
        self.description_frame.place(x=(self.window_width - self.description_width) // 2, y=self.window_height)

        # ---------------- Toggle Button ----------------
        # This button will be placed at the bottom of the screen
        self.toggle_button = customtkinter.CTkButton(
            self,
            text="See Analysis",
            command=self.toggle_description,
            corner_radius=20,
            hover_color=("green","darkgreen"),  # Change hover color to green
            font=('Arial', 16, 'bold'),
            fg_color="green",
            bg_color="#000001",
            width=300,
            height=50,
        )

 


        # Position at the bottom center of the screen
        self.toggle_button.place(relx=0.5, rely=0.5, anchor="center")

        pywinstyles.set_opacity(self.toggle_button, color="#000001")

        # Track whether the description is visible or hidden.
        self.description_visible = False

        # Bind window resize event to ensure panel resizes correctly
        self.bind("<Configure>", self.on_resize)

        

        # ------------ Profile Button -----------------
        self.profile_button = customtkinter.CTkButton(
            self.webcam_frame,
            text="O",
            width=40,
            height=40,
            corner_radius=80,
            fg_color="transparent",
            bg_color="#000001",  # Make the background transparent
            text_color="green",
            hover_color=("gray75","green"),
            border_width=2,
            border_color="green",
            command=self.open_settings
        )

        self.profile_button.place(relx=0.9, rely=0.1, anchor="ne")
        pywinstyles.set_opacity(self.profile_button, color="#000001")



    def open_settings(self):
        """Opens the settings window.
        settings_window = SettingsWindow(self) # Pass self (MainWindow) as master
        self.withdraw()
        settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        settings_window.focus()

        settings_window.grab_set()
        """
        #settings_window = SettingsWindow(self)
        #self.grab_release()
        #self.wait_window(settings_window)
        self.grab_release()
        self.destroy()

       

    #TODO: Pranav handle integration
    def toggle_description(self):
        """Toggle the description panel"""
        if self.analyzed: 
            if self.description_visible:
                self.animate_slide(show=False)
                self.toggle_button.configure(text="Show Description")
                pywinstyles.set_opacity(self.toggle_button, color="#000001")
            else:
                self.animate_slide(show=True)
                self.toggle_button.configure(text="Hide Description")
                pywinstyles.set_opacity(self.toggle_button, color="#000001")
            self.description_visible = not self.description_visible
        elif self.frame != None:
            # If the image hasn't been analyzed yet, process it
            self.toggle_button.configure(text="Analyzing image...")
            self.toggle_button.configure(state="disabled")
            self.pause_webcam = True
            self.food_recommender.process_product_image_cv2(self.frame)
            self.food_recommender.create_response_json()
            self.frame = self.food_recommender.draw_bounding_boxes(self.frame)
            self.analyzed = True
            self.toggle_button.configure(state="normal")
            self.toggle_description()

    def animate_slide(self, show=True):
        """
        Animate the description frame sliding up/down.
        Only the description frame moves - the button stays at the bottom.
        """
        # Set target positions for description frame
        if show:
            target_desc_y = self.window_height - self.description_height - 600
        else:
            target_desc_y = self.window_height

        # Get current position
        current_desc_y = self.description_frame.winfo_y()

        step = 30  # pixels per iteration
        if show:
            if current_desc_y > target_desc_y:
                new_desc_y = max(target_desc_y, current_desc_y - step)
                self.description_frame.place_configure(y=new_desc_y)
                self.after(2, lambda: self.animate_slide(show=True))
        else:
            if current_desc_y < target_desc_y:
                new_desc_y = min(target_desc_y, current_desc_y + step)
                self.description_frame.place_configure(y=new_desc_y)
                self.after(2, lambda: self.animate_slide(show=False))

    def parse_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}")
            return None

    def on_resize(self, event):
        """Handle window resize to ensure panel stays properly positioned"""
        # Only update if the window size actually changed
        if event.widget == self and (event.width != getattr(self, '_last_width', None) or
                                     event.height != getattr(self, '_last_height', None)):
            self._last_width = event.width
            self._last_height = event.height
            self.window_width = event.width
            self.window_height = event.height

            # Create a new frame with updated width in the constructor
            frame_height = self.description_height + 200
            new_description_frame = Frame(
                self,
                row_count=1,
                col_count=1,
                row_weight=1,
                col_weight=1,
                corner_radius=20,
                width=self.description_width,
                height=frame_height,
                bg_color="#000001",
                fg_color="white"
            )

            # Prevent the new frame from resizing based on contents
            new_description_frame.grid_propagate(False)
            new_description_frame.grid_columnconfigure(0, weight=0)

            # Move the description label to the new frame
            textbox_height = (frame_height / 2) + 100
            self.description_label.grid_forget()
            self.description_label = customtkinter.CTkTextbox(
                new_description_frame,
                wrap="word",
                font=("Arial", 18),
                fg_color="white",
                corner_radius=20,
                height = textbox_height,
                width = self.description_width-50
            )

            self.description_label.grid(
                row=0,
                column=0,
                padx=50,
                pady=(0,100),
                sticky="n"
            )

            data = self.parse_json(RESPONSE_JSON_PATH)

            self.description_label.tag_add("colored_text", "1.0", "1.16")
            self.description_label.tag_config("colored_text",background="#1d1e1e",foreground="red")
            self.description_label.grid(row=0, column=0, padx=20, pady=(20,50), sticky="new")

            # Clear the textbox and enable editing
            self.description_label.configure(state="normal")
            self.description_label.delete("1.0", "end")

            # Define tags for formatting (only colors, as 'font' is forbidden)
            self.description_label.tag_config("bold_big", foreground="black")
            self.description_label.tag_config("bold_bigger", foreground="black")
            self.description_label.tag_config("bold", foreground="black")
            self.description_label.tag_config("italic_small", foreground="gray")
            self.description_label.tag_config("rating_red", foreground="red")
            self.description_label.tag_config("rating_yellow", foreground="yellow")
            self.description_label.tag_config("rating_lightgreen", foreground="light green")
            self.description_label.tag_config("rating_darkgreen", foreground="dark green")

            # [product_name]
            self.description_label.insert("end", "Product Name: ", "bold_big")
            self.description_label.insert("end", data.get("product_name", "Unknown Product") + "\n", "bold_bigger")

            # [category]
            self.description_label.insert("end", "Category: ", "bold_bigger")
            self.description_label.insert("end", data.get("category", "Unknown Category") + "\n\n", "italic_small")

            # divider line
            self.description_label.insert("end", "-"*50 + "\n\n", "bold")

            # Recommended: [is_appropriate]
            self.description_label.insert("end", "Recommended: ", "bold_big")
            is_app = data.get("is_appropriate", "N/A")
            if is_app.lower() == "yes":
                tag_app = "rating_darkgreen"
            elif is_app.lower() == "maybe":
                tag_app = "rating_yellow"
            elif is_app.lower() == "no":
                tag_app = "rating_red"
            else:
                tag_app = "bold"
            self.description_label.insert("end", is_app + "\n", tag_app)

            # [rating] (color coded)
            rating = data.get("rating", 0)
            if 1 <= rating <= 4:
                rating_tag = "rating_red"
            elif 5 <= rating <= 6:
                rating_tag = "rating_yellow"
            elif 7 <= rating <= 8:
                rating_tag = "rating_lightgreen"
            elif 9 <= rating <= 10:
                rating_tag = "rating_darkgreen"
            else:
                rating_tag = "bold"

            self.description_label.insert("end","Rating: ", "bold_big")
            self.description_label.insert("end", str(rating) + "\n\n", rating_tag)

            # divider line
            self.description_label.insert("end", "-"*50 + "\n\n", "bold")

            # [feedback]
            self.description_label.insert("end", "Feedback: ", "bold_big")
            self.description_label.insert("end", data.get("feedback", "No feedback provided.") + "\n\n", "bold")

            # divider line
            self.description_label.insert("end", "-"*50 + "\n\n", "bold")

            # [nutrition_info] (each line separately)
            nutrition_info = data.get("nutrition_info", {})
            print(nutrition_info)
            for key, value in  nutrition_info.items():
                self.description_label.insert("end", f"{key}: {value}\n", "bold")
            self.description_label.insert("end", "\n")

            # Make the textbox read-only again
            self.description_label.configure(state="disabled")

            # Destroy old description frame and update reference
            self.description_frame.destroy()
            self.description_frame = new_description_frame

            # Recalculate x-coordinate to center the description frame
            x_coord = 70
            if self.description_visible:
                self.description_frame.place(x= x_coord, y=self.window_height - self.description_height)
                pywinstyles.set_opacity(self.description_frame, color="#000001")
            else:
                self.description_frame.place(x=x_coord, y=self.window_height)
                pywinstyles.set_opacity(self.description_frame, color="#000001")

            # button stuff inside
            self.alternatives_button = customtkinter.CTkButton(
                self.description_frame,
                text="Alternatives",
                command=self.show_alternatives,  # You'll need to create this method
                corner_radius=10,
                hover_color=("green", "darkgreen"),
                font=('Arial', 14, 'bold'),
                fg_color="green",
                bg_color="#000001",
                width=140,
                height=40,
            )

            self.ingredients_button = customtkinter.CTkButton(
                self.description_frame,
                text="Ingredients",
                command=self.show_ingredients,  # You'll need to create this method
                corner_radius=10,
                hover_color=("green", "darkgreen"),
                font=('Arial', 14, 'bold'),
                fg_color="green",
                bg_color="#000001",
                width=140,
                height=40,
            )

            self.alternatives_button.place(relx=0.25, rely=0.85, anchor="center")
            self.ingredients_button.place(relx=0.75, rely=0.85, anchor="center")

            pywinstyles.set_opacity(self.alternatives_button, color="#000001")
            pywinstyles.set_opacity(self.ingredients_button, color="#000001")
            # Update toggle button position to stay at bottom
            self.toggle_button.place_configure(rely=0.95)

    def show_alternatives(self):
        pass

    def show_ingredients(self):
        pass

    def create_rounded_frame(self, image, corner_radius):
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)

        width, height = image.size
        draw.rounded_rectangle([(0, 0), (width, height)],
                               corner_radius,
                               fill=255)

        # Apply mask to image
        output = Image.new('RGBA', image.size, (0, 0, 0, 0))
        output.paste(image, mask=mask)

        outline = Image.new('RGBA', image.size, (0,0,0,0))
        draw_outline = ImageDraw.Draw(outline)

        draw_outline.rounded_rectangle([(0, 0), (width, height)],
                                        corner_radius,
                                        fill=None,
                                        outline='green',
                                        width=10)

        output = Image.alpha_composite(output, outline)
        return output

    def update_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            if self.frame != None and self.pause_webcam:
                frame = self.frame
            else:
                self.frame = frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get target dimensions (subtracting margins as needed)
            target_width = self.webcam_frame.winfo_width() - 150
            target_height = self.webcam_frame.winfo_height() - 150

            if target_width > 0 and target_height > 0:
                # Original frame dimensions
                orig_height, orig_width, _ = frame.shape
                target_aspect = target_width / target_height
                orig_aspect = orig_width / orig_height

                # Crop the frame to match the target aspect ratio
                if orig_aspect > target_aspect:
                    # Frame is wider than target: crop horizontally
                    new_width = int(target_aspect * orig_height)
                    x_offset = (orig_width - new_width) // 2
                    frame_cropped = frame[:, x_offset:x_offset + new_width]
                else:
                    # Frame is taller than target: crop vertically
                    new_height = int(orig_width / target_aspect)
                    y_offset = (orig_height - new_height) // 2
                    frame_cropped = frame[y_offset:y_offset + new_height, :]

                # Resize the cropped frame to the target dimensions
                frame_resized = cv2.resize(frame_cropped, (target_width, target_height))

                image = Image.fromarray(frame_resized)
                rounded_image = self.create_rounded_frame(image, 40)
                imgtk = ImageTk.PhotoImage(image=rounded_image)
                self.webcam_label.configure(image=imgtk)
                self.webcam_label.image = imgtk

        self.after(10, self.update_webcam)

    def on_close(self):
        self.cap.release()
        self.destroy()


def fade_window(window, start_alpha=1.0, end_alpha=0.0, step=0.01, delay=5):
    """Helper function to fade a window in or out"""
    def _fade_step(current_alpha):
        if start_alpha > end_alpha:  # Fading out
            if current_alpha > end_alpha:
                current_alpha -= step
                window.attributes('-alpha', current_alpha)
                window.after(delay, lambda: _fade_step(current_alpha))
            else:
                window.destroy()
        else:  # Fading in
            if current_alpha < end_alpha:
                current_alpha += step
                window.attributes('-alpha', current_alpha)
                window.after(delay, lambda: _fade_step(current_alpha))
    
    _fade_step(start_alpha)

def mainTest():
    
    loading_screen = LoadingScreen()
    loading_screen.after(0, lambda:loading_screen.grab_set())
    loading_screen.mainloop()

    app = OpenLabelApp()
    app.after(0, lambda: app.grab_set())
    app.after(0, lambda: fade_window(app, 0.0, 1.0))
    app.mainloop()

    while True:
        main_app = MainWindow()
        main_app.after(0, lambda:main_app.grab_set())
        main_app.after(0, lambda: fade_window(main_app, 0.0, 1.0))  # Fade in the main window
        main_app.mainloop()

        settings = SettingsWindow()
        settings.after(0, lambda:settings.grab_set())
        settings.after(0, lambda: fade_window(settings, 0.0, 1.0))
        settings.mainloop()



if __name__ == '__main__':
    #time.sleep(2)
    mainTest()