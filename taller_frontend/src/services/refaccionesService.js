import api from "./api";

const BASE = "/refacciones/";

const refaccionesService = {
  getAll: async () => {
    const res = await api.get(BASE);
    return res.data;
  },
};

export default refaccionesService;
