from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def index(request):
	print(request.user)
	return render(request, 'index.html')

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
	return redirect('login')