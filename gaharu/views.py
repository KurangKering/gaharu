from django.shortcuts import render, HttpResponse
from .models import Dataset
from django.core.files.base import ContentFile
import base64
from .libraries.glcm import GLCM
from .libraries.feature import Morfologi
import uuid
import numpy as np
import cv2
from pprint import pprint
from sklearn.model_selection import StratifiedKFold
from itertools import islice, count
from gaharu.libraries.anfis_pytorch.myanfis import train_hybrid, predict_data_test
import torch
def index(request):
    return HttpResponse('welcome')


def data_master(request):
    datasets = Dataset.objects.all()
    context = {
        "datasets": datasets,
        "lanjut": 'kdok'
    }
    return render(request, 'gaharu/data_master.html', context)


def proses_input(request):
    QueryDict = request.POST
    image64 = QueryDict.get('image')
    kelas = QueryDict.get('kelas')

    formatt, imgstr = image64.split(';base64,')
    ext = formatt.split('/')[-1]
    filename = str(uuid.uuid4())
    fileImg = ContentFile(base64.b64decode(imgstr), name=filename+"." + ext)
    image = cv2.imdecode(np.fromstring(fileImg.read(), np.uint8), 1)

    feature = Morfologi(image)
    glcm = GLCM(image)

    dataset = Dataset()
    dataset.filename = fileImg
    dataset.form_factor = feature.form_factor()
    dataset.aspect_ratio = feature.aspect_ratio()
    dataset.rect = feature.rect()
    dataset.narrow_factor = feature.narrow_factor()
    dataset.prd = feature.prd()
    dataset.plw = feature.plw()
    dataset.idm = glcm.idm()
    dataset.entropy = glcm.entropy()
    dataset.asm = glcm.asm()
    dataset.contrast = glcm.contrast()
    dataset.correlation = glcm.korelasi()
    dataset.kelas = kelas
    dataset.is_extracted = 1
    dataset.save()

    return HttpResponse('welcome')


def data_ekstraksi(request):
    return HttpResponse('welcome')
    pass


def data_anfis(request):
    pass


def proses_anfis(request):
    epoch = int(request.GET.get('epoch'))
    folds = int(request.GET.get('folds'))
    fold = int(request.GET.get('fold'))

    df = Dataset.pdobjects.all().to_dataframe().iloc[:, 2:14]
    x = df.iloc[:, :11]
    y = df.iloc[:, 11]
    skf = StratifiedKFold(n_splits=folds)
    split = skf.split(x,y)

    fold = fold - 1
    train_index, test_index = next(islice(split, fold, fold + 1))

    train_data = df.iloc[train_index].to_numpy()
    test_data = df.iloc[test_index].to_numpy()
    x_test = test_data[:, :-1]
    y_test = test_data[:, -1]

    model = train_hybrid(train_data, epoch)
    modelname = "{} folds {} epoch fold {}.fis".format(folds, epoch, fold)
    torch.save(model, modelname)
    predicted = predict_data_test(model, x_test, y_test)


    return HttpResponse(predicted)


def klasifikasi(request):
    return HttpResponse('welcome')
    pass


def pengujian(request):
    return HttpResponse('welcome')
    pass
