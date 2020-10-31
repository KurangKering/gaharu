from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, Http404
from .models import Dataset, Model
from django.core.files.base import ContentFile
import base64
from .libraries.glcm import GLCM
from .libraries.feature import Morfologi
import uuid
import numpy as np
import cv2
from PIL import Image
from pprint import pprint
from sklearn.model_selection import StratifiedKFold
from itertools import islice, count
import json
from utils import pretty_request
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
import os
from os.path import join
from django.conf import settings
import csv
import tempfile


def index(request):
    if not request.user.is_authenticated:
        return redirect("index")
    return render(request, 'dashboard.html')


def data_master(request):
    if not request.user.is_authenticated:
        return redirect("index")
    datasets = Dataset.pdobjects.all()
    kelass = [0, 1, 2, 3]
    context = {
        "datasets": datasets,
        "kelass": kelass
    }
    return render(request, 'gaharu/data-master.html', context)

def tambah_data_master(request):
    return render(request, 'gaharu/tambah-data-master.html')

def proses_tambah_data_master(request):
    if not request.user.is_authenticated:
        return redirect("index")
    QueryDict = request.POST
    image64 = QueryDict.get('image')
    kelas = QueryDict.get('kelas')
    formatt, imgstr = image64.split(';base64,')
    ext = formatt.split('/')[-1]
    filename = str(uuid.uuid4())
    fileImg = ContentFile(base64.b64decode(imgstr), name=filename + "." + ext)
    image = cv2.imdecode(np.fromstring(fileImg.read(), np.uint8), 1)

    morfologi = Morfologi(image)
    image_gray = morfologi.gray
    image_binary = morfologi.cleaned.astype(int)*255

    image_clean = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    image_gray = base64.b64encode(cv2.imencode('.jpg', image_gray)[1]).decode()
    image_binary = base64.b64encode(cv2.imencode('.jpg', image_binary)[1]).decode()

    glcm = GLCM(image)

    ROUNDING = 5
    prd      =  round(morfologi.prd(), ROUNDING)
    plw      =  round(morfologi.plw(), ROUNDING)
    rect     =  round(morfologi.rect(), ROUNDING)
    nf       =  round(morfologi.narrow_factor(), ROUNDING)
    ar       =  round(morfologi.aspect_ratio(), ROUNDING)
    ff       =  round(morfologi.form_factor(), ROUNDING)

    idm      = round(glcm.idm(), ROUNDING)
    entropy  = round(glcm.entropy(), ROUNDING)
    asm      = round(glcm.asm(), ROUNDING)
    contrast = round(glcm.contrast(), ROUNDING)
    corr     = round(glcm.korelasi(), ROUNDING)

    dataset = Dataset()
    dataset.filename = fileImg
    dataset.form_factor = ff
    dataset.aspect_ratio = ar
    dataset.rect = rect
    dataset.narrow_factor = nf
    dataset.prd = prd
    dataset.plw = plw

    dataset.idm = idm
    dataset.entropy = entropy
    dataset.asm = asm
    dataset.contrast = contrast
    dataset.correlation = corr
    dataset.kelas = kelas
    dataset.save()

    success = 1
    context = {
        'success': success,
        'image_clean': image_clean,
        'image_gray': image_gray,
        'image_binary': image_binary
    }
    return JsonResponse(context, safe=False)

def hapus_data(request):
    data_id = request.POST.get('data_id')
    print(data_id)
    data = Dataset.pdobjects.get(id=data_id)
    data.filename.delete()
    data.delete()

    success = 1
    context = {
        'success': success
    }
    return JsonResponse(context, safe=False)


def detail_gambar(request):
    id = int(request.POST.get('id'));
    dataset = Dataset.pdobjects.get(id=id)
    filepath = dataset.filename.path
    image = cv2.imread(filepath)
    R = image[:, :, 2]
    G = image[:, :, 1]
    B = image[:, :, 0]

    morfologi = Morfologi(image)

    image_gray = morfologi.gray
    image_binary = morfologi.cleaned.astype(int)*255

    image_clean = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    image_gray = base64.b64encode(cv2.imencode('.jpg', image_gray)[1]).decode()
    image_binary = base64.b64encode(cv2.imencode('.jpg', image_binary)[1]).decode()

    success = 1
    context = {
        'success': success,
        'image_clean': image_clean,
        'image_gray': image_gray,
        'image_binary': image_binary
    }

    return JsonResponse(context, safe=False)

