import cv2
from skimage.feature import greycomatrix
from skimage import img_as_ubyte
import numpy as np

class GLCM:
	def __init__(self, img_path, ROUNDING=4):
		img = img_path
		self.ROUNDING = ROUNDING
		image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		distance = [1]
		angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
		image = img_as_ubyte(image.astype('int64'))
		glcm_mat = greycomatrix(image,
								distances=distance,
								angles=angles)
		JML_PIKSEL = 256*256
		self.L = 256

		# matriks glcm untuk tiap sudut [0, 45, 90, 135]
		sudut_0 = glcm_mat[:, :, 0, 0]  # 0
		sudut_45 = glcm_mat[:, :, 0, 1]  # 45
		sudut_90 = glcm_mat[:, :, 0, 2]  # 90
		sudut_135 = glcm_mat[:, :, 0, 3]  # 135

		# normalisasi
		normal_0 = sudut_0/JML_PIKSEL
		normal_45 = sudut_45/JML_PIKSEL
		normal_90 = sudut_90/JML_PIKSEL
		normal_135 = sudut_135/JML_PIKSEL
		self.glcm = (normal_0+normal_45+normal_90+normal_135)/4

	def get_idm(self):
		idm = 0.0
		for x in range(self.L):
			for y in range(self.L):
				idm += self.glcm[x, y] / (1 + np.power((x - y), 2))
		return round(idm, self.ROUNDING)

	def get_entropy(self):
		E = 0.0
		for x in range(self.L):
			for y in range(self.L):
				if (self.glcm[x, y] > 0):
					E -= self.glcm[x, y] * np.log(self.glcm[x, y])
		return round(E, self.ROUNDING)

	def get_asm(self):
		return round(np.power(self.glcm.flatten(), 2).sum(), self.ROUNDING)

	def get_contrast(self):
		con = 0.0
		# kontras = kontras + (a-b)*(a-b)*(Mean_GLCM(a+1,b+1));
		for x in range(0, self.L-1):
			for y in range(0, self.L-1):
				con = con + (x-y)*(x-y) * (self.glcm[x+1, y+1])
		return round(con, self.ROUNDING)

	def get_korelasi(self):
		mean_baris = 0
		mean_kolom = 0
		varian_baris = 0
		varian_kolom = 0
		korelasi_ = 0

		# hitung mean

		for i in range(0, self.L-1):
			for j in range(0, self.L-1):
				mean_baris = mean_baris + i * self.glcm[i+1, j+1]
				mean_kolom = mean_kolom + j * self.glcm[i+1, j+1]

		for i in range(0, self.L-1):
			for j in range(0, self.L-2):
				varian_baris = varian_baris + \
					(i-mean_baris) * (i-mean_baris) * self.glcm[i+1, j+1]
				varian_kolom = varian_kolom + \
					(j-mean_kolom) * (j-mean_kolom) * self.glcm[i+1, j+1]

		for i in range(0, self.L-1):
			for j in range(0, self.L-2):
				korelasi_ = korelasi_ + \
					((i-mean_baris)*(j-mean_kolom) *
					 self.glcm[i+1, j+1])/(varian_baris*varian_kolom)

		return round(korelasi_, self.ROUNDING)
