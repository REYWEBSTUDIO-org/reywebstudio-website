// ================= EMAILJS INIT =================
(function(){
  emailjs.init("Z1p5FINUUPHvQAlZI");
})();

// ================= CONTACT FORM =================
let form = document.getElementById("contactForm");

form.addEventListener("submit", function(e) {
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

  emailjs.send("service_kziwxou", "template_x7jg3r7", {
    name: name,
    email: email,
    message: message
  })
  .then(() => {
    alert("✅ Message sent!");
    form.reset();
  })
  .catch(() => {
    alert("❌ Failed to send");
  })
  .finally(() => {
    button.innerText = "Send Message";
    button.disabled = false;
  });
});

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