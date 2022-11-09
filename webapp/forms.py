from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password1', 'password2']



class PreguntasForm(forms.ModelForm):
    pregunta = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Pregunta', 'id': 'id_pregunta'}))
    respuesta = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Respuesta', 'id': 'id_respuesta'}))
    class Meta:
        model = Pregunta
        fields = ['pregunta', 'respuesta']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class GradoForm(forms.ModelForm):

    class Meta:
        model = Grado
        fields = ['nombre', 'alias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del grado', 'id': 'nombre_grado_form_grado'}),
            'alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alias del grado', 'id': 'alias_grado_form_grado'}),

        }
        labels = {
            'nombre': 'Nombre del grado',
            'alias': 'Alias del grado',
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre del grado es obligatorio',
                'max_length': 'El nombre del grado no puede tener mas de 50 caracteres',
                'min_length': 'El nombre del grado no puede tener menos de 3 caracteres',
            },
            'alias': {
                'max_length': 'El alias del grado no puede tener mas de 50 caracteres',
                'min_length': 'El alias del grado no puede tener menos de 3 caracteres',
            },
        }
        # """

       

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'alias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'id': 'nombre_profesor_form_profesor'}),
            'alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alias', 'id': 'alias_profesor_form_profesor'}),
        }
        labels = {
            'nombre': 'Nombre',
            'alias': 'Alias',
        }
        error_messages = {
            'nombre': {
                'max_length': "Nombre muy largo",
                'required': "Nombre requerido",
            },
            'alias': {
                'max_length': "Alias muy largo",
            },
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia 
        # para grado que solo sean los que tiene status_model = True
        fields = ['nombre', 'grado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'id': 'nombre_materia_form_materia'}),
            'grado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grado', 'id': 'grado_materia_form_materia'}),
        }
        labels = {
            'nombre': 'Nombre',
            'grado': 'Grado',
        }
        error_messages = {
            'nombre': {
                'max_length': "Nombre muy largo",
                'required': "Nombre requerido",
            },
            'grado': {
                'required': "Grado requerido",
            },
        }
    # hacer que grado sean solo status_model = True
    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        self.fields['grado'].queryset = Grado.objects.filter(status_model=True).order_by('nombre')



class NewHorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['nombre','ciclo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'id': 'nombre_horario_form_horario'}),
            'ciclo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciclo', 'id': 'ciclo_horario_form_horario'}),
        }
        labels = {
            'nombre': 'Nombre',
            'ciclo': 'Ciclo',
        }
        error_messages = {
            'nombre': {
                'max_length': "Nombre muy largo",
                'required': "Nombre requerido",
            },
            'ciclo': {
                'max_length': "Nombre largo",
            },
        }




class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['id', 'nombre', 'ciclo' ,'estado_del_horario', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo', 'cantidad_periodo', 'hora_inicio', 'duracion_periodo_hour', 'duracion_periodo_minute']
        widgets = {
            'id': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'id', 'id': 'id_horario_form_horario'}),
            'nombre': forms.TextInput(attrs={'class': 'm-1', 'placeholder': 'Nombre', 'id': 'nombre_horario_form_horario'}),
            'ciclo': forms.TextInput(attrs={'class': 'm-1', 'placeholder': 'Ciclo', 'id': 'ciclo_horario_form_horario'}),
            'estado_del_horario': forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden', 'id': 'estado_horario_form_horario'}),
            'Lunes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Lunes')",'id': 'Lunes_horario_form_horario'}),
            'Martes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Martes')", 'id': 'Martes_horario_form_horario'}),
            'Miercoles': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Miercoles')", 'id': 'Miercoles_horario_form_horario'}),
            'Jueves': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Jueves')", 'id': 'Jueves_horario_form_horario'}),
            'Viernes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Viernes')", 'id': 'Viernes_horario_form_horario'}),
            'Sabado': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Sabado')", 'id': 'Sabado_horario_form_horario'}),
            'Domingo': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Domingo')", 'id': 'Domingo_horario_form_horario'}),
            'cantidad_periodo': forms.NumberInput(attrs={'class': '', 'placeholder': 'Cantidad de periodos', 'style': 'width: 50px', 'id': 'cantidad_periodo_horario_form_horario'}),
            'hora_inicio': forms.TimeInput(attrs={'class': '', 'style': 'width: 100px', 'placeholder': 'Hora de inicio', 'id': 'hora_inicio_horario_form_horario'}, format='%H:%M'),
            'duracion_periodo_hour': forms.NumberInput(attrs={'class': 'ml-1', 'style': 'width: 50px', 'placeholder': 'Duracion de periodo', 'id': 'duracion_periodo_horas_form_horario'}),
            'duracion_periodo_minute': forms.NumberInput(attrs={'class': 'ml-1', 'style': 'width: 50px', 'placeholder': 'Duracion de periodo', 'id': 'duracion_periodo_minutos_form_horario'}),
        }

        labels = {
            'nombre': 'Nombre',
            'ciclo': 'Ciclo',
            'cantidad_periodo': 'Cantidad de periodos por dia ',
            'hora_inicio': 'Hora de inicio',
            'duracion_periodo_hour': 'Duracion de periodo (horas)',
            'duracion_periodo_minute': 'Duracion de periodo (minutos)',
        }
        error_messages = {
            'nombre': {
                'max_length': 'Nombre demasiado largo',
                'required': 'Nombre requerido',
            },
            'ciclo':{
                'max_length': 'Ciclo demasiado largo',
            }
        }
