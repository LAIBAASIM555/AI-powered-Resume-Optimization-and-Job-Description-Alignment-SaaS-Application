import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { dashboardAPI, analysisAPI } from '../services/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import AnimatedCounter from '../components/common/AnimatedCounter';
import { FileText, TrendingUp, Award, BarChart3, Activity, Target, Calendar, Trash2, Settings, User } from 'lucide-react';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const navigate = useNavigate();

  const handleDeleteData = async () => {
    try {
      // This would need to be implemented in the backend
      // For now, just show a message
      alert('Delete data functionality would be implemented here. This requires backend API endpoint.');
    } catch (error) {
      console.error('Failed to delete data:', error);
      alert('Failed to delete data. Please try again.');
    }
  };

  const handleDeleteAnalysis = async (analysisId) => {
    if (!window.confirm('Are you sure you want to delete this analysis? This action cannot be undone.')) {
      return;
    }

    try {
      await analysisAPI.delete(analysisId);
      // Refresh the history after deletion
      const [statsResponse, historyResponse] = await Promise.all([
        dashboardAPI.getStats(),
        analysisAPI.getHistory(20),
      ]);
      setStats(statsResponse.data);
      setHistory(historyResponse.data);
    } catch (error) {
      console.error('Failed to delete analysis:', error);
      alert('Failed to delete analysis. Please try again.');
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showSettings && !event.target.closest('.settings-dropdown')) {
        setShowSettings(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showSettings]);

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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600 text-lg">Track your resume analysis history and performance</p>
          </div>
          <div className="flex gap-3">
            <Button
              onClick={() => navigate('/upload')}
              size="lg"
              className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <Target className="h-5 w-5 mr-2" />
              New Analysis
            </Button>
            <div className="relative settings-dropdown">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors duration-200"
              >
                <Settings className="h-5 w-5 text-gray-600" />
              </button>
              {showSettings && (
                <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 z-10">
                  <div className="p-4 border-b border-gray-200">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <User className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Account Settings</p>
                        <p className="text-sm text-gray-500">Manage your profile</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-2">
                    <button
                      onClick={() => {
                        if (window.confirm('Are you sure you want to delete all your data? This action cannot be undone.')) {
                          handleDeleteData();
                        }
                      }}
                      className="w-full flex items-center space-x-2 px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
                    >
                      <Trash2 className="h-4 w-4" />
                      <span>Delete All Data</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="text-center hover:scale-105 transition-all duration-300 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
            <div className="flex items-center justify-center mb-3">
              <div className="p-3 bg-blue-500 rounded-full">
                <FileText className="h-6 w-6 text-white" />
              </div>
            </div>
            <div className="text-sm text-gray-600 mb-1 font-medium">Total Analyses</div>
            <div className="text-4xl font-bold text-blue-600 mb-2">
              <AnimatedCounter value={stats?.total_analyses || 0} />
            </div>
            <div className="text-xs text-gray-500">Resume optimizations</div>
          </Card>
          <Card className="text-center hover:scale-105 transition-all duration-300 bg-gradient-to-br from-green-50 to-green-100 border-green-200">
            <div className="flex items-center justify-center mb-3">
              <div className="p-3 bg-green-500 rounded-full">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
            </div>
            <div className="text-sm text-gray-600 mb-1 font-medium">Average Score</div>
            <div className="text-4xl font-bold text-green-600 mb-2">
              <AnimatedCounter value={stats?.average_score ? Math.round(stats.average_score) : 0} />
              <span className="text-2xl">%</span>
            </div>
            <div className="text-xs text-gray-500">ATS compatibility</div>
          </Card>
          <Card className="text-center hover:scale-105 transition-all duration-300 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
            <div className="flex items-center justify-center mb-3">
              <div className="p-3 bg-purple-500 rounded-full">
                <Award className="h-6 w-6 text-white" />
              </div>
            </div>
            <div className="text-sm text-gray-600 mb-1 font-medium">Best Score</div>
            <div className="text-4xl font-bold text-purple-600 mb-2">
              <AnimatedCounter value={stats?.best_score ? Math.round(stats.best_score) : 0} />
              <span className="text-2xl">%</span>
            </div>
            <div className="text-xs text-gray-500">Personal record</div>
          </Card>
          <Card className="text-center hover:scale-105 transition-all duration-300 bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
            <div className="flex items-center justify-center mb-3">
              <div className="p-3 bg-orange-500 rounded-full">
                <Activity className="h-6 w-6 text-white" />
              </div>
            </div>
            <div className="text-sm text-gray-600 mb-1 font-medium">Improvement</div>
            <div className={`text-4xl font-bold mb-2 ${stats?.improvement && stats.improvement > 0 ? 'text-green-600' : 'text-gray-600'}`}>
              {stats?.improvement ? (
                <>
                  <AnimatedCounter value={Math.abs(Math.round(stats.improvement))} />
                  <span className="text-2xl">%</span>
                </>
              ) : '0%'}
            </div>
            <div className="text-xs text-gray-500">Score improvement</div>
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
                        <button
                          onClick={() => handleDeleteAnalysis(item.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="h-4 w-4 inline" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No analyses yet</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by analyzing your first resume.</p>
              <div className="mt-6">
                <Button onClick={() => navigate('/upload')}>
                  Upload Resume
                </Button>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;

