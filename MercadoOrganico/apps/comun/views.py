# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def Home(request):
	return render(request, "Index.html")
