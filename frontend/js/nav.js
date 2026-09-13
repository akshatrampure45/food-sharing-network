// Populates the #auth-area slot in the nav: shows a Login button when
// logged out, or a profile icon + dropdown (name/email/role + Logout)
// when logged in. Also reveals/hides any nav links marked with the
// "nav-protected" class (Browse Nearby, Donate Food) so those only ever
// appear once the person is actually signed in — not before.
function initNavAuth(loginHref, homeHref) {
  const slot = document.getElementById("auth-area");
  if (!slot) return;

  const protectedLinks = document.querySelectorAll(".nav-protected");

  const token = localStorage.getItem("access_token");
  if (!token) {
    protectedLinks.forEach((el) => el.setAttribute("hidden", ""));
    slot.innerHTML = `<a class="btn btn-primary btn-sm" href="${loginHref}">Login</a>`;
    return;
  }

  api.me()
    .then((user) => {
      protectedLinks.forEach((el) => el.removeAttribute("hidden"));

      const initial = (user.name || "?").trim().charAt(0).toUpperCase();
      slot.innerHTML = `
        <div class="profile-widget">
          <button class="profile-icon" id="profile-toggle" type="button" aria-haspopup="true" aria-expanded="false">${initial}</button>
          <div class="profile-dropdown" id="profile-dropdown" hidden>
            <div class="profile-name">${user.name}</div>
            <div class="profile-email">${user.email}</div>
            <div class="profile-role">${user.role}</div>
            <button class="btn btn-ghost btn-sm btn-block" id="logout-btn" type="button">Logout</button>
          </div>
        </div>`;

      const toggle = document.getElementById("profile-toggle");
      const dropdown = document.getElementById("profile-dropdown");

      toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        const isHidden = dropdown.hasAttribute("hidden");
        if (isHidden) dropdown.removeAttribute("hidden");
        else dropdown.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", String(isHidden));
      });

      document.addEventListener("click", (e) => {
        if (!slot.contains(e.target)) dropdown.setAttribute("hidden", "");
      });

      document.getElementById("logout-btn").addEventListener("click", () => {
        localStorage.removeItem("access_token");
        window.location.href = homeHref;
      });
    })
    .catch(() => {
      // Token expired or invalid — fall back to showing Login, keep
      // protected links hidden too.
      protectedLinks.forEach((el) => el.setAttribute("hidden", ""));
      localStorage.removeItem("access_token");
      slot.innerHTML = `<a class="btn btn-primary btn-sm" href="${loginHref}">Login</a>`;
    });
}

// Gate a page behind login: if there's no token, redirect immediately to
// the login page (carrying ?next=<this page> so login/signup can send the
// person back to what they actually wanted). Returns false when redirecting
// so the caller can skip running the rest of the page's logic.
function requireAuth(loginHref, currentPage) {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = `${loginHref}?next=${encodeURIComponent(currentPage)}`;
    return false;
  }
  return true;
}
