import { useState, useEffect } from "react";
import proveedoresService from "../../services/proveedoresService";

export default function ProveedorForm({ initialData, onCancel, onSuccess }) {
  const [form, setForm] = useState({
    nombre: "",
    rfc: "",
    telefono: "",
    direccion: "",
    condiciones_pago: "",
  });

  const [loading, setLoading] = useState(false);

  // Cargar datos iniciales cuando se edita
  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validaciones mínimas
    if (!form.nombre.trim()) {
      alert("Ingrese el nombre del proveedor");
      return;
    }
    if (!form.rfc.trim()) {
      alert("Ingrese el RFC");
      return;
    }

    try {
      setLoading(true);

      if (initialData) {
        await proveedoresService.update(initialData.id, form);
      } else {
        await proveedoresService.create(form);
      }

      onSuccess();
    } catch (err) {
      console.error("Error guardando proveedor:", err);
      alert("Ocurrió un error al guardar el proveedor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-xl font-bold mb-4">
        {initialData ? "Editar proveedor" : "Nuevo proveedor"}
      </h2>

      <form onSubmit={handleSubmit} className="grid gap-4">
        <input
          name="nombre"
          value={form.nombre}
          onChange={handleChange}
          placeholder="Nombre del proveedor"
        />

        <input
          name="rfc"
          value={form.rfc}
          onChange={handleChange}
          placeholder="RFC"
        />

        <input
          name="telefono"
          value={form.telefono}
          onChange={handleChange}
          placeholder="Teléfono"
        />

        <input
          name="direccion"
          value={form.direccion}
          onChange={handleChange}
          placeholder="Dirección"
        />

        <input
          name="condiciones_pago"
          value={form.condiciones_pago}
          onChange={handleChange}
          placeholder="Condiciones de pago"
        />

        <div className="flex gap-2">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Guardando..." : "Guardar"}
          </button>

          <button type="button" className="btn-secondary" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}
