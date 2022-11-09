from django.db import models
from django.utils import timezone
from django.forms import model_to_dict
from django.contrib.auth.models import User


# User
class Pregunta(models.Model):
    activo = models.BooleanField(default=True)
    pregunta = models.CharField(max_length=100, unique=True)
    respuesta = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.pregunta

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'pregunta'
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'


class Grado(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    alias = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status_model = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        ordering = ['activo', 'nombre', ]


class Profesor(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    alias = models.CharField(max_length=50, blank=True, null=True)
    profesion = models.CharField(max_length=50, blank=True, null=True)
    status_model = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['activo', 'nombre', ]


class Materia(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(
        max_length=50, blank=False, null=False)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    status_model = models.BooleanField(default=True)

    def __str__(self):
        #consultar el nombre del grado

        return str(self.nombre+ '-'+ self.grado.nombre)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['activo', 'nombre', ]


class Aula(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['activo', 'nombre', ]


class Horario(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    ciclo = models.CharField(max_length=50, default='')
    descripcion = models.TextField(blank=True, null=True)
    estado_del_horario = models.CharField(
        max_length=50, blank=True, null=True)
    no_page = models.IntegerField(default=1)
    status_model = models.BooleanField(default=False)

    Lunes = models.BooleanField(default=True)
    Martes = models.BooleanField(default=True)
    Miercoles = models.BooleanField(default=True)
    Jueves = models.BooleanField(default=True)
    Viernes = models.BooleanField(default=True)
    Sabado = models.BooleanField(default=False)
    Domingo = models.BooleanField(default=False)

    cantidad_periodo = models.IntegerField(default=7)
    hora_inicio = models.TimeField(default=timezone.now)
    duracion_periodo_hour = models.IntegerField(default=1)
    duracion_periodo_minute = models.IntegerField(default=0)

    # anotaciones para asignatura en Textarea
    anotaciones_asignatura = models.TextField(
        blank=True, null=True, default='')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # restar 10 horas a la hora de inicio
        try:
            self.hora_inicio = self.hora_inicio - timezone.timedelta(hours=10)
        except:
            pass

    def __str__(self):
        return f"{self.nombre} - {self.ciclo}"

    def Dias_list(self):
        return [self.Lunes, self.Martes, self.Miercoles, self.Jueves, self.Viernes, self.Sabado, self.Domingo]

    def Duracion_str(self):
        return '{}:{}'.format(self.duracion_periodo_hour, self.duracion_periodo_minute)

    def Dias_dict(self):
        return {'Lunes': self.Lunes, 'Martes': self.Martes, 'Miercoles': self.Miercoles, 'Jueves': self.Jueves, 'Viernes': self.Viernes, 'Sabado': self.Sabado, 'Domingo': self.Domingo}

    def Cantidad_periodos(self):
        cantidad = 0
        for dia in self.Dias_list():
            if dia:
                cantidad += 1
        return cantidad

    class Meta:
        verbose_name = 'Plantilla de horario'
        verbose_name_plural = 'Plantillas de horario'
        ordering = ['activo', 'nombre', ]


class Recesos(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    periodo = models.IntegerField(default=None, null=False, blank=False)
    hora_duracion = models.IntegerField(default=0)
    minuto_duracion = models.IntegerField(default=30)
    status_model = models.BooleanField(default=True)

    def Duracion_str(self):
        """verifica que sea 00:00"""
        if self.hora_duracion < 10:
            hora = '0{}'.format(self.hora_duracion)
        else:
            hora = self.hora_duracion
        if self.minuto_duracion < 10:
            minuto = '0{}'.format(self.minuto_duracion)
        else:
            minuto = self.minuto_duracion
        return '{}:{}'.format(hora, minuto)

    class Meta:
        verbose_name = 'Receso'
        verbose_name_plural = 'Recesos'


class EstadoProfesorHorario(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    cantidad_max_periodo = models.IntegerField(default=0)
    Lunes = models.BooleanField(default=True)
    Martes = models.BooleanField(default=True)
    Miercoles = models.BooleanField(default=True)
    Jueves = models.BooleanField(default=True)
    Viernes = models.BooleanField(default=True)
    Sabado = models.BooleanField(default=True)
    Domingo = models.BooleanField(default=True)
    anotaciones = models.TextField(blank=True, null=True)
    status_model = models.BooleanField(default=True)

    def __str__(self):
        return self.profesor.nombre

    class Meta:
        verbose_name = 'Estado de profesor en horario'
        verbose_name_plural = 'Estados de profesor en horario'
        ordering = ['activo', ]


class EstadoGradoHorario(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.DO_NOTHING)
    Lunes = models.BooleanField(default=True)
    Martes = models.BooleanField(default=True)
    Miercoles = models.BooleanField(default=True)
    Jueves = models.BooleanField(default=True)
    Viernes = models.BooleanField(default=True)
    Sabado = models.BooleanField(default=True)
    Domingo = models.BooleanField(default=True)
    status_model = models.BooleanField(default=True)

    def __str__(self):
        return self.grado.nombre

    class Meta:
        verbose_name = 'Estado de grado en horario'
        verbose_name_plural = 'Estados de grado en horario'
        ordering = ['activo', ]


class EstadoMateriaHorario(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.DO_NOTHING)
    Lunes = models.BooleanField(default=True)
    Martes = models.BooleanField(default=True)
    Miercoles = models.BooleanField(default=True)
    Jueves = models.BooleanField(default=True)
    Viernes = models.BooleanField(default=True)
    Sabado = models.BooleanField(default=True)
    Domingo = models.BooleanField(default=True)

    def __str__(self):
        return self.materia.nombre

    class Meta:
        verbose_name = 'Estado de materia en horario'
        verbose_name_plural = 'Estados de materia en horario'
        ordering = ['activo', ]


class EstadoAulaHorario(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.activo)

    class Meta:
        verbose_name = 'Estado de aula en horario'
        verbose_name_plural = 'Estados de aula en horario'
        ordering = ['activo', ]


class CondicionEstadoProfesorHorario(models.Model):
    activo = models.BooleanField(default=True)
    estado_profesor_horario = models.ForeignKey(
        EstadoProfesorHorario, on_delete=models.CASCADE)
    dia = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio = models.IntegerField(default=0)
    minuto_inicio = models.IntegerField(default=0)
    hora_fin = models.IntegerField(default=0)
    minuto_fin = models.IntegerField(default=0)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Condicion de estado de profesor en horario'
        verbose_name_plural = 'Condiciones de estado de profesor en horario'
        ordering = ['activo', ]


class CondicionEstadoGradoHorario(models.Model):
    activo = models.BooleanField(default=True)
    estado_grado_horario = models.ForeignKey(
        EstadoGradoHorario, on_delete=models.CASCADE)
    dia = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio = models.IntegerField(default=0)
    minuto_inicio = models.IntegerField(default=0)
    hora_fin = models.IntegerField(default=0)
    minuto_fin = models.IntegerField(default=0)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Condicion de estado de grado en horario'
        verbose_name_plural = 'Condiciones de estado de grado en horario'
        ordering = ['activo', ]


class CondicionEstadoMateriaHorario(models.Model):
    activo = models.BooleanField(default=True)
    estado_materia_horario = models.ForeignKey(
        EstadoMateriaHorario, on_delete=models.CASCADE)
    dia = models.CharField(max_length=255, blank=True, null=True)
    hora_inicio = models.IntegerField(default=0)
    minuto_inicio = models.IntegerField(default=0)
    hora_fin = models.IntegerField(default=0)
    minuto_fin = models.IntegerField(default=0)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Condicion de estado de materia en horario'
        verbose_name_plural = 'Condiciones de estado de materia en horario'
        ordering = ['activo', ]


class Asignatura(models.Model):
    activo = models.BooleanField(default=True)
    profesor = models.ForeignKey(
        EstadoProfesorHorario, on_delete=models.CASCADE)
    materia = models.ForeignKey(EstadoMateriaHorario, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['activo', ]

    def __str__(self) -> str:
        return f'{self.profesor} _ {self.materia} _ {self.horario}'

class Periodo(models.Model):
    activo = models.BooleanField(default=True)
    nombre = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default='Periodo')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, blank=True)
    dia = models.CharField(max_length=10, blank=False, null=False)
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.dia + ' ' + self.hora_inicio.strftime('%H:%M') + '-' + self.hora_fin.strftime('%H:%M')

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ['dia', 'hora_inicio']



class VersionHorario(models.Model):
    activo = models.BooleanField(default=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    version = models.IntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Version de horario'
        verbose_name_plural = 'Versiones de horario'
        ordering = ['activo', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            version = VersionHorario.objects.filter(horario=self.horario).count()
            self.version = version + 1
        except:
            self.version = 1

    def __str__(self):
        return str(self.horario.nombre) + ' - ' + str(self.version)

    


class PeriodoHorario(models.Model):
    activo = models.BooleanField(default=True)
    no_periodo = models.IntegerField(default=1)
    dia = models.CharField(max_length=10, blank=False, null=False)
    version_horario = models.ForeignKey(VersionHorario, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)
    status_model = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Periodo de horario'
        verbose_name_plural = 'Periodos de horario'
        ordering = ['activo', ]

    