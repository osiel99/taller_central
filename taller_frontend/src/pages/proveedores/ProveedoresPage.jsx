import { useEffect, useState } from "react";
import proveedoresService from "../../services/proveedoresService";
import ProveedoresTable from "../../components/proveedores/ProveedoresTable";
import ProveedorForm from "../../components/proveedores/ProveedorForm";

export default function ProveedoresPage() {
  const [proveedores, setProveedores] = useState([]);
  const [modo, setModo] = useState("lista"); // lista | crear | editar
  const [proveedorEdit, setProveedorEdit] = useState(null);
  const [loading, setLoading] = useState(true);

  const cargarProveedores = async () => {
    try {
      setLoading(true);
      const data = await proveedoresService.getAll();
      setProveedores(data);
    } catch (err) {
      console.error("Error cargando proveedores:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarProveedores();
  }, []);

  return (
    <div>
      {/* Loader */}
      {loading && <p className="text-gray-500 mb-4">Cargando proveedores...</p>}

      {/* LISTA */}
      {modo === "lista" && !loading && (
        <ProveedoresTable
          proveedores={proveedores}
          onCrear={() => {
            setProveedorEdit(null); // Limpia datos previos
            setModo("crear");
          }}
          onEditar={(p) => {
            setProveedorEdit(p);
            setModo("editar");
          }}
          onEliminar={async (id) => {
            try {
              await proveedoresService.remove(id);
              cargarProveedores();
            } catch (err) {
              console.error("Error eliminando proveedor:", err);
            }
          }}
        />
      )}

      {/* FORMULARIO */}
      {(modo === "crear" || modo === "editar") && (
        <ProveedorForm
          initialData={modo === "editar" ? proveedorEdit : null}
          onCancel={() => {
            setProveedorEdit(null);
            setModo("lista");
          }}
          onSuccess={() => {
            cargarProveedores();
            setProveedorEdit(null);
            setModo("lista");
          }}
        />
      )}
    </div>
  );
}
