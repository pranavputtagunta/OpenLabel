import customtkinter as ctk
import json
from PIL import Image, ImageTk
import os

class IngredientsWindow(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        
        # Configure window
        self.title("Ingredients Information")
        self.geometry("800x600")
        self._set_appearance_mode("light")
        self.configure(fg_color="white")

        # Back button at top
        self.back_button = ctk.CTkButton(
            self,
            text="← Back",
            font=("Arial Bold", 12),
            fg_color="transparent",
            text_color="green",
            hover_color="#e0e0e0",
            corner_radius=20,
            width=100,
            height=32,
            command=self.on_back
        )
        self.back_button.pack(anchor="nw", padx=20, pady=10)

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Ingredients List",
            font=("Arial Bold", 24),
            text_color="green"
        )
        self.title_label.pack(pady=(0, 20))

        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            width=700,
            height=450
        )
        self.scroll_frame.pack(expand=True, fill="both", padx=20)

        # Load and display ingredients
        self.load_ingredients()

        # Bottom back button
        self.bottom_back_button = ctk.CTkButton(
            self,
            text="Close Window",
            font=("Arial Bold", 14),
            fg_color="green",
            hover_color="darkgreen",
            corner_radius=20,
            width=200,
            height=40,
            command=self.on_back
        )
        self.bottom_back_button.pack(pady=20)

    def load_ingredients(self):
        try:
            with open("./backend/response.json", "r") as f:
                data = json.load(f)
                ingredients = data.get("ingredients", [])
                self.create_ingredient_dropdowns(ingredients)
        except Exception as e:
            print(f"Error loading ingredients: {e}")

    def create_ingredient_dropdowns(self, ingredients):
        for ingredient in ingredients:
            # Create frame for each ingredient
            ingredient_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#f8f8f8",
                corner_radius=15,
                height=60
            )
            ingredient_frame.pack(fill="x", pady=5, padx=10)
            ingredient_frame.pack_propagate(False)

            # Create content frame for description with better styling
            content_frame = ctk.CTkFrame(
                ingredient_frame,
                fg_color="#f0f0f0",
                corner_radius=10
            )
            
            # Create description label with improved formatting
            desc_label = ctk.CTkLabel(
                content_frame,
                text=ingredient["description"],
                font=("Arial", 12),
                text_color="#555555",
                wraplength=600,
                justify="left",
                anchor="w",  # Align text to left
                fg_color="transparent",
                padx=15,  # Add horizontal padding
                pady=10   # Add vertical padding
            )
            desc_label.pack(fill="both", expand=True)

            # Variable to track dropdown state
            is_expanded = ctk.BooleanVar(value=False)

    def create_ingredient_dropdowns(self, ingredients):
        def create_toggle_function(ing_frame, content_frame, expanded):
            def toggle():
                if expanded.get():
                    content_frame.pack(fill="x", padx=10, pady=(0, 10))
                    ing_frame.configure(height=150)
                else:
                    content_frame.pack_forget()
                    ing_frame.configure(height=60)
            return toggle

        def create_button_update(button, expanded, name):
            def update_text(*args):
                button.configure(text=f"{name} ▲" if expanded.get() else f"{name} ▼")
            return update_text

        for ingredient in ingredients:
            # Create frame for each ingredient
            ingredient_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#f8f8f8",
                corner_radius=15,
                height=60
            )
            ingredient_frame.pack(fill="x", pady=5, padx=10)
            ingredient_frame.pack_propagate(False)

            # Create content frame for description
            content_frame = ctk.CTkFrame(
                ingredient_frame,
                fg_color="#f0f0f0",
                corner_radius=10
            )
            
            # Create description label
            desc_label = ctk.CTkLabel(
                content_frame,
                text=ingredient["description"],
                font=("Arial", 12),
                text_color="#555555",
                wraplength=600,
                justify="left",
                anchor="w",
                fg_color="transparent",
                padx=15,
                pady=10
            )
            desc_label.pack(fill="both", expand=True)

            # Create state variable for this ingredient
            is_expanded = ctk.BooleanVar(value=False)
            
            # Create the toggle function for this ingredient
            toggle_func = create_toggle_function(ingredient_frame, content_frame, is_expanded)

            # Create ingredient button
            ingredient_button = ctk.CTkButton(
                ingredient_frame,
                text=f"{ingredient['ingredient_name']} ▼",
                font=("Arial Bold", 14),
                fg_color="transparent",
                text_color="green",
                hover_color="#e0e0e0",
                corner_radius=10,
                anchor="w",
                command=lambda exp=is_expanded, tog=toggle_func: (exp.set(not exp.get()), tog())
            )
            ingredient_button.pack(fill="x", padx=15, pady=10)

            # Set up button text update
            update_text = create_button_update(ingredient_button, is_expanded, ingredient['ingredient_name'])
            is_expanded.trace_add('write', update_text)
    
    def on_back(self):
        self.destroy()

if __name__ == "__main__":
    app = IngredientsWindow()
    app.mainloop()