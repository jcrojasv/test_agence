from django import forms
from apps.consultor.models import CaoUsuario, CaoFatura


class ConsultorForm(forms.Form):
    
    class_form = 'form-control'

    users = CaoUsuario.get_for_select()

    years = CaoFatura.get_years()

    list_month = [(x, x) for x in range(1, 12)]

    year_ini = forms.ChoiceField(
                choices=years,
                widget=forms.Select(
                    attrs={
                      'class':class_form+' width_select',
                    }
                ))
    year_end = forms.ChoiceField(
                choices=years,
                widget=forms.Select(
                    attrs={
                      'class':class_form+' width_select',
                    }
                ))

    month_ini = forms.ChoiceField(
                choices=list_month,
                widget=forms.Select(
                    attrs={
                      'class':class_form+' width_select',
                    }
                  )
              )

    month_end = forms.ChoiceField(
                choices=list_month,
                widget=forms.Select(
                    attrs={
                      'class':class_form+' width_select',
                    }
                  )
              )
    consultants = forms.MultipleChoiceField(label="Consultores", 
                 choices=users, 
                 widget=forms.SelectMultiple(
                    attrs={
                      'class': class_form,
                      'size': 10,
                    }
                ))

    co_select = forms.MultipleChoiceField( 
                 widget=forms.SelectMultiple(
                    attrs={
                      'class': class_form,
                      'size': 10,
                    }
                ))
    