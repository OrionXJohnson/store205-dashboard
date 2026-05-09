import DashboardCard from "../../components/common/DashboardCard";
import MetricCard from "../../components/common/MetricCard";

import type { PeriodType } from "../../types/common";
import type { SystemsRankings } from "../../types/systems";

import {
  formatCurrency,
  formatNumber,
} from "../../utils/formatters";
import { getPeriodLabel } from "../../utils/periods";

interface SystemsRankingsSectionProps {
  rankings: SystemsRankings;
  period: PeriodType;
}

export default function SystemsRankingsSection({
  rankings,
  period,
}: SystemsRankingsSectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Systems Rankings`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <MetricCard
          label="RPU Rank"
          value={`#${rankings.rpu.rank} of ${rankings.rpu.total_stores}`}
        />

        <MetricCard
          label="Attach RPU Rank"
          value={`#${rankings.total_attach_rpu.rank} of ${rankings.total_attach_rpu.total_stores}`}
        />

        <MetricCard
          label="ASP Rank"
          value={`#${rankings.asp.rank} of ${rankings.asp.total_stores}`}
        />

        <MetricCard
          label="Primary Units Rank"
          value={`#${rankings.primary_units.rank} of ${rankings.primary_units.total_stores}`}
        />

        <MetricCard
          label="RPU"
          value={formatCurrency(rankings.rpu.metric_value)}
        />

        <MetricCard
          label="Attach RPU"
          value={formatCurrency(rankings.total_attach_rpu.metric_value)}
        />

        <MetricCard
          label="ASP"
          value={formatCurrency(rankings.asp.metric_value)}
        />

        <MetricCard
          label="Primary Units"
          value={formatNumber(rankings.primary_units.metric_value)}
        />
      </div>
    </DashboardCard>
  );
}