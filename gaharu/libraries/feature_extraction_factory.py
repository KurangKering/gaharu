from .glcm import GLCM
from .morfologi import Morfologi

class FeatureExtractionFactory:
	def __init__(self):
		pass

	def make_morfologi(self, rgb_array):
		return Morfologi(rgb_array)

	def make_glcm(self, rgb_array):
		return GLCM(rgb_array)
