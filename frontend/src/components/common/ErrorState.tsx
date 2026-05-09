interface ErrorStateProps {
  message: string;
}

export default function ErrorState({ message }: ErrorStateProps) {
  return (
    <div className="p-8 text-xl font-semibold text-red-600">
      {message}
    </div>
  );
}