// Reads ?next=<page> from the URL so login/signup can send the person back
// to whatever protected page (browse.html or donate.html) sent them here.
// Restricted to a known allowlist so this can't be abused as an open redirect.
function getNextDestination() {
  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");
  const allowed = ["browse.html", "donate.html"];
  return allowed.includes(next) ? next : "browse.html";
}

async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  try {
    const { access_token } = await api.login({ email, password });
    localStorage.setItem("access_token", access_token);
    window.location.href = getNextDestination();
  } catch (err) {
    document.getElementById("error-msg").textContent = err.message;
  }
}

async function handleSignup(event) {
  event.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const payload = {
    name: document.getElementById("name").value,
    email,
    password,
    role: document.getElementById("role").value,
  };
  try {
    await api.signup(payload);
    // Signup doesn't return a token — log in immediately after so the
    // person lands inside the app instead of back at the login form.
    const { access_token } = await api.login({ email, password });
    localStorage.setItem("access_token", access_token);
    window.location.href = getNextDestination();
  } catch (err) {
    document.getElementById("error-msg").textContent = err.message;
  }
}

// Preserve ?next=... when the person switches between the login and
// signup forms, so the original destination survives that detour too.
document.addEventListener("DOMContentLoaded", () => {
  const search = window.location.search;
  if (!search) return;
  document.querySelectorAll(".auth-switch a").forEach((a) => {
    a.href = a.getAttribute("href") + search;
  });
});
