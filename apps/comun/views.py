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
from .models import Usuario, Direccion

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
            info_usuario = [{'mensaje': "OK",
                             'rol': usuario.id_rol.nombre,
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
        mensaje ="ok"
    else:
        mensaje= "no"
    return JsonResponse({"mensaje": mensaje})

@csrf_exempt
def get_rol_view(request):
    usuario = Usuario.objects.get(auth_user_id=request.user)
    return JsonResponse({'mensaje': usuario.id_rol.nombre})

@csrf_exempt
def get_usuario(request):
    if request.method == "GET":
        usuario = Usuario.objects.get(auth_user_id=request.user)
        direccion = Direccion.objects.get(id_usuario_comprador=usuario)
        datos_usuario = [{'id': usuario.id,
                            'nombres': usuario.auth_user_id.first_name,
                            'apellidos': usuario.auth_user_id.last_name,
                            'telefono': usuario.telefono,
                            'direccion': direccion.direccion,
                            'correo': usuario.auth_user_id.email
                            }]

    data_convert = json.dumps(datos_usuario)
    return HttpResponse(data_convert)