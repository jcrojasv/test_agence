from django.shortcuts import render
from django.http import HttpResponse
from apps.consultor.models import CaoUsuario
from apps.consultor.forms import ConsultorForm
from django.db import connection
print (connection.queries)

def index(request):
	data = {
	  'lang': request.LANGUAGE_CODE,
	  'form' : ConsultorForm(),
	}
	return render(request, 'consultor/con_desempenho.html', data)
