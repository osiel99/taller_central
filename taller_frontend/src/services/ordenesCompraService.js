import api from "./api";

const BASE = "/ordenes_compra/";

const ordenesCompraService = {
  getAll: async () => {
    const res = await api.get(BASE);
    return res.data;
  },

  create: async (data) => {
    const res = await api.post(BASE, data);
    return res.data;
  },

  // Importar desde JSON o TEXTO
  importar: async (payload) => {
    const res = await api.post(`${BASE}importar/`, payload);
    return res.data;
  },

  // Importar desde Excel (.xlsx)
  importarExcel: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post(`${BASE}importar_excel/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return res.data;
  },

  // Importar desde PDF real (binario)
  importarPDF: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post(`${BASE}importar_pdf/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return res.data;
  },
};

export default ordenesCompraService;
