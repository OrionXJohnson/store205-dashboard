import { useEffect, useState } from "react";

import {
  fetchStoreSalesRankings,
  fetchStoreSalesSummary,
} from "../api/salesApi";

import ErrorState from "../components/common/ErrorState";
import LoadingState from "../components/common/LoadingState";
import PeriodSelector from "../components/common/PeriodSelector";

import SalesRankingsSection from "../features/sales/SalesRankingsSection";
import SalesSummarySection from "../features/sales/SalesSummarySection";

import PageHeader from "../components/layout/PageHeader";

import type { PeriodType } from "../types/common";

import type {
  SalesRankings,
  SalesSummary,
} from "../types/sales";


export default function DashboardPage() {
  const [salesData, setSalesData] = useState<SalesSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<PeriodType>("daily");
  const [rankings, setRankings] = useState<SalesRankings | null>(null);

  useEffect(() => {
    async function loadSalesData() {
      try {
        setLoading(true);

        const [
            salesResponse,
            rankingsResponse,
        ] = await Promise.all([
            fetchStoreSalesSummary(205, selectedPeriod),
            fetchStoreSalesRankings(205, selectedPeriod),
        ]);

        setSalesData(salesResponse.data);
        setRankings(rankingsResponse.data.rankings);
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
  <div>
    <PageHeader
      title="Overview"
      description="High-level Store 205 sales performance and rankings."
      actions={
        <PeriodSelector
          selectedPeriod={selectedPeriod}
          onChange={setSelectedPeriod}
        />
      }
    />

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
  </div>
);
}