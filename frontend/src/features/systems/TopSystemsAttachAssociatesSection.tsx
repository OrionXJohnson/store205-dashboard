import DashboardCard from "../../components/common/DashboardCard";

import type { PeriodType } from "../../types/common";
import type { SystemsAssociate } from "../../types/systems";

import {
  formatCurrency,
  formatNumber,
  formatPercent,
} from "../../utils/formatters";
import { getPeriodLabel } from "../../utils/periods";

interface TopSystemsAttachAssociatesSectionProps {
  associates: SystemsAssociate[];
  period: PeriodType;
}

export default function TopSystemsAttachAssociatesSection({
  associates,
  period,
}: TopSystemsAttachAssociatesSectionProps) {
  return (
    <DashboardCard title={`${getPeriodLabel(period)} Top Systems Attach RPU Associates`}>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="border-b border-gray-200 text-sm text-gray-500">
              <th className="py-3 pr-4 font-medium">Rank</th>
              <th className="py-3 pr-4 font-medium">Associate</th>
              <th className="py-3 pr-4 font-medium">Units</th>
              <th className="py-3 pr-4 font-medium">Attach RPU</th>
              <th className="py-3 pr-4 font-medium">RPU</th>
              <th className="py-3 pr-4 font-medium">Service Plans</th>
              <th className="py-3 pr-4 font-medium">ESET</th>
              <th className="py-3 pr-4 font-medium">Monitors</th>
            </tr>
          </thead>

          <tbody>
            {associates.map((associate, index) => (
              <tr
                key={associate.associate_name}
                className="border-b border-gray-100"
              >
                <td className="py-3 pr-4 font-semibold text-gray-900">
                  #{index + 1}
                </td>

                <td className="py-3 pr-4 font-medium text-gray-900">
                  {associate.associate_name}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatNumber(associate.primary_units)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatCurrency(associate.total_attach_rpu)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatCurrency(associate.rpu)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatPercent(associate.service_plans_attach_percent)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatPercent(associate.eset_attach_percent)}
                </td>

                <td className="py-3 pr-4 text-gray-700">
                  {formatPercent(associate.monitors_attach_percent ?? 0)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardCard>
  );
}