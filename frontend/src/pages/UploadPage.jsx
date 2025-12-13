import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeAPI, jobAPI, analysisAPI } from '../services/api';
import FileUpload from '../components/upload/FileUpload';
import JobInput from '../components/upload/JobInput';
import Button from '../components/common/Button';
import Card from '../components/common/Card';

const UploadPage = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobData, setJobData] = useState({ title: '', company: '', raw_text: '' });
  const [resumeId, setResumeId] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [uploadingResume, setUploadingResume] = useState(false);
  const [savingJob, setSavingJob] = useState(false);
  const navigate = useNavigate();

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setUploadingResume(true);
    setError('');
    try {
      const response = await resumeAPI.upload(resumeFile);
      setResumeId(response.data.id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setUploadingResume(false);
    }
  };

  const handleJobCreate = async () => {
    if (!jobData.raw_text || jobData.raw_text.length < 10) {
      setError('Please enter a job description (at least 10 characters)');
      return;
    }

    setSavingJob(true);
    setError('');
    try {
      const response = await jobAPI.create(jobData);
      setJobId(response.data.id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create job description');
    } finally {
      setSavingJob(false);
    }
  };

  const handleAnalyze = async () => {
    // Check if we have either resumeId (already uploaded) or resumeFile (ready to upload)
    if (!resumeId && !resumeFile) {
      setError('Please upload a resume file first');
      return;
    }
    
    // Check if we have either jobId (already saved) or valid job description text
    if (!jobId && (!jobData.raw_text || jobData.raw_text.length < 10)) {
      setError('Please enter a job description (at least 10 characters)');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Step 1: Upload resume if not already uploaded
      let currentResumeId = resumeId;
      if (!currentResumeId) {
        const resumeResponse = await resumeAPI.upload(resumeFile);
        currentResumeId = resumeResponse.data.id;
        setResumeId(currentResumeId);
      }

      // Step 2: Create job description if not already created
      let currentJobId = jobId;
      if (!currentJobId) {
        const jobResponse = await jobAPI.create(jobData);
        currentJobId = jobResponse.data.id;
        setJobId(currentJobId);
      }

      // Step 3: Run analysis
      const response = await analysisAPI.analyze(currentResumeId, currentJobId);
      navigate(`/results/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analyze Your Resume</h1>
          <p className="text-gray-600">Upload your resume and job description to get instant ATS analysis</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded shadow-sm">
            <div className="flex items-center">
              <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Left: Resume Upload */}
          <Card title="Upload Your Resume">
            <FileUpload onFileSelect={setResumeFile} selectedFile={resumeFile} />
            {resumeFile && !resumeId && (
              <div className="mt-6">
                <Button
                  onClick={handleResumeUpload}
                  loading={uploadingResume}
                  disabled={!resumeFile || uploadingResume}
                  className="w-full"
                >
                  {uploadingResume ? 'Uploading...' : 'Upload Resume'}
                </Button>
              </div>
            )}
            {resumeId && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm flex items-center">
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Resume uploaded successfully
              </div>
            )}
          </Card>

          {/* Right: Job Description */}
          <Card title="Add Job Description">
            <JobInput onJobChange={setJobData} jobData={jobData} />
            {jobData.raw_text && jobData.raw_text.length >= 10 && !jobId && (
              <div className="mt-6">
                <Button
                  onClick={handleJobCreate}
                  loading={savingJob}
                  disabled={!jobData.raw_text || jobData.raw_text.length < 10 || savingJob}
                  className="w-full"
                >
                  {savingJob ? 'Saving...' : 'Save Job Description'}
                </Button>
              </div>
            )}
            {jobId && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm flex items-center">
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Job description saved
              </div>
            )}
          </Card>
        </div>

        {/* Analyze Button */}
        <div className="text-center">
          <Button
            onClick={handleAnalyze}
            loading={loading}
            disabled={(!resumeId && !resumeFile) || (!jobId && (!jobData.raw_text || jobData.raw_text.length < 10)) || loading}
            size="lg"
            className="px-12 py-4 text-lg"
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </Button>
          <p className="mt-4 text-sm text-gray-500">
            {(!resumeId && !resumeFile) && (!jobId && !jobData.raw_text) && 'Please upload a resume and add a job description to continue'}
            {(resumeId || resumeFile) && (!jobId && !jobData.raw_text) && 'Please add a job description to continue'}
            {(!resumeId && !resumeFile) && (jobId || jobData.raw_text) && 'Please upload a resume to continue'}
            {(resumeId || resumeFile) && (jobId || (jobData.raw_text && jobData.raw_text.length >= 10)) && 'Ready to analyze!'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;

