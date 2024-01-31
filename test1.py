import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Video capture
cap = cv2.VideoCapture('juggling2.mov')

kernel = np.ones((5,5), np.uint8)

#Initialize the background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()


#creating xy list for location tracking
points = []
# Initialize a counter for the centroids
centroid_counter = 0

while True:
   # Read the frame
   ret, frame = cap.read()
   if not ret:
      break
   
   fgmask = cv2.dilate(frame, kernel, iterations = 5)
   
   fgmask = cv2.GaussianBlur(frame, (7,7), 5)
   # Apply background subtraction
   fgmask = fgbg.apply(frame)
   
   
   # Apply erosion
   fgmask = cv2.erode(fgmask, kernel, iterations = 3)
   
   
   
   
   # Apply dilation
   fgmask = cv2.dilate(fgmask, kernel, iterations = 3)
   
    
   #Clean up image
   fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
   

   #Draw shapes around detected balls
   # Find contours in the mask
   contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   for contour in contours:
      # Ignore small contours
      if cv2.contourArea(contour) < 1700: 
         continue
         
      (x, y, w, h) = cv2.boundingRect(contour)
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      #cv2.putText(frame, "BALL", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

   
      mome = cv2.moments(contour)
      cX = int(mome["m10"] / mome["m00"])
      cY = int(mome["m01"] / mome["m00"])
      cv2.circle(frame, (cX,cY), 3, (0,255,0), -1)
      xy = (cX,cY)
     
      points.append(xy)
      # Increment the counter
      centroid_counter += 1
   # Display the frame
   cv2.imshow('Frame', frame)
   
   # Break the loop on 'q' key press
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
# Release the video capture object
cap.release()
print(centroid_counter/3)
# Close all OpenCV windows
cv2.destroyAllWindows()

