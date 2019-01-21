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
        
        from_date = request.POST['year_ini']+'-'+request.POST['month_ini']+'-01'
        to_date = request.POST['year_end']+'-'+request.POST['month_end']+'-01'

        row_data = []
        for u in request.POST.getlist('co_select'):
            result = CaoFatura.tmp_sql_totals(from_date, to_date, u)
            rows = []
            t_renta = 0
            t_costo_fijo = 0
            t_comision = 0
            t_lucro = 0
            for r in result:
                usuario = r.no_usuario
                lucro = r.ganancia_neta - (r.costo_fijo + r.comision)
                t_renta += r.ganancia_neta
                t_costo_fijo += r.costo_fijo
                t_comision += r.comision
                t_lucro += lucro  
                rows.append({
                    'periodo': r.periodo,
                    'data_emissao': r.data_emissao.strftime('%B, %Y'),
                    'no_usuario': r.no_usuario,
                    'co_usuario': r.co_usuario,
                    'ganancia_neta': r.ganancia_neta,
                    'comision': r.comision,
                    'lucro': lucro, 
                    })
            if len(rows) > 0:

                row_data.append({
                    'usuario': usuario, 
                    'rows': rows,
                    't_renta': t_renta,
                    't_costo_fijo': t_costo_fijo,
                    't_comision': t_comision,
                    't_lucro': t_lucro,
                    })
             
                
        data = {
            'fecha': from_date,
            'fecha_end': to_date, 
            'consultor': row_data,
        }

        
    else:
        data = {'status': 'error en el metodo',}

    return render(request, 'consultor/_table_relatorio.html', data)