def download_csv(request):
    print(request.GET.urlencode())
    tipe = request.GET.get("type")
    data_id = int(request.GET.get("id"))

    dataset = Dataset.pdobjects.get(id=data_id)
    filepath = dataset.filename.path
    image = cv2.imread(filepath)

    R = image[:, :, 2]
    G = image[:, :, 1]
    B = image[:, :, 0]

    morfologi = Morfologi(image)

    image_gray = morfologi.gray
    image_binary = morfologi.cleaned.astype(int)*255



    image_to_download = ""

    if (tipe == "R"):
        image_to_download = R
    elif (tipe == "G"):
        image_to_download = G
    elif (tipe == "B"):
        image_to_download = B
    elif (tipe == "gray"):
        image_to_download = image_gray
    elif (tipe == "binary"):
        image_to_download = image_binary
    else:
        raise Http404


    namafile = "{}_{}.csv".format(tipe, str(data_id))
    handle, fn = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(handle,"w", encoding='utf8',errors='surrogateescape',\
                  newline='') as f:
        writer=csv.writer(f)
        for row in image_to_download:
            try:
                writer.writerow(row)
            except Exception as e:
                print ('Error in writing row:',e)
        f.close()

    response = None

    with open(fn, 'rb') as fh:
        response = HttpResponse(
            fh.read(), content_type="text/csv")
        response['Content-Disposition'] = 'inline; filename=' + namafile
    os.remove(fn)
    return response

    raise Http404


def proses_input(request):
    if not request.user.is_authenticated:
        return redirect("index")
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
    if not request.user.is_authenticated:
        return redirect("index")
    return HttpResponse('welcome')
    pass


def data_anfis(request):
    if not request.user.is_authenticated:
        return redirect("index")
    models = Model.objects.all()
    
    context = {
        'models': models
    }
    return render(request, 'gaharu/data-anfis.html', context)


def tambah_model(request):
    if not request.user.is_authenticated:
        return redirect("index")
    return render(request, 'gaharu/tambah-model.html')


