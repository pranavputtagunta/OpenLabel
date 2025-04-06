import cv2
import PIL
import process_product_img as processor

food_recommender = processor.FoodRecommender('user_preferences.json')


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Could not open video device")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Check for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # Press 's' to stop and process the frame
        cv2.destroyWindow('Camera Feed')

        # Convert the frame to PIL Image
        image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        response = food_recommender.process_product_image(image)
        food_recommender.create_response_json()
        print("Response from Food Recommender:", response)

        # Draw a circle marker on the frame
        frame = cv2.circle(frame, (int(frame.shape[1] * response['center_coordinates']['x']), int(frame.shape[0] * response['center_coordinates']['y'])), 20, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('Captured Frame', frame)
        cv2.waitKey(0)  # Wait indefinitely until another key is pressed

    elif key == ord('c'):  # Press 'c' to continue the loop
        cv2.destroyWindow('Captured Frame')

    # Display the image (optional)
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()