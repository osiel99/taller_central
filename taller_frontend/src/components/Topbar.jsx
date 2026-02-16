export default function Topbar() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="w-full h-16 bg-slate-100 border-b border-slate-300 flex items-center justify-end px-6">
      <button
        onClick={handleLogout}
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition"
      >
        Cerrar sesión
      </button>
    </div>
  );
}
