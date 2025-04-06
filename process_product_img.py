import google.generativeai as genai
import os
import json
import PIL.Image as Image
from PIL import ImageFile

# Set your API key here

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

default_system_insructions = """
You are a helpful assistant that determines whether a product image is appropriate for a specific user based on their preferences.
You will receive a product image and user preferences, including dietary restrictions and goals. Your task is to analyze the image and provide feedback on its appropriateness based on the user's preferences.
Please output only a JSON with the following fields and no other response. Don't include extra brackets, special characters, or any other text. Start and end with curly braces. The JSON should be formatted as follows:

- "is_appropriate": A yes, no, or maybe indicating whether the product is appropriate for the user based on their preferences.
- "rating": An integer rating from 1 to 10, where 1 is not recommended at all and 10 is recommended. 1-4 is not appropriate, 5-7 is somewhat appropriate, and 8-10 is very appropriate.
- "category": The category of the product (e.g., food, beverage, supplement).
- "product_name": The name of the product in the image. Respond with "error" if no object is detected in the image.
- "image_url": The URL of the product image from the web.
- "bounding_box": The coordinates of the bounding box around the product in the image. This should be in [ymin, xmin, ymax, xmax] normalized from 0-1000 for every coordinate with the top left as the origin.
- "feedback": string providing details on why the image is or isn't appropriate
- "nutrition_info":
    "calories": string providing the calorie content of the product,
    "protein": string providing the protein content of the product,
    "carbohydrates": string providing the carbohydrate content of the product,
    "fat": string providing the fat content of the product,
    "sugar": string providing the sugar content of the product,
    "fiber": string providing the fiber content of the product,
- "price": string providing the price of the product in the image
- "alternative_products": list of similar products that are more appropriate for the user if the product is not appropriate. Make the alternatives either diet versions of it or snacks that are very similar but healthier. None if it is appropriate.
- "ingredients": list of ingredients in the product.
    "ingredient_name": string providing the name of the ingredient,
    "description": string providing a description of the ingredient and health impacts,

{
  "is_appropriate": "yes" or "no" or "maybe",
  "rating": int,
  "category": "string",
  "product_name": "string",
  "image_url": "string",
  "bounding_box": {
    "ymin": int,
    "xmin": int,
    "ymax": int,
    "xmax": int
  },
  "feedback": "string",
  "nutrition_info": {
    "calories": string,
    "protein": string,
    "carbohydrates": string,
    "fat": string,
    "sugar": string,
    "fiber": string
  },
  "price": string,
  "alternative_products": [
    {
      "product_name": string,
      "image_url": string
    }
  ] or None,
  "ingredients": [
    {
      "ingredient_name": string,
      "description": string
    }
  ]
}
"""

default_safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

default_config = {
    "temperature": 0.25,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"
}

class UserPreferences:
    diet: str
    food_restrictions: [str]
    goals: [str]

    def to_dict(self):
        return {
            "diet": self.diet,
            "food_restrictions": self.food_restrictions,
            "goals": self.goals
        }

class FoodRecommender:
    def __init__(self, user_pref_json: str, system_instructions=default_system_insructions, safety_settings=default_safety_settings, config=default_config):
        self.user_preferences = get_user_preferences(user_pref_json)
        self.response = None
        self.model = genai.GenerativeModel(
            model_name= "gemini-2.0-flash",
            safety_settings=safety_settings,
            system_instruction=system_instructions,
            generation_config=config
        )

    def process_product_image(self, image: ImageFile) -> dict:
        # Call the API to process the product image
        response = self.model.generate_content(contents=[json.dumps(self.user_preferences.to_dict()), image])
        # Parse the response and return it as a dictionary
        self.response = json.loads(response.text[response.text.index("{"):response.text.rindex("}")+1])
        return self.response
    
    def create_response_json(self, file_path: str = "response.json"):
        # Check if the response is available
        if self.response is None:
            raise Exception("No response available. Please process an image first.")
        # Create a JSON file with the response
        with open(file_path, 'w') as file:
            json.dump(self.response, file, indent=4)

def get_user_preferences(json_file_path: str) -> UserPreferences:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        user_preferences = UserPreferences()
        user_preferences.diet = data.get('diet', '').split(",")
        user_preferences.food_restrictions = data.get('food_restrictions', '').split(",")
        user_preferences.goals = data.get('goals', [])
    return user_preferences

def get_PIL_image(image_path: str) -> Image.Image:
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None