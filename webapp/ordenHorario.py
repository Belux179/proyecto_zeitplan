import time
import re
import pandas as pd
import numpy as np
        

class Asignacion:
    def __init__(self, grado: str, id_profesor: int, profesor: str, id_materia: int, materia: str, id_asignacion: int):
        self.grado = grado
        self.id_profesor = id_profesor
        self.profesor = profesor
        self.id_materia = id_materia
        self.materia = materia
        self.id_asignacion = id_asignacion
        self.dias = []
        self.contador = 0

    def __repr__(self):
        return "asignacion({}, {})".format(self.grado, self.profesor)

    def __str__(self):
        return self.materia

    def __eq__(self, other):
        """
        si dos asignaciones tienen el mismo grado, profesor, materia y id_asignacion, entonces son iguales
        si envia un int, entonces compara el id_profesor
        """
        if isinstance(other, Asignacion):
            return (self.grado, self.profesor, self.materia) == (other.grado, other.profesor, other.materia) and self.id_asignacion == other.id_asignacion
        if isinstance(other, int):
            return self.id_profesor == other
        return False

    def __hash__(self):
        return hash((self.grado, self.profesor, self.materia, self.id_asignacion))


class Periodo:

    def __init__(self, periodo: str, hora_inicio, hora_fin):
        self.periodo = periodo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self._asignacion = None

    def __str__(self):
        if self._asignacion is None:
            return "Periodo {}: {} {}".format(self.periodo, self.hora_inicio, self.hora_fin)
        else:
            return "Periodo {}: {} {} {}".format(self.periodo, self.hora_inicio, self.hora_fin, self._asignacion, self._asignacion.profesor)

    def __repr__(self):
        return f"Periodo({self.periodo})"

    @property
    def asignacion(self):
        if self.type == 'Receso':
            return self.type
        return self._asignacion

    @asignacion.setter
    def asignacion(self, clase):
        if isinstance(clase, Asignacion):
            if self.type == 'Receso':
                raise ValueError('No se puede asignar una clase a un receso')
            self._asignacion = clase
            return True

        self._asignacion = None

    @property
    def periodo(self):
        return self._periodo

    @periodo.setter
    def periodo(self, value):
        if re.match(r"Periodo \d+", value) or re.match(r"Receso \d+", value):
            self.type, self._periodo = value.split(" ")
            self._periodo = int(self._periodo)
            return
        if type(value) == int:
            self._periodo = value
            return
        raise TypeError(
            "El periodo debe ser un string ('Periodo 44' o 'Receso 44')")


