from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect, reverse
try:
    from .forms import PeriodoHorarioForm
    from .models import *
except ImportError:
    from forms import PeriodoHorarioForm
    from models import PeriodoHorario
try:

    from .ordenHorario import Asignacion as AsigH, HorarioClass as Hor, Horario_General as HorG
except ImportError:
    from ordenHorario import Asignacion as AsigH, HorarioClass as Hor, Horario_General as HorG

def GeneradorConteo(cont: int = 0):
    """
    Generador conteo 0, 1, 2, 
    """
    while True:
        yield cont
        cont += 1


class AllHorarioView:

    def select_posicion(self, now_posicion, posicion, id_horario):
        if posicion == 1 and now_posicion != 1:
            return redirect('plantilla', id_horario=id_horario)
        if posicion == 2 and now_posicion != 2:
            return redirect('select_profesor', id_horario=id_horario)
        if posicion == 3 and now_posicion != 3:
            return redirect('select_grado', id_horario=id_horario)
        if posicion == 4 and now_posicion != 4:
            return redirect('asignaturas', id_horario=id_horario)
        if posicion == 5 and now_posicion != 5:
            return redirect('select_periodo', id_horario=id_horario)
        if posicion == 10:
            return redirect('horario_display', id_horario=id_horario)


class GeneradorHorario:
    def recesos_dict(self, id_horario: int):
        """
        dict: {no_periodo: duración del recreo, no_periodo: duración del recreo, no_periodo: duración del recreo, ...}
        """
        recesos = {}
        try:
            for rec in Recesos.objects.filter(horario=id_horario):
                recesos[int(rec.periodo)] = rec.Duracion_str()
            return recesos
        except Recesos.DoesNotExist:
            return None

    def periodos_generador(self, hora_inicio: str = '7:00', intervalo: str = '0:30', decanso: str = '00:00', no_periodos: int = 8, recreos: dict = None) -> list:
        """
        recreos: {no_periodo: duración del recreo}
        """
        if no_periodos < 1:
            raise ValueError('no_periodos debe ser mayor a 0')
        cont_periodo = 1
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M')
        intervalo = datetime.strptime(intervalo, '%H:%M')
        decanso = datetime.strptime(decanso, '%H:%M')
        recreos = {k: datetime.strptime(v, '%H:%M')
                   for k, v in recreos.items()} if recreos else {}
        while True:
            # enviar [hora de inicio, sum(hora de inicio + intervalo)]
            if cont_periodo-1 in recreos:
                yield ['Receso', hora_inicio.strftime('%H:%M'), (hora_inicio + timedelta(hours=recreos[cont_periodo-1].hour, minutes=recreos[cont_periodo-1].minute)).strftime('%H:%M')]
                hora_inicio += timedelta(hours=recreos[cont_periodo-1].hour,
                                         minutes=recreos[cont_periodo-1].minute)
                cont_periodo += 1
                continue
            yield [hora_inicio.strftime('%H:%M'), (hora_inicio + timedelta(hours=intervalo.hour, minutes=intervalo.minute)).strftime('%H:%M')]
            hora_inicio = hora_inicio + \
                timedelta(hours=intervalo.hour, minutes=intervalo.minute) + \
                timedelta(hours=decanso.hour, minutes=decanso.minute)
            if cont_periodo > no_periodos-1:
                break
            cont_periodo += 1

    def nw_horario_generador(self, dias_activos: list = None, hora_inicio: str = '7:00', intervalo: str = '0:40', decanso: str = '00:00', no_periodos: int = 8, recreos: dict = None) -> dict:
        """
        dias_activos: default = [True, True, True, True, True, False, False] (Lunes a Viernes) [L, M, Mi, J, V, S, D]
        recreos: {no_periodo: duración del recreo}
        dict: {dia: [[periodo 1, [hora de inicio, hora de fin]], [periodo 2, [hora de inicio, hora de fin]], ...]} 

        """
        print(recreos)

        dias_activos = [True, True, True, True, True, False,
                        False] if dias_activos is None else dias_activos
        dias = ['Lunes', 'Martes', 'Miercoles',
                'Jueves', 'Viernes', 'Sabado', 'Domingo']
        dias = [dias[i] for i, v in enumerate(dias_activos) if dias_activos[i]]
        # verificar que no_periodos sea mayor a 0
        if no_periodos < 1:
            raise ValueError('no_periodos debe ser mayor a 0')
        horario = {}
        for dia in dias:
            # print(dia)
            for enum, periodo in enumerate(self.periodos_generador(hora_inicio, intervalo, decanso, no_periodos, recreos)):
                if periodo[0] == 'Receso':
                    horario.setdefault(dia, []).append(
                        [f'Receso {enum+1}', periodo[1:]])
                else:
                    horario.setdefault(dia, []).append(
                        [f'Periodo {enum+1}', periodo])
        return horario

    def disactive_periodo(self, horario: dict, dia: str, no_periodo: int):
        try:
            periodos = horario[dia]
            periodo = periodos[no_periodo-1]
            next_periodos = periodos[no_periodo:]
            if periodo:
                periodos.pop(no_periodo-1)
            for no, valor in enumerate(next_periodos):
                name, no = valor[0].split(' ')
                valor[0] = f'{name} {int(no)-1}'
            return horario
        except KeyError:
            return horario

    def change_hour(self, horario: dict, dia: str, no_periodo: int, nw_hour: str, nw_duracion: str = None):
        """
        datos_periodos_next -> [duracion, descanso_respecto al anterior periodo]
        """
        try:
            periodo = horario[dia][no_periodo-1]
            next_periodos = horario[dia][no_periodo:]
            # datos_periodos_next
            # for i in next_periodos:
        except KeyError:
            return horario

    def horario_JSON(self, horario: dict):
        """
        return [{ 'Lunes': 'Periodo 1 7:00 - 8:30', 'Martes': 'Periodo 1 7:00 - 8:30', 'Miércoles': 'Periodo 1 7:00 - 8:30', 'Jueves': 'Periodo 1 7:00 - 8:30', 'Viernes': 'Periodo 1 7:00 - 8:30', 'id_fila': 1 },...]
        """
        dias = list(horario.keys())
        try:
            cantidad_max = max([len(horario[dia]) for dia in dias])
        except ValueError:
            return []
        iterador = []
        for value in horario.values():
            iterador.append(iter(value))
        horario_json = []
        for i in range(cantidad_max):
            fila = {}
            dias_semana = ['Lunes', 'Martes', 'Miercoles',
                           'Jueves', 'Viernes', 'Sabado', 'Domingo']
            for dia, it in zip(dias, iterador):
                try:
                    periodo = next(it)
                    fila[dia] = f'{periodo[0]} {periodo[1][0]} - {periodo[1][1]}'
                except StopIteration:
                    fila[dia] = ''
                finally:
                    dias_semana.remove(dia)
            for dia in dias_semana:
                fila[dia] = ''
            fila['id_fila'] = i+1
            horario_json.append(fila)
        return horario_json

    def change_checkbox(self, dia: str, id_horario: int):
        """"
        funcion para cambiar el estado del dia seleccionado del dia del id_horario
        example: horario.Lunes (True) -> horario.Lunes (False)
        """
        try:
            horario = Horario.objects.get(id=id_horario)
            if dia == 'Lunes':
                horario.Lunes = not horario.Lunes
            elif dia == 'Martes':
                horario.Martes = not horario.Martes
            elif dia == 'Miercoles':
                horario.Miercoles = not horario.Miercoles
            elif dia == 'Jueves':
                horario.Jueves = not horario.Jueves
            elif dia == 'Viernes':
                horario.Viernes = not horario.Viernes
            elif dia == 'Sabado':
                horario.Sabado = not horario.Sabado
            elif dia == 'Domingo':
                horario.Domingo = not horario.Domingo
            horario.save()
            return True
        except Horario.DoesNotExist:
            return False


