import api from "./api";

const BASE = "/vehiculos/";

const vehiculosService = {
  // Obtener todos los vehículos
  getAll: async () => {
    const res = await api.get(BASE);
    return res.data;
  },

  // Crear un vehículo
  create: async (data) => {
    const res = await api.post(BASE, data);
    return res.data;
  },

  // Actualizar un vehículo
  update: async (id, data) => {
    const res = await api.put(`${BASE}${id}/`, data);
    return res.data;
  },

  // Eliminar un vehículo
  remove: async (id) => {
    const res = await api.delete(`${BASE}${id}/`);
    return res.data;
  },
};

export default vehiculosService;
