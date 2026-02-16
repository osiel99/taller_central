import { useState } from "react";
import ordenesCompraService from "../../services/ordenesCompraService";

export default function ImportarOCModal({ tipo = "texto", onClose, onImported }) {
  const [contenido, setContenido] = useState("");
  const [archivo, setArchivo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImport = async () => {
    try {
      setLoading(true);

      // Validaciones
      if ((tipo === "excel" || tipo === "pdf") && !archivo) {
        alert("Seleccione un archivo antes de importar");
        setLoading(false);
        return;
      }

      if ((tipo === "texto" || tipo === "json") && !contenido.trim()) {
        alert("Pegue el contenido antes de importar");
        setLoading(false);
        return;
      }

      // Llamadas al backend
      if (tipo === "excel") {
        await ordenesCompraService.importarExcel(archivo);
      } else if (tipo === "pdf") {
        await ordenesCompraService.importarPDF(archivo);
      } else {
        await ordenesCompraService.importar({
          tipo,
          contenido,
        });
      }

      onImported();
    } catch (error) {
      console.error("Error al importar:", error);
      alert("Ocurrió un error al importar la orden de compra");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setContenido("");
    setArchivo(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-lg w-full max-w-xl">
        <h2 className="text-xl font-bold mb-4">
          Importar Orden de Compra ({tipo.toUpperCase()})
        </h2>

        {/* MODO TEXTO / JSON */}
        {(tipo === "texto" || tipo === "json") && (
          <textarea
            className="w-full h-48 border p-2"
            placeholder="Pega aquí el contenido del PDF o JSON"
            value={contenido}
            onChange={(e) => setContenido(e.target.value)}
          />
        )}

        {/* MODO ARCHIVO */}
        {(tipo === "excel" || tipo === "pdf") && (
          <input
            type="file"
            accept={tipo === "excel" ? ".xlsx" : ".pdf"}
            onChange={(e) => setArchivo(e.target.files[0])}
            className="w-full border p-2"
          />
        )}

        <div className="flex justify-end gap-2 mt-4">
          <button className="btn-secondary" onClick={handleClose} disabled={loading}>
            Cancelar
          </button>
          <button className="btn-primary" onClick={handleImport} disabled={loading}>
            {loading ? "Importando..." : "Importar"}
          </button>
        </div>
      </div>
    </div>
  );
}
