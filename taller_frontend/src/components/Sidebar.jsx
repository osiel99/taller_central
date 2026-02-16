import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-60 bg-slate-800 text-white h-screen p-6 box-border">
      <h2 className="text-xl font-bold mb-8">Taller Municipal</h2>

      <nav className="flex flex-col gap-4">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/vehiculos"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Vehículos
        </NavLink>

        <NavLink
          to="/ordenes"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Órdenes de Servicio
        </NavLink>

        <NavLink
          to="/inventario"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Inventario
        </NavLink>

        <NavLink
          to="/ordenes-compra"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Compras
        </NavLink>

        <NavLink
          to="/reportes"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Reportes
        </NavLink>

        <NavLink
          to="/usuarios"
          className={({ isActive }) =>
            isActive ? "text-yellow-300 font-semibold" : "text-white"
          }
        >
          Usuarios
        </NavLink>
      </nav>
    </div>
  );
}
