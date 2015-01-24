import cv2
import numpy as np
import glob
import winsound
import time

listoffiles=[]
topleft_coords = [0, 0]

# predefined sizes of cutout window you can cycle through [width, height]
cutout_sizes = [ [20, 40], [40, 80], [60, 120], [80, 160], [100, 200], [120, 240] ]
cutout_size_idx = 0

image_idx = 0
cutout_idx = 0

# build a list of sample images
for image_file in glob.glob("SAIVT-SoftBio/Uncontrolled/Subject001/Camera01/*.jpeg"):
    print(image_file)
    listoffiles.append(image_file)

# count the number of samples collected so far
for sample_file in glob.glob("samples/*.*"):
    cutout_idx += 1

# read the first image from the list
image = cv2.imread(listoffiles[image_idx])

# callback function for mouse events
def callback_function(event,x,y,flags,param):
    global topleft_coords, cutout_idx
    if event == cv2.EVENT_LBUTTONDOWN:
        image_copy = np.copy(image)
        cv2.rectangle(image_copy, (x, y), (x + cutout_sizes[cutout_size_idx][0], y + cutout_sizes[cutout_size_idx][1]), (0, 255, 0), 1)
        cv2.imshow("image", image_copy)
        topleft_coords[0] = x
        topleft_coords[1] = y
    if event == cv2.EVENT_RBUTTONDOWN:
        winsound.Beep(440, 200)
        time.sleep(0.2)
        region = image[topleft_coords[1] : topleft_coords[1] + cutout_sizes[cutout_size_idx][1], topleft_coords[0] : topleft_coords[0] + cutout_sizes[cutout_size_idx][0]]
        path = "samples/cutout_%05d.png" % cutout_idx
        cv2.imwrite(path, region)
        cutout_idx += 1
        print path + " saved!"

# create display window, show the initial image
cv2.namedWindow('image')
cv2.imshow("image", image)

# bind the mouse events to callback function
cv2.setMouseCallback('image', callback_function)


while(True):
    key_pressed = cv2.waitKey(1) & 0xFF
    # load and show next image from the list
    if key_pressed == ord('x') and (image_idx < len(listoffiles)-1):
        image_idx += 1
        image = cv2.imread(listoffiles[image_idx])
        cv2.imshow("image", image)
        print "displaying image", image_idx+1, " out of ", len(listoffiles)-1
    # load and show previous image from the list
    if key_pressed == ord('z') and (image_idx > 0):
        image_idx -= 1
        image = cv2.imread(listoffiles[image_idx])
        cv2.imshow("image", image)
        print "displaying image", image_idx+1, " out of ", len(listoffiles)-1
    # increase image sample size
    if key_pressed == ord('s') and cutout_size_idx < len(cutout_sizes) - 1:
        cutout_size_idx += 1
        print "cutout size is " + str(cutout_sizes[cutout_size_idx])
    # decrease image sample size
    if key_pressed == ord('a') and cutout_size_idx > 0:
        cutout_size_idx -= 1
        print "cutout size is " + str(cutout_sizes[cutout_size_idx])
    # exit when ESC hit
    elif key_pressed == 27:
        break

cv2.destroyAllWindows()