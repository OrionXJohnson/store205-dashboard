import type { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  description?: string;
  actions?: ReactNode;
}

export default function PageHeader({
  title,
  description,
  actions,
}: PageHeaderProps) {
  return (
    <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">
          {title}
        </h2>

        {description ? (
          <p className="mt-2 text-gray-600">
            {description}
          </p>
        ) : null}
      </div>

      {actions ? <div>{actions}</div> : null}
    </div>
  );
}