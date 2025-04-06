import customtkinter
import json

USER_PROFILE_FILE = "./backend/user_profile.json"

class SettingsWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Profile Settings")
        self.geometry("400x700")
        self.label = customtkinter.CTkLabel(self, text="Settings Content")
        self.label.pack(pady=20)
        self._set_appearance_mode("light")
        self.configure(fg_color="white")

        self.grab_set()
        self.update_idletasks()  # Update the window to ensure it is on top

        
        # Create frame for content
        self.frame = customtkinter.CTkFrame(self, fg_color="white")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title label
        self.title_label = customtkinter.CTkLabel(
            self.frame,
            text="Profile Settings",
            font=("Arial", 24, "bold"),
            text_color="green"
        )
        self.title_label.pack(pady=20)
        
        # Create entry fields
        self.create_entry_field("Name:", "name_entry")
        self.create_entry_field("Diet:", "diet_entry")
        self.create_entry_field("Restrictions:", "restrictions_entry")
        self.create_entry_field("Health Goals:", "health_goals_entry", height=100, multiline=True)
        
        self.populatefields()  # Populate fields with current profile data
        # Update button
        self.update_button = customtkinter.CTkButton(
            self.frame,
            text="Update Profile",
            command=self.update_profile,
            fg_color="green",
            hover_color="darkgreen",
            corner_radius=20,
            height=40,
            border_width=2,
            border_color="white"
        )
        self.update_button.pack(pady=20)
        
        # Make window modal (blocks interaction with main window)
        self.grab_set()
    
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
        
    def create_entry_field(self, label_text, attr_name, height=40, multiline=False):
        """Helper method to create labeled entry fields"""
        frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = customtkinter.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 14),
            text_color="green"
        )
        label.pack(anchor="w")
        
        if multiline:
            widget = customtkinter.CTkTextbox(
                frame,
                height=height,
                corner_radius=10,
                border_width=2,
                border_color="#E0E0E0",
                fg_color="white",
                text_color="black"
            )
        else:
            widget = customtkinter.CTkEntry(
                frame,
                height=height,
                corner_radius=10,
                border_width=2,
                border_color="#E0E0E0",
                fg_color="white",
                text_color="black"
            )
        
        widget.pack(fill="x", pady=(5, 0))
        setattr(self, attr_name, widget)
    
    def populatefields(self):
         #this will pop entry fields w/ curr profile data (incase no new data is needed to be added)
        data = self.parse_json(USER_PROFILE_FILE)
        print(data)

        if data:
            self.name_entry.insert(0, data.get("name", ""))
            self.diet_entry.insert(0, data.get("diet", ""))
            self.restrictions_entry.insert(0, data.get("food_restrictions", ""))
            self.health_goals_entry.insert("0.0", data.get("goals", ""))

    def update_profile(self):
        updated_profile = {
            "name": self.name_entry.get(),
            "diet": self.diet_entry.get(),
            "food_restrictions": self.restrictions_entry.get(),
            "goals": self.health_goals_entry.get("0.0", "end").strip()
        }

        # Update the JSON file
        self.update_json_file(updated_profile)

        self.grab_release()
        self.destroy() # Close the settings window


    def update_json_file(self, updated_profile):
        try:
            with open(USER_PROFILE_FILE, 'w') as f:
                json.dump(updated_profile, f, indent=4)
            print(f"Profile updated and saved to {USER_PROFILE_FILE}")
        except Exception as e:
            print(f"Error updating JSON file: {e}")

if __name__ == "__main__":
    # This block is for testing SettingsWindow independently (optional)
    app = SettingsWindow()
    app.mainloop()