import customtkinter as ctk
import requests
from PIL import Image, ImageTk
import json
import os
import io

class AlternativesWindow(ctk.CTk):
    def __init__(self, product_data=None):
        super().__init__()
        
        # Configure window
        self.title("Alternative Products")
        self.geometry("800x600")
        self._set_appearance_mode("light")
        self.configure(fg_color="white")

        # Back button
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
        
        # Create scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            width=750,
            height=500  # Adjusted to accommodate back button
        )
        self.main_frame.pack(pady=(0, 20), padx=20, expand=True, fill="both")
        
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
        self.bottom_back_button.pack(pady=(0, 20))

        # Store product data
        self.product_data = self.parse_json("./backend/response.json")
        
        # Create product cards
        self.create_product_cards()
    
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
        
    def get_default_data(self):
        return {
            "alternative_products": [
                {
                    "product_name": "Example Product",
                    "image_url": "placeholder.png"
                }
            ]
        }
    
    def create_product_card(self, product, row):
        # Create frame for product card
        card_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#f8f8f8",
            corner_radius=15,
            height=150
        )
        card_frame.pack(pady=10, padx=20, fill="x")
        card_frame.pack_propagate(False)

        product = self.parse_json("./backend/response.json")["alternative_products"][row] 
        print(product)
        try:
            # Load and resize product image from URL
            # Note: In production, you'd want to download and cache the image
            response = requests.get(product.get("image_url", ""))

            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))  # Use placeholder for now
                image = image.resize((120, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                image_label = ctk.CTkLabel(
                    card_frame,
                    image=photo,
                    text=""
                )
                image_label.image = photo
                image_label.pack(side="left", padx=15, pady=15)
            else:
                raise Exception("Failed to fetch image")
        except:
            placeholder = ctk.CTkLabel(
                card_frame,
                text="No Image",
                width=120,
                height=120,
                fg_color="#eeeeee",
                text_color="gray"
            )
            placeholder.pack(side="left", padx=15, pady=15)
        
        # Create info frame
        info_frame = ctk.CTkFrame(
            card_frame,
            fg_color="transparent"
        )
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
        
        # Product name
        name_label = ctk.CTkLabel(
            info_frame,
            text=product.get("product_name", "Unknown Product"),
            font=("Arial Bold", 16),
            text_color="#2F2F2F",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # View button that opens URL
        view_button = ctk.CTkButton(
            info_frame,
            text="View on Amazon",
            font=("Arial Bold", 12),
            fg_color="green",
            hover_color="darkgreen",
            corner_radius=20,
            width=120,
            height=32,
            command=lambda url=product.get("product_link"): self.open_url(url)
        )
        view_button.pack(anchor="w", pady=(10, 0))
    
    def create_product_cards(self):
        for i, product in enumerate(self.product_data.get("alternative_products", [])):
            self.create_product_card(product, i)
    
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
    
    def on_back(self):
        self.destroy()

if __name__ == "__main__":
    # Test window with sample data
    test_data = {
        "alternative_products": [
            {
                "product_name": "Gluten-Free Crackers",
                "image_url": "https://www.amazon.com/Gluten-Free-Crackers/s?k=Gluten-Free+Crackers"
            },
            {
                "product_name": "Vegetable Sticks",
                "image_url": "https://www.amazon.com/Vegetable-Sticks/s?k=Vegetable+Sticks"
            }
        ]
    }
    app = AlternativesWindow(test_data)
    app.mainloop()