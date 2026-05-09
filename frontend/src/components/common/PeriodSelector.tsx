import type { PeriodType } from "../../types/common";

interface PeriodSelectorProps {
  selectedPeriod: PeriodType;
  onChange: (period: PeriodType) => void;
  allowedPeriods?: PeriodType[];
}

const PERIOD_OPTIONS: {
  label: string;
  value: PeriodType;
}[] = [
  {
    label: "Daily",
    value: "daily",
  },
  {
    label: "PPTD",
    value: "pay_period_to_date",
  },
  {
    label: "MTD",
    value: "month_to_date",
  },
  {
    label: "QTD",
    value: "quarter_to_date",
  },
];

export default function PeriodSelector({
  selectedPeriod,
  onChange,
  allowedPeriods,
}: PeriodSelectorProps) {
  const visibleOptions = allowedPeriods
    ? PERIOD_OPTIONS.filter((option) =>
        allowedPeriods.includes(option.value)
      )
    : PERIOD_OPTIONS;

  return (
    <div className="flex flex-wrap gap-3">
      {visibleOptions.map((option) => {
        const isSelected = option.value === selectedPeriod;

        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={
              isSelected
                ? "px-4 py-2 rounded-lg bg-blue-600 text-white font-medium"
                : "px-4 py-2 rounded-lg bg-white text-gray-700 border border-gray-300 hover:bg-gray-100"
            }
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}