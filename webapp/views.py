from multiprocessing import context
from re import U
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
# importar JsonResponse
from django.http import JsonResponse

# user
from django.contrib.auth.models import User
from django import forms
from .functionHorario import AllHorarioView, Asig, OrdHorario


# home con validacion de usuario con login_required
class HomeView(TemplateView):
    template_name = 'web/home.html'
    model = Horario

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # borrar todo horario que tenga status_model = False y no_page = 1
        Horario.objects.filter(status_model=False, no_page=1).delete()
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context = {
            'horarios': Horario.objects.all(),
            'form_nwhorario': NewHorarioForm(),
        }
        return context


class ProfesoresView(ListView):
    model = Profesor
    template_name = 'web/profesor.html'
    form_class = ProfesorForm

    # usando get_context_data y dispatch para enviar el formulario y validar el usuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'form_add_profesor': ProfesorForm(),
            'Profesores': Profesor.objects.all(),
            'form_nwhorario': NewHorarioForm(),
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profesores')
        return render(request, self.template_name, {'form': form, 'Profesores': Profesor.objects.all()})


class GradosView(ListView):
    model = Grado
    template_name = 'web/grado.html'
    form_class = GradoForm
    second_form_class = MateriaForm

    # usando get_context_data y dispatch para enviar el formulario y validar el usuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'Grados': Grado.objects.all(),
            'form_nwhorario': NewHorarioForm(),
            'Materias': Materia.objects.all(),
        }
        if 'form_grado' not in context:
            context['form_add_grado'] = GradoForm
        if 'form_materia' not in context:
            context['form_add_materia'] = MateriaForm
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('tipo') == 'grado':
            form = self.form_class(request.POST)
            form_grado, form_materia = form, self.second_form_class()
        if request.POST.get('tipo') == 'materia':
            form = self.second_form_class(request.POST)
            form_grado, form_materia = self.form_class(), form
        if form.is_valid():
            form.save()
            return redirect('grados')
        return render(request, self.template_name, {'form_grado': form_grado, 'form_materia': form_materia, 'Grados': Grado.objects.all(), 'Materias': Materia.objects.all()})


class UsuarioView(ListView):
    template_name = 'web/usuario.html'
    model = User
    form_class = UserForm
    second_form_class = PreguntasForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UsuarioView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            form_pregunta = PreguntasForm(
                instance=Pregunta.objects.get(usuario=self.request.user))
        except ObjectDoesNotExist:
            form_pregunta = PreguntasForm()
        context = {
            'form_usuario': self.form_class(instance=self.request.user),
            'form_pregunta': form_pregunta,
            'form_nwhorario': NewHorarioForm(),
            'id_user': self.request.user.id,
        }
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('tipo') == 'usuario':
            # validar que el password1 y password2 sean iguales
            if request.POST.get('password1') != request.POST.get('password2'):
                raise ValidationError('Las contraseñas no coinciden')
            user = User.objects.get(id=request.user.id)
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            # encriptar la contraseña y guardar la
            user.set_password(request.POST.get('password1'))
            user.save()
            return redirect('usuario')
        try:
            form_pregunta = PreguntasForm(
                instance=Pregunta.objects.get(usuario=self.request.user))
        except ObjectDoesNotExist:
            form_pregunta = PreguntasForm()
        form_usuario = self.form_class(instance=self.request.user)
        form_nwhorario = NewHorarioForm()
        return render(request, self.template_name, {'form': form_usuario, 'form_pregunta': form_pregunta, 'form_nwhorario': form_nwhorario, 'id_user': self.request.user.id})


