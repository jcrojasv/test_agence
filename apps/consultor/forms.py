from django import forms
from apps.consultor.models import CaoUsuario


class ConsultorForm(forms.Form):
    
    class_form = 'form-control'

    users = CaoUsuario.get_for_select()

    date_ini = forms.CharField(
                max_length=7,
                widget=forms.TextInput(
                    attrs={
                      'class':class_form + ' from',
                      'placeholder': 'Fecha inicio',
                      'autocomplete': 'off',
                    }
                ))
    date_end = forms.CharField(
               max_length=7,
               widget=forms.TextInput(
                    attrs={
                      'class':class_form + ' to',
                      'placeholder': 'Fecha fin',
                      'autocomplete': 'off',
                    }
                ))
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
    