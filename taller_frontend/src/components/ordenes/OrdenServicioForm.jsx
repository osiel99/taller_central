import { useState, useEffect } from "react";
import ordenesServicioService from "../../services/ordenesServicioService";
import vehiculosService from "../../services/vehiculosService";

export default function OrdenServicioForm({ initialData, onCancel, onSuccess }) {
  const [vehiculos, setVehiculos] = useState([]);
  const [loadingVehiculos, setLoadingVehiculos] = useState(true);

  const [form, setForm] = useState(
    initialData || {
      vehiculo_id: "",
      fecha: "",
      descripcion: "",
      estatus: "Pendiente",
    }
  );

  useEffect(() => {
    const cargarVehiculos = async () => {
      try {
        setLoadingVehiculos(true);
        const data = await vehiculosService.getAll();
        setVehiculos(data);
      } catch (err) {
        console.error("Error cargando vehículos:", err);
      } finally {
        setLoadingVehiculos(false);
      }
    };

    cargarVehiculos();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validación mínima
    if (!form.vehiculo_id) {
      alert("Seleccione un vehículo");
      return;
    }
    if (!form.fecha) {
      alert("Seleccione una fecha");
      return;
    }

    const payload = {
      ...form,
      vehiculo_id: Number(form.vehiculo_id),
    };

    try {
      if (initialData) {
        await ordenesServicioService.update(initialData.id, payload);
      } else {
        await ordenesServicioService.create(payload);
      }

      onSuccess();
    } catch (err) {
      console.error("Error guardando orden:", err);
      alert("Ocurrió un error al guardar la orden");
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-xl font-bold mb-4">
        {initialData ? "Editar Orden" : "Nueva Orden de Servicio"}
      </h2>

      <form onSubmit={handleSubmit} className="grid gap-4">

        {/* Vehículos */}
        {loadingVehiculos ? (
          <p className="text-gray-500">Cargando vehículos...</p>
        ) : (
          <select name="vehiculo_id" value={form.vehiculo_id} onChange={handleChange}>
            <option value="">Seleccione un vehículo</option>
            {vehiculos.map((v) => (
              <option key={v.id} value={v.id}>
                {v.placa} - {v.marca} {v.modelo}
              </option>
            ))}
          </select>
        )}

        {/* Fecha */}
        <input
          type="date"
          name="fecha"
          value={form.fecha}
          onChange={handleChange}
        />

        {/* Descripción */}
        <textarea
          name="descripcion"
          value={form.descripcion}
          onChange={handleChange}
          placeholder="Descripción del servicio"
        />

        {/* Estatus */}
        <select name="estatus" value={form.estatus} onChange={handleChange}>
          <option value="Pendiente">Pendiente</option>
          <option value="En proceso">En proceso</option>
          <option value="Finalizado">Finalizado</option>
        </select>

        <div className="flex gap-2">
          <button type="submit" className="btn-primary">Guardar</button>
          <button type="button" className="btn-secondary" onClick={onCancel}>Cancelar</button>
        </div>
      </form>
    </div>
  );
}
