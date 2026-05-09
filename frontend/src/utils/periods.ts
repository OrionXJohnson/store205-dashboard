import type { PeriodType } from "../types/common";

export function getPeriodLabel(period: PeriodType): string {
  switch (period) {
    case "daily":
      return "Daily";

    case "pay_period_to_date":
      return "PPTD";

    case "month_to_date":
      return "MTD";

    case "quarter_to_date":
      return "QTD";

    default:
      return "Unknown";
  }
}