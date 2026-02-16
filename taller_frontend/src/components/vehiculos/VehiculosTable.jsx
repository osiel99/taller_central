import { useState, useMemo } from "react";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default function VehiculosTable({ vehiculos, onCrear, onEditar, onEliminar }) {
  const lista = Array.isArray(vehiculos) ? vehiculos : [];

  // -----------------------------
  // ESTADOS PARA FILTROS Y BUSQUEDA
  // -----------------------------
  const [busqueda, setBusqueda] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("");
  const [filtroArea, setFiltroArea] = useState("");

  // -----------------------------
  // PAGINACIÓN
  // -----------------------------
  const [pagina, setPagina] = useState(1);
  const porPagina = 10;

  const tiposUnicos = [...new Set(lista.map((v) => v.tipo))];
  const areasUnicas = [...new Set(lista.map((v) => v.area_asignada))];

  // -----------------------------
  // FILTRADO + BUSQUEDA
  // -----------------------------
  const filtrados = useMemo(() => {
    return lista
      .filter((v) =>
        v.numero_economico.toLowerCase().includes(busqueda.toLowerCase())
      )
      .filter((v) => (filtroTipo ? v.tipo === filtroTipo : true))
      .filter((v) => (filtroArea ? v.area_asignada === filtroArea : true));
  }, [lista, busqueda, filtroTipo, filtroArea]);

  // -----------------------------
  // PAGINACIÓN FINAL
  // -----------------------------
  const totalPaginas = Math.ceil(filtrados.length / porPagina);
  const inicio = (pagina - 1) * porPagina;
  const paginaActual = filtrados.slice(inicio, inicio + porPagina);

  const cambiarPagina = (nueva) => {
    if (nueva >= 1 && nueva <= totalPaginas) {
      setPagina(nueva);
    }
  };

  // -----------------------------
  // EXPORTAR A EXCEL
  // -----------------------------
  const exportarExcel = () => {
    const hoja = XLSX.utils.json_to_sheet(filtrados);
    const libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, hoja, "Vehículos");

    const excelBuffer = XLSX.write(libro, { bookType: "xlsx", type: "array" });
    const archivo = new Blob([excelBuffer], { type: "application/octet-stream" });

    saveAs(archivo, "vehiculos.xlsx");
  };

  return (
    <div className="card">

      {/* HEADER */}
      <div className="card-header flex justify-between items-center">
        <h2 className="text-xl font-bold">Vehículos</h2>

        <div className="flex gap-2">
          <button className="btn-secondary" onClick={exportarExcel}>
            Exportar Excel
          </button>
          <button className="btn-primary" onClick={onCrear}>
            + Nuevo vehículo
          </button>
        </div>
      </div>

      {/* FILTROS */}
      <div className="p-4 grid grid-cols-1 md:grid-cols-4 gap-4">

        <input
          type="text"
          placeholder="Buscar por número económico"
          className="input"
          value={busqueda}
          onChange={(e) => {
            setBusqueda(e.target.value);
            setPagina(1);
          }}
        />

        <select
          className="input"
          value={filtroTipo}
          onChange={(e) => {
            setFiltroTipo(e.target.value);
            setPagina(1);
          }}
        >
          <option value="">Todos los tipos</option>
          {tiposUnicos.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>

        <select
          className="input"
          value={filtroArea}
          onChange={(e) => {
            setFiltroArea(e.target.value);
            setPagina(1);
          }}
        >
          <option value="">Todas las áreas</option>
          {areasUnicas.map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>

      </div>

      {/* TABLA */}
      <table className="table">
        <thead>
          <tr>
            <th>Núm. Económico</th>
            <th>Tipo</th>
            <th>Placas</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Año</th>
            <th>Núm. Serie</th>
            <th>Área Asignada</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {paginaActual.length === 0 && (
            <tr>
              <td colSpan="9" className="text-center py-4 text-gray-500">
                No hay vehículos registrados
              </td>
            </tr>
          )}

          {paginaActual.map((v) => (
            <tr key={v.id}>
              <td>{v.numero_economico}</td>
              <td>{v.tipo}</td>
              <td>{v.placas}</td>
              <td>{v.marca}</td>
              <td>{v.modelo}</td>
              <td>{v.anio}</td>
              <td>{v.numero_serie}</td>
              <td>{v.area_asignada}</td>

              <td className="flex gap-2">
                <button className="btn-secondary" onClick={() => onEditar(v)}>
                  Editar
                </button>
                <button className="btn-danger" onClick={() => onEliminar(v.id)}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* PAGINACIÓN */}
      <div className="flex justify-center items-center gap-4 py-4">
        <button className="btn-secondary" onClick={() => cambiarPagina(pagina - 1)}>
          Anterior
        </button>

        <span>Página {pagina} de {totalPaginas}</span>

        <button className="btn-secondary" onClick={() => cambiarPagina(pagina + 1)}>
          Siguiente
        </button>
      </div>
    </div>
  );
}
