from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Dataset, Model
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
import json
from utils import pretty_request

def index(request):
    return HttpResponse('welcome')


def data_master(request):
    datasets = Dataset.pdobjects.all()
    kelass = [0, 1, 2, 3]
    context = {
        "datasets": datasets,
        "kelass": kelass
    }
    return render(request, 'gaharu/data-master.html', context)


def proses_input(request):
    QueryDict = request.POST
    image64 = QueryDict.get('image')
    kelas = QueryDict.get('kelas')
    formatt, imgstr = image64.split(';base64,')
    ext = formatt.split('/')[-1]
    filename = str(uuid.uuid4())
    fileImg = ContentFile(base64.b64decode(imgstr), name=filename + "." + ext)
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

    response = {
        'success': 1,
    }
    return JsonResponse(response, safe=False)


def data_ekstraksi(request):
    return HttpResponse('welcome')
    pass


def data_anfis(request):
    models = Model.objects.all()
    context = {
        'models': models
    }
    return render(request, 'gaharu/data-anfis.html', context)

def tambah_model(request):
    return render(request, 'gaharu/tambah-model.html')

def proses_pelatihan(request):
    simpan = request.POST.get('simpan')
    nama_model = request.POST.get('nama_model')
    persen_uji = request.POST.get('persen_uji')

     



def proses_anfis(request):
    epoch = int(request.GET.get('epoch')) if request.GET.get('epoch') else 1
    folds = int(request.GET.get('folds')) if request.GET.get('folds') else 10
    fold = int(request.GET.get('fold')) if request.GET.get('fold') else 1
    opsi = int(request.GET.get('opsi')) if request.GET.get('opsi') else 1

    data_master = Dataset.pdobjects.all().to_dataframe()
    df = data_master.copy().iloc[:, 2:14]
    x = df.iloc[:, :11]
    y = df.iloc[:, 11]
    fold = fold - 1

    if (opsi == 1):
        skf = StratifiedKFold(n_splits=folds)
        collection_index = []
        loop = 1
        for train_index, test_index in (skf.split(x, y)):
            dictt = {
                'fold': loop,
                'index_latih': train_index.tolist(),
                'index_uji': test_index.tolist()
            }
            collection_index.append(dictt)
            loop = loop + 1

        context = {
            'result': json.dumps(collection_index),
            'data_master': df.to_json()
        }
        return JsonResponse(context, safe=False)

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
