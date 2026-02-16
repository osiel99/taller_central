import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ordenesCompraService from "../../services/ordenesCompraService";
import OrdenCompraDetalle from "./OrdenCompraDetalle";

export default function OrdenCompraDetallePage() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const cargar = async () => {
    try {
      setLoading(true);

      // Validación mínima
      const ocId = Number(id);
      if (isNaN(ocId)) {
        setError("ID de orden inválido");
        return;
      }

      const d = await ordenesCompraService.getById(ocId);
      setData(d);
    } catch (err) {
      console.error("Error cargando orden de compra:", err);
      setError("No se pudo cargar la orden de compra");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargar();
  }, [id]);

  if (loading) return <p>Cargando orden de compra...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!data) return <p>No se encontró la orden de compra.</p>;

  return <OrdenCompraDetalle data={data} />;
}