def proses_pelatihan(request):
    if not request.user.is_authenticated:
        return redirect("index")
    from gaharu.libraries.anfis_matlab import AnfisMatlab
    import matlab
    import matlab.engine
    simpan = int(request.POST.get('simpan')
                 ) if request.POST.get('simpan') else -1
    epoch = int(request.POST.get('epoch')) if request.POST.get('epoch') else 1
    persen_uji = float(request.POST.get('persen_uji')) if request.POST.get(
        'persen_uji') else float(20)

    dataset = Dataset.pdobjects.all().to_dataframe()
    columns = ['id', 'form_factor', 'aspect_ratio', 'rect',
               'narrow_factor', 'prd', 'plw', 'idm', 'entropy', 'asm', 'contrast',
               'correlation', 'kelas']
    df = dataset.loc[:, columns].copy()
    persen_uji = persen_uji / 100
    train_df, test_df = train_test_split(
        df, test_size=persen_uji, stratify=df.loc[:, ['kelas']], random_state=0)
    train_df = train_df.sort_index()
    test_df = test_df.sort_index()

    train_data = train_df.copy()
    test_data = test_df.copy()

    X_train = train_data.loc[:, ~train_data.columns.isin(['id', 'kelas'])]
    Y_train = train_data.loc[:, train_data.columns.isin(['kelas'])]
    X_test = test_data.loc[:, ~test_data.columns.isin(['id', 'kelas'])]
    Y_test = test_data.loc[:, test_data.columns.isin(['kelas'])]

    scaler = MinMaxScaler()
    scaler.fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled_with_class = np.concatenate(
        (X_train_scaled, Y_train.to_numpy()), axis=1)

    Y_test_reshape = Y_test.to_numpy().reshape(-1)
    engine = matlab.engine.find_matlab()[0]
    engine = matlab.engine.connect_matlab(engine)
    matlablibdir = join(settings.BASE_DIR, 'matlab')
    engine.cd(matlablibdir)
    am = AnfisMatlab(engine)
    filename = str(uuid.uuid4()) + ".fis"
    radii = 0.5
    savefis = join(settings.MEDIA_ROOT, 'fis', filename)
    dirfis = am.make_fis(X_train_scaled, Y_train.to_numpy(), radii, savefis)

    am.mulai_pelatihan(X_train_scaled_with_class, dirfis, epoch, dirfis)
    predicted = am.mulai_pengujian(X_test_scaled, dirfis)
    print(predicted)
    flat_predicted = np.concatenate(predicted)
    num_correct = int(np.sum(flat_predicted == Y_test_reshape))
    print(num_correct)

    test_data = test_data.astype({"kelas": int})
    test_data['kelas_predicted'] = flat_predicted.reshape(-1, 1)

   
    accuracy = float((num_correct / Y_test.count()) * 100)

    train_data_ids = train_data['id'].tolist()
    test_data_ids = test_data['id'].tolist()

    pickle_data = {
        'model': dirfis,
        'train_data': train_data,
        'test_data': test_data,
        'train_data_ids': train_data_ids,
        'test_data_ids': test_data_ids,
        'epoch': epoch,
        'accuracy': accuracy,
        'num_correct': num_correct,
        'scaler': scaler
    }

    dirwithfilename = join('models', filename)
    path = join(settings.MEDIA_ROOT, dirwithfilename)


    with open(path, 'wb') as handle:
        pickle.dump(pickle_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


    datalatih_ids = json.dumps(train_data_ids)
    datauji_ids = json.dumps(test_data_ids)
    accuracy = accuracy
    total_data_test = len(test_data)

    model_to_database = {
        'filename': dirwithfilename,
        'datalatih_ids': datalatih_ids,
        'datauji_ids': datauji_ids,
        'accuracy': accuracy,
        'epoch': epoch
    }

    if (simpan == 1):
        save_model = Model(**model_to_database)
        save_model.save()
    else:
        os.remove(dirfis)

    start_number = 1
    train_data.insert(0, 'nomor', range(start_number, start_number + len(train_data)))
    test_data.insert(0, 'nomor', range(start_number, start_number + len(test_data)))


    table_train = json.loads(train_data.to_json(orient="records"))
    table_test = json.loads(test_data.to_json(orient="records"))
    context = {
        "table_train": table_train,
        "table_test": table_test,
        "jumlah_benar": num_correct,
        "total_data_test": total_data_test,
        "akurasi": accuracy,
        "epoch": epoch,
    }


    context = {
        "table_train": table_train,
        "table_test": table_test,
        "jumlah_benar": num_correct,
        "total_data_test": total_data_test,
        "akurasi": accuracy,
        "epoch": epoch,
    }
    return JsonResponse(context, safe=False)


def hapus_anfis(request):
    if not request.user.is_authenticated:
        return redirect("index")
    model_id = int(request.POST.get('model_id'))
    model = Model.objects.get(id=model_id)
    model.filename.delete()
    model.delete()

    # os.remove(path)
    # model.delete()
    context = {
       'success': '1'
    }
    return JsonResponse(context, safe=False)

def lihat_anfis(request, model_id):
    model_id = int(model_id)
    model = Model.objects.get(id=model_id)
    model_path = model.filename.path

    with open(model_path, 'rb') as handle:
        model_file = pickle.load(handle)

    train_data = model_file['train_data']
    test_data = model_file['test_data']
    epoch = model_file['epoch']
    accuracy = model_file['accuracy']
    num_correct = model_file['num_correct']

    table_train = json.loads(train_data.to_json(orient="records"))
    table_test = json.loads(test_data.to_json(orient="records"))
    total_data_test = len(test_data)
    context = {
        "model_id": model_id,
        "table_train": table_train,
        "table_test": table_test,
        "jumlah_benar": num_correct,
        "akurasi": accuracy,
        'epoch': epoch,
        'total_data_test': total_data_test
    }
    return render(request, 'gaharu/lihat-anfis.html', context)



def pengujian(request):
    if not request.user.is_authenticated:
        return redirect("index")
    models = Model.objects.all()
    context = {
        'models': models
    }
    return render(request, 'gaharu/pengujian.html', context)

def proses_pengujian(request):
    response = {
    'cdsfs':'sfsd'
    }
    return JsonResponse(response, safe=False)