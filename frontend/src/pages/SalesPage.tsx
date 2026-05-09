import { useEffect, useState } from "react";

import {
  fetchDepartmentSalesBreakdown,
  fetchTopSalesStores,
} from "../api/salesApi";

import ErrorState from "../components/common/ErrorState";
import LoadingState from "../components/common/LoadingState";
import PeriodSelector from "../components/common/PeriodSelector";

import DepartmentBreakdownSection from "../features/sales/DepartmentBreakdownSection";
import TopSalesStoresSection from "../features/sales/TopSalesStoresSection";
import DepartmentSalesChart from "../features/sales/DepartmentSalesChart";

import PageHeader from "../components/layout/PageHeader";

import type { PeriodType } from "../types/common";

import type {
  DepartmentSalesBreakdown,
  TopSalesStore,
} from "../types/sales";

export default function SalesPage() {
  const [selectedPeriod, setSelectedPeriod] =
    useState<PeriodType>("daily");

  const [departments, setDepartments] = useState<
    DepartmentSalesBreakdown[]
  >([]);

  const [topSalesStores, setTopSalesStores] = useState<
    TopSalesStore[]
  >([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSalesDetails() {
      try {
        setLoading(true);

        const [departmentsResponse, topStoresResponse] =
          await Promise.all([
            fetchDepartmentSalesBreakdown(205, selectedPeriod),
            fetchTopSalesStores(selectedPeriod, 10),
          ]);

        setDepartments(departmentsResponse.data);
        setTopSalesStores(topStoresResponse.data.stores);
      } catch (err) {
        console.error(err);

        setError("Failed to load sales details.");
      } finally {
        setLoading(false);
      }
    }

    loadSalesDetails();
  }, [selectedPeriod]);

  if (loading) {
    return <LoadingState message="Loading sales details..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div>
        <PageHeader
            title="Sales Details"
            description="Department performance and store comparison details."
            actions={
                <PeriodSelector
                selectedPeriod={selectedPeriod}
                onChange={setSelectedPeriod}
                />
            }
        />
        <DepartmentSalesChart
            departments={departments}
            period={selectedPeriod}
        />
      <div className="mt-8">
        <DepartmentBreakdownSection
            departments={departments}
            period={selectedPeriod}
        />
      </div>
      <div className="mt-8">
        <TopSalesStoresSection
            stores={topSalesStores}
            period={selectedPeriod}
        />
      </div>
    </div>
  );
}