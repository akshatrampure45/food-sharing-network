// Point this at your backend (local FastAPI dev server, or Render/EC2 URL in production)
const API_BASE = "http://localhost:8000";

function authHeader() {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function apiRequest(path, { method = "GET", body = null, auth = false } = {}) {
  const headers = { "Content-Type": "application/json", ...(auth ? authHeader() : {}) };
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

const api = {
  signup: (data) => apiRequest("/auth/signup", { method: "POST", body: data }),
  login: (data) => apiRequest("/auth/login", { method: "POST", body: data }),
  me: () => apiRequest("/auth/me", { auth: true }),
  createListing: (data) => apiRequest("/listings/", { method: "POST", body: data, auth: true }),
  listAll: () => apiRequest("/listings/"),
  listNearby: (lat, lng, radiusKm = 5) =>
    apiRequest(`/listings/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`),
  createMatch: (data) => apiRequest("/matches/", { method: "POST", body: data, auth: true }),
};
