export default function OrdenesServicioTable({ ordenes, onCrear, onEditar, onEliminar }) {
  const lista = ordenes || [];

  return (
    <div className="card">
      <div className="card-header flex justify-between">
        <h2 className="text-xl font-bold">Órdenes de Servicio</h2>
        <button className="btn-primary" onClick={onCrear}>+ Nueva Orden</button>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>Vehículo</th>
            <th>Fecha</th>
            <th>Descripción</th>
            <th>Estatus</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {lista.length === 0 && (
            <tr>
              <td colSpan="5" className="text-center py-4 text-gray-500">
                No hay órdenes de servicio registradas
              </td>
            </tr>
          )}

          {lista.map((o) => (
            <tr key={o.id}>
              <td>{o.vehiculo_id}</td>
              <td>{o.fecha}</td>
              <td>{o.descripcion}</td>
              <td>{o.estatus}</td>
              <td className="flex gap-2">
                <button className="btn-secondary" onClick={() => onEditar(o)}>Editar</button>
                <button className="btn-danger" onClick={() => onEliminar(o.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
