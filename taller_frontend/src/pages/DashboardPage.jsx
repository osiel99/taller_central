import { useEffect, useState } from "react";
import api from "../services/api";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const cargarDashboard = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No hay token, usuario no autenticado");
        return;
      }

      const res = await api.get("/dashboard/general", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setData(res.data);
    } catch (err) {
      console.error("Error cargando dashboard:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarDashboard();
  }, []);

  return (
    <div>
      <h1>Dashboard General</h1>

      {loading && <p>Cargando...</p>}

      {data && (
        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          <div style={{
            background: "#e2e8f0",
            padding: "20px",
            borderRadius: "8px",
            width: "200px"
          }}>
            <h3>Vehículos</h3>
            <p>{data.total_vehiculos}</p>
          </div>

          <div style={{
            background: "#e2e8f0",
            padding: "20px",
            borderRadius: "8px",
            width: "200px"
          }}>
            <h3>Órdenes activas</h3>
            <p>{data.ordenes_activas}</p>
          </div>

          <div style={{
            background: "#e2e8f0",
            padding: "20px",
            borderRadius: "8px",
            width: "200px"
          }}>
            <h3>Refacciones bajas</h3>
            <p>{data.refacciones_bajo_inventario}</p>
          </div>
        </div>
      )}
    </div>
  );
}
