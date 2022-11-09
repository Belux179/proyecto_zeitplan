from django.urls import path
from .views import *
from .ajax import *

urlpatterns = []

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profesores/', ProfesoresView.as_view(), name='profesores'),
    path('grados/', GradosView.as_view(), name='grados'),
    path('usuario/', UsuarioView.as_view(), name='usuario'),
    path('exportar/', ExportarView.as_view(), name='exportar'),
]

# ajax
urlpatterns += [
    path('profesores/ajax/', ProfesoresAjax.as_view(), name='profesores_ajax'),
    path('grados/ajax/', GradosAjax.as_view(), name='grados_ajax'),
    path('materias/ajax/', MateriasAjax.as_view(), name='materias_ajax'),
    path('horarios/ajax/', HorariosAjax.as_view(), name='horarios_ajax'),
    path('periodos/ajax/', PeriodosAjax.as_view(), name='periodos_ajax'),
    path('usuario/ajax/', UsuarioAjax.as_view(), name='usuario_ajax'),
    path('newhorario/ajax/', NewHorarioAjax.as_view(), name='newhorario_ajax'),
]
# """
urlpatterns += [
    path('modif/<int:id_horario>/',
         Select_page_HorarioView.as_view(), name='modif'),
    path('plantilla/<int:id_horario>/',
         PlantillaView.as_view(), name='plantilla'),
    path('select_profesor/<int:id_horario>/',
         SelectProfesorView.as_view(), name='select_profesor'),
    path('select_grado/<int:id_horario>/',
         SelectGradoView.as_view(), name='select_grado'),
    path('select_asignatura/<int:id_horario>/',
         Select_AsignaturasView.as_view(), name='asignaturas'),
    # path('select_periodo/<int:id_horario>/', SelectPeriodoView.as_view(), name='select_periodo'),
    path('horario_display/<int:id_horario>/',
           HorarioDisplayView.as_view(), name='horario_display'),
]

# ajax new_horario
urlpatterns += [
    path('plantilla/ajax/', PlantillaAjax.as_view(), name='plantilla_ajax'),
    path('select_profesor/ajax/', SelectProfesorAjax.as_view(),
         name='select_profesores_ajax'),
    path('select_grado/ajax/', SelectGradoAjax.as_view(),
         name='select_grados_ajax'),
    path('select_materia/ajax/', SelectMateriaAjax.as_view(),
         name='select_materias_ajax'),
    path('select_asignatura/ajax/', SelectAsignaturaAjax.as_view(),
         name='select_asignaturas_ajax'),
     path('display_horario/ajax/', DisplayHorarioAjax.as_view(),
           name='display_horario_ajax'),
]
"""
# PDF
urlpatterns += [
    path('horario_pdf1/<int:id_horario>/<int:id_grado>', HorarioPDFView.as_view(), name='horario'),
]
"""