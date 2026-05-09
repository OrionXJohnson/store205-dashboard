import DashboardCard from "../../components/common/DashboardCard";
import MetricCard from "../../components/common/MetricCard";

import type { SalesSummary } from "../../types/sales";

import {
  formatCurrency,
  formatNumber,
} from "../../utils/formatters";

interface SalesSummarySectionProps {
  salesData: SalesSummary;
}

export default function SalesSummarySection({
  salesData,
}: SalesSummarySectionProps) {
  return (
    <DashboardCard title="Daily Sales Summary">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <MetricCard
          label="Sales Amount"
          value={formatCurrency(salesData.sales_amount)}
        />

        <MetricCard
          label="Transactions"
          value={formatNumber(salesData.transaction_count)}
        />

        <MetricCard
          label="Average Transaction"
          value={formatCurrency(salesData.average_transaction)}
        />

        <MetricCard
          label="Service Plan Sales"
          value={formatCurrency(salesData.service_plan_sales)}
        />
      </div>
    </DashboardCard>
  );
}