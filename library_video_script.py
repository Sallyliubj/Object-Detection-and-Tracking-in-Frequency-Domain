import cv2 as cv
import numpy as np
import os

def find_local_maximums(lst):
    local_maximums = []
    for i in range(0, len(lst) - 1):
        if lst[i][0] > lst[i - 1][0] and lst[i][0] > lst[i + 1][0]:
            local_maximums.append(lst[i])
    return local_maximums

# Path to the folder containing images
folder_path = 'Videos_with_moving_stickers/library_vid'

# Get list of image files in the folder
image_files = sorted([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))])

# Load the first image to get dimensions
first_image = cv.imread(image_files[0], 0)
first_image_f = np.fft.fftshift(np.fft.fft2(first_image))
first_image_mags = np.log(1 + np.abs(first_image_f))
first_image_mags = np.uint8(255 * first_image_mags / np.max(first_image_mags))
background_blurred_fft = cv.GaussianBlur(first_image_mags, (9,9), 2)
height, width = first_image.shape

# initialize frame counter
c = 0

# grayscale value thesholds between which our sticker shows up
threshold_low = 18
threshold_high = 36

for image_file in image_files:
    # Read every 1 in every c images
    if (c % 10 == 0):
        image = cv.imread(image_file, 0)
        image = cv.flip(image, 0)
        image = cv.flip(image, 1)

        # Perform FFT
        f_transform = np.fft.fft2(image)
        f_shift = np.abs(np.fft.fftshift(f_transform))
        mags = np.log(1 + np.abs(f_shift))
        mags = np.uint8(255 * mags / np.max(mags))

        # Perform a gaussian blur on the mags since fft is inherintly 'noisy'
        blurred_fft = cv.GaussianBlur(mags, (9, 9), 2)

        # Background subtract to isolatet noise
        backgound_subtract_of_blurred_fft = blurred_fft - background_blurred_fft

        # Isolate the fft content corresponding to the sticker
        low_fft = backgound_subtract_of_blurred_fft > threshold_low
        high_fft = backgound_subtract_of_blurred_fft < threshold_high
        sticker_isolated_fft = backgound_subtract_of_blurred_fft.copy()
        sticker_isolated_fft[low_fft & high_fft] = 255
        sticker_isolated_fft[~(low_fft & high_fft)] = 0

        # Create display with isolated sticker fft, background subtracted blurred fft, blurred fft, and image
        upper_disp = np.hstack((sticker_isolated_fft, image))
        lower_disp = np.hstack((backgound_subtract_of_blurred_fft, blurred_fft))
        disp = np.vstack((upper_disp, lower_disp))

        # Display video: press any key to move forward c frames
        cv.namedWindow('Display', cv.WINDOW_NORMAL)
        cv.resizeWindow('Display', 1200, 720)
        cv.imshow('Display', disp)
        cv.waitKey(0)

    c += 1

cv.destroyAllWindows()
