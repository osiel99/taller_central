import { Layout, Menu } from "antd";
import {
  DashboardOutlined,
  CarOutlined,
  FileDoneOutlined,
  ShoppingCartOutlined,
  InboxOutlined,
  FileSearchOutlined,
  TeamOutlined,
} from "@ant-design/icons";
import { Link, Outlet, useLocation } from "react-router-dom";

const { Header, Sider, Content } = Layout;

export default function DashboardLayout() {
  const location = useLocation();

  // Normalizamos la ruta para evitar crashes con rutas hijas
  const currentPath = location.pathname.split("/").slice(0, 3).join("/");

  const menuItems = [
    {
      key: "/dashboard",
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Dashboard</Link>,
    },
    {
      key: "/dashboard/vehiculos",
      icon: <CarOutlined />,
      label: <Link to="/dashboard/vehiculos">Vehículos</Link>,
    },
    {
      key: "/dashboard/ordenes-servicio",
      icon: <FileDoneOutlined />,
      label: <Link to="/dashboard/ordenes-servicio">Órdenes de Servicio</Link>,
    },
    {
      key: "/dashboard/ordenes-compra",
      icon: <ShoppingCartOutlined />,
      label: <Link to="/dashboard/ordenes-compra">Órdenes de Compra</Link>,
    },
    {
      key: "/dashboard/recepciones",
      icon: <FileSearchOutlined />,
      label: <Link to="/dashboard/recepciones">Recepciones</Link>,
    },
    {
      key: "/dashboard/inventario",
      icon: <InboxOutlined />,
      label: <Link to="/dashboard/inventario">Inventario</Link>,
    },
    {
      key: "/dashboard/proveedores",
      icon: <TeamOutlined />,
      label: <Link to="/dashboard/proveedores">Proveedores</Link>,
    },
  ];

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider theme="dark" collapsible>
        <div
          style={{
            height: 60,
            margin: 16,
            background: "rgba(255,255,255,0.2)",
            borderRadius: 8,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "white",
            fontWeight: "bold",
          }}
        >
          TALLER
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[currentPath]}
          items={menuItems}
        />
      </Sider>

      <Layout>
        <Header
          style={{
            background: "#fff",
            padding: "0 20px",
            fontWeight: "bold",
            fontSize: 18,
          }}
        >
          Taller Municipal — Panel de Control
        </Header>

        <Content style={{ margin: "20px", padding: 20, background: "#fff" }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
