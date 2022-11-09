from django.contrib import admin
from .models import *

# Register your models here.
"""
class AulaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'grado', 'profesor')
    list_filter = ('grado', 'profesor')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    fields = ('nombre', 'capacidad', 'grado', 'profesor')
    list_editable = ['capacidad'] 
    list_per_page = 5
admin.site.register(Aula, AulaAdmin)
"""

#Preguntas de recuperacion 
"""
activo = models.BooleanField(default=True)
pregunta = models.CharField(max_length=100, unique=True)
respuesta = models.CharField(max_length=100)
usuario = models.ForeignKey(User, on_delete=models.CASCADE)
fecha_creacion = models.DateTimeField(default=timezone.now)
fecha_modificacion = models.DateTimeField(default=timezone.now)
"""
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'pregunta', 'respuesta', 'usuario')
    list_filter = ('activo',)
    search_fields = ('pregunta','usuario')
    ordering = ('pregunta',)
    fields = ('pregunta', 'respuesta', 'activo')
    list_per_page = 5

class GradoAdmin(admin.ModelAdmin):
    list_display = ('activo','nombre', 'alias', 'status_model') 
    
    search_fields = ('activo','nombre','alias', 'status_model')
    ordering = ('activo','nombre',)
    list_per_page = 5

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('activo','nombre', 'alias', 'status_model')
    search_fields = ('activo','nombre','alias', 'status_model')
    ordering = ('activo','nombre',)
    list_per_page = 5

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('activo','nombre', 'grado', 'status_model')
    list_filter = ('activo','grado', 'status_model')
    search_fields = ('activo','nombre', 'status_model')
    ordering = ('activo','nombre',)
    fields = ('activo','nombre', 'grado', 'status_model')
    list_per_page = 5



class HorarioAdmin(admin.ModelAdmin):
    list_display = ('activo','nombre', 'no_page')
    list_filter = ('activo','estado_del_horario',)
    search_fields = ('nombre','estado_del_horario',)
    ordering = ('nombre','status_model',)
    fields = (
        'activo','nombre', 'ciclo','estado_del_horario',
        'no_page','status_model',)
    list_per_page = 5
    
class EstadoProfesorHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'horario', 'profesor')
    list_filter = ('activo', 'horario', 'profesor')
    search_fields = ('activo', 'horario', 'profesor')
    ordering = ('activo', 'horario', 'profesor')
    fields = ('activo', 'horario', 'profesor')
    list_per_page = 5


class EstadoGradoHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'horario', 'grado')
    list_filter = ('activo', 'horario', 'grado')
    search_fields = ('activo', 'horario', 'grado')
    ordering = ('activo', 'horario', 'grado')
    fields = ('activo', 'horario', 'grado')
    list_per_page = 5

class EstadoMateriaHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'horario', 'materia')
    list_filter = ('activo', 'horario', 'materia')
    search_fields = ('activo', 'horario', 'materia')
    ordering = ('activo', 'horario', 'materia')
    fields = ('activo', 'horario', 'materia')
    list_per_page = 5


class EstadoAulaHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'horario', 'aula')
    list_filter = ('activo', 'horario', 'aula')
    search_fields = ('activo', 'horario', 'aula')
    ordering = ('activo', 'horario', 'aula')
    fields = ('activo', 'horario', 'aula')
    list_per_page = 5


class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'profesor', 'materia', 'horario')
    list_filter = ('activo', 'profesor', 'materia', 'horario')
    search_fields = ('activo', 'profesor', 'materia', 'horario')
    ordering = ('activo', 'profesor', 'materia', 'horario')
    fields = ('activo', 'profesor', 'materia', 'horario')
    list_per_page = 5

    def __str__(self):
        return f"{self.profesor} - {self.materia} - {self.horario}"


class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('activo','nombre', 'asignatura', 'dia', 'hora_inicio', 'hora_fin')
    list_filter = ('activo','asignatura', 'dia', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre', 'asignatura', 'dia', 'hora_inicio', 'hora_fin')
    ordering = ('activo','nombre', 'asignatura', 'dia', 'hora_inicio', 'hora_fin')
    fields = ('activo','nombre', 'asignatura', 'dia', 'hora_inicio', 'hora_fin')
    list_per_page = 5

class VersionHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'horario', 'version', 'fecha', 'status_model')
    list_filter = ('activo', 'horario', 'version', 'fecha', 'status_model')
    search_fields = ('activo', 'horario', 'version', 'fecha', 'status_model')
    ordering = ('activo', 'horario', 'version', 'fecha', 'status_model')
    fields = ('activo', 'horario', 'version', 'status_model')
    list_per_page = 5


class PeriodoHorarioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'no_periodo', 'dia', 'version_horario', 'asignatura', 'hora_inicio', 'hora_fin')
    list_filter = ('activo', 'no_periodo', 'dia', 'version_horario', 'asignatura', 'hora_inicio', 'hora_fin')
    search_fields = ('activo', 'no_periodo', 'dia', 'version_horario', 'asignatura', 'hora_inicio', 'hora_fin')
    ordering = ('activo', 'no_periodo', 'dia', 'version_horario', 'asignatura', 'hora_inicio', 'hora_fin')
    fields = ('activo', 'no_periodo', 'dia', 'version_horario', 'asignatura', 'hora_inicio', 'hora_fin')
    list_per_page = 20
    
#admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Grado, GradoAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Horario, HorarioAdmin)
#admin.site.register(EstadoProfesorHorario, EstadoProfesorHorarioAdmin)
#admin.site.register(EstadoGradoHorario, EstadoGradoHorarioAdmin)
#admin.site.register(EstadoMateriaHorario, EstadoMateriaHorarioAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
#admin.site.register(Periodo, PeriodoAdmin)
#daf
admin.site.register(VersionHorario, VersionHorarioAdmin)
admin.site.register(PeriodoHorario, PeriodoHorarioAdmin)
