function mostrarAlertaExitosaRedireccion(titulo, mensaje, urlRedireccion) {
    Swal.fire({
        icon: 'success',
        title: titulo,
        text: mensaje,
        confirmButtonText: 'Aceptar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = urlRedireccion;
        }
    });
}