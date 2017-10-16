# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import sendgrid
import json
from django.contrib.auth import authenticate, login, logout
from sendgrid import Email
from sendgrid.helpers.mail import Content, Mail
from .models import Usuario

rolUser = ""

@csrf_exempt
def Home(request):
	return render(request, "index.html")

def sendMailNotification(email, subject, msj):
	aux4="S"
	aux7="G.CR"
	aux3="nMhIu_QzSL0LTN9nLVUw.pFEJY"
	aux1="LyU-PAg2SlXRGI-PHIGWy7XwhWTZfZK8_sFv60"
	sg = sendgrid.SendGridAPIClient(apikey=aux4+aux7+aux3+aux1)
	from_email = Email("no-reply-mercado@grupo4.com")
	to_email = Email(email)
	content = Content("text/plain", msj)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            usuario = Usuario.objects.get(auth_user_id=request.user)
            global rolUser
            rolUser = usuario.rol.nombre
            info_usuario = [{'mensaje': "OK",
                             'rol': usuario.rol.nombre,
                             'username': username}]
        else:
            info_usuario = [{'mensaje': "Nombre de usuario o clave inválido",
                             'rol': "",
                             'username': ""}]
    data_convert = json.dumps(info_usuario)
    return HttpResponse(data_convert)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'mensaje': 'ok'})

@csrf_exempt
def logged_view(request):
    if request.user.is_authenticated():
        if rolUser == "":
            mensaje = "no"
        else:
            mensaje = rolUser
    else:
        mensaje= "no"
    return JsonResponse({"mensaje": mensaje})

