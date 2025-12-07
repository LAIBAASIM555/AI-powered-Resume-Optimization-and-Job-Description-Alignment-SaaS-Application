import { useState } from 'react';

const Recommendations = ({ recommendations }) => {
  const [expanded, setExpanded] = useState({});

  const toggleExpand = (index) => {
    setExpanded({ ...expanded, [index]: !expanded[index] });
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Recommendations</h3>
        <p className="text-gray-500">No recommendations available.</p>
      </div>
    );
  }

  // Group by priority
  const grouped = {
    high: recommendations.filter(r => r.priority === 'high'),
    medium: recommendations.filter(r => r.priority === 'medium'),
    low: recommendations.filter(r => r.priority === 'low'),
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-6">Recommendations</h3>
      
      <div className="space-y-4">
        {['high', 'medium', 'low'].map(priority => (
          grouped[priority].length > 0 && (
            <div key={priority}>
              <h4 className="text-sm font-medium text-gray-600 mb-2 uppercase tracking-wide">
                {priority} Priority
              </h4>
              <div className="space-y-3">
                {grouped[priority].map((rec, index) => (
                  <div
                    key={index}
                    className={`border rounded-lg p-4 ${getPriorityColor(rec.priority)}`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-xs font-semibold px-2 py-1 rounded">
                            {rec.priority.toUpperCase()}
                          </span>
                          <span className="text-xs text-gray-600">{rec.category}</span>
                        </div>
                        <p className="font-medium text-sm mb-1">{rec.message}</p>
                        {expanded[index] && rec.details && (
                          <p className="text-sm mt-2 opacity-90">{rec.details}</p>
                        )}
                      </div>
                      {rec.details && (
                        <button
                          onClick={() => toggleExpand(index)}
                          className="ml-2 text-sm font-medium hover:underline"
                        >
                          {expanded[index] ? 'Less' : 'More'}
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        ))}
      </div>
    </div>
  );
};

export default Recommendations;

