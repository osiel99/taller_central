import api from "./api";

// === LOGIN ===
export async function loginRequest(username, password) {
  const res = await api.post("/auth/login", {
    username,
    password,
  });

  return res.data; // { access_token, token_type }
}

// === GUARDAR TOKEN ===
export function saveToken(token) {
  localStorage.setItem("token", token);
}

// === VALIDAR TOKEN ===
export function isTokenValid() {
  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp > now;
  } catch {
    return false;
  }
}

// === CERRAR SESIÓN ===
export function logout() {
  localStorage.removeItem("token");
}

