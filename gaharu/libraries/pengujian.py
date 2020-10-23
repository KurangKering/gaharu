def proses_pengujian(request):
    if not request.user.is_authenticated:
        return redirect("index")
    model_id = int(request.POST.get('model_id'))
    image64 = request.POST.get('image')
    formatt, imgstr = image64.split(';base64,')
    ext = formatt.split('/')[-1]
    filename = str(uuid.uuid4())
    fileImg = ContentFile(base64.b64decode(imgstr), name=filename + "." + ext)
    image = cv2.imdecode(np.fromstring(fileImg.read(), np.uint8), 1)

    morfologi = Morfologi(image)
    glcm = GLCM(image)

    image_gray = morfologi.gray
    image_binary = morfologi.cleaned.astype(int)*255

    image_clean = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    image_gray = base64.b64encode(cv2.imencode('.jpg', image_gray)[1]).decode()
    image_binary = base64.b64encode(cv2.imencode('.jpg', image_binary)[1]).decode()

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

    dataset = {}
    dataset['form_factor'] = ff
    dataset['aspect_ratio'] = ar
    dataset['rect'] = rect
    dataset['narrow_factor'] = nf
    dataset['prd'] = prd
    dataset['plw'] = plw
    dataset['idm'] = idm
    dataset['entropy'] = entropy
    dataset['asm'] = asm
    dataset['contrast'] = contrast
    dataset['correlation'] = corr

    test_data = np.fromiter(dataset.values(), dtype=float).reshape(1,-1)


    model = Model.objects.get(id=model_id)
    model_path = model.filename.path

    with open(model_path, 'rb') as handle:
        model_file = pickle.load(handle)

    scaler = model_file['scaler']
    model_anfis = model_file['model'];
    test_data_scaled = scaler.transform(test_data)
    predicted =  predict_pengujian(model_anfis, test_data_scaled)
    variables = {
        "prd": prd,
        "plw": plw,
        "rect": rect,
        "nf": nf,
        "ar": ar,
        "ff": ff,
        "idm": idm,
        "entropy": entropy,
        "asm": asm,
        "contrast": contrast,
        "corr": corr,
    }
    kelas_kelas = ['CRASSNA', 'MICROCARPA', 'SINENSIS', 'SUBINTEGRA'];
    kelas_hasil = kelas_kelas[predicted.item()]
    
    response = {
        'success': 1,
        'predicted': predicted.item(),
        'fitur': json.dumps(dataset),
        'fitur_scaled': list(test_data_scaled.reshape(-1)),
        'variables': variables,
        'image_clean': image_clean,
        'image_gray': image_gray,
        'image_binary': image_binary,
        'kelas_hasil': kelas_hasil

    }
    return JsonResponse(response, safe=False)