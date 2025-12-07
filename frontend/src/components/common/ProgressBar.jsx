const ProgressBar = ({ value, label, className = '' }) => {
  const getColor = (val) => {
    if (val >= 90) return 'bg-green-500';
    if (val >= 70) return 'bg-blue-500';
    if (val >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          <span className="text-sm font-medium text-gray-700">{value}%</span>
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          className={`h-full transition-all duration-500 ${getColor(value)}`}
          style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;

