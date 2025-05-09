function abrirFormularioModificar(servicio_id) {
    // Usamos fetch para obtener el formulario de Django (backend)
    fetch(`/modificar/${servicio_id}/`)
        .then(response => response.text())  // Obtenemos la respuesta como HTML
        .then(html => {
            // Creamos un Sweet Alert con el formulario cargado
            swal({
                title: "Modificar Servicio",
                content: html,  // Insertamos el formulario en el modal
                buttons: {
                    cancel: "Cancelar",
                    confirm: "Modificar"
                }
            }).then((willModify) => {
                if (willModify) {
                    // Si el usuario decide modificar, enviamos el formulario
                    let form = document.getElementById('formModificar');
                    let formData = new FormData(form);

                    fetch(`/modificar/${servicio_id}/`, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}'  // Incluir el CSRF token
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Servicio modificado exitosamente');
                            location.reload();  // Recargamos la página o actualizamos el contenido
                        } else {
                            alert('Hubo un error al modificar el servicio');
                        }
                    });
                }
            });
        });
}