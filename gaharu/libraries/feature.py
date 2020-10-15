from skimage.color import rgb2hsv
from skimage.filters import gaussian, threshold_otsu
from skimage.color import rgb2gray
from skimage import measure
from skimage.morphology import (
    disk,
    binary_closing,
    flood_fill,
    label,
    remove_small_objects)
from PIL import Image
import numpy as np
from skimage.io import imsave
import os
import cv2

import numpy as np
import scipy as sp
import scipy.ndimage


def flood_fill(test_array, h_max=255):
    input_array = np.copy(test_array)
    el = sp.ndimage.generate_binary_structure(2, 2).astype(np.int)
    inside_mask = sp.ndimage.binary_erosion(
        ~np.isnan(input_array), structure=el)
    output_array = np.copy(input_array)
    output_array[inside_mask] = h_max
    output_old_array = np.copy(input_array)
    output_old_array.fill(0)
    el = sp.ndimage.generate_binary_structure(2, 1).astype(np.int)
    while not np.array_equal(output_old_array, output_array):
        output_old_array = np.copy(output_array)
        output_array = np.maximum(input_array, sp.ndimage.grey_erosion(
            output_array, size=(3, 3), footprint=el))
    return output_array


def imcomplement(matrix):
    """
    Return the imcomplement of the matrix/image. Equivalent to Matlab's imcomplement function.
    """
    newmatrix = -matrix + np.max(matrix) + np.min(matrix)
    return newmatrix


def morphology(img):
    """
    proses morfologi: 
    img: gray
    """
    RADIUS = 4
    binary = (img > 170).astype(np.float)
    complement = imcomplement(binary)
    structure = disk(RADIUS)
    enclosed = binary_closing(complement, structure)
    imfilled = flood_fill(enclosed)
    cleaned = remove_small_objects(imfilled, min_size=60, connectivity=2)
    return cleaned


class Morfologi:
    def __init__(self, img):
        """
        img: image path-> string
        """
        self.img = img
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.binary = (self.gray > 170).astype(np.float)
        self.cleaned = morphology(self.gray)
        labels = measure.label(self.cleaned)

        self.props = measure.regionprops(labels)[0]
        self.diameter = self.props.equivalent_diameter
        self.area = self.props.area
        self.perimeter = self.props.perimeter
        self.length = self.props.major_axis_length
        self.width = self.props.minor_axis_length
        self.r = self.img[:, :, 2]
        self.g = self.img[:, :, 1]
        self.b = self.img[:, :, 0]

        # filename, ext = os.path.splitext(img)
        # filename_gray = filename+"-gray"+ext
        # filename_bin = filename+"-bin"+ext
        # filename_cleaned = filename+"-cleaned"+ext

        # im = Image.fromarray(self.gray)
        # im = im.convert("L")

        # im.save(filename_gray)
        # imsave(filename_bin, self.binary)
        # imsave(filename_cleaned, self.cleaned.astype(int))

    def form_factor(self):
        return (4 * np.pi * self.area)/(self.perimeter**2)

    def aspect_ratio(self):
        return self.length/self.width

    def rect(self):
        return (self.length*self.width)/self.area

    def narrow_factor(self):
        return self.diameter/self.length

    def prd(self):
        return self.perimeter/self.diameter

    def plw(self):
        return self.perimeter/(self.length+self.width)


if __name__ == '__main__':
    from skimage.io import imread
    import sys
    filename = sys.argv[1]
    morf = Morfologi(filename)
    print("python", "\t", "\t", )
    print("===============")
    print("prd\t", morf.prd())
    print("plw\t", morf.plw())
    print("rect\t", morf.rect())
    print("narrow factor\t", morf.narrow_factor())
    print("aspect ratio\t", morf.aspect_ratio())
    print("form factor\t", morf.form_factor())
