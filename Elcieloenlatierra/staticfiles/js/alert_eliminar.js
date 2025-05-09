function confirmarEliminarServicio() {
    const botonesEliminar = document.querySelectorAll('.boton-eliminar-servicio');
    const csrfTokenContainer = document.getElementById('csrf-token-container');
    const csrfToken = csrfTokenContainer.dataset.csrfToken;
  
    botonesEliminar.forEach(boton => {
      boton.addEventListener('click', function(event) {
        event.preventDefault();
  
        const servicioId = this.dataset.servicioId;
        const servicioTitulo = this.dataset.servicioTitulo;
        const eliminarUrl = `/servicios/eliminar/${servicioId}/`;
  
        Swal.fire({
          title: `¿Estás seguro de eliminar "${servicioTitulo}"?`,
          text: "¡No podrás revertir esta acción!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar'
        }).then((result) => {
          if (result.isConfirmed) {
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfToken);
  
            fetch(eliminarUrl, {
              method: 'POST',
              body: formData,
              headers: {
                'X-Requested-With': 'XMLHttpRequest',
              },
            })
            .then(response => {
              if (response.ok) {

                window.location.reload(); 
              } else {
 
                console.error('Error al eliminar el servicio:', response);
                Swal.fire('Error', 'No se pudo eliminar el servicio.', 'error');
              }
            })
            .catch(error => {
              console.error('Error de red:', error);
              Swal.fire('Error', 'Hubo un problema de conexión.', 'error');
            });
          }
        });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    const csrfTokenContainer = document.getElementById('csrf-token-container');
    const csrfToken = csrfTokenContainer.dataset.csrfToken;
    confirmarEliminarServicio(csrfToken);
  });

