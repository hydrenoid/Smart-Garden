import cv2
import numpy as np
import time
from fastiecm import fastiecm
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (1920, 1080)},
                                                      display="lores")
picam2.configure(camera_config)
picam2.start()

def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (r.astype(float) - b) / bottom # THIS IS THE CHANGED LINE
    return ndvi



#TODO: Takes a picture and saves it to the file "/Smart-Garden/Images/Originals"
def take_picture():
    
    

    original = picam2.capture_array("main")

    timestr = time.strftime("%Y%m%d-%H%M%S")

    cv2.imwrite('../Images/Originals/original.png', original)
    
    # Resize the image to fit in the window, e.g., 800x450
    resized_orig_image = cv2.resize(original, (400, 225))
    cv2.imwrite('../Images/Originals/resized.png', resized_orig_image)


    contrasted_image = contrast_stretch(original)
    ndvi_image = calc_ndvi(contrasted_image)
    ndvi_contrasted = contrast_stretch(ndvi_image)
    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    cv2.imwrite('../Images/final.png', color_mapped_image)
    
    # Resize the image to fit in the window, e.g., 800x450
    resized_image = cv2.resize(color_mapped_image, (800, 450))

    # Save the resized image temporarily (or you can use a memory buffer)
    temp_path = '../Images/final_resized.png'
    cv2.imwrite(temp_path, resized_image)
    
    print('PICTURE TAKEN AND SAVED')

    #todo process the image
    #health = process_image(original, timestr)


#TODO: Sparse out the plants from the rest of picture
def photo_sparse():
    print('Parsing out pictures.')


#TODO: Process image and return a health percentage
def process_image(original, timestr):
    contrasted = contrast_stretch(original)

    ndvi = calc_ndvi(contrasted)

    ndvi_contrasted = contrast_stretch(ndvi)

    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)

    cv2.imwrite('Images/Originals/original_' + timestr, color_mapped_image)

    # TODO: generate health index from image
    health = 0
    return health


