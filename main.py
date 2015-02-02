import cv2
import numpy as np
import glob
import winsound
import time

template_listoffiles = []
test_listoffiles = []
topleft_coords = [0, 0]

# predefined sizes of cutout window you can cycle through [width, height]
cutout_sizes = [[20, 40], [40, 80], [60, 120], [80, 160], [100, 200], [120, 240]]
cutout_size_idx = 0

template_image_idx = 0
test_image_idx = 0

# initialize the ORB detector/descriptor
orb = cv2.ORB()


# build a list of sample images
for template_image_file in glob.glob("SAIVT-SoftBio/Uncontrolled/Subject001/Camera01/*.jpeg"):
    print(template_image_file)
    template_listoffiles.append(template_image_file)

# build a list of images for testing
for test_image_file in glob.glob("SAIVT-SoftBio/Uncontrolled/Subject001/Camera03/*.jpeg"):
    print(test_image_file)
    test_listoffiles.append(test_image_file)

# read the first images from the list
image_template = cv2.imread(template_listoffiles[template_image_idx])
image_test = cv2.imread(test_listoffiles[test_image_idx])

# callback function for mouse events
def callback_function(event, x, y, flags, param):
    global topleft_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        image_copy = np.copy(image_joint)
        cv2.rectangle(image_copy, (x, y), (x + cutout_sizes[cutout_size_idx][0], y + cutout_sizes[cutout_size_idx][1]),
                      (0, 255, 0), 1)
        cv2.imshow("joint image", image_copy)
        topleft_coords[0] = x
        topleft_coords[1] = y
    if event == cv2.EVENT_RBUTTONDOWN:  # change the event from cutout saving to looking for similar object
        winsound.Beep(440, 200)
        time.sleep(0.2)
        cv2.destroyWindow("window")
        region = image_template[topleft_coords[1] - 20: topleft_coords[1] + cutout_sizes[cutout_size_idx][1] + 20,
                 topleft_coords[0] - 20: topleft_coords[0] + cutout_sizes[cutout_size_idx][0] + 20]
        keypoints_region = orb.detect(region, None)
        cv2.drawKeypoints(region, keypoints_region, region)
        cv2.imshow("window", region)



image_joint = np.hstack((image_template, image_test))

# create display window, show the initial image
cv2.namedWindow("joint image")
cv2.imshow("joint image", image_joint)

# bind the mouse events to callback function
cv2.setMouseCallback('joint image', callback_function)

while (True):
    key_pressed = cv2.waitKey(1) & 0xFF
    # load and show next image from the template image list
    if key_pressed == ord('x') and (template_image_idx < len(template_listoffiles) - 1):
        template_image_idx += 1
        image_template = cv2.imread(template_listoffiles[template_image_idx])
        image_joint = np.hstack((image_template, image_test))
        cv2.imshow("joint image", image_joint)
        print "displaying image", template_image_idx + 1, " out of ", len(template_listoffiles) - 1
    # load and show previous image from the template image list
    if key_pressed == ord('z') and (template_image_idx > 0):
        template_image_idx -= 1
        image_template = cv2.imread(template_listoffiles[template_image_idx])
        image_joint = np.hstack((image_template, image_test))
        cv2.imshow("joint image", image_joint)
        print "displaying image", template_image_idx + 1, " out of ", len(template_listoffiles) - 1
    # load and show next image from the test image list
    if key_pressed == ord('.') and (test_image_idx < len(test_listoffiles) - 1):
        test_image_idx += 1
        image_test = cv2.imread(test_listoffiles[test_image_idx])
        image_joint = np.hstack((image_template, image_test))
        cv2.imshow("joint image", image_joint)
        print "displaying image", test_image_idx + 1, " out of ", len(test_listoffiles) - 1
    # load and show previous image from the test image list
    if key_pressed == ord(',') and (test_image_idx > 0):
        test_image_idx -= 1
        image_test = cv2.imread(test_listoffiles[test_image_idx])
        image_joint = np.hstack((image_template, image_test))
        cv2.imshow("joint image", image_joint)
        print "displaying image", test_image_idx + 1, " out of ", len(test_listoffiles) - 1
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