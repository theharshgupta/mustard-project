from matplotlib import image
import numpy as np
import os
from PIL import Image
import json

def distance(pixel, background_pixel):
    # vals and standard have to be lists of lenth 3
    # nonstandard distance formula
    return abs(sum(pixel - background_pixel))


def hue_calc(pixel):
    # pixel is a list
    a = max(pixel)
    i = min(pixel)
    diff = (a - i)
    if diff == 0:
        diff = 1
    if pixel.index(a) == 1:
        return 60 * (2 + (pixel[2] - pixel[0]) / diff)
    elif pixel.index(a) == 0:
        return 60 * ((pixel[1] - pixel[2]) / diff)
    else:
        return 60 * (4 + (pixel[0] - pixel[1]) / diff)


def saturation_calc(pixel):
    if max(pixel):
        return (max(pixel) - min(pixel)) / max(pixel)
    else:
        return 0


def calculate_percentage(filename, tolerance=20):
    background = np.array([255, 255, 255])
    X_rgb = []
    top_pixels_to_be_removed = 50
    min_bottom_pixel = 480
    # filename is the image
    img = image.imread(filename)
    arr = np.array(img)
    X_rgb.append(arr[top_pixels_to_be_removed:min_bottom_pixel, :, :])
    # takes pixel rows between top_pixels_to_be_removed and min_bottom_p
    n_of_relevant_pixels = 0
    height, width = arr.shape[0], arr.shape[1]
    total_pixels = height * width
    n1, n2, n3, n4 = 0, 0, 0, 0
    done = 0
    total = width * 4
    for i in range(height):
        for j in range(width):
            done += 1
            pixel = arr[i, j]
            pixel2 = [pixel[0] / 255, pixel[1] / 255, pixel[2] / 255]
            hue, saturation, value = hue_calc(pixel2), saturation_calc(pixel2), max(pixel2)
            r, g, b = pixel[0] * np.ones((2, 2)), pixel[1] * np.ones((2, 2)), pixel[2] * np.ones((2, 2))
            image_array = np.dstack((r, g, b)).astype(np.uint8)
            im = Image.fromarray(image_array)
            print(100 * done / total, "percent done | ", done, [hue, saturation, value])
            if distance(pixel, background) > tolerance and saturation > 0.1 and hue < 150:
                n_of_relevant_pixels += 1
                if (hue > 53 or (hue > 47 and value < 0.65)) and saturation > 0.3 and value > 0.17:
                    im.save('g' + str(done) + '.png')
                    n1 += 1
                    # (40,58) (59,60),(73,62), (96, 64)
                elif (value < 0.63) and hue < 45:
                    im.save('b' + str(done) + '.png')
                    n4 += 1
                else:
                    im.save('n' + str(done) + '.png')
                    n2 += 1
            else:
                n3 += 1
                im.save('np' + str(done) + '.png')

    green_percentage = n1 / n_of_relevant_pixels
    brown_percentage = n4 / n_of_relevant_pixels
    sample_and_not_green_or_brown_percentage = n2 / n_of_relevant_pixels
    Acceptable = n3 / n_of_relevant_pixels < 0.5
    return json.dumps({'Green Percentage': green_percentage, 'Brown Percentage': brown_percentage,
                       'Sample_not_brown_or_green': sample_and_not_green_or_brown_percentage, 'Seems Good': Acceptable})