from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from apps.consultor.models import CaoUsuario, CaoFatura
from apps.consultor.forms import ConsultorForm
from django.db import connection
from django.core.serializers import serialize

print (connection.queries)

def index(request):
    users = ''
    for u in ['anapaula.chiodaro', 'show']:
        users += "'"+u+"',"

    users = users[:-1] 
    #consulta de relatorio
    result = CaoFatura.tmp_sql_totals('2007-02-01', '2007-04-01', users)


    ##print(result)

    
    data = {
      'lang': request.LANGUAGE_CODE,
      'form' : ConsultorForm(),
    }
    return render(request, 'consultor/con_desempenho.html', data)


def ajax_relatorio(request):

    if request.method == 'POST':
        form = ConsultorForm(request.POST)
        
        from_date = split_date(request.POST['date_ini'])
        to_date = split_date(request.POST['date_end'])

        row_data = []
        for u in request.POST.getlist('co_select'):
            result = CaoFatura.tmp_sql_totals(from_date, to_date, u)
            rows = []
            for r in result:
                usuario = r.no_usuario
                lucro = r.ganacia_neta - (r.costo_fijo + r.comision)
                  
                rows.append({
                    'periodo': r.periodo,
                    'no_usuario': r.no_usuario,
                    'co_usuario': r.co_usuario,
                    'ganacia_neta': r.ganacia_neta,
                    'comision': r.comision,
                    'lucro': lucro, 
                    })
            if len(rows) > 0:  
                row_data.append({'usuario': usuario, 'rows': rows})
             
                
        data = {
            'fecha': from_date,
            'fecha_end': to_date, 
            'consultor': row_data,
        }

        
    else:
        data = {'status': 'error en el metodo',}

    return render(request, 'consultor/_table_relatorio.html', data)

def split_date(_date):
    _date = _date.split('/')
    return _date[1]+'-'+_date[0]+'-01'
