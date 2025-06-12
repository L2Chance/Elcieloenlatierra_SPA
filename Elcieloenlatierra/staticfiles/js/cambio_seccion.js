function mostrarSeccion(id) {
  const secciones = document.querySelectorAll(".contenedor-general section");
  secciones.forEach((sec) => (sec.style.display = "none"));

  const seccionActiva = document.querySelector(`.${id}`);
  if (seccionActiva) {
    seccionActiva.style.display = "block";
  }

  const botones = document.querySelectorAll("button");
  botones.forEach((btn) => btn.classList.remove("activo"));

  const botonActivo = Array.from(botones).find((btn) =>
    btn.getAttribute("onclick").includes(id)
  );
  if (botonActivo) {
    botonActivo.classList.add("activo");
  }
  
}

