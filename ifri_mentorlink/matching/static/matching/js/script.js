(function () {
  "use strict";

  const form = document.getElementById("search-form");
  const stateBox = document.getElementById("results-state");
  const list = document.getElementById("results-list");
  const countLabel = document.getElementById("results-count");
  const submitBtn = form.querySelector(".btn-search");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    runSearch();
  });

  function runSearch() {
    const subjects = document.getElementById("subjects").value.trim();
    const time = document.getElementById("time").value.trim();
    const filiere = document.getElementById("filiere").value.trim();

    if (!subjects || !time) {
      showError("Veuillez renseigner au moins une matière et une heure souhaitée.");
      return;
    }

    setLoading(true);

    const params = new URLSearchParams({ subjects: subjects, time: time });
    if (filiere) params.set("filiere", filiere);

    fetch("/api/search/?" + params.toString(), {
      method: "GET",
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        setLoading(false);
        if (!result.ok) {
          showError(result.data.error || "Une erreur est survenue.");
          return;
        }
        renderResults(result.data.results);
      })
      .catch(function () {
        setLoading(false);
        showError("Impossible de contacter le serveur. Vérifiez que Django est bien lancé.");
      });
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.querySelector("span").textContent = isLoading
      ? "Recherche en cours…"
      : "Rechercher un mentor";
  }

  function showError(message) {
    list.hidden = true;
    list.innerHTML = "";
    countLabel.textContent = "";
    stateBox.hidden = false;
    stateBox.innerHTML = '<div class="error-state">' + escapeHtml(message) + "</div>";
  }

  function renderResults(results) {
    if (!results || results.length === 0) {
      stateBox.hidden = false;
      list.hidden = true;
      list.innerHTML = "";
      countLabel.textContent = "0 résultat";
      stateBox.innerHTML =
        '<div class="empty-state">' +
        "<p>Aucun mentor compatible pour cette recherche.</p>" +
        '<p class="empty-state__sub">Essayez une autre matière, ou élargissez le créneau horaire.</p>' +
        "</div>";
      return;
    }

    stateBox.hidden = true;
    list.hidden = false;
    countLabel.textContent =
      results.length + (results.length > 1 ? " résultats" : " résultat");

    list.innerHTML = results.map(renderMentorCard).join("");
  }

  function renderMentorCard(mentor) {
    const sealClass = mentor.score >= 70 ? "score-seal score-seal--high" : "score-seal";
    const commonChips = mentor.common_subjects
      .map(function (s) {
        return '<span class="chip">' + escapeHtml(s) + "</span>";
      })
      .join("");

    return (
      '<li class="mentor-card">' +
      "<div>" +
      '<h3 class="mentor-card__name">' + escapeHtml(mentor.name) + "</h3>" +
      '<p class="mentor-card__meta">' + escapeHtml(mentor.field_of_study) + "</p>" +
      '<p class="mentor-card__row"><strong>Matières en commun :</strong></p>' +
      '<div class="chips">' + commonChips + "</div>" +
      '<p class="mentor-card__row" style="margin-top:10px;"><strong>Disponibilités :</strong> ' +
      escapeHtml(mentor.availabilities.join(" · ")) +
      "</p>" +
      '<div class="chips">' +
      '<span class="chip chip--format">' + escapeHtml(mentor.mentoring_format) + "</span>" +
      "</div>" +
      "</div>" +
      '<div class="' + sealClass + '">' +
      '<span class="score-seal__value">' + mentor.score + "</span>" +
      '<span class="score-seal__label">/ 100</span>' +
      "</div>" +
      "</li>"
    );
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
})();
