document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatWindow = document.getElementById("chatbot-window");
  const sendBtn = document.getElementById("chatbot-send");
  const input = document.getElementById("chatbot-input");
  const messages = document.getElementById("chatbot-messages");

  const qaPairs = {
    Hola: "¡Hola! ¿En qué puedo ayudarte?",
    Gracias: "¡De nada! Si necesitas algo más, aquí estoy.",
    horarios:
      "Nuestro horario de atención es de lunes a viernes, de 7:00 a 23:00hs.",
    precios: "Los precios varían según el servicio. ¿Qué servicio te interesa?",
    gracias: "¡De nada! Si necesitas algo más, aquí estoy.",
    "usuario administrador": "Usuario: LautyDos \n - Contraseña: 1234",
    "usuario profesional": "Usuario: LautyTres \n - Contraseña: L44087709P",
    "usuario cliente": "Usuario: LautyCuatro \n - Contraseña: 12345",
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
