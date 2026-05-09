import DashboardCard from "../../components/common/DashboardCard";
import type { DepartmentSalesBreakdown } from "../../types/sales";
import { formatCurrency, formatNumber } from "../../utils/formatters";
import type { PeriodType } from "../../types/common";

import { getPeriodLabel } from "../../utils/periods";

interface DepartmentBreakdownSectionProps {
  departments: DepartmentSalesBreakdown[];
  period: PeriodType;
}

export default function DepartmentBreakdownSection({
  departments,
  period,
}: DepartmentBreakdownSectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Department Breakdown`}
>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="border-b border-gray-200 text-sm text-gray-500">
              <th className="py-3 pr-4 font-medium">Department</th>
              <th className="py-3 pr-4 font-medium">Sales</th>
              <th className="py-3 pr-4 font-medium">Transactions</th>
              <th className="py-3 pr-4 font-medium">SP Sales</th>
            </tr>
          </thead>

          <tbody>
            {departments.map((department) => (
              <tr
                key={department.department_code}
                className="border-b border-gray-100"
              >
                <td className="py-3 pr-4 font-medium text-gray-900">
                  {department.department_name} ({department.department_code})
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatCurrency(department.sales_amount)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatNumber(department.transaction_count)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatCurrency(department.service_plan_sales)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardCard>
  );
}