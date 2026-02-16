import api from "./api";

const ordenesServicioService = {
  getAll: async () => {
    const res = await api.get("/ordenes_servicio/");
    return res.data;
  },

  create: async (data) => {
    const res = await api.post("/ordenes_servicio/", data);
    return res.data;
  },

  update: async (id, data) => {
    const res = await api.put(`/ordenes_servicio/${id}/`, data);
    return res.data;
  },

  remove: async (id) => {
    const res = await api.delete(`/ordenes_servicio/${id}/`);
    return res.data;
  },
};

export default ordenesServicioService;
