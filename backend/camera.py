import cv2
import PIL
import backend.process_product_img as processor

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

        # Convert the frame to PIL Image
        image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        response = food_recommender.process_product_image(image)
        print("Response from Food Recommender:", response)

        # Draw a bounding box around the detected object (optional)
        if response['product_name'] == "error":
            print("Error in processing the image.")
            continue

        food_recommender.create_response_json()

        x_min = int(frame.shape[1] * response['bounding_box']['xmin'] / 1000)
        y_min = int(frame.shape[0] * response['bounding_box']['ymin'] / 1000)
        x_max = int(frame.shape[1] * response['bounding_box']['xmax'] / 1000)
        y_max = int(frame.shape[0] * response['bounding_box']['ymax'] / 1000)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Camera Feed', frame)
        cv2.waitKey(0)  # Wait indefinitely until another key is pressed

    elif key == ord('c'):  # Press 'c' to continue the loop
        pass

    # Display the image (optional)
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()