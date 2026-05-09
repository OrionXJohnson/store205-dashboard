import { useEffect, useState } from "react";

import ErrorState from "../components/common/ErrorState";
import LoadingState from "../components/common/LoadingState";
import SalesSummarySection from "../features/sales/SalesSummarySection";
import { fetchDepartmentSalesBreakdown, fetchStoreSalesSummary } from "../api/salesApi";
import DepartmentBreakdownSection from "../features/sales/DepartmentBreakdownSection";
import type {
  DepartmentSalesBreakdown,
  SalesSummary,
} from "../types/sales";
import PeriodSelector from "../components/common/PeriodSelector";

import type { PeriodType } from "../types/common";


export default function DashboardPage() {
  const [salesData, setSalesData] = useState<SalesSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [departments, setDepartments] = useState<DepartmentSalesBreakdown[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<PeriodType>("daily");

  useEffect(() => {
    async function loadSalesData() {
      try {
        setLoading(true);

        const [salesResponse, departmentsResponse] = await Promise.all([
            fetchStoreSalesSummary(205, selectedPeriod),
            fetchDepartmentSalesBreakdown(205, selectedPeriod),
        ]);

        setSalesData(salesResponse.data);
        setDepartments(departmentsResponse.data);
      } catch (err) {
        console.error(err);

        setError("Failed to load sales data.");
      } finally {
        setLoading(false);
      }
    }

    loadSalesData();
  }, [selectedPeriod]);

  if (loading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  if (!salesData) {
    return <ErrorState message="No data available." />;
  }

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Store 205 Dashboard
        </h1>
        <div className="mb-8 flex justify-end">
            <PeriodSelector
                selectedPeriod={selectedPeriod}
                onChange={setSelectedPeriod}
            />
        </div>
        <SalesSummarySection salesData={salesData} />
        <div className="mt-8">
            <DepartmentBreakdownSection departments={departments} />
        </div>
      </div>
    </main>
  );
}