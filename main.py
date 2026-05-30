import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

print("📸 Capturing background... Please move away")
time.sleep(3)

# -------- Capture Background --------
bg = None
for i in range(30):
    ret, bg = cap.read()
bg = np.flip(bg, axis=1)

print("✅ Background captured. Come in front with white cloth.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)

    # -------- Original Frame --------
    original_view = frame.copy()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # -------- WHITE COLOR RANGE --------
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Clean mask
    mask = cv2.medianBlur(mask, 7)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # -------- Invisible Effect --------
    cloak_area = cv2.bitwise_and(bg, bg, mask=mask)
    normal_area = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
    invisible_view = cv2.addWeighted(cloak_area, 1, normal_area, 1, 0)

    # -------- Show Both Windows --------
    cv2.imshow("Original Camera", original_view)
    cv2.imshow("Invisible Effect", invisible_view)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
