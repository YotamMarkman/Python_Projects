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
 
def detect_and_recognize_number(frame):
    # Convert to grayscale with adaptive thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding for better contrast
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return frame, None

    # Find the largest hand contour
    hand_contour = max(contours, key=cv2.contourArea)
    
    # Convex hull and convexity defects
    hull = cv2.convexHull(hand_contour, returnPoints=False)
    defects = cv2.convexityDefects(hand_contour, hull)

    if defects is None:
        return frame, None

    # Count fingers more robustly
    finger_count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = hand_contour[s][0]
        end = hand_contour[e][0]
        far = hand_contour[f][0]

        # Compute angle and distance
        a = np.linalg.norm(start - far)
        b = np.linalg.norm(end - far)
        c = np.linalg.norm(start - end)

        # Enhanced angle calculation with depth threshold
        angle = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))
        if angle < np.pi/2 and d > 10000:  # Added depth threshold
            finger_count += 1

    # Visualize results
    cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
    hull_points = cv2.convexHull(hand_contour)
    cv2.drawContours(frame, [hull_points], -1, (255, 0, 0), 2)

    return frame, finger_count + 1  # Add thumb


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
    detecting_second_number = True
    print("Put up the amount of fingers corresponding to the number you want\n")

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Allow a little delay for everything to get sorted
    time.sleep(5)

    while detecting_first_number or not detecting_first_number:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, number = detect_and_recognize_number(frame)

        if number is not None:
            if detecting_first_number:
                firstNumber.append(number)
                print(f"Added {number} to the first number.")

            time.sleep(2)  # Small delay to stabilize detections

        # Display the video feed
        cv2.imshow("Finger Detection", processed_frame)

        # Ask user whether to continue or stop after detecting each number
        if number is not None:
            user_input = input("Do you want to continue detecting for this number? (yes/no): ").strip().lower()
            if user_input == "no":
                break
            elif user_input != "yes":
                print("Invalid input. Assuming 'yes'.")
                
    cap.release()
    
    print("Now show for the second numebr")
    
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Allow a little delay for everything to get sorted
    time.sleep(5)

    while detecting_second_number or not detecting_second_number:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, number = detect_and_recognize_number(frame)

        if number is not None:
            if detecting_second_number:
                secondNumber.append(number)
                print(f"Added {number} to the second number.")

            time.sleep(2)  # Small delay to stabilize detections

        # Display the video feed
        cv2.imshow("Finger Detection", processed_frame)

        # Ask user whether to continue or stop after detecting each number
        if number is not None:
            user_input = input("Do you want to continue detecting for this number? (yes/no): ").strip().lower()
            if user_input == "no":
                break
            elif user_input != "yes":
                print("Invalid input. Assuming 'yes'.")
    
    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

    combined_first_number = int("".join(map(str, firstNumber))) if firstNumber else None
    combined_second_number = int("".join(map(str, secondNumber))) if secondNumber else None

    # Perform the calculation
    if combined_first_number is not None and combined_second_number is not None:
        result = calculations(combined_first_number, combined_second_number, calculation)
        print(f"Result of {calculation}: {result}")
    else:
        print("Failed to detect both numbers.")

