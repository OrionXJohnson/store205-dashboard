import type { ReactNode } from "react";

interface DashboardCardProps {
  title: string;
  children: ReactNode;
}

export default function DashboardCard({
  title,
  children,
}: DashboardCardProps) {
  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        {title}
      </h2>

      {children}
    </section>
  );
}