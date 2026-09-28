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

  // ✅ Validation
  if (name === "" || email === "" || message === "") {
    alert("Please fill all fields!");
    return;
  }

  if (!email.includes("@")) {
    alert("Enter a valid email!");
    return;
  }

  // 🔄 Loading state
  button.innerText = "Sending...";
  button.disabled = true;

  // 🚀 REAL EMAIL SEND
  emailjs.send("service_kziwxou", "template_x7jg3r7", {
    name: name,
    email: email,
    message: message
  })
  .then(function() {
    alert("✅ Message sent successfully!");
    form.reset();
  })
  .catch(function(error) {
    alert("❌ Failed to send message");
    console.log(error);
  })
  .finally(function() {
    button.innerText = "Send Message";
    button.disabled = false;
  });

});

// ================= HIRE BUTTON =================
function hireMe() {
  window.open("https://mail.google.com/mail/?view=cm&fs=1&to=your@email.com&su=Project Inquiry&body=Hi I need a website");
}