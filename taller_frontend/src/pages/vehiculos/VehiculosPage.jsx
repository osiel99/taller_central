import { useEffect, useState } from "react";
import VehiculosTable from "../../components/vehiculos/VehiculosTable";
import VehiculoForm from "../../components/vehiculos/VehiculoForm";
import vehiculosService from "../../services/vehiculosService";

export default function VehiculosPage() {
  const [vehiculos, setVehiculos] = useState([]);
  const [modo, setModo] = useState("lista"); // lista | crear | editar
  const [vehiculoEdit, setVehiculoEdit] = useState(null);
  const [loading, setLoading] = useState(true);

  const cargarVehiculos = async () => {
    try {
      setLoading(true);
      const data = await vehiculosService.getAll();
      setVehiculos(data);
    } catch (err) {
      console.error("Error cargando vehículos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarVehiculos();
  }, []);

  return (
    <div>
      {/* Loader */}
      {loading && <p className="text-gray-500 mb-4">Cargando vehículos...</p>}

      {/* LISTA */}
      {modo === "lista" && !loading && (
        <VehiculosTable
          vehiculos={vehiculos}
          onCrear={() => {
            setVehiculoEdit(null); // Limpia datos previos
            setModo("crear");
          }}
          onEditar={(v) => {
            setVehiculoEdit(v);
            setModo("editar");
          }}
          onEliminar={async (id) => {
            try {
              await vehiculosService.remove(id);
              cargarVehiculos();
            } catch (err) {
              console.error("Error eliminando vehículo:", err);
            }
          }}
        />
      )}

      {/* FORMULARIO (crear o editar) */}
      {(modo === "crear" || modo === "editar") && (
        <VehiculoForm
          initialData={modo === "editar" ? vehiculoEdit : null}
          onCancel={() => {
            setVehiculoEdit(null);
            setModo("lista");
          }}
          onSuccess={() => {
            cargarVehiculos();
            setVehiculoEdit(null);
            setModo("lista");
          }}
        />
      )}
    </div>
  );
}
