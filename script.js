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
  // Enroll form -> posts to Web3Forms (free) which emails the owner
  const ENROLL_ENDPOINT = "https://api.web3forms.com/submit";
  const WEB3_KEY = "adc05c72-d4fa-4788-9611-979119dc54d6"; // free Web3Forms access key
  const enroll = document.getElementById("enrollForm");
  const enrollNote = document.getElementById("enrollNote");
  if (enroll) {
    enroll.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = enroll.querySelector("#eName").value.trim();
      const phone = enroll.querySelector("#ePhone").value.trim();
      const email = enroll.querySelector("#eEmail").value.trim();
      const course = enroll.querySelector("#eCourse").value;
      if (!name || !email || !course) {
        enrollNote.textContent = "Please complete all fields to enroll.";
        return;
      }
      const payload = new URLSearchParams({
        access_key: WEB3_KEY,
        subject: "New Course Enrollment - Xcalibur Cuts",
        from_name: "Xcalibur Cuts Website",
        name: name, phone: phone, email: email, course: course
      });
      if (ENROLL_ENDPOINT && WEB3_KEY) {
        fetch(ENROLL_ENDPOINT, { method: "POST", body: payload }).catch(function () {});
      }
      enrollNote.textContent =
        "Thanks, " + name + "! Your interest in \"" + course + "\" is received. We'll contact you with next steps.";
      enroll.reset();
    });
  }

  // Share button (native share sheet, copy-link fallback)
  const shareBtn = document.getElementById("shareBtn");
  const shareNote = document.getElementById("shareNote");
  if (shareBtn) {
    shareBtn.addEventListener("click", async function () {
      const data = {
        title: "Xcalibur Cuts Barber Salon",
        text: "Check out Xcalibur Cuts Barber Salon!",
        url: "https://marioprovidence-code.github.io/xcalibur-cuts/"
      };
      if (navigator.share) {
        try {
          await navigator.share(data);
        } catch (e) { /* user cancelled */ }
      } else if (navigator.clipboard) {
        try {
          await navigator.clipboard.writeText(data.url);
          if (shareNote) shareNote.textContent = "Link copied to clipboard!";
        } catch (e) {
          if (shareNote) shareNote.textContent = "Could not copy link.";
        }
      }
    });
  }

  // PWA: register service worker + install prompt
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("sw.js").catch(function () {});
    });
  }
  let deferredPrompt = null;
  const installBtn = document.getElementById("installAppBtn");
  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    if (installBtn) installBtn.hidden = false;
  });
  if (installBtn) {
    installBtn.addEventListener("click", async function () {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
      installBtn.hidden = true;
    });
  }
  window.addEventListener("appinstalled", function () {
    if (installBtn) installBtn.hidden = true;
  });

  // Gallery lightbox
  const lb = document.getElementById("lightbox");
  const lbContent = document.getElementById("lbContent");
  const lbClose = document.getElementById("lbClose");
  if (lb && lbContent) {
    document.querySelectorAll(".gallery__grid .tile img, .gallery__grid .tile video").forEach(function (el) {
      el.style.cursor = "zoom-in";
      el.addEventListener("click", function () {
        const clone = el.cloneNode(true);
        if (clone.tagName === "VIDEO") {
          clone.setAttribute("controls", "");
          clone.removeAttribute("muted");
          clone.autoplay = true;
          clone.loop = true;
        }
        lbContent.innerHTML = "";
        lbContent.appendChild(clone);
        lb.classList.add("open");
        lb.setAttribute("aria-hidden", "false");
      });
    });
    function closeLb() {
      lb.classList.remove("open");
      lb.setAttribute("aria-hidden", "true");
      lbContent.innerHTML = "";
    }
    if (lbClose) lbClose.addEventListener("click", closeLb);
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLb(); });
  }
})();
