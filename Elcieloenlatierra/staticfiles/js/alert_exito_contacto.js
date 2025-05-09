function mostrarAlertaExitosaContacto(titulo, mensaje) {
  Swal.fire({
    icon: "success",
    title: titulo,
    html: mensaje,
    confirmButtonText: "Aceptar",
  });
}
