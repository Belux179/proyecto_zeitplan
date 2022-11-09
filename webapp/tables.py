from .models import *
from table import *
from table.columns import Column
from table.utils import *
"""
class ProfesorTable(Table): 
    id = Column(field='id', header='ID')
    nombre = Column(field='nombre', header='Nombre')
    alias = Column(field='alias', header='Alias')
    
    class Meta:
        model = Profesor
        attrs = {'class': 'paleblue'}
        fields = ['id', 'nombre', 'alias']
        sequence = ['id', 'nombre', 'alias']
        exclude = ['id']
        empty_text = "No hay profesores registrados"
        """
#clase de tabla para los profesores con las columnas de id, nombre, alias y acciones para editar y eliminar
class ProfesorTable(Table):
    id = Column(field='id', header='ID')
    nombre = Column(field='nombre', header='Nombre')
    alias = Column(field='alias', header='Alias')
    acciones = Column(field='acciones', header='Acciones')
    
    class Meta:
        model = Profesor
        attrs = {'class': 'paleblue'}
        fields = ['id', 'nombre', 'alias', 'acciones']
        sequence = ['id', 'nombre', 'alias', 'acciones']
        exclude = ['id']
        empty_text = "No hay profesores registrados"
    
    def render_acciones(self, record):
        return '<a href="/webapp/profesores/{}/edit/"><i class="fas fa-edit"></i></a> <a href="/webapp/profesores/{}/delete/"><i class="fas fa-trash-alt"></i></a>'.format(record.id, record.id)

