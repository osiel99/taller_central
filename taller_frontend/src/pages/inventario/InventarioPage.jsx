import { useEffect, useState } from "react";
import api from "../../services/api";

export default function InventarioPage() {
  const [inventario, setInventario] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const cargarInventario = async () => {
    try {
      setLoading(true);
      const res = await api.get("/inventario/");
      setInventario(res.data);
    } catch (err) {
      console.error("Error cargando inventario:", err);
      setError("No se pudo cargar el inventario");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarInventario();
  }, []);

  if (loading) return <p>Cargando inventario...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="container">
      <h1>Inventario</h1>

      <table className="table table-striped mt-4">
        <thead>
          <tr>
            <th>Clave</th>
            <th>Descripción</th>
            <th>Unidad</th>
            <th>Existencia</th>
            <th>Precio Promedio</th>
            <th>Último Movimiento</th>
          </tr>
        </thead>

        <tbody>
          {inventario.length === 0 && (
            <tr>
              <td colSpan="6" className="text-center py-4 text-gray-500">
                No hay artículos en inventario
              </td>
            </tr>
          )}

          {inventario.map((item) => (
            <tr key={item.clave}>
              <td>{item.clave}</td>
              <td>{item.descripcion}</td>
              <td>{item.unidad}</td>
              <td>{item.existencia}</td>
              <td>
                {item.precio_promedio != null
                  ? `$${item.precio_promedio.toFixed(2)}`
                  : "N/A"}
              </td>
              <td>{item.ultimo_movimiento || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
