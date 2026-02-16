import axios from "axios";

const api = axios.create({
  baseURL: "http://taller_backend:8000/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor de errores global
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);

    let msg = "Error en la solicitud";

    const detail = error.response?.data?.detail;

    if (Array.isArray(detail)) {
      msg = detail.map((d) => d.msg).join("\n");
    } else if (typeof detail === "string") {
      msg = detail;
    } else if (!error.response) {
      msg = "No se pudo conectar con el servidor";
    }

    alert(msg);
    return Promise.reject(error);
  }
);

export default api;
