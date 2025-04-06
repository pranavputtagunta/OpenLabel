import customtkinter as ctk
from PIL import Image, ImageTk
import os
import json
import tkinter.messagebox as ctk_messagebox


class OpenLabelApp(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("600x900")
        self.title("OpenLabel")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        self.current_page = "welcome"
        self.progress_value = 0
        self.user_profile_data = self.load_user_profile()
        self.backend_data = {}  # To store data received from the backend
        self.progress_bar = ctk.CTkProgressBar(self, height=8)
        self.progress_bar.pack(side="bottom", fill="x")
        self.progress_label = ctk.CTkLabel(self, text="0%", font=("Helvetica", 10), text_color="#555", bg_color="#eeeeee")
        self.progress_label.pack(side="bottom", pady=(0, 5))
        self.update_progress()


        
        self.show_welcome_page()
        # Example of automatically loading backend data on startup (uncomment to use):
        # self.after(1000, lambda: self.update_user_profile_from_backend('backend_data.json'))


    def update_progress(self):
        self.progress_bar.set(self.progress_value)
        percentage = int(self.progress_value * 100)
        self.progress_label.configure(text=f"{percentage}%")

    def load_user_profile(self):
        filename = "user_profile.json"
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Warning: JSON file '{filename}' is corrupted. Starting with an empty profile.")
            return {}

    def update_user_profile_from_backend(self, backend_json_path):
        try:
            with open(backend_json_path, "r") as f:
                backend_data = json.load(f)
                if "diet" in backend_data:
                    self.user_profile_data["diet"] = backend_data["diet"]
                if "food_restrictions" in backend_data:
                    self.user_profile_data["food_restrictions"] = backend_data["food_restrictions"]
                if "goals" in backend_data:
                    self.user_profile_data["goals"] = backend_data["goals"]

                self.save_user_data(self.user_profile_data)
                print(f"User profile updated from backend data in '{backend_json_path}'.")
                if self.current_page == "results":
                    self.show_results_page(self.user_profile_databack)
                elif self.current_page == "preferences":
                    self.show_user_preferences_page()
                elif self.current_page == "welcome":
                    ctk_messagebox.showinfo("Profile Updated", f"User profile updated from '{backend_json_path}'.")
        except FileNotFoundError:
            print(f"Error: Backend JSON file not found at '{backend_json_path}'.")
            ctk_messagebox.showerror("Error", f"Backend JSON file not found at '{backend_json_path}'.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{backend_json_path}'.")
            ctk_messagebox.showerror("Error", f"Could not decode JSON from '{backend_json_path}'.")
        except Exception as e:
            print(f"An error occurred while updating profile from backend: {e}")
            ctk_messagebox.showerror("Error", f"An error occurred: {e}")

    def display_backend_data(self, backend_data):
        self.current_page = "backend_data"
        self.progress_value = 1.0
        self.update_progress()
        for widget in self.winfo_children():
            if widget != self.progress_bar and widget != self.progress_label:
                widget.destroy()
        self.configure(bg="#eeeeee")

        main_label = ctk.CTkLabel(self, text=backend_data.get("product_name", "Product Information"),
                                  font=("Helvetica", 30, "bold"), text_color="#333", bg_color="#eeeeee", wraplength=580, justify="center")
        main_label.pack(pady=(20, 10), padx=10)

        appropriate_text = "Appropriate for you:"
        appropriate_value = "Yes" if backend_data.get("is_appropriate") == "yes" else "No"
        appropriate_color = "#4CAF50" if appropriate_value == "Yes" else "#F44336"
        appropriate_label = ctk.CTkLabel(self, text=f"{appropriate_text} {appropriate_value}",
                                         font=("Helvetica", 20, "bold"), text_color=appropriate_color, bg_color="#eeeeee")
        appropriate_label.pack(pady=(10, 5))

        if backend_data.get("feedback"):
            feedback_label = ctk.CTkLabel(self, text="Feedback:", font=("Helvetica", 18, "bold"), text_color="#555", bg_color="#eeeeee", anchor="w")
            feedback_label.pack(pady=(10, 5), padx=20, fill="x")
            feedback_text_label = ctk.CTkLabel(self, text=backend_data.get("feedback"), font=("Helvetica", 16), text_color="#555", bg_color="#eeeeee", wraplength=560, justify="left", anchor="w")
            feedback_text_label.pack(pady=(0, 10), padx=20, fill="x")

        nutrition_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        nutrition_frame.pack(pady=(15, 10), padx=20, fill="x")
        nutrition_title = ctk.CTkLabel(nutrition_frame, text="Nutrition Information", font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#f0f0f0")
        nutrition_title.pack(pady=(10, 5))
        nutrition = backend_data.get("nutrition_info", {})
        for key, value in nutrition.items():
            label = ctk.CTkLabel(nutrition_frame, text=f"{key.capitalize()}: {value}", font=("Helvetica", 16), text_color="#555", bg_color="#f0f0f0", anchor="w")
            label.pack(pady=(2, 2), padx=15, fill="x")

        if backend_data.get("ingredients"):
            ingredients_frame = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=10)
            ingredients_frame.pack(pady=(15, 10), padx=20, fill="x")
            ingredients_title = ctk.CTkLabel(ingredients_frame, text="Ingredients", font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#e0e0e0")
            ingredients_title.pack(pady=(10, 5))
            for ingredient in backend_data["ingredients"]:
                name = ingredient.get("ingredient_name", "N/A")
                description = ingredient.get("description", "")
                ingredient_label = ctk.CTkLabel(ingredients_frame, text=f"- {name}", font=("Helvetica", 16, "bold"), text_color="#555", bg_color="#e0e0e0", anchor="w")
                ingredient_label.pack(pady=(2, 0), padx=15, fill="x")
                if description:
                    description_label = ctk.CTkLabel(ingredients_frame, text=f"  ({description})", font=("Helvetica", 14, "italic"), text_color="#777", bg_color="#e0e0e0", wraplength=540, justify="left", anchor="w")
                    description_label.pack(pady=(0, 2), padx=25, fill="x")

        if backend_data.get("alternative_products"):
            alternatives_frame = ctk.CTkFrame(self, fg_color="#f0f8ff", corner_radius=10)
            alternatives_frame.pack(pady=(15, 20), padx=20, fill="x")
            alternatives_title = ctk.CTkLabel(alternatives_frame, text="Alternative Products", font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#f0f8ff")
            alternatives_title.pack(pady=(10, 5))
            for alt in backend_data["alternative_products"]:
                name = alt.get("product_name", "N/A")
                alt_label = ctk.CTkLabel(alternatives_frame, text=f"- {name}", font=("Helvetica", 16), text_color="#555", bg_color="#f0f8ff", anchor="w")
                alt_label.pack(pady=(2, 2), padx=15, fill="x")

        scan_button = ctk.CTkButton(self, text="Scan",
                                     command=self.finish,
                                     fg_color="#4CAF50",
                                     hover_color="#45a049",
                                     text_color="#eeeeee",
                                     font=("Helvetica", 18),
                                     corner_radius=30, width=180, height=50)
        scan_button.pack(pady=20)

    def finish(self):
        self.grab_release()
        self.destroy()

    def show_user_preferences_page(self):
        self.current_page = "preferences"
        self.progress_value = 0.25
        self.update_progress()
        for widget in self.winfo_children():
            if widget != self.progress_bar and widget != self.progress_label:
                widget.destroy()
        self.configure(bg="#eeeeee")
        user_data = self.user_profile_data.copy()

        def ask_dietary_restrictions():
            label = ctk.CTkLabel(self, text="What is your general diet? (e.g., vegetarian, vegan, omnivore)",
                                 font=("Helvetica", 18), text_color="black", bg_color="#eeeeee", wraplength=450, justify="center")
            label.pack(pady=(50, 10))
            diet_entry = ctk.CTkEntry(self, width=400, font=("Helvetica", 16), border_color="#888")
            diet_entry.insert(0, user_data.get("diet", ""))
            diet_entry.pack(pady=15)

            def on_diet_submit():
                diet_input = diet_entry.get().strip()
                user_data["diet"] = diet_input
                label.destroy()
                diet_entry.destroy()
                diet_submit_button.destroy()
                ask_food_restrictions()

            diet_submit_button = ctk.CTkButton(self, text="Next", command=on_diet_submit,
                                         fg_color="#388E3C", hover_color="#2F6A2F", text_color="#eeeeee",
                                         font=("Helvetica", 18), corner_radius=25, width=150, height=40)
            diet_submit_button.pack(pady=20)

        def ask_food_restrictions():
            self.progress_value = 0.50
            self.update_progress()
            label = ctk.CTkLabel(self, text="Please list any specific food restrictions or allergies, separated by commas (e.g., pecans, gluten, peanuts)",
                                 font=("Helvetica", 18), text_color="black", bg_color="#eeeeee", wraplength=450, justify="center")
            label.pack(pady=(50, 10))
            restrictions_entry = ctk.CTkEntry(self, width=400, font=("Helvetica", 16), border_color="#888")
            restrictions_entry.insert(0, user_data.get("food_restrictions", ""))
            restrictions_entry.pack(pady=15)

            def on_restrictions_submit():
                restrictions_input = restrictions_entry.get().strip()
                user_data["food_restrictions"] = restrictions_input
                label.destroy()
                restrictions_entry.destroy()
                restrictions_submit_button.destroy()
                ask_goals()

            restrictions_submit_button = ctk.CTkButton(self, text="Next", command=on_restrictions_submit,
                                         fg_color="#388E3C", hover_color="#2F6A2F", text_color="#eeeeee",
                                         font=("Helvetica", 18), corner_radius=25, width=150, height=40)
            restrictions_submit_button.pack(pady=20)

        def ask_goals():
            self.progress_value = 0.75
            self.update_progress()
            label = ctk.CTkLabel(self, text="What are your health and dietary goals? Please describe them briefly.",
                                 font=("Helvetica", 18), text_color="black", bg_color="#eeeeee", wraplength=450, justify="center")
            label.pack(pady=(50, 10))
            goals_entry = ctk.CTkTextbox(self, width=400, height=150, font=("Helvetica", 16), border_color="#888")
            goals_entry.insert("0.0", user_data.get("goals", ""))
            goals_entry.pack(pady=15)

            def on_goals_submit():
                self.update_progress()
                goals_input = goals_entry.get("0.0", "end").strip()
                user_data["goals"] = goals_input
                label.destroy()
                goals_entry.destroy()
                goals_submit_button.destroy()
                self.save_user_data(user_data)
                self.show_results_page(user_data)

            goals_submit_button = ctk.CTkButton(self, text="Finish", command=on_goals_submit,
                                         fg_color="#388E3C", hover_color="#2F6A2F", text_color="#eeeeee",
                                         font=("Helvetica", 18), corner_radius=25, width=150, height=40)
            goals_submit_button.pack(pady=20)

        ask_dietary_restrictions()

    def show_welcome_page(self):
        self.transient(self.master)
        self.grab_set()
        self.update_idletasks()
        self.current_page = "welcome"
        self.progress_value = 0
        self.update_progress()
        for widget in self.winfo_children():
            if widget != self.progress_bar and widget != self.progress_label:
                widget.destroy()
        self.configure(bg="#eeeeee")

        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            logo_image_pil = Image.open(logo_path).resize((500, 500))
            logo_image_tk = ImageTk.PhotoImage(logo_image_pil)
            logo_label = ctk.CTkLabel(self, image=logo_image_tk, text="", bg_color="#eeeeee")
            logo_label.image = logo_image_tk
            logo_label.pack(pady=30)
            self.after(100, lambda: self.fade_in_widget(logo_label))
        except FileNotFoundError:
            print("Error: logo.png not found. Please place it in the same directory as the script.")
            fallback_label = ctk.CTkLabel(self, text="[Logo]", font=("Helvetica", 24), text_color="gray", bg_color="#eeeeee")
            fallback_label.pack(pady=30)
            

        description_label = ctk.CTkLabel(self, text="Scan a product or edit your preferences.",
                                         font=("Helvetica", 20), text_color="#555", bg_color="#eeeeee",
                                         wraplength=400,
                                         justify="center")
        description_label.pack(pady=40)

        scan_button = ctk.CTkButton(self, text="Edit Preferences", command=self.show_user_preferences_page,
                                     width=350, height=60, font=("Helvetica", 20, "bold"),
                                     fg_color="#388E3C", hover_color="#2F6A2F",
                                     text_color="#eeeeee", corner_radius=30)

        self.after(500, lambda: self.fade_in_widget(description_label))
        scan_button.pack(pady=20)
        self.after(1000, lambda: self.fade_in_widget(scan_button))

    def save_user_data(self, user_data):
        """Saves user data to a JSON file in the specified format."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "user_profile.json")
        print(f"Debug: Script directory: {script_dir}")
        print(f"Debug: Full filename to save: {filename}")
        try:
            os.makedirs(script_dir, exist_ok=True)
            print(f"Debug: os.makedirs('{script_dir}', exist_ok=True) executed without error.")
            with open(filename, "w") as f:
                json.dump(user_data, f, indent=4)
                print(f"Debug: Successfully wrote data to '{filename}'.")
            print(f"User data saved to {filename} in the format for the backend.")
        except Exception as e:
            print(f"Error saving user data: {e}")
            print(f"Debug: Error details: {e}")

    def show_results_page(self, user_data):
        self.current_page = "results"
        self.progress_value = 1.0
        self.update_progress()
        for widget in self.winfo_children():
            if widget != self.progress_bar and widget != self.progress_label:
                widget.destroy()
        self.configure(bg="#eeeeee")

        results_label = ctk.CTkLabel(self, text="Profile Updated!",
                                     font=("Helvetica", 42, "bold"),
                                     text_color="#228B22",
                                     bg_color="#eeeeee")
        results_label.pack(pady=(60, 20))

        thank_you_label = ctk.CTkLabel(self, text="Your profile information has been updated.",
                                         font=("Helvetica", 24),
                                         text_color="#555",
                                         bg_color="#eeeeee")
        thank_you_label.pack(pady=(20, 40))

        data_heading_label = ctk.CTkLabel(self, text="Here's your current profile information:",
                                           font=("Helvetica", 20, "italic"),
                                           text_color="#777",
                                           bg_color="#eeeeee")
        data_heading_label.pack(pady=(30, 20))

        data_display_frame = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=10)
        data_display_frame.pack(padx=40, pady=30, fill="both", expand=True)

        diet_text = "General Diet: "
        diet_value = user_data.get("diet", "Not specified")
        diet_label = ctk.CTkLabel(data_display_frame, text=f"{diet_text}",
                                      font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#f5f5f5", anchor="w")
        diet_label.pack(padx=25, pady=(20, 10), fill="x")
        diet_value_label = ctk.CTkLabel(data_display_frame, text=f"{diet_value}",
                                            font=("Helvetica", 18), text_color="#555", bg_color="#f5f5f5", anchor="w", wraplength=data_display_frame.winfo_width() - 50, justify="left")
        diet_value_label.pack(padx=25, pady=(0, 15), fill="x")
        diet_value_label.bind("<Configure>", lambda e: diet_value_label.configure(wraplength=e.width - 50))

        restrictions_text = "Food Restrictions: "
        restrictions_value = user_data.get("food_restrictions", "Not specified")
        restrictions_label = ctk.CTkLabel(data_display_frame, text=f"{restrictions_text}",
                                      font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#f5f5f5", anchor="w")
        restrictions_label.pack(padx=25, pady=(15, 10), fill="x")
        restrictions_value_label = ctk.CTkLabel(data_display_frame, text=f"{restrictions_value}",
                                            font=("Helvetica", 18), text_color="#555", bg_color="#f5f5f5", anchor="w", wraplength=data_display_frame.winfo_width() - 50, justify="left")
        restrictions_value_label.pack(padx=25, pady=(0, 15), fill="x")
        restrictions_value_label.bind("<Configure>", lambda e: restrictions_value_label.configure(wraplength=e.width - 50))

        goals_text = "Goals: "
        goals_value = user_data.get("goals", "Not specified")
        goals_label = ctk.CTkLabel(data_display_frame, text=f"{goals_text}",
                                      font=("Helvetica", 18, "bold"), text_color="#333", bg_color="#f5f5f5", anchor="w")
        goals_label.pack(padx=25, pady=(15, 10), fill="x")
        goals_value_label = ctk.CTkLabel(data_display_frame, text=f"{goals_value}",
                                            font=("Helvetica", 18), text_color="#555", bg_color="#f5f5f5", anchor="w", wraplength=data_display_frame.winfo_width() - 50, justify="left")
        goals_value_label.pack(padx=25, pady=(0, 20), fill="x")
        goals_value_label.bind("<Configure>", lambda e: goals_value_label.configure(wraplength=e.width - 50))

        scan_button = ctk.CTkButton(self, text="Scan",
                                     command=self.finish,
                                     fg_color="#4CAF50",
                                     hover_color="#45a049",
                                     text_color="#eeeeee",
                                     font=("Helvetica", 20),
                                     corner_radius=30, width=180, height=50)
        scan_button.pack(pady=30)