class EstadoProfesorHorarioForm(forms.ModelForm):
    class Meta:
        model = EstadoProfesorHorario
        fields = ['cantidad_max_periodo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo','anotaciones']
        widgets = {
            'cantidad_max_periodo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad maxima de periodos', 'id': 'cantidad_max_periodo_horario_form_horario'}),
            'Lunes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Lunes')",'id': 'Lunes_horario_form_horario'}),
            'Martes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Martes')", 'id': 'Martes_horario_form_horario'}),
            'Miercoles': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Miercoles')", 'id': 'Miercoles_horario_form_horario'}),
            'Jueves': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Jueves')", 'id': 'Jueves_horario_form_horario'}),
            'Viernes': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Viernes')", 'id': 'Viernes_horario_form_horario'}),
            'Sabado': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Sabado')", 'id': 'Sabado_horario_form_horario'}),
            'Domingo': forms.CheckboxInput(attrs={'class': '','onclick':"check_dias('Domingo')", 'id': 'Domingo_horario_form_horario'}),
            'anotaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Anotaciones', 'id': 'anotaciones_horario_form_horario'}),
        }
        labels = {
            'cantidad_max_periodo': 'Cantidad maxima de periodos',
            'anotaciones': 'Anotaciones',
        }
        error_messages = {
            'cantidad_max_periodo': {
                'max_length': 'Cantidad maxima de periodos demasiado larga',
                'required': 'Cantidad maxima de periodos requerida',
            },
        }

        def __init__(self, *args, **kwargs):
            horario = kwargs.pop('horario') # get the horario from the view
            horario = Horario.objects.get(id=horario)
            super(EstadoProfesorHorarioForm, self).__init__(*args, **kwargs)
            # hide the fields that are not in the horario
            if not horario.Lunes:
                self.fields['Lunes'].widget = forms.HiddenInput()
            if not horario.Martes:
                self.fields['Martes'].widget = forms.HiddenInput()
            if not horario.Miercoles:
                self.fields['Miercoles'].widget = forms.HiddenInput()
            if not horario.Jueves:
                self.fields['Jueves'].widget = forms.HiddenInput()
            if not horario.Viernes:
                self.fields['Viernes'].widget = forms.HiddenInput()
            if not horario.Sabado:
                self.fields['Sabado'].widget = forms.HiddenInput()
            if not horario.Domingo:
                self.fields['Domingo'].widget = forms.HiddenInput() 

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['profesor', 'materia',  'horario']
        widgets = {
            'profesor': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'profesor': 'Profesor',
            'materia': 'Materia',
            'horario': 'Horario',
        }
        help_texts = {
            'profesor': 'Seleccione el profesor de la asignatura',
            'materia': 'Seleccione la materia de la asignatura',
            'horario': 'Seleccione el horario de la asignatura',
        }
        error_messages = {
            'profesor': {
                'required': 'Profesor requerido',
            },
            'materia': {
                'required': 'Materia requerida',
            },
            'horario': {
                'required': 'Horario requerido',
            },
        }
        
    def __init__(self, *args, **kwargs):
        # escoger los profesores de los estadosprofesorhorairo que esten activos 
        list_profesores = EstadoProfesorHorario.objects.filter(activo=True, horario=kwargs['initial']['horario']) 
        list_profesores = [profesor.profesor for profesor in list_profesores]
        super(AsignaturaForm, self).__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(id__in=list_profesores)
        

class PeriodoHorarioForm(forms.ModelForm):
    class Meta:
        model = PeriodoHorario
        fields = ['hora_inicio', 'hora_fin', 'version_horario', 'asignatura']
        widgets = {
            'version_horario': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(),
            'hora_fin': forms.TimeInput(),
            'asignatura': forms.Select(attrs={'class': 'form-control'}),
        }
        