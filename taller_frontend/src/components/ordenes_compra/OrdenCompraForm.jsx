import { useEffect, useState } from "react";
import ordenesCompraService from "../../services/ordenesCompraService";
import refaccionesService from "../../services/refaccionesService";

export default function OrdenCompraForm({ onCancel, onSuccess }) {
  const [refacciones, setRefacciones] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    proveedor: "",
    factura: "",
    detalles: [],
  });

  useEffect(() => {
    const cargar = async () => {
      try {
        setLoading(true);
        const data = await refaccionesService.getAll();
        setRefacciones(data);
      } catch (err) {
        console.error("Error cargando refacciones:", err);
      } finally {
        setLoading(false);
      }
    };
    cargar();
  }, []);

  const agregarDetalle = () => {
    setForm({
      ...form,
      detalles: [
        ...form.detalles,
        { refaccion_id: "", cantidad: 1, precio_unitario: 0 },
      ],
    });
  };

  const actualizarDetalle = (i, campo, valor) => {
    const nuevos = [...form.detalles];
    nuevos[i][campo] = valor;
    setForm({ ...form, detalles: nuevos });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validaciones mínimas
    if (!form.proveedor.trim()) {
      alert("Ingrese el proveedor");
      return;
    }

    if (form.detalles.length === 0) {
      alert("Agregue al menos una partida");
      return;
    }

    if (form.detalles.some((d) => !d.refaccion_id)) {
      alert("Seleccione una refacción en todas las partidas");
      return;
    }

    // Construcción del payload
    const payload = {
      proveedor: form.proveedor,
      factura: form.factura || null,
      detalles: form.detalles.map((d) => ({
        refaccion_id: Number(d.refaccion_id),
        cantidad: Number(d.cantidad),
        precio_unitario: Number(d.precio_unitario),
      })),
    };

    try {
      await ordenesCompraService.create(payload);
      onSuccess();
    } catch (err) {
      console.error("Error guardando orden de compra:", err);
      alert("Ocurrió un error al guardar la orden de compra");
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-xl font-bold mb-4">Nueva Orden de Compra</h2>

      {loading && <p className="text-gray-500">Cargando refacciones...</p>}

      {!loading && (
        <form onSubmit={handleSubmit} className="grid gap-4">

          {/* PROVEEDOR */}
          <input
            placeholder="Proveedor"
            value={form.proveedor}
            onChange={(e) => setForm({ ...form, proveedor: e.target.value })}
          />

          {/* FACTURA */}
          <input
            placeholder="Factura (opcional)"
            value={form.factura}
            onChange={(e) => setForm({ ...form, factura: e.target.value })}
          />

          <h3 className="font-bold">Detalles</h3>

          {form.detalles.map((d, i) => (
            <div key={i} className="grid grid-cols-3 gap-2">

              {/* REFACCIÓN */}
              <select
                value={d.refaccion_id}
                onChange={(e) =>
                  actualizarDetalle(i, "refaccion_id", Number(e.target.value))
                }
              >
                <option value="">Seleccione refacción</option>
                {refacciones.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.descripcion}
                  </option>
                ))}
              </select>

              {/* CANTIDAD */}
              <input
                type="number"
                value={d.cantidad}
                onChange={(e) =>
                  actualizarDetalle(i, "cantidad", Number(e.target.value))
                }
                placeholder="Cantidad"
              />

              {/* PRECIO UNITARIO */}
              <input
                type="number"
                value={d.precio_unitario}
                onChange={(e) =>
                  actualizarDetalle(i, "precio_unitario", Number(e.target.value))
                }
                placeholder="Precio unitario"
              />
            </div>
          ))}

          <button type="button" className="btn-secondary" onClick={agregarDetalle}>
            + Agregar detalle
          </button>

          <div className="flex gap-2 mt-4">
            <button type="submit" className="btn-primary">Guardar</button>
            <button type="button" className="btn-secondary" onClick={onCancel}>
              Cancelar
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
