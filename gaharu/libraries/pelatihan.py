from .models import Dataset, Model
import base64
from .libraries.glcm import GLCM
from .libraries.feature import Morfologi
import uuid
import numpy as np
import cv2
from .libraries.anfis_pytorch.myanfis import train_hybrid_modified, predict_data_test
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
from os.path import join
from django.conf import settings


class Pelatihan:
    def __init__(data, persentase, epoch, simpan, nama_model):
        self.__data = data
        self.__persentase = persentase
        self.__epoch = epoch
        self.__simpan = simpan
        self.__nama_model = nama_model
        self.mulai_pelatihan()

    def is_simpan():
        return True if self.__simpan == 1 else False

    def get_persentase():
        return float(self.__persentase) / 100

    def get_data():
        return self.__data

    def get_epoch():
        return int(self.__epoch)

    def get_nama_model():
        return self.__nama_model

    def proses_pelatihan(request):
    if not request.user.is_authenticated:
        return redirect("index")
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

    model = train_hybrid_modified(X_train_scaled_with_class, epoch)
    Y_test_reshape = Y_test.to_numpy().reshape(-1)
    cat_act, cat_pred = predict_data_test(model, X_test_scaled, Y_test_reshape)

    Y_test_predicted = cat_pred.cpu().detach().numpy()
    num_correct = sum_torch(cat_act == cat_pred).item()

    test_data = test_data.astype({"kelas": int})
    test_data['kelas_predicted'] = Y_test_predicted.reshape(-1, 1)

   
    accuracy = float((num_correct / Y_test.count()) * 100)

    train_data_ids = train_data['id'].tolist()
    test_data_ids = test_data['id'].tolist()

    pickle_data = {
        'model': model,
        'train_data': train_data,
        'test_data': test_data,
        'train_data_ids': train_data_ids,
        'test_data_ids': test_data_ids,
        'epoch': epoch,
        'accuracy': accuracy,
        'num_correct': num_correct,
        'scaler': scaler
    }

    filename = str(uuid.uuid4())
    dirwithfilename = join('models', filename)
    path = join(settings.MEDIA_ROOT, dirwithfilename)


    with open(path, 'wb') as handle:
        pickle.dump(pickle_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


    filename = filename
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
    return JsonResponse(context, safe=False)


