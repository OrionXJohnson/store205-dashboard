import { NavLink, Outlet } from "react-router-dom";

const NAV_ITEMS = [
  {
    label: "Overview",
    path: "/",
  },
  {
    label: "Sales",
    path: "/sales",
  },
  {
    label: "Systems",
    path: "/systems",
  },
  {
    label: "MA Attach",
    path: "/ma-attach",
  },
];

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-8 py-5">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Store 205 Dashboard
              </h1>

              <p className="text-sm text-gray-500">
                Sales, Systems, and attach performance analytics
              </p>
            </div>

            <nav className="flex flex-wrap gap-2">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    isActive
                      ? "px-4 py-2 rounded-lg bg-blue-600 text-white font-medium"
                      : "px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8">
        <Outlet />
      </main>
    </div>
  );
}