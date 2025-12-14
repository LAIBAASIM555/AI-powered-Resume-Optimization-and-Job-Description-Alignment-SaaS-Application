import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { analysisAPI } from '../services/api';
import ScoreCard from '../components/results/ScoreCard';
import SkillsList from '../components/results/SkillsList';
import Recommendations from '../components/results/RecommendationsNew';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import ProgressBar from '../components/common/ProgressBar';
import AnimatedCounter from '../components/common/AnimatedCounter';
import { ArrowLeft, Download, Share2, Calendar, FileText } from 'lucide-react';

const ResultsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await analysisAPI.getOne(id);
        setAnalysis(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load analysis');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchAnalysis();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card>
          <p className="text-red-600">{error || 'Analysis not found'}</p>
          <Button onClick={() => navigate('/upload')} className="mt-4">
            Go to Upload
          </Button>
        </Card>
      </div>
    );
  }

  const breakdown = analysis.score_breakdown || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-6">
            <div className="flex items-center space-x-4">
              <Button
                variant="secondary"
                onClick={() => navigate('/dashboard')}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Dashboard</span>
              </Button>
              <div className="flex items-center space-x-2 text-gray-500">
                <Calendar className="h-4 w-4" />
                <span className="text-sm">{new Date(analysis.created_at).toLocaleDateString()}</span>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                variant="secondary"
                className="flex items-center space-x-2"
                onClick={() => window.print()}
              >
                <Download className="h-4 w-4" />
                <span>Export</span>
              </Button>
              <Button
                variant="secondary"
                className="flex items-center space-x-2"
                onClick={() => navigator.share?.({ title: 'Resume Analysis Results', url: window.location.href })}
              >
                <Share2 className="h-4 w-4" />
                <span>Share</span>
              </Button>
            </div>
          </div>

          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Analysis Results</h1>
            <p className="text-xl text-gray-600">Your resume has been analyzed against the job description</p>
            <div className="flex items-center justify-center space-x-2 mt-3">
              <FileText className="h-5 w-5 text-gray-400" />
              <span className="text-gray-500">{analysis.resume_filename || 'Resume'}</span>
            </div>
          </div>
        </div>

        {/* Score Card */}
        <div className="mb-8 flex justify-center">
          <ScoreCard score={analysis.ats_score} />
        </div>

        {/* Score Breakdown */}
        <Card title="Score Breakdown" className="mb-8 animate-fade-in bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-blue-100">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-semibold text-gray-800">Skills Match</span>
                  <span className="text-2xl font-bold text-blue-600">
                    <AnimatedCounter value={Math.round(breakdown.skills_score || 0)} duration={1500} />
                    <span className="text-lg">%</span>
                  </span>
                </div>
                <ProgressBar value={breakdown.skills_score || 0} />
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-green-100">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-semibold text-gray-800">Experience Alignment</span>
                  <span className="text-2xl font-bold text-green-600">
                    <AnimatedCounter value={Math.round(breakdown.experience_score || 0)} duration={1500} />
                    <span className="text-lg">%</span>
                  </span>
                </div>
                <ProgressBar value={breakdown.experience_score || 0} />
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-purple-100">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-semibold text-gray-800">Keywords Match</span>
                  <span className="text-2xl font-bold text-purple-600">
                    <AnimatedCounter value={Math.round(breakdown.keywords_score || 0)} duration={1500} />
                    <span className="text-lg">%</span>
                  </span>
                </div>
                <ProgressBar value={breakdown.keywords_score || 0} />
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-orange-100">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-semibold text-gray-800">Achievements</span>
                  <span className="text-2xl font-bold text-orange-600">
                    <AnimatedCounter value={Math.round(breakdown.achievements_score || 0)} duration={1500} />
                    <span className="text-lg">%</span>
                  </span>
                </div>
                <ProgressBar value={breakdown.achievements_score || 0} />
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-red-100">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-semibold text-gray-800">Format & Structure</span>
                  <span className="text-2xl font-bold text-red-600">
                    <AnimatedCounter value={Math.round(breakdown.format_score || 0)} duration={1500} />
                    <span className="text-lg">%</span>
                  </span>
                </div>
                <ProgressBar value={breakdown.format_score || 0} />
              </div>
            </div>
          </div>
        </Card>

        {/* Skills Comparison */}
        <Card title="Skills Analysis" className="mb-8 animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <SkillsList
            matched={analysis.matched_skills}
            missing={analysis.missing_skills}
          />
        </Card>

        {/* Recommendations */}
        <div className="mb-8 animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <Recommendations recommendations={analysis.recommendations} />
        </div>

        {/* Summary Section */}
        {analysis.original_summary && (
          <Card title="Summary" className="mb-8">
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Original Summary</h4>
                <p className="text-gray-600">{analysis.original_summary}</p>
              </div>
              {analysis.improved_summary && (
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Improved Summary</h4>
                  <p className="text-gray-600">{analysis.improved_summary}</p>
                </div>
              )}
            </div>
          </Card>
        )}

        {/* Actions */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button onClick={() => navigate('/upload')} variant="primary" size="lg" className="px-8">
            Analyze Another Resume
          </Button>
          <Button onClick={() => navigate('/dashboard')} variant="secondary" size="lg" className="px-8">
            View Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;

