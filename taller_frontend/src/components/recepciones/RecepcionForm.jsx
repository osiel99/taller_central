import { useEffect, useState } from "react";
import recepcionesService from "../../services/recepcionesService";
import ordenesCompraService from "../../services/ordenesCompraService";
import refaccionesService from "../../services/refaccionesService";

export default function RecepcionForm({ onCancel, onSuccess }) {
  const [ordenes, setOrdenes] = useState([]);
  const [refacciones, setRefacciones] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    oc_id: "",
    recibido_por: "",
    detalles: [],
  });

  useEffect(() => {
    const cargar = async () => {
      try {
        setLoading(true);
        const ocs = await ordenesCompraService.getAll();
        const refs = await refaccionesService.getAll();
        setOrdenes(ocs);
        setRefacciones(refs);
      } catch (err) {
        console.error("Error cargando datos:", err);
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
        { refaccion_id: "", cantidad_recibida: 1, cantidad_oc: null },
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
    if (!form.oc_id) {
      alert("Seleccione una Orden de Compra");
      return;
    }
    if (!form.recibido_por.trim()) {
      alert("Ingrese quién recibió la mercancía");
      return;
    }
    if (form.detalles.length === 0) {
      alert("Agregue al menos un detalle");
      return;
    }
    if (form.detalles.some((d) => !d.refaccion_id)) {
      alert("Seleccione una refacción en todos los detalles");
      return;
    }

    // Construcción del payload
    const payload = {
      oc_id: Number(form.oc_id),
      recibido_por: form.recibido_por,
      detalles: form.detalles.map((d) => ({
        refaccion_id: Number(d.refaccion_id),
        cantidad_recibida: Number(d.cantidad_recibida),
        cantidad_oc: d.cantidad_oc === null ? null : Number(d.cantidad_oc),
      })),
    };

    try {
      await recepcionesService.create(payload);
      onSuccess();
    } catch (err) {
      console.error("Error guardando recepción:", err);
      alert("Ocurrió un error al guardar la recepción");
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-xl font-bold mb-4">Nueva Recepción</h2>

      {loading && <p className="text-gray-500">Cargando datos...</p>}

      {!loading && (
        <form onSubmit={handleSubmit} className="grid gap-4">

          {/* ORDEN DE COMPRA */}
          <select
            value={form.oc_id}
            onChange={(e) =>
              setForm({ ...form, oc_id: Number(e.target.value) })
            }
          >
            <option value="">Seleccione Orden de Compra</option>
            {ordenes.map((oc) => (
              <option key={oc.id} value={oc.id}>
                OC #{oc.id} — {oc.proveedor}
              </option>
            ))}
          </select>

          {/* RECIBIDO POR */}
          <input
            placeholder="Recibido por"
            value={form.recibido_por}
            onChange={(e) =>
              setForm({ ...form, recibido_por: e.target.value })
            }
          />

          <h3 className="font-bold">Detalles recibidos</h3>

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

              {/* CANTIDAD RECIBIDA */}
              <input
                type="number"
                value={d.cantidad_recibida}
                onChange={(e) =>
                  actualizarDetalle(
                    i,
                    "cantidad_recibida",
                    Number(e.target.value)
                  )
                }
                placeholder="Cantidad recibida"
              />

              {/* CANTIDAD OC (OPCIONAL) */}
              <input
                type="number"
                value={d.cantidad_oc ?? ""}
                onChange={(e) =>
                  actualizarDetalle(
                    i,
                    "cantidad_oc",
                    e.target.value === "" ? null : Number(e.target.value)
                  )
                }
                placeholder="Cantidad en OC (opcional)"
              />
            </div>
          ))}

          <button
            type="button"
            className="btn-secondary"
            onClick={agregarDetalle}
          >
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