class HorarioClass:

    def __init__(self, grado: str, horario=None, profesor_id_list=None):
        # condiciones comprimidas
        self._horario = []
        if horario:
            self.horario = horario
        self.grado = grado
        self.profesores = profesor_id_list
        self._asignaciones = []

    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, dic: dict):
        """
        crear property por cada dia de la semana

        """
        self.dias = []
        self.dias_str = []
        for dia in dic:
            setattr(self, dia.lower(), [])
            for periodo in dic[dia]:
                try:
                    dia_a = getattr(self, dia.lower()).append(
                        Periodo(periodo[0], periodo[1][0], periodo[1][1]))
                    self.dias.append(dia_a)
                    # agregar el dia a la lista de dias_str sin repetir
                    if dia.lower() not in self.dias_str:
                        self.dias_str.append(dia.lower())
                    getattr(self, dia.lower())[-1].dia = dia.lower()
                except IndexError:
                    pass
        self._horario = dic

    def __str__(self) -> str:
        return f'Horario de {self.grado}'

    def __repr__(self) -> str:
        return f'Horario({self.grado})'

    def __eq__(self, other) -> bool:
        if isinstance(other, HorarioClass):
            return self.grado == other.grado
        return False

    def __hash__(self) -> int:
        return hash(self.grado)

    def __iter__(self):
        return iter(self.dias)

    def periodos_vacios_list(self) -> list:
        """
        retorna una lista de periodos vacios en el horario
        """
        list = []
        for dia in self.dias:
            list += self.periodos_vacios_dia(dia)

    def periodos_vacios_dia(self, dia):
        """
        retorna una lista de periodos vacios en el dia
        """
        if isinstance(dia, str):
            dia = dia.lower()
            return [periodo for periodo in getattr(self, dia) if periodo.asignacion is None]
        if isinstance(dia, list):
            return [periodo for periodo in dia if periodo.asignacion is None]

    @property
    def asignaciones(self):
        return self._asignaciones

    @asignaciones.setter
    def asignaciones(self, asignaciones):
        if asignaciones is None:
            self._asignaciones = []
            return
        if isinstance(asignaciones, list):
            for asignacion in asignaciones:
                if not isinstance(asignacion, Asignacion):
                    raise TypeError(
                        "El objeto debe ser una instancia de Asignacion")
            self._asignaciones = asignaciones
            return
        if isinstance(asignaciones, Asignacion):
            if asignaciones in self._asignaciones:
                return
            self._asignaciones.append(asignaciones)
            return
        raise TypeError(
            "El objeto debe ser una instancia de Asignacion o lista de Asignaciones")

    def generador_asignaciones(self):
        """
        generador de asignaciones es infinito y aleatorio y cada vuelta envia un False
        """
        # lista de seguridad
        lista = [x for x in self.asignaciones]
        import random
        while True:
            if len(lista) == 0:
                yield False
                lista = [x for x in self.asignaciones]
            numero = random.randint(0, len(lista)-1)
            yield lista.pop(numero)

    def asignar_materias(self):
        """
        recorrera todo el horario en busqueda en periodos sin asignacion y lo llenara con el metodo generador
        """
        generador = self.generador_asignaciones()
        for dia in self.dias_str:
            for periodo in getattr(self, dia):
                if periodo.asignacion is None:
                    try:
                        asignacion = next(generador)
                        if asignacion is False:
                            return False
                        periodo.asignacion = asignacion
                    except ValueError:
                        continue
        return True

    def asignar_materias_inicial(self):
        generador = self.generador_asignaciones()
        for dia in self.dias_str:
            for periodo in getattr(self, dia):
                if periodo.asignacion is None:
                    try:
                        asignacion = next(generador)
                        if asignacion is False:
                            continue
                        periodo.asignacion = asignacion
                    except ValueError:
                        continue
        return True

    def asignacion_materia_ubica(self, periodo: Periodo):
        """
        asigna una asignacion a un dia y periodo especifico
        el periodo es de acuerdo 1 - ...
        """
        if periodo.asignacion is not None:
            return False
        if not isinstance(periodo, Periodo):
            raise TypeError("El objeto debe ser una instancia de Periodo")
        for asignacion in self.generador_asignaciones():
            if not asignacion:
                Periodo.asignacion = asignacion
                yield True
            else:
                yield False

    def view_pd(self):
        """
        se usara pandas para poner el horario de forma de columna y filas
        """
        max = 0
        for dia in self.dias_str:
            if len(getattr(self, dia)) > max:
                max = len(getattr(self, dia))
        df = pd.DataFrame(columns=self.dias_str, index=range(1, max+1))
        for dia in self.dias_str:
            for periodo in getattr(self, dia):
                df.loc[periodo.periodo, dia] = periodo.asignacion
        return df


