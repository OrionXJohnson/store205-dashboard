import DashboardCard from "../../components/common/DashboardCard";

import type { PeriodType } from "../../types/common";
import type { TopSalesStore } from "../../types/sales";

import { formatCurrency, formatNumber } from "../../utils/formatters";
import { getPeriodLabel } from "../../utils/periods";

interface TopSalesStoresSectionProps {
  stores: TopSalesStore[];
  period: PeriodType;
  highlightedStoreId?: number;
}

export default function TopSalesStoresSection({
  stores,
  period,
  highlightedStoreId = 205,
}: TopSalesStoresSectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Top Stores by Sales`}>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="border-b border-gray-200 text-sm text-gray-500">
              <th className="py-3 pr-4 font-medium">Rank</th>
              <th className="py-3 pr-4 font-medium">Store</th>
              <th className="py-3 pr-4 font-medium">Sales</th>
              <th className="py-3 pr-4 font-medium">Transactions</th>
              <th className="py-3 pr-4 font-medium">Avg Transaction</th>
              <th className="py-3 pr-4 font-medium">SP Sales</th>
            </tr>
          </thead>

          <tbody>
            {stores.map((store, index) => {
              const isHighlighted = store.store_id === highlightedStoreId;

              return (
                <tr
                  key={store.store_id}
                  className={
                    isHighlighted
                      ? "border-b border-blue-100 bg-blue-50"
                      : "border-b border-gray-100"
                  }
                >
                  <td className="py-3 pr-4 font-semibold text-gray-900">
                    #{index + 1}
                  </td>

                  <td className="py-3 pr-4 font-medium text-gray-900">
                    {store.store_name}
                    {isHighlighted ? " ← Store 205" : ""}
                  </td>

                  <td className="py-3 pr-4 text-gray-700">
                    {formatCurrency(store.sales_amount)}
                  </td>

                  <td className="py-3 pr-4 text-gray-700">
                    {formatNumber(store.transaction_count)}
                  </td>

                  <td className="py-3 pr-4 text-gray-700">
                    {formatCurrency(store.average_transaction)}
                  </td>

                  <td className="py-3 pr-4 text-gray-700">
                    {formatCurrency(store.service_plan_sales)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </DashboardCard>
  );
}