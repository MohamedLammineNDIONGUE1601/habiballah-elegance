document.addEventListener("DOMContentLoaded", function () {
  // Menu mobile
  const burger = document.querySelector(".menu-burger");
  const nav = document.querySelector(".nav-principale");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      nav.classList.toggle("ouvert");
    });
  }

  // Sélecteurs de quantité (+ / -)
  document.querySelectorAll(".selecteur-quantite").forEach(function (selecteur) {
    const input = selecteur.querySelector("input[type='number'], input[type='text']");
    const moins = selecteur.querySelector(".moins");
    const plus = selecteur.querySelector(".plus");
    const max = input ? parseInt(input.dataset.max || "99", 10) : 99;

    if (moins) {
      moins.addEventListener("click", function () {
        let val = parseInt(input.value || "1", 10);
        if (val > 1) input.value = val - 1;
      });
    }
    if (plus) {
      plus.addEventListener("click", function () {
        let val = parseInt(input.value || "1", 10);
        if (val < max) input.value = val + 1;
      });
    }
  });

  // Galerie produit : changer l'image principale au clic sur une miniature
  document.querySelectorAll(".galerie-miniatures img").forEach(function (miniature) {
    miniature.addEventListener("click", function () {
      const principale = document.querySelector(".galerie-principale img");
      if (principale) principale.src = miniature.dataset.full || miniature.src;
    });
  });

  // Masquer automatiquement les messages après quelques secondes
  const messages = document.querySelectorAll(".messages li");
  messages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = "opacity .5s ease";
      msg.style.opacity = "0";
      setTimeout(function () { msg.remove(); }, 500);
    }, 4500);
  });

  // Formulaires de quantité dans le panier : soumission auto au changement
  document.querySelectorAll(".form-quantite-panier").forEach(function (form) {
    const input = form.querySelector("input[type='number']");
    if (input) {
      input.addEventListener("change", function () {
        form.submit();
      });
    }
  });

  // Assistant de gestion réservé aux membres de l'équipe
  const assistantPage = document.querySelector("[data-assistant-api]");
  if (assistantPage) {
    const form = assistantPage.querySelector(".assistant-form");
    const input = assistantPage.querySelector("#assistant-question");
    const messages = assistantPage.querySelector(".assistant-messages");
    const csrf = assistantPage.querySelector("[name='csrfmiddlewaretoken']").value;

    function ajouterMessage(texte, agent) {
      const message = document.createElement("div");
      message.className = "assistant-message" + (agent ? " assistant-message-agent" : " assistant-message-utilisateur");
      message.textContent = texte;
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight;
    }

    function envoyerQuestion(question) {
      if (!question.trim()) return;
      ajouterMessage(question, false);
      input.value = "";
      fetch(assistantPage.dataset.assistantApi, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ question: question })
      })
        .then(function (response) { return response.json(); })
        .then(function (data) { ajouterMessage(data.reponse || data.erreur, true); })
        .catch(function () { ajouterMessage("Je ne parviens pas à joindre le service de gestion pour le moment.", true); });
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      envoyerQuestion(input.value);
    });
    assistantPage.querySelectorAll("[data-question]").forEach(function (button) {
      button.addEventListener("click", function () { envoyerQuestion(button.dataset.question); });
    });
  }
});
