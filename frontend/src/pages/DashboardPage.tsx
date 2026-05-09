import { useEffect, useState } from "react";

import {
  fetchDepartmentSalesBreakdown,
  fetchStoreSalesRankings,
  fetchStoreSalesSummary,
  fetchTopSalesStores,
} from "../api/salesApi";

import ErrorState from "../components/common/ErrorState";
import LoadingState from "../components/common/LoadingState";
import PeriodSelector from "../components/common/PeriodSelector";

import DepartmentBreakdownSection from "../features/sales/DepartmentBreakdownSection";
import SalesRankingsSection from "../features/sales/SalesRankingsSection";
import SalesSummarySection from "../features/sales/SalesSummarySection";
import TopSalesStoresSection from "../features/sales/TopSalesStoresSection";

import type { PeriodType } from "../types/common";

import type {
  DepartmentSalesBreakdown,
  SalesRankings,
  SalesSummary,
  TopSalesStore,
} from "../types/sales";


export default function DashboardPage() {
  const [salesData, setSalesData] = useState<SalesSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [departments, setDepartments] = useState<DepartmentSalesBreakdown[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<PeriodType>("daily");
  const [rankings, setRankings] = useState<SalesRankings | null>(null);
  const [topSalesStores, setTopSalesStores] = useState<TopSalesStore[]>([]);

  useEffect(() => {
    async function loadSalesData() {
      try {
        setLoading(true);

        const [
            salesResponse,
            departmentsResponse,
            rankingsResponse,
            topSalesStoresResponse,
        ] = await Promise.all([
            fetchStoreSalesSummary(205, selectedPeriod),
            fetchDepartmentSalesBreakdown(205, selectedPeriod),
            fetchStoreSalesRankings(205, selectedPeriod),
            fetchTopSalesStores(selectedPeriod, 10),
        ]);

        setSalesData(salesResponse.data);
        setDepartments(departmentsResponse.data);
        setRankings(rankingsResponse.data.rankings);
        setTopSalesStores(topSalesStoresResponse.data.stores);
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

  if (!salesData || !rankings) {
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
            <SalesSummarySection
                salesData={salesData}
                period={selectedPeriod}
            />
        <div className="mt-8">
            <SalesRankingsSection
                rankings={rankings}
                period={selectedPeriod}
            />
        </div>
        <div className="mt-8">
            <TopSalesStoresSection
                stores={topSalesStores}
                period={selectedPeriod}
            />
        </div>
        <div className="mt-8">
            <DepartmentBreakdownSection
                departments={departments}
                period={selectedPeriod}
            />
        </div>
      </div>
    </main>
  );
}