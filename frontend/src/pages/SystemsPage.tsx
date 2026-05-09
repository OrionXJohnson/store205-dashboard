import { useEffect, useState } from "react";

import {
  fetchSystemsRankings,
  fetchSystemsSummary,
  fetchTopSystemsAttachAssociates,
  fetchTopSystemsRpuAssociates,
} from "../api/systemsApi";

import ErrorState from "../components/common/ErrorState";
import LoadingState from "../components/common/LoadingState";
import PeriodSelector from "../components/common/PeriodSelector";
import PageHeader from "../components/layout/PageHeader";

import SystemsRankingsSection from "../features/systems/SystemsRankingsSection";
import SystemsSummarySection from "../features/systems/SystemsSummarySection";
import TopSystemsAttachAssociatesSection from "../features/systems/TopSystemsAttachAssociatesSection";
import TopSystemsRpuAssociatesSection from "../features/systems/TopSystemsRpuAssociatesSection";

import type { PeriodType } from "../types/common";
import type {
  SystemsAssociate,
  SystemsRankings,
  SystemsSummary,
} from "../types/systems";

export default function SystemsPage() {
  const [selectedPeriod, setSelectedPeriod] =
    useState<PeriodType>("daily");

  const SYSTEMS_PERIODS: PeriodType[] = [
    "daily",
    "pay_period_to_date",
    "month_to_date",
  ];

  const [systemsData, setSystemsData] =
    useState<SystemsSummary | null>(null);
  const [rankings, setRankings] =
    useState<SystemsRankings | null>(null);
  const [topRpuAssociates, setTopRpuAssociates] = useState<
    SystemsAssociate[]>([]);

  const [topAttachAssociates, setTopAttachAssociates] =
    useState<SystemsAssociate[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSystemsData() {
      try {
        const [
            summaryResponse,
            rankingsResponse,
            topRpuAssociatesResponse,
            topAttachAssociatesResponse,
        ] = await Promise.all([
            fetchSystemsSummary(205, selectedPeriod),
            fetchSystemsRankings(205, selectedPeriod),
            fetchTopSystemsRpuAssociates(205, selectedPeriod, 5),
            fetchTopSystemsAttachAssociates(205, selectedPeriod, 5),
        ]);

        setSystemsData(summaryResponse.data);
        setRankings(rankingsResponse.data.rankings);

        setTopRpuAssociates(
            topRpuAssociatesResponse.data.associates
        );

        setTopAttachAssociates(
            topAttachAssociatesResponse.data.associates
        );
      } catch (err) {
        console.error(err);

        setError("Failed to load Systems data.");
      } finally {
        setLoading(false);
      }
    }

    loadSystemsData();
  }, [selectedPeriod]);

  if (loading) {
    return <LoadingState message="Loading Systems details..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  if (!systemsData || !rankings) {
    return <ErrorState message="No Systems data available." />;
  }

  return (
    <div>
      <PageHeader
        title="Systems Details"
        description="RPU, attach performance, and Systems sales metrics."
        actions={
          <PeriodSelector
            selectedPeriod={selectedPeriod}
            onChange={setSelectedPeriod}
            allowedPeriods={SYSTEMS_PERIODS}
          />
        }
      />

      <SystemsSummarySection
        systemsData={systemsData}
        period={selectedPeriod}
      />

    <div className="mt-8">
        <SystemsRankingsSection
            rankings={rankings}
            period={selectedPeriod}
        />
    </div>
    <div className="mt-8">
        <TopSystemsRpuAssociatesSection
            associates={topRpuAssociates}
            period={selectedPeriod}
        />
    </div>

    <div className="mt-8">
        <TopSystemsAttachAssociatesSection
            associates={topAttachAssociates}
            period={selectedPeriod}
        />
    </div>
    </div>
  );
}