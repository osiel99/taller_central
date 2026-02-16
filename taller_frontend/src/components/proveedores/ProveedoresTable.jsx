export default function ProveedoresTable({ proveedores, onCrear, onEditar, onEliminar }) {
  const lista = proveedores || [];

  return (
    <div className="card">
      <div className="card-header flex justify-between">
        <h2 className="text-xl font-bold">Proveedores</h2>
        <button className="btn-primary" onClick={onCrear}>+ Nuevo proveedor</button>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>RFC</th>
            <th>Teléfono</th>
            <th>Dirección</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {lista.length === 0 && (
            <tr>
              <td colSpan="5" className="text-center py-4 text-gray-500">
                No hay proveedores registrados
              </td>
            </tr>
          )}

          {lista.map((p) => (
            <tr key={p.id} className="hover:bg-gray-100">
              <td>{p.nombre}</td>
              <td>{p.rfc}</td>
              <td>{p.telefono}</td>
              <td>{p.direccion}</td>
              <td className="flex gap-2">
                <button className="btn-secondary" onClick={() => onEditar(p)}>Editar</button>
                <button className="btn-danger" onClick={() => onEliminar(p.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
