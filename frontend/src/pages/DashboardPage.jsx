import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { dashboardAPI, analysisAPI } from '../services/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsResponse, historyResponse] = await Promise.all([
          dashboardAPI.getStats(),
          analysisAPI.getHistory(20),
        ]);
        setStats(statsResponse.data);
        setHistory(historyResponse.data);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const chartData = history
    .slice()
    .reverse()
    .map((item, index) => ({
      name: `Analysis ${index + 1}`,
      score: item.ats_score,
    }));

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <Button onClick={() => navigate('/upload')}>
            New Analysis
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card>
            <div className="text-sm text-gray-600 mb-1">Total Analyses</div>
            <div className="text-3xl font-bold text-gray-900">
              {stats?.total_analyses || 0}
            </div>
          </Card>
          <Card>
            <div className="text-sm text-gray-600 mb-1">Average Score</div>
            <div className="text-3xl font-bold text-blue-600">
              {stats?.average_score ? stats.average_score.toFixed(1) : 'N/A'}
            </div>
          </Card>
          <Card>
            <div className="text-sm text-gray-600 mb-1">Best Score</div>
            <div className="text-3xl font-bold text-green-600">
              {stats?.best_score ? stats.best_score.toFixed(1) : 'N/A'}
            </div>
          </Card>
          <Card>
            <div className="text-sm text-gray-600 mb-1">Improvement</div>
            <div className={`text-3xl font-bold ${stats?.improvement && stats.improvement > 0 ? 'text-green-600' : 'text-gray-600'}`}>
              {stats?.improvement ? `${stats.improvement > 0 ? '+' : ''}${stats.improvement.toFixed(1)}%` : 'N/A'}
            </div>
          </Card>
        </div>

        {/* Score Trend Chart */}
        {chartData.length > 0 && (
          <Card title="Score Trend" className="mb-8">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  name="ATS Score"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        )}

        {/* Analysis History */}
        <Card title="Recent Analyses">
          {history.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Resume
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Job Title
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr key={item.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.resume_filename || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.job_title || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 text-xs font-semibold rounded-full ${
                            item.ats_score >= 90
                              ? 'bg-green-100 text-green-800'
                              : item.ats_score >= 70
                              ? 'bg-blue-100 text-blue-800'
                              : item.ats_score >= 50
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {item.ats_score.toFixed(1)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => navigate(`/results/${item.id}`)}
                          className="text-blue-600 hover:text-blue-900 mr-4"
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>No analyses yet. Start by uploading a resume!</p>
              <Button onClick={() => navigate('/upload')} className="mt-4">
                Upload Resume
              </Button>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;

