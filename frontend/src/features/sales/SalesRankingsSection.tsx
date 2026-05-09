import DashboardCard from "../../components/common/DashboardCard";
import MetricCard from "../../components/common/MetricCard";

import type { SalesRankings } from "../../types/sales";
import type { PeriodType } from "../../types/common";

import { getPeriodLabel } from "../../utils/periods";
import {
  formatCurrency,
  formatNumber,
  formatPercent,
} from "../../utils/formatters";

interface SalesRankingsSectionProps {
  rankings: SalesRankings;
  period: PeriodType;
}

export default function SalesRankingsSection({
  rankings,
  period,
}: SalesRankingsSectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Sales Rankings`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <MetricCard
          label="Sales Rank"
          value={`#${rankings.sales_amount.rank} of ${rankings.sales_amount.total_stores}`}
        />

        <MetricCard
          label="Transaction Rank"
          value={`#${rankings.transaction_count.rank} of ${rankings.transaction_count.total_stores}`}
        />

        <MetricCard
          label="Average Transaction Rank"
          value={`#${rankings.average_transaction.rank} of ${rankings.average_transaction.total_stores}`}
        />

        <MetricCard
          label="No Sales ID Share Rank"
          value={`#${rankings.no_sales_share.rank} of ${rankings.no_sales_share.total_stores}`}
        />

        <MetricCard
          label="Sales Value"
          value={formatCurrency(rankings.sales_amount.metric_value)}
        />

        <MetricCard
          label="Transaction Count"
          value={formatNumber(rankings.transaction_count.metric_value)}
        />

        <MetricCard
          label="Average Transaction"
          value={formatCurrency(rankings.average_transaction.metric_value)}
        />

        <MetricCard
          label="No Sales ID Share"
          value={formatPercent(rankings.no_sales_share.metric_value)}
        />
      </div>
    </DashboardCard>
  );
}