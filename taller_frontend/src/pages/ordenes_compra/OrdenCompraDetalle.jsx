export default function OrdenCompraDetalle({ data }) {
  const oc = data.orden_compra;
  const recepciones = data.recepciones || [];
  const diferencias = data.diferencias || [];

  const detalles = oc.detalles || [];

  const subtotal = detalles.reduce(
    (acc, d) => acc + d.cantidad * (d.precio_unitario || 0),
    0
  );
  const iva = subtotal * 0.16;
  const total = subtotal + iva;

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-4">
        Orden de Compra #{oc.id}
      </h2>

      {/* DATOS GENERALES */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div><strong>Proveedor:</strong> {oc.proveedor}</div>
        <div>
          <strong>Fecha:</strong>{" "}
          {oc.fecha_oc ? new Date(oc.fecha_oc).toLocaleDateString() : "—"}
        </div>
        <div><strong>Factura:</strong> {oc.factura || "—"}</div>
        <div><strong>Estado:</strong> {oc.estado}</div>
      </div>

      {/* DETALLES */}
      <h3 className="text-xl font-bold mb-2">Partidas</h3>

      {detalles.length === 0 && (
        <p className="text-gray-500 mb-4">No hay partidas registradas.</p>
      )}

      {detalles.length > 0 && (
        <table className="table mb-6">
          <thead>
            <tr>
              <th>Clave</th>
              <th>Descripción</th>
              <th>Unidad</th>
              <th>Cantidad</th>
              <th>Precio</th>
              <th>Importe</th>
            </tr>
          </thead>
          <tbody>
            {detalles.map((d) => (
              <tr key={d.id}>
                <td>{d.refaccion?.clave || "—"}</td>
                <td>{d.refaccion?.descripcion || "—"}</td>
                <td>{d.refaccion?.unidad_medida || "—"}</td>
                <td>{d.cantidad}</td>
                <td>${d.precio_unitario?.toFixed(2) || "0.00"}</td>
                <td>${(d.cantidad * (d.precio_unitario || 0)).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* TOTALES */}
      <div className="text-right mb-6">
        <p><strong>Subtotal:</strong> ${subtotal.toFixed(2)}</p>
        <p><strong>IVA (16%):</strong> ${iva.toFixed(2)}</p>
        <p className="text-xl font-bold"><strong>Total:</strong> ${total.toFixed(2)}</p>
      </div>

      {/* RECEPCIONES */}
      <h3 className="text-xl font-bold mb-2">Recepciones</h3>

      {recepciones.length === 0 && <p>No hay recepciones registradas.</p>}

      {recepciones.map((r) => (
        <div key={r.id} className="mb-4 p-4 border rounded">
          <p><strong>Recepción #{r.id}</strong></p>
          <p>
            Fecha:{" "}
            {r.fecha_recepcion
              ? new Date(r.fecha_recepcion).toLocaleDateString()
              : "—"}
          </p>
          <p>Recibido por: {r.recibido_por}</p>

          <table className="table mt-2">
            <thead>
              <tr>
                <th>Refacción</th>
                <th>Cant. Recibida</th>
                <th>Cant. OC</th>
              </tr>
            </thead>
            <tbody>
              {r.detalles.map((d) => (
                <tr key={d.id}>
                  <td>{d.refaccion?.descripcion || "—"}</td>
                  <td>{d.cantidad_recibida}</td>
                  <td>{d.cantidad_oc ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      {/* DIFERENCIAS */}
      <h3 className="text-xl font-bold mt-6 mb-2">Diferencias</h3>

      {diferencias.length === 0 && (
        <p className="text-gray-500">No hay diferencias.</p>
      )}

      {diferencias.length > 0 && (
        <table className="table">
          <thead>
            <tr>
              <th>Refacción</th>
              <th>OC</th>
              <th>Recibido</th>
              <th>Diferencia</th>
            </tr>
          </thead>
          <tbody>
            {diferencias.map((d, i) => (
              <tr key={i}>
                <td>{d.descripcion}</td>
                <td>{d.cantidad_oc}</td>
                <td>{d.recibido}</td>
                <td>{d.diferencia}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
