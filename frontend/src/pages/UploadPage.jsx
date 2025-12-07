import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeAPI, jobAPI, analysisAPI } from '../services/api';
import FileUpload from '../components/upload/FileUpload';
import JobInput from '../components/upload/JobInput';
import Button from '../components/common/Button';
import Card from '../components/common/Card';

const UploadPage = () => {
  const [step, setStep] = useState(1);
  const [resumeFile, setResumeFile] = useState(null);
  const [jobData, setJobData] = useState({ title: '', company: '', raw_text: '' });
  const [resumeId, setResumeId] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await resumeAPI.upload(resumeFile);
      setResumeId(response.data.id);
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setLoading(false);
    }
  };

  const handleJobCreate = async () => {
    if (!jobData.raw_text || jobData.raw_text.length < 10) {
      setError('Please enter a job description (at least 10 characters)');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await jobAPI.create(jobData);
      setJobId(response.data.id);
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create job description');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!resumeId || !jobId) {
      setError('Please complete both steps');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await analysisAPI.analyze(resumeId, jobId);
      navigate(`/results/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Step Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    step >= s ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
                  }`}
                >
                  {s}
                </div>
                {s < 3 && (
                  <div
                    className={`w-16 h-1 ${step > s ? 'bg-blue-600' : 'bg-gray-300'}`}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-center mt-4 space-x-16">
            <span className={step >= 1 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Upload Resume
            </span>
            <span className={step >= 2 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Add Job Description
            </span>
            <span className={step >= 3 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Analyze
            </span>
          </div>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-8">
          {/* Left: Resume Upload */}
          <Card title="Step 1: Upload Your Resume">
            <FileUpload onFileSelect={setResumeFile} selectedFile={resumeFile} />
            {step === 1 && (
              <div className="mt-6">
                <Button
                  onClick={handleResumeUpload}
                  loading={loading}
                  disabled={!resumeFile}
                  className="w-full"
                >
                  Upload Resume
                </Button>
              </div>
            )}
            {step > 1 && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded text-green-700 text-sm">
                ✓ Resume uploaded successfully
              </div>
            )}
          </Card>

          {/* Right: Job Description */}
          <Card title="Step 2: Add Job Description">
            <JobInput onJobChange={setJobData} jobData={jobData} />
            {step === 2 && (
              <div className="mt-6">
                <Button
                  onClick={handleJobCreate}
                  loading={loading}
                  disabled={!jobData.raw_text || jobData.raw_text.length < 10}
                  className="w-full"
                >
                  Save Job Description
                </Button>
              </div>
            )}
            {step > 2 && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded text-green-700 text-sm">
                ✓ Job description saved
              </div>
            )}
          </Card>
        </div>

        {/* Analyze Button */}
        {step >= 3 && (
          <div className="mt-8 text-center">
            <Button
              onClick={handleAnalyze}
              loading={loading}
              size="lg"
              className="px-12"
            >
              Analyze Resume
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;