class Asig:

    def Asignatura(self, id_horario):
        """
        :materia: se quita todo las materias ya asignadas y solo los que tienen su EstadoMateriaHorario esta activo
        return {asignatura: Asignatura, materia: Materia}

        """
        asignatura = Asignatura.objects.filter(horario=id_horario, activo=True)
        materia = EstadoMateriaHorario.objects.filter( horario=id_horario, activo=True, asignatura=None)
        profesores = EstadoProfesorHorario.objects.filter(
            horario=id_horario, activo=True)
        anotaciones = Horario.objects.get(id=id_horario).anotaciones_asignatura
        return {
            'asignaciones': asignatura, 'materias': materia,
            'profesores': profesores, 'anotaciones': anotaciones,


        }

    def Profesores_no_asignados(self, id_horario):
        """
        :profesor: [{id_profesor: id, nombre: nombre, alias: alias, no_asignaciones: no_asignaciones}]
        :no_asignaciones: numero de asignaciones que tiene el profesor en el horario 
        return profesor
        """
        profesores = EstadoProfesorHorario.objects.filter(
            horario=id_horario, activo=True)
        asignaciones = Asignatura.objects.filter(horario=id_horario)
        profesores_no_asignados = []
        for profesor in profesores:
            no_asignaciones = asignaciones.filter(profesor=profesor).count()
            profesores_no_asignados.append({
                'id_profesor': int(profesor.profesor.id),
                'nombre': str(profesor.profesor.nombre),
                'alias': str(profesor.profesor.alias),
                'no_asignaciones': int(no_asignaciones)
            })
        return profesores_no_asignados


class gradooo:
    def __init__(self, horario):
        self.horario = horario


