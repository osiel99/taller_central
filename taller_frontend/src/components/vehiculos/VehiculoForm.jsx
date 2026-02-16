import { useState } from "react";
import vehiculosService from "../../services/vehiculosService";

const TIPOS = [
  "AUTOMOVIL", "BARREDORA", "PICK UP", "CARGADOR FRONTAL",
  "COMPACTADOR PATA DE CABRA", "TRAILA", "GRUA", "MONTACARGAS",
  "MOTOCICLETA", "PIPA", "RECOLECTOR", "REDILAS", "REMOLQUE",
  "RETROEXCAVADORA", "VOLTEO"
];

const MARCAS = [
  "VOLKSWAGEN", "GLOBAL", "CHEVROLET", "RAM", "NISSAN", "FORD",
  "CATERPILLAR", "FREIGHTLINER", "KARCHER", "GMC", "DODGE",
  "INTERNATIONAL", "KENWORTH"
];

const AREAS = [
  "DIRECCIÓN DE SERVICIOS PÚBLICOS",
  "LIMPIEZA",
  "EMBELLECIMIENTO URBANO",
  "CENTRAL DE SERVICIOS",
  "ALUMBRADO PÚBLICO",
  "PANTEONES"
];

const MODELOS = [
  "Jetta", "M3", "NP 300", "2500", "1500", "TORNADO", "F 250", "F 150",
  "SILVERADO 1500", "SILVERADO 2500", "SILVERADO 3500", "700", "4000",
  "M2", "KODIAK", "CRYPTON", "T 370", "977K", "826C", "MYL02A25V",
  "H 100", "420D"
];

export default function VehiculoForm({ initialData, onCancel, onSuccess }) {
  const [form, setForm] = useState(
    initialData || {
      numero_economico: "",
      tipo: "",
      placas: "",
      marca: "",
      modelo: "",
      anio: "",
      numero_serie: "",
      area_asignada: "",
    }
  );

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = { ...form, anio: Number(form.anio) };

    if (initialData) {
      await vehiculosService.update(initialData.id, payload);
    } else {
      await vehiculosService.create(payload);
    }

    onSuccess();
  };

  return (
    <div className="card p-6">
      <h2 className="text-xl font-bold mb-4">
        {initialData ? "Editar vehículo" : "Nuevo vehículo"}
      </h2>

      <form onSubmit={handleSubmit} className="grid gap-4">

        <input
          name="numero_economico"
          value={form.numero_economico}
          onChange={handleChange}
          placeholder="Número económico"
          required
        />

        {/* SELECT TIPO */}
        <select name="tipo" value={form.tipo} onChange={handleChange} required>
          <option value="">Seleccione tipo</option>
          {TIPOS.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>

        <input
          name="placas"
          value={form.placas}
          onChange={handleChange}
          placeholder="Placas"
        />

        {/* SELECT MARCA */}
        <select name="marca" value={form.marca} onChange={handleChange} required>
          <option value="">Seleccione marca</option>
          {MARCAS.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        {/* SELECT MODELO */}
        <select name="modelo" value={form.modelo} onChange={handleChange} required>
          <option value="">Seleccione modelo</option>
          {MODELOS.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        <input
          name="anio"
          value={form.anio}
          onChange={handleChange}
          placeholder="Año"
          type="number"
          required
        />

        <input
          name="numero_serie"
          value={form.numero_serie}
          onChange={handleChange}
          placeholder="Número de serie"
          required
        />

        {/* SELECT AREA */}
        <select
          name="area_asignada"
          value={form.area_asignada}
          onChange={handleChange}
          required
        >
          <option value="">Seleccione área</option>
          {AREAS.map((a) => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>

        <div className="flex gap-2">
          <button type="submit" className="btn-primary">Guardar</button>
          <button type="button" className="btn-secondary" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}
