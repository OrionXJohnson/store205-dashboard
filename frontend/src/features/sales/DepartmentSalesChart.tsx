import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import DashboardCard from "../../components/common/DashboardCard";

import type { PeriodType } from "../../types/common";
import type { DepartmentSalesBreakdown } from "../../types/sales";

import { formatCurrency } from "../../utils/formatters";
import { getPeriodLabel } from "../../utils/periods";

interface DepartmentSalesChartProps {
  departments: DepartmentSalesBreakdown[];
  period: PeriodType;
}

interface DepartmentSalesChartData {
  department: string;
  sales: number;
}

export default function DepartmentSalesChart({
  departments,
  period,
}: DepartmentSalesChartProps) {
  const chartData: DepartmentSalesChartData[] = departments.map(
    (department) => ({
      department: department.department_code,
      sales: department.sales_amount,
    })
  );

  return (
    <DashboardCard title={`${getPeriodLabel(period)} Department Sales Chart`}>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="department" />

            <YAxis
              tickFormatter={(value) =>
                formatCurrency(Number(value)).replace(".00", "")
              }
            />

            <Tooltip
              formatter={(value) => formatCurrency(Number(value))}
              labelFormatter={(label) => `Department: ${label}`}
            />

            <Bar dataKey="sales" name="Sales" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </DashboardCard>
  );
}