class OrdHorario(GeneradorHorario):
    def __init__(self, id_horario):
        self.id_horario = id_horario
        self.profesores = EstadoProfesorHorario.objects.filter(
            horario=id_horario, activo=True)
        self.profesores_list = [
            profesor.profesor.nombre for profesor in self.profesores]
        self.profesores_id_list = [
            profesor.profesor.id for profesor in self.profesores]
        self.hor = HorG(profesores_list=self.profesores_list)
        self.init_grados()
        self.asignaciones()
    
    def asignar(self):
        """
        asigna los profesores a las materias en el horario 
        luego guarda los horarios en la base de datos VersionHorario y Periodo Horario
        """
        self.hor.asignar()
        # crear version horario
        version_horario = VersionHorario.objects.create(
            horario=Horario.objects.get(id=self.id_horario))
        # crear periodo horario
        for hora in self.hor.horario:
            for dia in hora.dias_str:
                for periodo in getattr(hora, dia):
                    """
                    PeriodoHorario(no_periodo, dia, version_horario, hora_inicio, hora_fin, asignatura)
                    """
                    per = PeriodoHorario()
                        # asignar periodo
                    per.hora_inicio = periodo.hora_inicio
                    per.hora_fin = periodo.hora_fin
                    per.version_horario = version_horario
                    per.dia = dia
                    per.no_periodo = periodo.periodo
                    if periodo.asignacion != 'Receso':
                        asignacion_previo = periodo.asignacion.id_asignacion 
                        per.asignatura = Asignatura.objects.get(
                            id=periodo.asignacion.id_asignacion)
                    else:
                        per.asignatura = Asignatura.objects.get(
                            id=asignacion_previo)
                        per.type = 'Receso'
                    per.save()
        

    @property
    def id_horario(self):
        return self.__id_horario

    @id_horario.setter
    def id_horario(self, id_horario):
        self.__id_horario = id_horario
        recesos = self.recesos_dict(id_horario)
        horarioModel = Horario.objects.get(id=id_horario)
        self.horario = self.nw_horario_generador(dias_activos=horarioModel.Dias_list(),
                                                    recreos=recesos, hora_inicio=horarioModel.hora_inicio.strftime('%H:%M'), intervalo=horarioModel.Duracion_str(), no_periodos=horarioModel.cantidad_periodo)
        
    def init_grados(self):
        """
        :hor = Hor('nombre_grado', self.horario, profesores_id_list_grado)
        :grados = {grado:[lista de profesores del grado]}

        """
        asign = Asignatura.objects.filter(horario=self.id_horario, activo=True)
        grados = {}
        for asignatura in asign:
            # si existe el grado en el diccionario
            if asignatura.materia.materia.grado in grados:
                # si el profesor no esta en la lista de profesores del grado
                if asignatura.profesor.profesor.id not in grados[asignatura.materia.materia.grado.nombre]:
                    grados[asignatura.materia.materia.grado.nombre].append(
                        asignatura.profesor.profesor.id)
                    continue
            grados[asignatura.materia.materia.grado.nombre] = [
                asignatura.profesor.profesor.id]
        
        for grado, profesores in grados.items():
            self.hor.horario = Hor(grado=grado, horario=self.horario,
                           profesor_id_list=list(profesores))

    def asignaciones(self):
        """
        :asignaciones = AsigH('1ro', 1:id_profesor, 'Juan', 1:id_materia, 'Matematicas', 1:id_asignacion)
        """
        asign = Asignatura.objects.filter(horario=self.id_horario, activo=True)
        asignaciones = []
        for asignatura in asign:
            asignaciones.append(AsigH(
                grado=asignatura.materia.materia.grado.nombre, 
                id_profesor=asignatura.profesor.profesor.id,
                profesor=asignatura.profesor.profesor.nombre, 
                id_materia=asignatura.materia.materia.id, 
                materia=asignatura.materia.materia.nombre, 
                id_asignacion=asignatura.id))

        self.hor.asignaciones = asignaciones

class Horario_pdf:
    def __init__(self, id_horario):
        self.id_horario = id_horario
        self.version_horario = VersionHorario.objects.filter(
            horario=id_horario).order_by('-id')[0]
        self.periodos_horario = PeriodoHorario.objects.filter(
            version_horario=self.version_horario.id)
        self.horario = Horario.objects.get(id=id_horario)
        

"""if __name__ == '__main__':
    #prueba = GeneradorHorario()
    horario = GeneradorHorario().nw_horario_generador(dias_activos=[True, True, False, False, False, False, False],
                                                      hora_inicio='7:00', intervalo='0:40', decanso='00:00', no_periodos=8, recreos={2: '00:10', 4: '00:10', 6: '00:10'})
    GeneradorHorario().change_hour(horario, 'Lunes', 2, '0:23', '0:30')
"""
"""
    for dia, periodos in horario.items():
        print(dia)
        for periodo in periodos:
            print(periodo)
        print('')
    print(horario)
"""
"""
    # horario=GeneradorHorario().horario_JSON(horario)
    print(horario)

    pass
"""
