import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";

import DashboardLayout from "../layouts/DashboardLayout";

// Páginas existentes
import LoginPage from "../pages/LoginPage";
import DashboardPage from "../pages/DashboardPage";

// Nuevos módulos
import InventarioPage from "../pages/inventario/InventarioPage";
import VehiculosPage from "../pages/vehiculos/VehiculosPage";
import OrdenesServicioPage from "../pages/ordenes/OrdenesServicioPage";
import OrdenesCompraPage from "../pages/ordenes_compra/OrdenesCompraPage";
import OrdenCompraDetallePage from "../pages/ordenes_compra/OrdenCompraDetallePage";
import RecepcionesPage from "../pages/recepciones/RecepcionesPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        {/* LOGIN */}
        <Route path="/" element={<LoginPage />} />

        {/* RUTAS PROTEGIDAS */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          {/* Dashboard principal */}
          <Route index element={<DashboardPage />} />

          {/* Vehículos */}
          <Route path="vehiculos" element={<VehiculosPage />} />

          {/* Órdenes de servicio */}
          <Route path="ordenes-servicio" element={<OrdenesServicioPage />} />

          {/* Órdenes de compra */}
          <Route path="ordenes-compra" element={<OrdenesCompraPage />} />
          <Route path="ordenes-compra/:id" element={<OrdenCompraDetallePage />} />

          {/* Recepciones */}
          <Route path="recepciones" element={<RecepcionesPage />} />

          {/* Inventario */}
          <Route path="inventario" element={<InventarioPage />} />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}