class Horario_General:

    def __init__(self, horario=None, profesores_list: list = None):
        self.horario = horario
        self.profesores = profesores_list
        self._asignaciones = []

    def __str__(self):
        return "Horario general"

    def __repr__(self):
        return "Horario general()"

    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, horario):
        if horario is None:
            self._horario = []
            return
        if isinstance(horario, HorarioClass):
            # verificar que horario no este ya
            if horario not in self._horario:
                self._horario.append(horario)
            return

        if isinstance(horario, list):
            self._horario = horario
            return
        raise TypeError(
            "El horario debe ser una lista de objetos HorarioClass o un objeto HorarioClass")

    @property
    def profesores(self):
        return self._profesores

    @profesores.setter
    def profesores(self, profesor_list):
        if profesor_list is None:
            self._profesores = []
            return
        if isinstance(profesor_list, list):
            for i in profesor_list:
                try:
                    if i not in self._profesores:
                        self._profesores = profesor_list
                except AttributeError:
                    self._profesores = profesor_list
            return
        if isinstance(profesor_list, str):
            self._profesores.append(profesor_list)
            return
        raise TypeError(
            "El profesor debe ser un string o una lista de strings")

    @property
    def asignaciones(self):
        return self._asignaciones

    @asignaciones.setter
    def asignaciones(self, asignaciones):
        if isinstance(asignaciones, list):
            for asignacion in asignaciones:
                if asignacion not in self._asignaciones and isinstance(asignacion, Asignacion):
                    self._asignaciones.append(asignacion)

            self.add_asig_horario()
            return
        if self._asignaciones != [] and isinstance(asignaciones, list):
            self.signaciones = []
            return
        raise TypeError(
            "El argumento debe ser una lista de Asignaciones()")

    def add_asig_horario(self):
        """
        se agregara a cada horario sus asignaciones correspondiente al grado
        """
        for horario in self.horario:
            for asignacion in self.asignaciones:
                if asignacion.grado == horario.grado:
                    horario.asignaciones = asignacion

    def if_entrelazar(self):
        """
        verifica si el horario si no exista un periodo con el mismo profesor en laubicacion que los demas horarios
        si existe devuelve True
        si no existe devuelve False
        """
        for horario in self.horario:
            gen_horarios = (horario for horario in self.horario)
            for next_horario in gen_horarios:
                if horario == next_horario:
                    try:
                        next_horario = next(gen_horarios)
                        dias = [
                            dia for dia in horario.dias_str if dia in next_horario.dias_str]
                        for dia in dias:
                            try:
                                for periodo1, periodo2 in zip(getattr(horario, dia), getattr(next_horario, dia)):
                                    if periodo1.type != 'Receso' and periodo2.type != 'Receso':
                                        if periodo1.asignacion.id_profesor == periodo2.asignacion.id_profesor:
                                            return True, periodo1, periodo2, dia, horario, next_horario
                            except Exception as e:
                                continue
                    except StopIteration:
                        pass
        return False, None, None, None, None, None

    def if_entrelazar_profesor(self, id_profesor: int, ubicacion_periodo: int, dia: str):
        """
        verifica si el profesor esta en el periodo en el dia y en la ubicacion
        si existe devuelve False
        si no existe devuelve True
        :ubicacion_periodo, es la ubicacion en la lista del dia 
        :dia, es el dia de la semana
        """
        for horario in self.horario:
            try:
                if getattr(horario, dia)[ubicacion_periodo-1].asignacion.id_profesor == id_profesor:
                    return False
            except Exception as e:
                print(e)
                pass
        return True

    def asignar(self):
        """
        asignar una clase a un horarios
        """
        # 1. asignar materias inicial
        for horario in self.horario:
            horario.asignar_materias_inicial()
        for i in range(150):
            # 2. verificar si noy ningun horario vacio
            for horario in self.horario:
                horario.asignar_materias_inicial()

            exite, periodo1, periodo2, dia, horario1, horario2 = self.if_entrelazar()
            if exite:
                for j in range(100):
                    try:
                        periodo1.asignacion = None
                        if horario1.asignacion_materia_ubica(periodo1):
                            continue
                        periodo2.asignacion = None
                        if horario2.asignacion_materia_ubica(periodo2):
                            continue
                        if self.if_entrelazar_profesor(periodo1.asignacion.id_profesor, periodo1.periodo, dia):
                            for horario in self.horario:
                                horario.asignar_materias_inicial()
                            break
                        for horario in self.horario:
                            horario.asignar_materias_inicial()

                    except Exception as e:
                        for horario in self.horario:
                            horario.asignar_materias_inicial()

            else:
                print(i)
                return True
