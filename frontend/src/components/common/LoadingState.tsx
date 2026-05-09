interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({
  message = "Loading...",
}: LoadingStateProps) {
  return (
    <div className="p-8 text-xl font-semibold text-gray-900">
      {message}
    </div>
  );
}