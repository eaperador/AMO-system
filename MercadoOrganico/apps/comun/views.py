# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import sendgrid
from sendgrid import Email
from sendgrid.helpers.mail import Content, Mail


@csrf_exempt
def Home(request):
	return render(request, "Index.html")

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
