import sys
from django.http import JsonResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from .models import *
from .forms import *

from .functionHorario import *


class UsuarioAjax(ListView):
    form = PreguntasForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type')
            usuario = request.user.id
            pregunta = request.POST.get('pregunta')
            respuesta = request.POST.get('respuesta')
            if type == 'frase':
                if pregunta != '' and respuesta != '':
                    try:
                        modelo = Pregunta.objects.get(usuario=usuario)
                        modelo.pregunta = pregunta
                        modelo.respuesta = respuesta
                        modelo.usuario = User.objects.get(id=usuario)
                        modelo.save()
                        return JsonResponse({'status': 'ok'})
                    except Exception as e:
                        return JsonResponse({'status': 'error'})
            return JsonResponse({'status': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ProfesoresAjax(ListView):
    model = Profesor
    form_class = ProfesorForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        profesores = list(Profesor.objects.all().values())
        return JsonResponse(profesores, safe=False)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            print('-'*64)
            id = request.POST.get('id', None)
            type_request = request.POST.get('type', None)
            if request.is_ajax():
                if type_request == 'data_profesor':
                    profesor = Profesor.objects.get(id=id)
                    data = {
                        'id': profesor.id,
                        'nombre': profesor.nombre,
                        'alias': profesor.alias,
                        'activo': profesor.activo,
                    }
                    return JsonResponse(data, status=200)

                if type_request == 'add_profesor':
                    form = self.form_class(request.POST)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({'message': 'Profesor agregado con exito'}, status=200)
                    html_form = str(form)
                    return JsonResponse({'form': html_form}, status=400)

                if type_request == 'update_profesor':
                    profesor = ProfesorForm(
                        request.POST, instance=Profesor.objects.get(id=id))
                    if profesor.is_valid():
                        profesor.save()
                        return JsonResponse({'message': 'Profesor actualizado con exito'}, status=200)
                    html_form = str(profesor)
                    return JsonResponse({'form': html_form, 'nombre': profesor.nombre}, status=400)

                if type_request == 'form_update_data_profesor':
                    profesor = Profesor.objects.get(id=id)
                    form = ProfesorForm(instance=profesor)
                    html_form = str(form)
                    return JsonResponse({'form': html_form, 'nombre': profesor.nombre}, status=200)

                if type_request == 'change_status':
                    profesor = Profesor.objects.get(id=id)
                    if profesor.activo:
                        profesor.activo = False
                    else:
                        profesor.activo = True
                    profesor.save()
                    return JsonResponse({'message': 'Profesor eliminado con exito'}, status=200)

                if type_request == 'delete':
                    profesor = Profesor.objects.get(id=id)
                    nombre = profesor.nombre
                    profesor.nombre = str(nombre) + ' (Eliminado)'
                    profesor.status_model = False
                    profesor.save()
                    return JsonResponse({'message': 'Profesor eliminado con exito'}, status=200)
            # filtrar por  'status_model' = True
            profesores = list(Profesor.objects.filter(
                status_model=True).values())
            return JsonResponse(profesores, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)


class GradosAjax(ListView):
    model = Grado
    form_class = GradoForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        grados = list(Grado.objects.all().values())
        return JsonResponse(grados, safe=False)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            id = request.POST.get('id', None)
            type_request = request.POST.get('type', None)
            if request.is_ajax():
                if type_request == 'data_grado':
                    grado = Grado.objects.get(id=id)
                    data = {
                        'nombre': grado.nombre,
                        'alias': grado.alias,
                        'activo': grado.activo,
                    }
                    return JsonResponse(data, status=200)

                if type_request == 'add_grado':
                    form = self.form_class(request.POST)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({'message': 'Grado agregado con exito'}, status=200)
                    html_form = str(form)
                    return JsonResponse({'form': html_form}, status=400)

                if type_request == 'update_grado':
                    grado = GradoForm(
                        request.POST, instance=Grado.objects.get(id=id))
                    if grado.is_valid():
                        grado.save()
                        return JsonResponse({'message': 'Grado actualizado con exito'}, status=200)
                    html_form = str(grado)
                    return JsonResponse({'form': html_form, 'nombre': grado.nombre}, status=400)

                if type_request == 'form_update_data_grado':
                    grado = Grado.objects.get(id=id)
                    form = GradoForm(instance=grado)
                    html_form = str(form)
                    return JsonResponse({'form': html_form, 'nombre': grado.nombre}, status=200)

                if type_request == 'change_status':
                    grado = Grado.objects.get(id=id)
                    if grado.activo:
                        grado.activo = False
                    else:
                        grado.activo = True
                    grado.save()
                    return JsonResponse({'message': 'Grado eliminado con exito'}, status=200)

                if type_request == 'delete':
                    materias = Materia.objects.filter(grado=id)
                    for materia in materias:
                        materia.status_model = False
                        materia.save()
                    grado = Grado.objects.get(id=id)
                    # cambiar el estado del modelo
                    grado.status_model = False
                    grado.save()
                    return JsonResponse({'message': 'Grado eliminado con exito'}, status=200)
            grados = list(Grado.objects.filter(status_model=True).values())
            return JsonResponse(grados, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)


class MateriasAjax(ListView):
    model = Materia

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        materias = list(Materia.objects.all().values())
        return JsonResponse(materias, safe=False)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            id = request.POST.get('id', None)
            type_request = request.POST.get('type', None)
            if request.is_ajax():
                if type_request == 'add_materia':
                    form = MateriaForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({'message': 'Materia agregada con exito'}, status=200)
                    html_form = str(form)
                    return JsonResponse({'form': html_form}, status=400)

                if type_request == 'update_materia':
                    materia = MateriaForm(
                        request.POST, instance=Materia.objects.get(id=id))
                    if materia.is_valid():
                        materia.save()
                        return JsonResponse({'message': 'Materia actualizada con exito'}, status=200)
                    html_form = str(materia)
                    return JsonResponse({'form': html_form, 'nombre': materia.nombre}, status=400)

                if type_request == 'form_update_data_materia':
                    materia = Materia.objects.get(id=id)
                    form = MateriaForm(instance=materia)
                    html_form = str(form)
                    return JsonResponse({'form': html_form, 'nombre': materia.nombre}, status=200)

                if type_request == 'form_add_data_materia':
                    form = MateriaForm()
                    # agregar el valor inicial de grado de acuerdo con el id del request id_grado
                    id_grado = request.POST.get('id_grado', None)
                    form.fields['grado'].initial = id_grado
                    html_form = str(form)
                    return JsonResponse({'form': html_form}, status=200)

                if type_request == 'change_status':
                    materia = Materia.objects.get(id=id)
                    if materia.activo:
                        materia.activo = False
                    else:
                        materia.activo = True
                    materia.save()
                    return JsonResponse({'message': 'Materia eliminada con exito'}, status=200)
                if type_request == 'form_html':
                    form = MateriaForm()
                    html_form = str(form)
                    return JsonResponse({'form': html_form}, status=200)

                if type_request == 'delete':
                    materia = Materia.objects.get(id=id)
                    # cambiar el estado del modelo
                    materia.status_model = False
                    materia.save()
                    return JsonResponse({'message': 'Materia eliminada con exito'}, status=200)

            materias = list(Materia.objects.filter(status_model=True).values())
            for materia in materias:
                materia['grado'] = Grado.objects.get(
                    id=materia['grado_id']).nombre
            return JsonResponse(materias, safe=False)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class NewHorarioAjax(ListView):
    model = Horario
    form = NewHorarioForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Horario agregado con exito', 'id': form.instance.id}, status=200)
            html_form = str(form)
            return JsonResponse({'form_html': html_form}, status=400)


class PlantillaAjax(ListView, GeneradorHorario):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type')
            id_horario = request.POST.get('id_horario')
            if request.is_ajax():
                if type == 'check_dias':
                    dia = request.POST.get('dia', None)
                    self.change_checkbox(dia, id_horario)
                    return JsonResponse({'message': 'Dias actualizados con exito'}, status=200)
                if type == 'agregar_receso':
                    try:
                        receso = Recesos.objects.get(
                            periodo=request.POST.get('periodo'))
                    except Recesos.DoesNotExist:
                        receso = Recesos()
                    finally:
                        receso.periodo = request.POST.get('periodo')
                        receso.hora_duracion = request.POST.get('hora')
                        receso.minuto_duracion = request.POST.get('minuto')
                        receso.horario = Horario.objects.get(id=id_horario)
                        receso.save()
                        return JsonResponse({'message': 'Receso agregado con exito'}, status=200)
                if type == 'eliminar_receso':
                    receso = Recesos.objects.get(periodo=int(
                        request.POST.get('periodo'))-1, horario=id_horario)
                    receso.delete()
                    return JsonResponse({'message': 'Receso eliminado con exito'}, status=200)
                horarioModel = Horario.objects.get(id=id_horario)
                if type == 'hora_inicio':
                    hora_previa = horarioModel.hora_inicio
                    hora_inicio = request.POST.get('hora', None)
                    horarioModel.hora_inicio = hora_inicio
                    horarioModel.save()
                    return JsonResponse({'message': 'Hora de inicio actualizada con exito'}, status=200)
                if type == 'no_periodos':
                    horarioModel.cantidad_periodo = request.POST.get(
                        'no_periodos')
                    horarioModel.save()
                    return JsonResponse({'message': 'Numero de periodos actualizado con exito'}, status=200)
                if type == 'duracion_periodo':
                    horarioModel.duracion_periodo_hour = request.POST.get(
                        'hora')
                    horarioModel.duracion_periodo_minute = request.POST.get(
                        'minuto')
                    horarioModel.save()
                    return JsonResponse({'message': 'Duracion de periodos actualizada con exito'}, status=200)
                if type == 'dias_activos':
                    return JsonResponse(horarioModel.Dias_dict(), safe=False, status=200)
                recesos = self.recesos_dict(id_horario)
                horario = self.nw_horario_generador(dias_activos=horarioModel.Dias_list(),
                                                    recreos=recesos, hora_inicio=horarioModel.hora_inicio.strftime('%H:%M'), intervalo=horarioModel.Duracion_str(), no_periodos=horarioModel.cantidad_periodo)
                if type == 'generador':
                    horario = self.horario_JSON(horario)
                    return JsonResponse(horario, status=200, safe=False)

                return JsonResponse({'message': 'error'}, status=400)
        except ValidationError as e:
            if type == 'hora_inicio':
                return JsonResponse({
                    'message': 'La hora de inicio debe tener un formato 00:00',
                    'hora': str(hora_previa)[:5],
                }, status=400)
            return JsonResponse({'message': str(e)}, status=400)
        except Exception as e:
            print('Error: ', sys.exc_info()[0])
            return JsonResponse({'message': str(e)}, status=400)


class HorariosAjax(ListView, GeneradorHorario):
    model = Horario

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # lista de horarios solo los activos
        horarios = list(Horario.objects.filter(activo=True).values())

        return JsonResponse(horarios, safe=False)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type_request = request.POST.get('type', None)

            if type_request == 'eliminar_horario':
                # solo cambia el status_model
                horario = Horario.objects.get(
                    id=request.POST.get('id_horario'))
                horario.status_model = False
                horario.save()
                return JsonResponse({'message': 'Horario eliminado con exito'}, status=200)
            if type_request == 'nw_plantilla':
                return JsonResponse(self.nw_plantilla(), safe=False)
            horarios = list(Horario.objects.filter(
                status_model=True).values())
            return JsonResponse(horarios, safe=False)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class SelectProfesorAjax(ListView):
    model = Profesor

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', None)
            if type == 'condiciones_save':
                try:
                    print(request.POST.get('cantidad_max_periodo'))
                    condicion = EstadoProfesorHorario.objects.get(
                        id=request.POST.get('id'))
                    condicion.cantidad_max_periodo = request.POST.get(
                        'cantidad_max_periodo')
                    condicion.anotaciones = request.POST.get('anotaciones')
                    condicion.Lunes = True if request.POST.get(
                        'Lunes') == 'true' else False
                    condicion.Martes = True if request.POST.get(
                        'Martes') == 'true' else False
                    condicion.Miercoles = True if request.POST.get(
                        'Miercoles') == 'true' else False
                    condicion.Jueves = True if request.POST.get(
                        'Jueves') == 'true' else False
                    condicion.Viernes = True if request.POST.get(
                        'Viernes') == 'true' else False
                    condicion.Sabado = True if request.POST.get(
                        'Sabado') == 'true' else False
                    condicion.Domingo = True if request.POST.get(
                        'Domingo') == 'true' else False
                    condicion.save()
                    return JsonResponse({'status': 'ok'}, status=200)
                except Exception as e:
                    print('Error: ', sys.exc_info()[0])
                    print(e)
                    return JsonResponse({'message': str(e)}, status=400)

            if type == 'change_status':
                estadoprofesor = EstadoProfesorHorario.objects.get(
                    id=request.POST.get('id'))
                estadoprofesor.activo = not estadoprofesor.activo
                estadoprofesor.save()
                return JsonResponse({'message': 'Profesor actualizado con exito'}, status=200)
            id_horario = request.POST.get('id_horario')
            if type == 'condiciones':
                estado_profesor = EstadoProfesorHorario.objects.get(
                    id=request.POST.get('id'))
                if estado_profesor.cantidad_max_periodo == 0:
                    estado_profesor.cantidad_max_periodo = Horario.objects.get(
                        id=id_horario).Cantidad_periodos()
                    estado_profesor.save()
                form = EstadoProfesorHorarioForm(instance=estado_profesor)
                # separa el form en 2 partes
                cantidad_max_periodo = str(form['cantidad_max_periodo'])
                Lunes = form['Lunes'].__str__()
                Martes = form['Martes'].__str__()
                Miercoles = form['Miercoles'].__str__()
                Jueves = form['Jueves'].__str__()
                Viernes = form['Viernes'].__str__()
                Sabado = form['Sabado'].__str__()
                Domingo = form['Domingo'].__str__()
                anotaciones = form['anotaciones'].__str__()

                context = {
                    'cantidad_max_periodos': cantidad_max_periodo,
                    'Lunes': Lunes, 'Martes': Martes, 'Miercoles': Miercoles, 'Jueves': Jueves, 'Viernes': Viernes, 'Sabado': Sabado, 'Domingo': Domingo,
                    'anotaciones': anotaciones,
                }
                return JsonResponse(context, safe=False, status=200)

            profesores = list(Profesor.objects.filter(
                status_model=True).values())
            profesores_list = []
            for p in profesores:
                try:
                    profesor = EstadoProfesorHorario.objects.get(
                        horario=Horario.objects.get(id=id_horario),
                        profesor=Profesor.objects.get(id=p['id'])
                    )
                except EstadoProfesorHorario.DoesNotExist:

                    profesor = EstadoProfesorHorario.objects.create(
                        horario=Horario.objects.get(id=id_horario),
                        profesor=Profesor.objects.get(id=p['id']),
                        cantidad_max_periodo=Horario.objects.get(
                            id=id_horario).Cantidad_periodos(),

                    )
                finally:
                    profesores_list.append({
                        'id': profesor.id,
                        'nombre': p['nombre'],
                        'alias': p['alias'],
                        'activo': profesor.activo,
                        'id_profesor': p['id']
                    })
            return JsonResponse(profesores_list, safe=False)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


class SelectGradoAjax(ListView):
    model = Grado

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', None)
            if type == 'change_status':
                try:
                    estadogrado = EstadoGradoHorario.objects.get(
                        id=request.POST.get('id'))
                    estadogrado.activo = not estadogrado.activo
                    estadogrado.save()
                    activo_grado = bool( estadogrado.activo )
                    print("Estado grado: ", estadogrado.activo)
                    estadomaterias = EstadoMateriaHorario.objects.filter(
                        horario=estadogrado.horario).filter(
                            materia__grado__id = estadogrado.grado.id)
                    for estadomateria in estadomaterias:
                        estadomateria.activo = activo_grado
                        estadomateria.save()
                    return JsonResponse({'message': 'Grado actualizado con exito'}, status=200)
                except Exception as e:
                    print(e)
            id_horario = request.POST.get('id_horario')
            grados_p = list(Grado.objects.filter(
                status_model=True, activo=True).values())
            grados_list = []
            for g in grados_p:
                try:
                    grado = EstadoGradoHorario.objects.get(
                        horario=Horario.objects.get(id=id_horario),
                        grado=Grado.objects.get(id=g['id'])
                    )
                except Exception as e:
                    grado = EstadoGradoHorario.objects.create(
                        horario=Horario.objects.get(id=id_horario),
                        grado=Grado.objects.get(id=g['id']),
                    )
                finally:
                    grados_list.append({
                        'id': grado.id,
                        'nombre': g['nombre'],
                        'alias': g['alias'],
                        'activo': grado.activo,
                        'id_grado': g['id']
                    })
            return JsonResponse(grados_list, safe=False)
        except Exception as e:
            print('Error: ', sys.exc_info()[0])
            print(e)

            return JsonResponse({'message': str(e)}, status=400)


class SelectMateriaAjax(ListView):
    model = Materia

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', None)
            if type == 'change_status':
                estadomateria = EstadoMateriaHorario.objects.get(
                    id=request.POST.get('id'))
                estadomateria.activo = not estadomateria.activo
                estadomateria.save()
                return JsonResponse({'message': 'Materia actualizada con exito'}, status=200)
            id_horario = request.POST.get('id_horario')
            # lista de id de los grados activos
            grados = list(EstadoGradoHorario.objects.filter(activo=True, status_model=True, horario=Horario.objects.get(id=id_horario)).values_list('grado__id', flat=True))
            print(grados)
            materias = list(Materia.objects.filter(status_model=True, grado__id__in=grados).values())
            materias_list = []
            for m in materias:
                try:
                    materia = EstadoMateriaHorario.objects.get(
                        horario=Horario.objects.get(id=id_horario),
                        materia=Materia.objects.get(id=m['id'])
                    )
                except EstadoMateriaHorario.DoesNotExist:
                    materia = EstadoMateriaHorario.objects.create(
                        horario=Horario.objects.get(id=id_horario),
                        materia=Materia.objects.get(id=m['id']),
                    )
                except:
                    materia = None
                finally:
                    if materia:
                        materias_list.append({
                            'id': materia.id,
                            'materia': m['nombre'],
                            'grado': Grado.objects.get(id=m['grado_id']).nombre,
                            'activo': materia.activo,
                            'id_materia': m['id']
                        })
            return JsonResponse(materias_list, safe=False)
        except Exception as e:
            print('Error: ', sys.exc_info()[0])
            return JsonResponse({'message': str(e)}, status=400)


class SelectAsignaturaAjax(ListView, Asig):
    model = Asignatura
    form_asignatura = AsignaturaForm
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', None)
            if type == 'asignar':
                Asignatura.objects.create(
                    profesor = EstadoProfesorHorario.objects.get(id=request.POST.get('id_profesor')),
                    materia = EstadoMateriaHorario.objects.get(id=request.POST.get('id_materia')),
                    horario = Horario.objects.get(id=request.POST.get('id_horario')),
                )
                return JsonResponse({'status': 'ok'}, status=200)
            if type == 'reasignar':
                asignatura = Asignatura.objects.get(id=request.POST.get('id_asignatura'))
                asignatura.profesor = EstadoProfesorHorario.objects.get(id=request.POST.get('id_profesor'))
                asignatura.save()
                return JsonResponse({'status': 'ok'}, status=200)
            if type == 'anotaciones':
                horario = Horario.objects.get(id=request.POST.get('id_horario'))
                horario.anotaciones_asignatura = request.POST.get('anotaciones')
                horario.save()

            if type == 'list_profesores_no_asigna':
                profesores = self.Profesores_no_asignados(request.POST.get('id_horario'))
                return JsonResponse(list(profesores), status=200, safe=False)

            return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

        
class PeriodosAjax(ListView):
    model = Periodo

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        periodos = list(Periodo.objects.all().values())
        return JsonResponse(periodos, safe=False)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        periodos = list(Periodo.objects.all().values())
        return JsonResponse(periodos, safe=False)

class DisplayHorarioAjax(ListView):
    model = Horario

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', None)
            # ultima version
            if type == 'horarios':
                """
                return JsonResponse({lunes : [{proferor: "nombrefffffffffffffffffffff", materia: "nombre22222222222222222", hora_inicio: "hora", hora_fin: "hora"},{proferor: "nombre2", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}],  miercoles : [{proferor: "nombre", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}], jueves : [{proferor: "nombre", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}], viernes : [{proferor: "nombre", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}], sabado : [{proferor: "nombre", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}], domingo : [{proferor: "nombre", materia: "nombre", hora_inicio: "hora", hora_fin: "hora"}]}, status=200, safe=False)
                segun el id_grado 
                """
                version = VersionHorario.objects.filter(horario=Horario.objects.get(id=request.POST.get('id_horario'))).order_by('-id')[0]
                periodosHorario = list(PeriodoHorario.objects.filter(version_horario=version).values())
                horarios = {}
                for p in periodosHorario:
                    grado_id = Asignatura.objects.get(id=p['asignatura_id']).materia.materia.grado.id
                    if grado_id == int(request.POST.get('id_grado')):
                        if p['dia'] not in horarios:
                            horarios[p['dia']] = []
                        horarios[p['dia']].append({
                            'profesor': Asignatura.objects.get(id=p['asignatura_id']).profesor.profesor.nombre,
                            'materia': Asignatura.objects.get(id=p['asignatura_id']).materia.materia.nombre,
                            'hora_inicio': p['hora_inicio'],
                            'hora_fin': p['hora_fin'],
                        })
                
                grado_nombre = str(Grado.objects.get(id=request.POST.get('id_grado')).nombre)
                # ordenar por hora
                for dia in horarios:
                    horarios[dia] = sorted(horarios[dia], key=lambda k: k['hora_inicio'])

                # ordenar por dia
                dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
                horario_ord = {}
                for d in dias:
                    if d in horarios:
                        horario_ord[d] = horarios[d]
                horarios = horario_ord
                return JsonResponse({'horarios':horarios, 'grado_nombre':grado_nombre}, status=200, safe=False)
 
                
            return JsonResponse({'message': 'Horario actualizado con exito'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)