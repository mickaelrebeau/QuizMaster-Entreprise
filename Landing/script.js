AOS.init({
  duration: 800,
  once: true,
  offset: 100,
});

const demoModal = document.getElementById("demo-modal");
const preinscriptionModal = document.getElementById("preinscription-modal");
const closeButtons = document.querySelectorAll(".close");

const API_BASE_URL = "https://quizmaster-landing-backend.up.railway.app";

function openDemoModal() {
  demoModal.style.display = "flex";
  document.body.style.overflow = "hidden";
}

function openPreinscriptionModal() {
  preinscriptionModal.style.display = "flex";
  document.body.style.overflow = "hidden";
}

function closeModal(modal) {
  modal.style.display = "none";
  document.body.style.overflow = "auto";
}

closeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const modal = button.closest(".modal");
    closeModal(modal);
  });
});

window.addEventListener("click", (e) => {
  if (e.target === demoModal) {
    closeModal(demoModal);
  }
  if (e.target === preinscriptionModal) {
    closeModal(preinscriptionModal);
  }
});

const demoForm = document.getElementById("demo-form");
const preinscriptionForm = document.getElementById("preinscription-form");
const contactForm = document.getElementById("contact-form");

async function handleFormSubmit(form, endpoint) {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  const submitButton = form.querySelector('button[type="submit"]');
  const originalText = submitButton.innerHTML;
  submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi...';
  submitButton.disabled = true;

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      showSuccessMessage(
        result.message || "Votre message a été envoyé avec succès !"
      );
      form.reset();
      if (form.closest(".modal")) {
        closeModal(form.closest(".modal"));
      }
    } else {
      const errorData = await response.json();
      throw new Error(
        errorData.error || "Erreur lors de l'envoi du formulaire"
      );
    }
  } catch (error) {
    showErrorMessage(
      error.message || "Une erreur est survenue. Veuillez réessayer."
    );
    console.error("Erreur:", error);
  } finally {
    submitButton.innerHTML = originalText;
    submitButton.disabled = false;
  }
}

function showSuccessMessage(message) {
  const toast = document.createElement("div");
  toast.className = "toast success";
  toast.innerHTML = `
    <i class="fas fa-check-circle"></i>
    <span>${message}</span>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("show");
  }, 100);

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

function showErrorMessage(message) {
  const toast = document.createElement("div");
  toast.className = "toast error";
  toast.innerHTML = `
    <i class="fas fa-exclamation-circle"></i>
    <span>${message}</span>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("show");
  }, 100);

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 5000);
}

demoForm.addEventListener("submit", (e) => {
  e.preventDefault();
  handleFormSubmit(demoForm, "/api/demo");
});

preinscriptionForm.addEventListener("submit", (e) => {
  e.preventDefault();
  handleFormSubmit(preinscriptionForm, "/api/preinscription");
});

contactForm.addEventListener("submit", (e) => {
  e.preventDefault();
  handleFormSubmit(contactForm, "/api/contact");
});

const header = document.querySelector("header");
let lastScroll = 0;

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll <= 0) {
    header.classList.remove("scroll-up");
    return;
  }

  if (currentScroll > lastScroll && !header.classList.contains("scroll-down")) {
    header.classList.remove("scroll-up");
    header.classList.add("scroll-down");
  } else if (
    currentScroll < lastScroll &&
    header.classList.contains("scroll-down")
  ) {
    header.classList.remove("scroll-down");
    header.classList.add("scroll-up");
  }
  lastScroll = currentScroll;
});

const stats = document.querySelectorAll(".stat-number");
let animated = false;

function animateStats() {
  if (animated) return;

  stats.forEach((stat) => {
    const target = parseInt(stat.textContent);
    let current = 0;
    const increment = target / 50;
    const duration = 2000;
    const interval = duration / 50;

    const counter = setInterval(() => {
      current += increment;
      if (current >= target) {
        stat.textContent = target + (stat.textContent.includes("%") ? "%" : "");
        clearInterval(counter);
      } else {
        stat.textContent =
          Math.floor(current) + (stat.textContent.includes("%") ? "%" : "");
      }
    }, interval);
  });

  animated = true;
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateStats();
      }
    });
  },
  { threshold: 0.5 }
);

const statsSection = document.querySelector(".hero-stats");
if (statsSection) {
  observer.observe(statsSection);
}

const observerOptions = {
  threshold: 0.1,
};

const observerAnimation = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("animate");
    }
  });
}, observerOptions);

document.querySelectorAll(".feature-card, .pricing-card").forEach((el) => {
  observerAnimation.observe(el);
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
