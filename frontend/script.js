// ================= EMAILJS INIT =================
// Guarded: if the EmailJS CDN is blocked or slow to load, this must not
// throw and take down the rest of script.js (menu, nav, reveal, etc).
try {
  emailjs.init("Z1p5FINUUPHvQAlZI");
} catch (err) {
  console.warn("EmailJS failed to initialize:", err);
}

// ================= DYNAMIC PROJECTS FETCHING =================
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function fetchProjects() {
  const container = document.querySelector("#projects .project-container");
  if (!container) return;

  try {
    const res = await fetch("/api/projects");
    if (!res.ok) return;
    const projects = await res.json();
    if (!projects || projects.length === 0) return;

    container.innerHTML = projects.map(proj => {
      const isLive = Boolean(proj.live_url && proj.live_url.trim().length > 0);
      const statusClass = isLive ? "project-status is-live" : "project-status";
      const statusText = isLive ? "Live" : "In progress";

      const linkHtml = isLive
        ? `<a href="${escapeHtml(proj.live_url)}" target="_blank" rel="noopener" class="project-link">Live demo</a>`
        : `<span class="project-link is-muted">Coming soon</span>`;

      return `
        <div class="project-card">
          <div class="project-thumb">
            <img src="${escapeHtml(proj.image_url)}" alt="${escapeHtml(proj.title)}" loading="lazy">
            <span class="${statusClass}">${statusText}</span>
          </div>
          <div class="project-body">
            <h3>${escapeHtml(proj.title)}</h3>
            <p>${escapeHtml(proj.description)}</p>
            ${linkHtml}
          </div>
        </div>
      `;
    }).join("");
  } catch (err) {
    console.warn("Could not load dynamic projects from backend; retaining default portfolio structure:", err);
  }
}

// Load dynamic projects on page load
document.addEventListener("DOMContentLoaded", fetchProjects);

// ================= CONTACT FORM (POST /api/leads + EmailJS) =================
let form = document.getElementById("contactForm");

if (form) {
  form.addEventListener("submit", async function(e) {
    e.preventDefault();

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let message = document.getElementById("message").value.trim();
    let button = form.querySelector("button");

    if (!name || !email || !message) {
      alert("Please fill all fields!");
      return;
    }

    if (!email.includes("@")) {
      alert("Enter a valid email!");
      return;
    }

    button.innerText = "Sending...";
    button.disabled = true;

    try {
      // 1. Save lead to PostgreSQL via backend FastAPI endpoint
      const response = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, email: email, message: message })
      });

      if (!response.ok) {
        throw new Error("Failed to save lead to database");
      }

      // 2. Dispatch EmailJS notification if available
      if (typeof emailjs !== "undefined") {
        emailjs.send("service_kziwxou", "template_x7jg3r7", {
          name: name,
          email: email,
          message: message
        }).catch(err => {
          console.warn("EmailJS notification failed:", err);
        });
      }

      alert("✅ Message sent successfully!");
      form.reset();
    } catch (err) {
      console.error("Contact form submit error:", err);
      alert("❌ Failed to send message. Please try again or email reywebstudio@email.com directly.");
    } finally {
      button.innerText = "Send Message";
      button.disabled = false;
    }
  });
}

// ================= HAMBURGER MENU =================
const toggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");

if (toggle && navLinks) {
  toggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");

    // change icon
    if (navLinks.classList.contains("active")) {
      toggle.innerHTML = '<i class="fas fa-times"></i>';
    } else {
      toggle.innerHTML = '<i class="fas fa-bars"></i>';
    }
  });

  // close menu when clicking link
  document.querySelectorAll("#nav-links a").forEach(link => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      toggle.innerHTML = '<i class="fas fa-bars"></i>';
    });
  });
}

// ================= HIRE BUTTON =================
function hireMe() {
  window.open("https://mail.google.com/mail/?view=cm&fs=1&to=reywebstudio@email.com&su=Project Inquiry&body=Hi I need a website");
}

// ================= SCROLL REVEAL =================
// Subtle, single-treatment fade-in for section blocks as they enter view.
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealEls = document.querySelectorAll(".reveal");

if (revealEls.length && !prefersReducedMotion && "IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -60px 0px" });

  revealEls.forEach(el => {
    // Only hide the element once we know we can bring it back.
    el.classList.add("reveal-armed");
    revealObserver.observe(el);
  });
}

// ================= ACTIVE NAV LINK =================
const sections = document.querySelectorAll("#hero, #projects, #services, #contact");
const navAnchors = document.querySelectorAll("#nav-links a");

if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        navAnchors.forEach(a => {
          a.classList.toggle("active", a.getAttribute("href") === `#${id}`);
        });
      }
    });
  }, { threshold: 0.5 });

  sections.forEach(section => navObserver.observe(section));
}