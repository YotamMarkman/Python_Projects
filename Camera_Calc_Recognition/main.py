import cv2
import numpy as np
import time

# Function for arithmetic calculations
def calculations(num1, num2, function_to_do) -> int:
    function_to_do = function_to_do.lower()
    if function_to_do == "add" or function_to_do == "addition":
        return num1 + num2
    elif function_to_do == "subtract" or function_to_do == "subtraction":
        return num1 - num2
    elif function_to_do == "multiply":
        return num1 * num2
    elif function_to_do == "divide" or function_to_do == "division":
        return num1 / num2
    else:
        return None
 
# Function to detect the number of fingers
def detect_and_recognize_number(frame):
    # Convert the frame to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return frame, None  # No hand detected

    # Assume the largest contour is the hand
    max_contour = max(contours, key=cv2.contourArea)

    # Find the convex hull and convexity defects
    hull = cv2.convexHull(max_contour, returnPoints=False)
    defects = cv2.convexityDefects(max_contour, hull)

    if defects is None:
        return frame, None  # No fingers detected

    # Count the number of defects (gaps between fingers)
    finger_count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(max_contour[s][0])
        end = tuple(max_contour[e][0])
        far = tuple(max_contour[f][0])

        # Use angles and distances to filter real fingers
        a = np.linalg.norm(np.array(start) - np.array(far))
        b = np.linalg.norm(np.array(end) - np.array(far))
        c = np.linalg.norm(np.array(start) - np.array(end))
        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))

        if angle <= np.pi / 2:  # Consider angles less than 90 degrees
            finger_count += 1

    # Add one to count the thumb
    fingers = finger_count + 1

    # Draw the contour and hull
    cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)
    hull_points = cv2.convexHull(max_contour)
    cv2.drawContours(frame, [hull_points], -1, (255, 0, 0), 2)

    return frame, fingers

# Main code
if __name__ == "__main__":
    # Pick the operation
    while True:
        calculation = input("Pick between: add, subtract, multiply, and divide:\n").lower()
        if calculation in ["add", "subtract", "multiply", "divide"]:
            break  # Valid input, exit the loop
        else:
            print("Invalid input. Please choose a valid operation: add, subtract, multiply, or divide.")

    # Initialize variables for numbers
    firstNumber = []
    secondNumber = []
    number = None
    detecting_first_number = True
    print("Put up the amount of fingers corresponding to the number you want\n")

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Allow a little delay for everything to get sorted
    time.sleep(3)

    while detecting_first_number or not detecting_first_number:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, number = detect_and_recognize_number(frame)

        if number is not None:
            if detecting_first_number:
                firstNumber.append(number)
                print(f"Added {number} to the first number.")
            else:
                secondNumber.append(number)
                print(f"Added {number} to the second number.")

            time.sleep(2)  # Small delay to stabilize detections

        # Display the video feed
        cv2.imshow("Finger Detection", processed_frame)

        # Ask user whether to continue or stop after detecting each number
        if number is not None:
            user_input = input("Do you want to continue detecting for this number? (yes/no): ").strip().lower()
            if user_input == "no":
                if detecting_first_number:
                    detecting_first_number = False
                    print("Now showing fingers for the second number.")
                else:
                    break
            elif user_input != "yes":
                print("Invalid input. Assuming 'yes'.")

    combined_first_number = int("".join(map(str, firstNumber))) if firstNumber else None
    combined_second_number = int("".join(map(str, secondNumber))) if secondNumber else None

    # Perform the calculation
    if combined_first_number is not None and combined_second_number is not None:
        result = calculations(combined_first_number, combined_second_number, calculation)
        print(f"Result of {calculation}: {result}")
    else:
        print("Failed to detect both numbers.")

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
