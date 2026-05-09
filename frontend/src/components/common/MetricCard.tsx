interface MetricCardProps {
  label: string;
  value: string;
}

export default function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div>
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="text-3xl font-bold text-gray-900">
        {value}
      </p>
    </div>
  );
}