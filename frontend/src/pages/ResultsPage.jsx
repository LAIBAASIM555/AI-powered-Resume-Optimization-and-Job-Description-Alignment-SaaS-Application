import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { analysisAPI } from '../services/api';
import ScoreCard from '../components/results/ScoreCard';
import SkillsList from '../components/results/SkillsList';
import Recommendations from '../components/results/Recommendations';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import ProgressBar from '../components/common/ProgressBar';

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
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between">
          <Button
            variant="secondary"
            onClick={() => navigate('/dashboard')}
          >
            ← Back to Dashboard
          </Button>
          <div className="text-sm text-gray-500">
            {new Date(analysis.created_at).toLocaleString()}
          </div>
        </div>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h1>
          <p className="text-gray-600">Your resume has been analyzed against the job description</p>
        </div>

        {/* Score Card */}
        <div className="mb-8 flex justify-center">
          <ScoreCard score={analysis.ats_score} />
        </div>

        {/* Score Breakdown */}
        <Card title="Score Breakdown" className="mb-8">
          <div className="space-y-4">
            <ProgressBar
              value={breakdown.skills_score || 0}
              label="Skills Match"
            />
            <ProgressBar
              value={breakdown.experience_score || 0}
              label="Experience Alignment"
            />
            <ProgressBar
              value={breakdown.keywords_score || 0}
              label="Keywords Match"
            />
            <ProgressBar
              value={breakdown.achievements_score || 0}
              label="Achievements"
            />
            <ProgressBar
              value={breakdown.format_score || 0}
              label="Format & Structure"
            />
          </div>
        </Card>

        {/* Skills Comparison */}
        <Card title="Skills Analysis" className="mb-8">
          <SkillsList
            matched={analysis.matched_skills}
            missing={analysis.missing_skills}
          />
        </Card>

        {/* Recommendations */}
        <div className="mb-8">
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

