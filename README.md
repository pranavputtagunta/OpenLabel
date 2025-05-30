# OpenLabel Guide
![Logo](/assets/logo.jpg)
## Project Story
**According to food allergy research and education, 3.4 million patients have food allergy related emergency room visits**

Most food products found in your average grocery store are not explicitly labeled and more often than not, the nutrition and ingredient labels on them are difficult to interpret for the average consumer. 

Furthermore, some food products that are marketed as _healthy products_ may contain potential harmful chemicals and allergens that can lead to drastic and unexpected outcomes.

We wanted to help people understand **exactly** what they are putting into their bodies in the context of their own health - not what the flashy packaging tends to lead you to believe.

**We believe everyone deserves honest food.**
## Overview
![devpost](https://devpost.com/software/openlabel)
## Installation
To start, clone the git repository
```
git clone https://github.com/pranavputtagunta/OpenLabel.git
```
Then, to install dependencies, run the command
```
pip install -r requirements.txt
```
Additionally, configure your API Key in 
```
backend/process_product_img.py
```
## Usage
To start VisLink, run this command in the project directory:
```
python MainWindow.py
```

After a few seconds, the following screen will show up.\
![Screen1](/assets/screen1.jpg)\
From here, you will have the ability to enter your diet preferences, restrictions, and goals. These will be used to personalize your recommendations.\
![Screen2](/assets/screen2.jpg)\
You can then take pictures of different food items using the analyze button, and the app will automatically detect and draw a bounding box around the image. Use the S in the top right to adjust your settings. Press R in the top right to reset and take another photo.\
![Screen3](/assets/screen3.jpg)\
After you take a picture, a description of the food will pop up, giving you feedback and recommendations on whether or not you should purchase it, depending on your goals.\
![Screen4](/assets/screen4.jpg)\
When you click the ingredients button, you can view a list of general ingredients. Clicking each one will provide a brief description and health impacts of the ingredient. If an ingredient isn't listed, you can search for it at the bottom.\
![Screen5](/assets/screen5.jpg)\
When you click the alternatives button, you can view a list of similar products that better align with your preferences along with an Amazon link to buy the product.\
![Screen6](/assets/screen6.jpg)\
![Screen7](/assets/screen7.jpg)\
