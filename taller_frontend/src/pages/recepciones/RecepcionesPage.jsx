import { useEffect, useState } from "react";
import recepcionesService from "../../services/recepcionesService";
import RecepcionesTable from "../../components/recepciones/RecepcionesTable";
import RecepcionForm from "../../components/recepciones/RecepcionForm";

export default function RecepcionesPage() {
  const [recepciones, setRecepciones] = useState([]);
  const [modo, setModo] = useState("lista"); // lista | crear
  const [loading, setLoading] = useState(true);

  const cargarRecepciones = async () => {
    try {
      setLoading(true);
      const data = await recepcionesService.getAll();
      setRecepciones(data);
    } catch (err) {
      console.error("Error cargando recepciones:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarRecepciones();
  }, []);

  return (
    <div>
      {/* Loader */}
      {loading && <p className="text-gray-500 mb-4">Cargando recepciones...</p>}

      {/* LISTA */}
      {modo === "lista" && !loading && (
        <RecepcionesTable
          recepciones={recepciones}
          onCrear={() => setModo("crear")}
        />
      )}

      {/* FORMULARIO */}
      {modo === "crear" && (
        <RecepcionForm
          onCancel={() => setModo("lista")}
          onSuccess={() => {
            cargarRecepciones();
            setModo("lista");
          }}
        />
      )}
    </div>
  );
}
