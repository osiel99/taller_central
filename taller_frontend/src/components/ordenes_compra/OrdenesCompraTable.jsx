import { Link } from "react-router-dom";

export default function OrdenesCompraTable({ ordenes, onCrear }) {
  const lista = ordenes || [];

  return (
    <div className="card">
      <div className="card-header flex justify-between">
        <h2 className="text-xl font-bold">Órdenes de Compra</h2>
        <button className="btn-primary" onClick={onCrear}>
          + Nueva Orden
        </button>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Proveedor</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Factura</th>
          </tr>
        </thead>

        <tbody>
          {lista.length === 0 && (
            <tr>
              <td colSpan="5" className="text-center py-4 text-gray-500">
                No hay órdenes de compra registradas
              </td>
            </tr>
          )}

          {lista.map((oc) => (
            <tr key={oc.id} className="hover:bg-gray-100 cursor-pointer">
              <td>
                <Link
                  to={`/dashboard/ordenes-compra/${oc.id}`}
                  className="text-blue-600 underline"
                >
                  #{oc.id}
                </Link>
              </td>

              <td>{oc.proveedor}</td>

              <td>
                {oc.fecha_oc
                  ? new Date(oc.fecha_oc).toLocaleDateString()
                  : "—"}
              </td>

              <td>{oc.estado}</td>

              <td>{oc.factura || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
