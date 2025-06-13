document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatWindow = document.getElementById("chatbot-window");
  const sendBtn = document.getElementById("chatbot-send");
  const input = document.getElementById("chatbot-input");
  const messages = document.getElementById("chatbot-messages");

  const qaPairs = {
  Hola: "¡Hola! ¿En qué puedo ayudarte?",
  Gracias: "¡De nada! Si necesitas algo más, aquí estoy.",
  horarios: "Nuestro horario de atención es de lunes a viernes, de 7:00 a 23:00hs.",
  precios: "Los precios varían según el servicio. ¿Qué servicio te interesa?",
  gracias: "¡De nada! Si necesitas algo más, aquí estoy.",
  "usuario administrador": "Usuario: LautyDos \n - Contraseña: 1234",
  "usuario profesional": "Usuario: LautyTres \n - Contraseña: L44087709P",
  "usuario cliente": "Usuario: Tomi11 \n - Contraseña: tomasgarcanteros",

  "la metodología":
    "¡Por supuesto! En Sentirse Bien SPA contamos con tres tipos de usuarios principales: Clientes, Profesionales y Administradores. Los Clientes pueden explorar los servicios disponibles y realizar reservas. Estas reservas, una vez gestionadas por un Administrador, se convierten en turnos confirmados. Además, los Clientes pueden acceder a su perfil para consultar sus turnos activos y su historial. Los Profesionales tienen acceso a su perfil profesional, donde visualizan los turnos asignados relacionados con su especialidad. Por su parte, los Administradores disponen de un panel de control completo desde donde gestionan servicios, profesiones, solicitudes, turnos y toda la actividad general de la plataforma.",

  masaje:
    "💆 Masaje\nTécnica manual que involucra la manipulación de los tejidos blandos del cuerpo para aliviar tensiones y mejorar la circulación.\nTurnos disponibles: mañana, tarde.",

  belleza:
    "💄 Belleza\nRealzá tu mejor versión con tratamientos personalizados que cuidan tu piel y resaltan tu belleza natural.\nTurnos disponibles: mañana, tarde.",

  "tratamientos faciales":
    "🌿 Tratamientos Faciales\nDescubrí nuestros tratamientos diseñados para limpiar, hidratar y revitalizar la piel de tu rostro.\nTurnos disponibles: mañana, tarde.",

  "tratamientos corporales":
    "🧖‍♀️ Tratamientos Corporales\nCuidados integrales para tu cuerpo que ayudan a mejorar la circulación, tonificar y relajar.\nTurnos disponibles: mañana, tarde, noche.",

  hidromasaje:
    "🛁 Hidromasaje\nSumergite en una experiencia de relajación profunda con nuestros hidromasajes que revitalizan cuerpo y mente.\nTurnos disponibles: tarde, noche.",

  yoga:
    "🧘 Yoga\nConectá cuerpo, mente y respiración a través de prácticas guiadas que equilibran tu energía.\nTurnos disponibles: tarde.",

  comprobante: "Sí, una vez que realice una reserva, recibirá un comprobante en el correo electrónico asociado a su cuenta.",
};


  toggleBtn.addEventListener("click", () => {
    if (chatWindow.style.display === "none") {
      chatWindow.style.display = "block";
      input.focus();
    } else {
      chatWindow.style.display = "none";
    }
  });

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  function sendMessage() {
    const userText = input.value.trim().toLowerCase();
    if (!userText) return;

    appendMessage("Tú", input.value);

    // Buscar respuesta
    let response = "Disculpa, no entendí tu pregunta. ¿Podés reformularla?";
    for (const question in qaPairs) {
      if (userText.includes(question)) {
        response = qaPairs[question];
        break;
      }
    }

    setTimeout(() => {
      appendMessage("Bot", response);
    }, 500);

    input.value = "";
    input.focus();
  }

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.style.marginBottom = "10px";
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }
  const suggestions = document.getElementById("chatbot-suggestions");

  input.addEventListener("input", () => {
    if (input.value.trim().length > 0) {
      suggestions.style.display = "none";
    } else {
      suggestions.style.display = "flex";
    }
  });

  function sendMessage() {
    const userText = input.value.trim().toLowerCase();
    if (!userText) return;

    suggestions.style.display = "none";

    appendMessage("Tú", input.value);

    let response = "Disculpa, no entendí tu pregunta. ¿Podés reformularla?";
    for (const question in qaPairs) {
      if (userText.includes(question)) {
        response = qaPairs[question];
        break;
      }
    }

    setTimeout(() => {
      appendMessage("Bot", response);
    }, 500);

    input.value = "";
    input.focus();
  }

  document.querySelectorAll(".suggestion").forEach((item) => {
    item.addEventListener("click", () => {
      input.value = item.textContent;
      sendMessage();
    });
  });

  toggleBtn.addEventListener("click", () => {
    const isVisible = chatWindow.classList.contains("visible");

    if (isVisible) {
      chatWindow.classList.remove("visible");
      setTimeout(() => {
        chatWindow.style.display = "none";
      }, 300);
    } else {
      chatWindow.style.display = "flex";
      setTimeout(() => {
        chatWindow.classList.add("visible");
        input.focus();
      }, 10);
    }
  });

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("chatbot-msg");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }
});
