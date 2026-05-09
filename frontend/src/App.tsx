import { Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";
import DashboardPage from "./pages/DashboardPage";
import MaAttachPage from "./pages/MaAttachPage";
import SalesPage from "./pages/SalesPage";
import SystemsPage from "./pages/SystemsPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/sales" element={<SalesPage />} />
        <Route path="/systems" element={<SystemsPage />} />
        <Route path="/ma-attach" element={<MaAttachPage />} />
      </Route>
    </Routes>
  );
}