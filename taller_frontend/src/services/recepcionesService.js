import api from "./api";

const BASE = "/recepciones/";

const recepcionesService = {
  getAll: async () => {
    const res = await api.get(BASE);
    return res.data;
  },

  create: async (data) => {
    const res = await api.post(BASE, data);
    return res.data;
  },
};

export default recepcionesService;
