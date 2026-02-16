import { useEffect, useState } from "react";
import ordenesServicioService from "../../services/ordenesServicioService";
import OrdenesServicioTable from "../../components/ordenes/OrdenesServicioTable";
import OrdenServicioForm from "../../components/ordenes/OrdenServicioForm";

export default function OrdenesServicioPage() {
  const [ordenes, setOrdenes] = useState([]);
  const [modo, setModo] = useState("lista"); // lista | crear | editar
  const [ordenEdit, setOrdenEdit] = useState(null);
  const [loading, setLoading] = useState(true);

  const cargarOrdenes = async () => {
    try {
      setLoading(true);
      const data = await ordenesServicioService.getAll();
      setOrdenes(data);
    } catch (err) {
      console.error("Error cargando órdenes de servicio:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  return (
    <div>
      {/* Loader */}
      {loading && <p className="text-gray-500 mb-4">Cargando órdenes...</p>}

      {/* LISTA */}
      {modo === "lista" && !loading && (
        <OrdenesServicioTable
          ordenes={ordenes}
          onCrear={() => {
            setOrdenEdit(null); // Limpia datos previos
            setModo("crear");
          }}
          onEditar={(o) => {
            setOrdenEdit(o);
            setModo("editar");
          }}
          onEliminar={async (id) => {
            try {
              await ordenesServicioService.remove(id);
              cargarOrdenes();
            } catch (err) {
              console.error("Error eliminando orden:", err);
            }
          }}
        />
      )}

      {/* FORMULARIO */}
      {(modo === "crear" || modo === "editar") && (
        <OrdenServicioForm
          initialData={modo === "editar" ? ordenEdit : null}
          onCancel={() => {
            setOrdenEdit(null);
            setModo("lista");
          }}
          onSuccess={() => {
            cargarOrdenes();
            setOrdenEdit(null);
            setModo("lista");
          }}
        />
      )}
    </div>
  );
}
