from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
import uuid
from django.core.files.base import ContentFile
import cv2
from gaharu.libraries.glcm import GLCM
import pickle
from gaharu.libraries.feature import Morfologi
import numpy as np
import json
import base64
import os
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from gaharu.models import Dataset, Model

def index(request):
	models = Model.objects.all()
	context = {
	'models': models
	}
	return render(request, 'index.html', context)

def index_lama(request):
	print(request.user)
	return render(request, 'index_lama.html')

def pengujian(request):
	return render(request, 'pengujian.html')

def process_pengujian(request):
    response = {
    'asdfs':'sdfs'
    }
    return JsonResponse(response, safe=False)

def login(request):
	return render(request, 'login.html')


def process_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	success = 0
	if user is not None:
		auth_login(request, user)
		success = 1
	context = {
		'success': success
	}
	return JsonResponse(context, safe=False)

def logout(request):
	auth_logout(request)
	return redirect('index')