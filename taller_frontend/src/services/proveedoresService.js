import api from "./api";

const BASE = "/proveedores/";

const proveedoresService = {
  getAll: async () => {
    try {
      const res = await api.get(BASE);
      return res.data;
    } catch (err) {
      console.error("Error obteniendo proveedores:", err);
      throw new Error("No se pudieron cargar los proveedores");
    }
  },

  create: async (data) => {
    try {
      const res = await api.post(BASE, data);
      return res.data;
    } catch (err) {
      console.error("Error creando proveedor:", err);
      throw new Error("No se pudo crear el proveedor");
    }
  },

  update: async (id, data) => {
    if (!id) throw new Error("ID inválido para actualizar proveedor");

    try {
      const res = await api.put(`${BASE}${id}/`, data);
      return res.data;
    } catch (err) {
      console.error("Error actualizando proveedor:", err);
      throw new Error("No se pudo actualizar el proveedor");
    }
  },

  remove: async (id) => {
    if (!id) throw new Error("ID inválido para eliminar proveedor");

    try {
      const res = await api.delete(`${BASE}${id}/`);
      return res.data;
    } catch (err) {
      console.error("Error eliminando proveedor:", err);
      throw new Error("No se pudo eliminar el proveedor");
    }
  },
};

export default proveedoresService;
