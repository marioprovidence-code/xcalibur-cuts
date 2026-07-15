(function () {
  "use strict";

  // Navbar scroll state
  const nav = document.getElementById("nav");
  const onScroll = function () {
    if (window.scrollY > 30) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  };
  window.addEventListener("scroll", onScroll);
  onScroll();

  // Mobile menu
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
      });
    });
  }

  // Footer year
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Booking form (demo only — no backend)
  const form = document.getElementById("bookingForm");
  const note = document.getElementById("bookingNote");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = form.querySelector("#name").value.trim();
      const service = form.querySelector("#service").value;
      const date = form.querySelector("#date").value;
      if (!name || !service || !date) {
        note.textContent = "Please complete all fields to confirm.";
        return;
      }
      note.textContent =
        "Thanks, " + name + "! Your " + service + " on " + date + " is requested. We'll call to confirm.";
      form.reset();
    });
  }
  // Enroll form -> posts to endpoint (Google Apps Script) which emails the owner
  const ENROLL_ENDPOINT = ""; // paste your Google Apps Script web app URL here
  const enroll = document.getElementById("enrollForm");
  const enrollNote = document.getElementById("enrollNote");
  if (enroll) {
    enroll.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = enroll.querySelector("#eName").value.trim();
      const phone = enroll.querySelector("#ePhone").value.trim();
      const course = enroll.querySelector("#eCourse").value;
      if (!name || !course) {
        enrollNote.textContent = "Please complete all fields to enroll.";
        return;
      }
      const payload = new URLSearchParams({ name: name, phone: phone, course: course });
      if (ENROLL_ENDPOINT) {
        fetch(ENROLL_ENDPOINT, { method: "POST", body: payload }).catch(function () {});
      }
      enrollNote.textContent =
        "Thanks, " + name + "! Your interest in \"" + course + "\" is received. We'll contact you with next steps.";
      enroll.reset();
    });
  }
})();
