import { useEffect, useState } from "react";
import ordenesCompraService from "../../services/ordenesCompraService";
import OrdenesCompraTable from "../../components/ordenes_compra/OrdenesCompraTable";
import OrdenCompraForm from "../../components/ordenes_compra/OrdenCompraForm";
import ImportarOCModal from "../../components/ordenes_compra/ImportarOCModal";

export default function OrdenesCompraPage() {
  const [ordenes, setOrdenes] = useState([]);
  const [modo, setModo] = useState("lista"); // lista | crear
  const [mostrarImportar, setMostrarImportar] = useState(false);

  const cargarOrdenes = async () => {
    const data = await ordenesCompraService.getAll();
    setOrdenes(data);
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  return (
    <div>
      {modo === "lista" && (
        <>
          <div className="flex justify-between mb-4">
            <button className="btn-primary" onClick={() => setModo("crear")}>
              + Nueva Orden
            </button>

            {/* NUEVO BOTÓN PARA IMPORTAR */}
            <button
              className="btn-secondary"
              onClick={() => setMostrarImportar(true)}
            >
              Importar Orden de Compra
            </button>
          </div>

          <OrdenesCompraTable ordenes={ordenes} />
        </>
      )}

      {modo === "crear" && (
        <OrdenCompraForm
          onCancel={() => setModo("lista")}
          onSuccess={() => {
            cargarOrdenes();
            setModo("lista");
          }}
        />
      )}

      {/* MODAL DE IMPORTACIÓN */}
      {mostrarImportar && (
        <ImportarOCModal
          onClose={() => setMostrarImportar(false)}
          onImported={() => {
            setMostrarImportar(false);
            cargarOrdenes();
          }}
        />
      )}
    </div>
  );
}