class Select_page_HorarioView(ListView, AllHorarioView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            id_horario = kwargs.get('id_horario')
            no_page = Horario.objects.get(id=id_horario).no_page
            return self.select_posicion(0, int(no_page), id_horario)
        except Exception as e:
            return redirect('home')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            id_horario = kwargs.get('id_horario')
            no_page_actual = request.POST.get('no_page_actual')
            horario = Horario.objects.get(id=id_horario)
            print('no_page_actual', no_page_actual)
            if int(no_page_actual)==10:
                hor = OrdHorario(id_horario)
                hor.asignar()
                return JsonResponse({'status': 'ok'}, status=200)
            if int(horario.no_page) == int(no_page_actual):
                if int(no_page_actual) == 4:
                    horario.no_page = 10 
                    hor = OrdHorario(id_horario)
                    hor.asignar()
                    
                else:   
                    horario.no_page = int(no_page_actual) + 1
                horario.save()
                
                return JsonResponse({'status': 'ok'}, status=200)
            else:
                return JsonResponse({'status': 'ok'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'}, status=500)


class PlantillaView(ListView):
    model = Horario
    template_name = 'new_horario/plantilla_horario.html'
    form_class = HorarioForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.id_horario = kwargs['id_horario']
            self.horario = Horario.objects.get(id=self.id_horario)

            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = {
            'id_horario': self.id_horario,
            'form': HorarioForm(instance=self.horario),
            'estado_del_horario': self.horario.no_page,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(instance=self.horario, data=request.POST)
        if form.is_valid():
            form.save()
            if self.horario.no_page == 1:
                self.horario.no_page = 2
                self.horario.status_model = True
                self.horario.save()
            return redirect('select_profesor', self.id_horario)
        return render(request, self.template_name, {'form': form, 'id_horario': self.id_horario, 'estado_del_horario': self.horario.no_page})


class SelectProfesorView(ListView):
    model = Profesor
    template_name = 'new_horario/select_profesor.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.id_horario = kwargs['id_horario']
            self.estado_del_horario = Horario.objects.get(
                id=self.id_horario).no_page
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('home')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context = {
            'id_horario': self.id_horario,
            'form_add_profesor': ProfesorForm(),
            'estado_del_horario': self.estado_del_horario,
        }
        return context

    def post(self, request, *args, **kwargs):
        pass
        return redirect('plantilla', self.id_horario)


class SelectGradoView(ListView):
    model = Grado
    template_name = 'new_horario/select_grado_materia.html'

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.id_horario = kwargs['id_horario']
            self.estado_del_horario = Horario.objects.get(
                id=self.id_horario).no_page
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.estado_del_horario)
        context = {
            'id_horario': self.id_horario,
            'form_add_grado': GradoForm(),
            'estado_del_horario': self.estado_del_horario,
        }
        return context

    def post(self, request, *args, **kwargs):
        pass
        return redirect('plantilla', self.id_horario)


class Select_AsignaturasView(ListView, Asig):
    template_name = 'new_horario/select_asignatura.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.id_horario = kwargs['id_horario']
            return super(Select_AsignaturasView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('home')

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context = {
                'id_horario': self.id_horario,
                'estado_del_horario': self.estado_del_horario,
                **self.Asignatura(self.id_horario),
            }
            return context
        except Exception as e:
            print(e)
            return redirect('home')

    def get_queryset(self):
        try:
            self.id_horario = self.kwargs['id_horario']
            self.estado_del_horario = Horario.objects.get(
                id=self.id_horario).no_page
            return 
        except Exception as e:
            print(e)
            return redirect('home')

class ExportarView(ListView):
    template_name = 'web/exportar.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  # """


class HorarioDisplayView(ListView):
    model = Horario
    template_name = 'new_horario/horario_display.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HorarioDisplayView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'id_horario': self.id_horario,
            'horario': self.horario,
            'grados': self.grados,
            'id_grado': self.id_grado_init,
            'nombre_grado': self.nombre_grado_init,
        }
        return context

    def post(self, request, *args, **kwargs):
        pass
        return redirect('plantilla', self.id_horario)
    
    def get_queryset(self):
        try:
            self.id_horario = self.kwargs['id_horario']
            self.horario = Horario.objects.get(id=self.id_horario)
            asignaciones = Asignatura.objects.filter(horario=self.horario)
            grados = []
            for asi in asignaciones:
                grados.append(asi.materia.materia.grado)
            self.grados = list(set(grados))
            self.id_grado_init = self.grados[0].id
            self.nombre_grado_init = self.grados[0].nombre
            print(self.grados)
            return Horario.objects.get(id=self.id_horario)
        except Exception as e:
            print(e)
            return redirect('home')

"""
# PDF 
# import reportlab
import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
# importar TA_CENTER

from reportlab.lib.enums import TA_CENTER


class HorarioPDFView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        try:
            id_grado = kwargs.get('id_grado')
            id_horario = kwargs.get('id_horario')
            grado = Grado.objects.get(id=id_grado)
            horario = Horario.objects.get(id=id_horario)
            # ultima version
            version = VersionHorario.objects.filter(horario=horario).order_by('-id')[0]
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + grado.nombre + '-horario.pdf'
            buffer = BytesIO()
            
            c = canvas.Canvas(buffer, pagesize=A4)
            
            # Header
            c.setLineWidth(.3)
            c.setFont("Helvetica-Bold", 22)
            c.drawString(30, 750, "Horario")
            c.setFont("Helvetica-Bold", 16)
            c.drawString(30, 850, grado.nombre)
            c.setFont("Helvetica-Bold", 14)
            dias_listta =['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
            # Horario tabla de los dias [hora, lunes, martes, miercoles, jueves, viernes, sabado]
            # Style 
            style = getSampleStyleSheet()
            styleBH = style["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.border = 0
            styleBH.padding = 0
            styleBH.textAlign = TA_CENTER
            styleBH.fontSize = 12
            styleBH.fontFamily = "Helvetica-Bold"
            dias_activo = []
            hora = Paragraph('''Hora''', styleBH)
            dias =[hora]
            if horario.Lunes:
                lunes = Paragraph('''Lunes''', styleBH)
                dias.append(lunes)
                dias_activo.append('lunes')
            if horario.Martes:
                martes = Paragraph('''Martes''', styleBH)
                dias.append(martes)
                dias_activo.append('martes')
            if horario.Miercoles:
                miercoles = Paragraph('''Miercoles''', styleBH)
                dias.append(miercoles)
                dias_activo.append('miercoles')
            if horario.Jueves:
                jueves = Paragraph('''Jueves''', styleBH)
                dias.append(jueves)
                dias_activo.append('jueves')
            if horario.Viernes:
                viernes = Paragraph('''Viernes''', styleBH)
                dias.append(viernes)
                dias_activo.append('viernes')
            if horario.Sabado:
                sabado = Paragraph('''Sabado''', styleBH)
                dias.append(sabado)
                dias_activo.append('sabado')
            if horario.Domingo:
                domingo = Paragraph('''Domingo''', styleBH)
                dias.append(domingo)
                dias_activo.append('domingo')
            data = [dias]

            # styleN = style["BodyText"]
            slyleN = style["Normal"]
            slyleN.alignment = TA_CENTER
            slyleN.border = 0
            slyleN.padding = 0
            slyleN.textAlign = TA_CENTER
            slyleN.fontSize = 8
            slyleN.fontFamily = "Helvetica-Bold"

            width, height = A4
            high = 650
            # sacar las horas sin repetir
            horas_list = PeriodoHorario.objects.filter(version_horario=version).order_by('hora_inicio').values_list('hora_inicio', 'hora_fin').distinct()
            
            for hora_inicio, horas_fin in horas_list:
                fila = []
                fila.append(Paragraph(f'{hora_inicio} - {horas_fin}', slyleN))
                periodos = PeriodoHorario.objects.filter(version_horario=version, hora_inicio=hora_inicio, hora_fin=horas_fin)
                # ordenar por dia
                 
                for dia in dias_activo:
                    for periodo in periodos:
                        if periodo.dia == dia:
                            fila.append(Paragraph(f'{periodo.asignatura.materia.materia.nombre} - {periodo.asignatura.materia.profesor.nombre}', slyleN))
                            break
                data.append(fila)
                high -= 20
                tabla = Table(data, colWidths=[1.5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm, 5 * cm])
                self.pdf.add_table(tabla)
        except Exception as e:
            print(e)
            pass
        """
