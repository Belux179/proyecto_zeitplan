<script type="application/javascript">
table_id = '#tabla_profesores';
try {
    $(document).ready(function() {
        $(table_id).DataTable({
            "processing": true,
            "responsive": true,
            "language": {
                {% load static %}
                "url": "{% static 'json/table_es.json' %}"
            },
            ajax: {
                url: '{% url 'profesores_ajax' %}',
                type: 'POST',
                dataSrc: '',
                data: {
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                }
            },
            columns: [
                {data: 'id'},
                {data: 'nombre'},
                {data: 'alias'},
                {data: 'activo'},
                {data: 'id'}
            ],
            columnDefs: [{
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    
                    return '<a onclick="update_profesor('+data+')" class="btn btn-primary btn-sm"><i class="fas fa-edit"></i></a>'+ 
                    '<a onclick="delete_profesor(' + data + ')" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></a>';
                }
            }, {
                targets: [-2],
                class: 'text-center',
                render: function(data, type, row) {
                    if (data == true) {
                        return '<span class="badge badge-success">Activo</span> <a onclick="change_status_profesor(' + row.id + ')" class="btn btn-success btn-sm"><i class="fa fa-check" ></i></a>';
                    } else {
                        return '<span class="badge badge-danger">Inactivo</span><a onclick="change_status_profesor(' + row.id + ')" class="btn btn-danger btn-sm ml-1"><i class="fa fa-times" ></i></a>';
                    }
                }
            }]

        });
    });// */
    
} catch (error) {
    console.log(error);
}
function change_status_profesor(id) {
    $.ajax({
        url: '{% url 'profesores_ajax' %}',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'id': id,
            'type': 'change_status'
        },
        success: function(data) {
            $(table_id).DataTable().ajax.reload();
        },
        error: function(data) {
            console.log(data);
        }
    });
}
function update_profesor(id, form_html='') {
    $.ajax({
        url: '{% url 'profesores_ajax' %}',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'id': id,
            'type': 'form_update_data_profesor'
        },
        success: function(data) {
            form_html = form_html || data.form;
            Swal.fire({
                title: 'Actualizar profesor ' + data.nombre,
                html:   '<form id="form_add_profesor" method="POST">'+
                            '{% csrf_token %}'+
                            '<input type="hidden" name="id" value="'+id+'">'+
                            form_html +               
                        '</form>', //*/
                showCancelButton: true,
                confirmButtonText: 'Actualizar',
                cancelButtonText: 'Cancelar',
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    const nombre = Swal.getPopup().querySelector('#nombre_profesor_form_profesor').value
                    const alias = Swal.getPopup().querySelector('#alias_profesor_form_profesor').value
                    if (!nombre) {
                        Swal.showValidationMessage(`Por favor ingrese el nombre`)
                    }
                    return { nombre: nombre, alias: alias }
                },
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: '{% url 'profesores_ajax' %}',
                        type: 'POST',
                        data: {
                            'csrfmiddlewaretoken': '{{ csrf_token }}',
                            'type': 'update_profesor',
                            'id': id,
                            'nombre': result.value.nombre,
                            'alias': result.value.alias,
                        },
                        success: function(data) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Profesor ' + data.nombre + ' actualizado',
                                timer: 1500
                            });
                            $(table_id).DataTable().ajax.reload();
                        },
                        error: function(data) {
                            update_profesor(id, data.responseJSON.form);
                        }
                    });
                }
            })
        },
        error: function(data) {
            console.log(data);
        }
    });
    
}
//funcion para eliminar un profesor
function delete_profesor(id) {
    Swal.fire({
        title: '¿Está seguro de eliminar el profesor?',
        text: "No podrá revertir esta acción",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '{% url 'profesores_ajax' %}',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                    'id': id,
                    'type': 'delete'
                },
                success: function(data) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Profesor eliminado',
                        timer: 1500
                    });
                    $(table_id).DataTable().ajax.reload();
                },
                error: function(data) {
                    console.log(data);
                }
            });
        }
    })
}

function add_profesor(form_html='') {
    form_html = form_html || '{{ form_add|escapejs }}';
    Swal.fire({
        title: 'Agregar profesor',
        html:   '<form id="form_add_profesor" method="POST">'+
                    '{% csrf_token %}'+
                    form_html +               
                '</form>', //*/
        showCancelButton: true,
        confirmButtonText: 'Agregar',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        preConfirm: () => {
            const nombre = Swal.getPopup().querySelector('#nombre_profesor_form_profesor').value
            const alias = Swal.getPopup().querySelector('#alias_profesor_form_profesor').value
            if (!nombre) {
                Swal.showValidationMessage(`Por favor ingrese el nombre`)
            }
            return { nombre: nombre, alias: alias }
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '{% url 'profesores_ajax' %}',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                    'type': 'add_profesor',
                    'nombre': result.value.nombre,
                    'alias': result.value.alias,
                },
                success: function(data) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Profesor agregado',
                        timer: 1500
                    });
                    $(table_id).DataTable().ajax.reload();
                },
                error: function(data) {
                    add_profesor(data.responseJSON.form);
                }
            });
        }
    })
}
    