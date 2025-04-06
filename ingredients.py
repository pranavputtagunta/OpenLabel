import customtkinter as ctk
import json
from PIL import Image, ImageTk
import backend.process_product_img as processor
import os

class IngredientsWindow(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        
        # Configure window
        self.title("Ingredients Information")
        self.geometry("800x800")
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


        # Create search frame
        self.search_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            height=120
        )
        self.search_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Search label
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="See an ingredient that's not on here? Just Ask:",
            font=("Arial Bold", 14),
            text_color="green"
        )
        self.search_label.pack(pady=(10, 5))

        # Create input and button layout frame
        self.input_frame = ctk.CTkFrame(
            self.search_frame,
            fg_color="transparent"
        )
        self.input_frame.pack(fill="x", padx=10)

        # Search input
        self.search_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter ingredient name...",
            font=("Arial", 12),
            height=35,
            width=500,
            corner_radius=10,
            border_color="green",
            fg_color="white",
            text_color="black"
        )
        self.search_input.pack(side="left", padx=(0, 10))

        # Search button
        self.search_button = ctk.CTkButton(
            self.input_frame,
            text="Search",
            font=("Arial Bold", 12),
            fg_color="green",
            hover_color="darkgreen",
            corner_radius=10,
            width=100,
            height=35,
            command=self.search_ingredient
        )
        self.search_button.pack(side="left")

        # Response label
        self.response_container = ctk.CTkFrame(
            self.search_frame,
            fg_color="white",
            corner_radius=15,
            height=120
        )
        self.response_container.pack(fill="x", padx=20, pady=(10, 0))

        # Inner response frame with subtle shadow effect
        self.response_frame = ctk.CTkFrame(
            self.response_container,
            fg_color="#f8f8f8",
            corner_radius=12,
            border_width=1,
            border_color="#e0e0e0"
        )
        self.response_frame.pack(fill="x", padx=5, pady=5, ipady=10)

        # Response header
        self.response_header = ctk.CTkLabel(
            self.response_frame,
            text="Search Results",
            font=("Arial Bold", 13),
            text_color="green",
            anchor="w"
        )
        self.response_header.pack(padx=15, pady=(10, 5), anchor="w")

        # Response content
        self.response_label = ctk.CTkLabel(
            self.response_frame,
            text="Enter an ingredient above to search...",
            font=("Arial", 12),
            text_color="#555555",
            wraplength=600,
            justify="left",
            anchor="w"
        )
        self.response_label.pack(padx=15, pady=(0, 10), fill="x")

        self.explainer = processor.IngredientExplainer('backend/user_profile.json')

    
    def search_ingredient(self):
        query = self.search_input.get().strip()
        if query:
            # Here you would typically make an API call or database query
            # For now, we'll just show a placeholder response

            response = self.explainer.get_response(query)
            self.response_label.configure(text=response)
        else:
            self.response_label.configure(text="Please enter an ingredient to search")


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