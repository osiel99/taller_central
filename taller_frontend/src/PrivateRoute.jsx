import { Navigate } from "react-router-dom";
import { isTokenValid } from "../services/authService";

export default function PrivateRoute({ children }) {
  const tokenEsValido = isTokenValid();

  if (!tokenEsValido) {
    return <Navigate to="/" replace />;
  }

  return children;
}
