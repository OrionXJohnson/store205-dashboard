import DashboardCard from "../../components/common/DashboardCard";
import MetricCard from "../../components/common/MetricCard";

import type { PeriodType } from "../../types/common";
import type { SystemsSummary } from "../../types/systems";

import {
  formatCurrency,
  formatNumber,
  formatPercent,
} from "../../utils/formatters";
import { getPeriodLabel } from "../../utils/periods";

interface SystemsSummarySectionProps {
  systemsData: SystemsSummary;
  period: PeriodType;
}

export default function SystemsSummarySection({
  systemsData,
  period,
}: SystemsSummarySectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Systems Summary`}>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <MetricCard
          label="Primary Units"
          value={formatNumber(systemsData.primary_units)}
        />

        <MetricCard
          label="ASP"
          value={formatCurrency(systemsData.asp)}
        />

        <MetricCard
          label="RPU"
          value={formatCurrency(systemsData.rpu)}
        />

        <MetricCard
          label="Attach Units per Primary"
          value={systemsData.attach_units_per_primary.toFixed(2)}
        />

        <MetricCard
          label="Total Attach RPU"
          value={formatCurrency(systemsData.total_attach_rpu)}
        />

        <MetricCard
          label="Service Plans Attach"
          value={formatPercent(systemsData.service_plans_attach_percent)}
        />

        <MetricCard
          label="ESET Attach"
          value={formatPercent(systemsData.eset_attach_percent)}
        />

        <MetricCard
          label="Office Attach"
          value={formatPercent(systemsData.office_attach_percent)}
        />

        <MetricCard
          label="Monitor Attach"
          value={formatPercent(systemsData.monitors_attach_percent)}
        />
      </div>
    </DashboardCard>
  );
}