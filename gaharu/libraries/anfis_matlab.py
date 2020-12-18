import matlab
import matlab.engine
import numpy as np
class AnfisMatlab():
	def __init__(self, matengine):
		self.matengine = matengine


	def create_fis(self, data_no_label, only_label, radii, dirsave):
		data_no_label = matlab.double(data_no_label.tolist())
		only_label = matlab.double(only_label.tolist())
		radii = float(radii)
		dirfis = self.matengine.create_fis(data_no_label, only_label, radii, dirsave, nargout=1)
		return dirfis


	def mulai_pelatihan(self, dtrain, dirfis, epoch, dirsavefis=''):
		dtrain = matlab.double(dtrain.tolist())
		epoch = float(epoch)

		rmse, stepsize = self.matengine.training(dtrain, dirfis, epoch, dirsavefis, nargout=2)
		rmse = np.asarray(rmse)
		stepsize = np.asarray(stepsize)
		return (dirsavefis, rmse, stepsize)

	def mulai_pengujian(self, duji, dirfis):
		duji = matlab.double(duji.tolist())
		predicted = self.matengine.testing(duji, dirfis, nargout=1)
		predicted = np.asarray(predicted)
		return predicted

