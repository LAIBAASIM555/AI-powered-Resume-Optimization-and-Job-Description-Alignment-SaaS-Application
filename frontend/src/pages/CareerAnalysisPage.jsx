import { useState, useEffect, useRef } from 'react';
import { Helmet } from 'react-helmet-async';
import { toast } from 'react-hot-toast';
import {
  Sparkles, Target, Briefcase, TrendingUp, GraduationCap,
  DollarSign, Star, ChevronDown, ChevronUp, CheckCircle,
  XCircle, Lightbulb, BarChart3, Compass, Rocket, BookOpen,
  Layers, Upload, FileText, AlertCircle, Zap, Brain,
  ArrowRight, Shield
} from 'lucide-react';
import { resumeAPI } from '../services/api';
import api from '../services/api';

export default function CareerAnalysisPage() {
  const [resumes, setResumes]               = useState([]);
  const [selectedResume, setSelectedResume] = useState('');
  const [analysis, setAnalysis]             = useState(null);
  const [loading, setLoading]               = useState(false);
  const [loadingStep, setLoadingStep]       = useState(0);
  const [error, setError]                   = useState(null);
  const [expandedCareer, setExpandedCareer] = useState(null);
  const [loadingResumes, setLoadingResumes] = useState(true);
  const [uploadLoading, setUploadLoading]   = useState(false);
  const [uploadError, setUploadError]       = useState(null);
  const [dragActive, setDragActive]         = useState(false);
  const fileInputRef = useRef(null);
  const stepTimerRef = useRef(null);

  useEffect(() => { fetchResumes(); }, []);

  /* ── Data fetch ── */
  const fetchResumes = async () => {
    try {
      const res = await api.get('/resume/');
      const raw = res.data?.resumes || res.data || [];
      const seen = new Map();
      for (const r of raw) {
        const name = r.filename || r.file_name || `Resume #${r.id}`;
        if (!seen.has(name) || r.id > seen.get(name).id) seen.set(name, r);
      }
      const data = Array.from(seen.values());
      setResumes(data);
      if (data.length > 0) setSelectedResume(data[0].id);
    } catch { /* silent */ } finally { setLoadingResumes(false); }
  };

  /* ── Upload ── */
  const handleDrop = async (e) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer?.files?.[0] || e.target?.files?.[0];
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'doc'].includes(ext)) {
      setUploadError('Only PDF or DOCX files are accepted.');
      return;
    }
    setUploadLoading(true);
    setUploadError(null);
    const t = toast.loading('Uploading & parsing resume…');
    try {
      const res = await resumeAPI.upload(file);
      const newResume = res.data;
      setResumes(prev => {
        const filtered = prev.filter(
          r => (r.filename || r.file_name) !== (newResume.filename || newResume.file_name)
        );
        return [newResume, ...filtered];
      });
      setSelectedResume(newResume.id);
      toast.success('Resume uploaded! Ready to analyze.', { id: t });
    } catch (err) {
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'object'
        ? (detail.reason || detail.message || 'Resume rejected — not a valid CV.')
        : (detail || 'Upload failed. Please try again.');
      setUploadError(msg);
      toast.error(msg, { id: t });
    } finally { setUploadLoading(false); }
  };

  /* ── Analyze ── */
  const LOADING_STEPS = [
    { icon: FileText,  label: 'Reading your resume...',      detail: 'Extracting text and structure' },
    { icon: Brain,     label: 'Identifying your skills...',  detail: 'Matching skills from 800+ skill database' },
    { icon: Briefcase, label: 'Scoring career matches...',   detail: 'Analyzing 30+ career paths for you' },
    { icon: Sparkles,  label: 'Building your report...',     detail: 'Ranking careers by best fit' },
  ];

  const handleAnalyze = async () => {
    if (!selectedResume) { toast.error('Please select or upload a resume first.'); return; }
    setLoading(true);
    setLoadingStep(0);
    setError(null);
    setAnalysis(null);
    const t = toast.loading('Analyzing your career profile…');

    // Advance steps at timed intervals to show progress
    let step = 0;
    stepTimerRef.current = setInterval(() => {
      step += 1;
      if (step < LOADING_STEPS.length) setLoadingStep(step);
      else clearInterval(stepTimerRef.current);
    }, 1800);

    try {
      const res = await api.post('/career/analyze', { resume_id: Number(selectedResume) });
      clearInterval(stepTimerRef.current);
      setLoadingStep(LOADING_STEPS.length); // mark all done
      setAnalysis(res.data);
      toast.success('Career analysis complete!', { id: t });
    } catch (err) {
      clearInterval(stepTimerRef.current);
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'string' ? detail : 'Analysis failed. Please try again.';
      setError(msg);
      toast.error(msg, { id: t });
    } finally { setLoading(false); setLoadingStep(0); }
  };

  /* ── Helpers ── */
  const getMatchGradient = (p) => p >= 75 ? 'from-emerald-500 to-green-400' : p >= 55 ? 'from-blue-500 to-cyan-400' : p >= 40 ? 'from-yellow-500 to-orange-400' : 'from-rose-500 to-pink-400';
  const getMatchBorder   = (p) => p >= 75 ? 'border-emerald-500/30 bg-emerald-500/5' : p >= 55 ? 'border-blue-500/30 bg-blue-500/5' : p >= 40 ? 'border-yellow-500/30 bg-yellow-500/5' : 'border-rose-500/30 bg-rose-500/5';
  const getDemandColor   = (d) => ({ 'Extremely High': 'text-purple-400', 'Very High': 'text-emerald-400', 'High': 'text-blue-400', 'Growing': 'text-cyan-400', 'Medium': 'text-yellow-400' })[d] || 'text-slate-400';

  /* ── Render ── */
  return (
    <>
      <Helmet>
        <title>Career Path Analyzer | ResumeAI</title>
        <meta name="description" content="Discover which careers match your resume skills and what to learn next." />
      </Helmet>

      <div className="min-h-screen bg-slate-50 dark:bg-[#030712] transition-colors duration-500 font-sans text-slate-900 dark:text-slate-300 relative pt-24 pb-20 overflow-hidden">

        {/* ── Background Decor (matches UploadPage) ── */}
        <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.03] dark:opacity-[0.05]">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#808080_1px,transparent_1px),linear-gradient(to_bottom,#808080_1px,transparent_1px)] bg-[size:24px_24px]" />
        </div>
        <div className="absolute top-[10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-600/10 dark:bg-indigo-600/20 blur-[120px] pointer-events-none z-0" />
        <div className="absolute bottom-[10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-purple-600/10 dark:bg-purple-600/20 blur-[120px] pointer-events-none z-0" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">

          {/* ── Page Header ── */}
          <div className="text-center mb-12 max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 text-indigo-600 dark:text-cyan-400 text-xs font-bold uppercase tracking-wider mb-6 shadow-sm">
              <Zap className="h-4 w-4 text-amber-500" /> AI-Powered Career Analysis
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-black text-slate-900 dark:text-white mb-6 tracking-tight">
              Career Path{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-500 dark:from-indigo-400 dark:to-purple-400">
                Analyzer
              </span>
            </h1>
            <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 font-medium dark:font-normal leading-relaxed">
              Drop your resume — discover which careers match your skills, what salary to expect, and exactly what to learn next.
            </p>
          </div>

          {/* ── Feature Cards (what you'll get) ── */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            {[
              { icon: Star,        color: 'from-indigo-500 to-indigo-600',  bg: 'bg-indigo-500/10', title: 'Best Career Match',     desc: 'Top career that fits your current skills with % score' },
              { icon: Briefcase,   color: 'from-blue-500 to-cyan-500',      bg: 'bg-blue-500/10',   title: '25+ Careers Ranked',     desc: 'Every eligible career scored &amp; ranked by match' },
              { icon: Lightbulb,   color: 'from-yellow-500 to-orange-400',  bg: 'bg-yellow-500/10', title: 'Skills to Learn',        desc: 'Exact skills that unlock higher-paying careers' },
              { icon: TrendingUp,  color: 'from-emerald-500 to-green-400',  bg: 'bg-emerald-500/10',title: 'Market Insights',        desc: 'Salary ranges, demand &amp; growth rate per career' },
            ].map(({ icon: Icon, color, bg, title, desc }) => (
              <div key={title} className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-2xl shadow-sm dark:shadow-none border border-slate-200 dark:border-white/10 p-5">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center mb-3 shadow-lg`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <p className="font-bold text-slate-900 dark:text-white text-sm mb-1">{title}</p>
                <p className="text-slate-500 dark:text-slate-400 text-xs leading-snug" dangerouslySetInnerHTML={{ __html: desc }} />
              </div>
            ))}
          </div>

          {/* ── Upload & Select Card ── */}
          <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-3xl shadow-xl dark:shadow-none border border-slate-200 dark:border-white/10 p-8 md:p-10 mb-8 relative overflow-hidden">
            {/* bg icon */}
            <div className="absolute top-0 right-0 p-8 opacity-[0.03] dark:opacity-[0.05] pointer-events-none">
              <Compass className="w-48 h-48 rotate-12" />
            </div>

            <div className="flex items-center gap-5 mb-8 relative z-10">
              <div className="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/20 border border-white/10">
                <Brain className="h-7 w-7 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-black text-slate-900 dark:text-white">Upload Your Resume</h2>
                <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 text-sm font-semibold mt-1">
                  <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full" /> Step 1 — Drop or select a resume
                </div>
              </div>
            </div>

            <div className="relative z-10 space-y-4">
              {/* Drag & Drop Zone */}
              <div
                onDragEnter={(e) => { e.preventDefault(); setDragActive(true); }}
                onDragOver={(e)  => { e.preventDefault(); setDragActive(true); }}
                onDragLeave={(e) => { e.preventDefault(); setDragActive(false); }}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`cursor-pointer border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-200 ${
                  dragActive
                    ? 'border-indigo-500 bg-indigo-500/10 scale-[1.01]'
                    : 'border-slate-300 dark:border-slate-700 hover:border-indigo-400 dark:hover:border-indigo-500 hover:bg-indigo-500/5'
                }`}
              >
                <input ref={fileInputRef} type="file" accept=".pdf,.doc,.docx" className="hidden" onChange={handleDrop} />
                {uploadLoading ? (
                  <div className="flex flex-col items-center gap-3 text-indigo-400">
                    <div className="w-8 h-8 border-2 border-indigo-400/30 border-t-indigo-400 rounded-full animate-spin" />
                    <span className="text-sm font-semibold">Uploading &amp; parsing resume…</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 dark:bg-indigo-500/20 flex items-center justify-center">
                      <Upload className="w-7 h-7 text-indigo-500 dark:text-indigo-400" />
                    </div>
                    <div>
                      <p className="font-bold text-slate-800 dark:text-white text-base">
                        <span className="text-indigo-600 dark:text-indigo-400">Click to upload</span> or drag &amp; drop
                      </p>
                      <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">PDF, DOC, DOCX — max 5MB</p>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-slate-400 dark:text-slate-500">
                      <Shield className="w-3 h-3" /> Validated &amp; parsed securely
                    </div>
                  </div>
                )}
              </div>

              {/* Upload error */}
              {uploadError && (
                <div className="flex items-start gap-3 p-4 bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 rounded-2xl animate-fade-in">
                  <AlertCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-rose-600 dark:text-rose-400 font-semibold text-sm">Resume Rejected</p>
                    <p className="text-rose-500 dark:text-rose-400/80 text-xs mt-0.5">{uploadError}</p>
                  </div>
                </div>
              )}

              {/* Divider */}
              <div className="flex items-center gap-3">
                <div className="flex-1 h-px bg-slate-200 dark:bg-slate-800" />
                <span className="text-xs text-slate-400 dark:text-slate-500 font-semibold uppercase tracking-wider">or choose existing</span>
                <div className="flex-1 h-px bg-slate-200 dark:bg-slate-800" />
              </div>

              {/* Dropdown */}
              {loadingResumes ? (
                <div className="h-12 bg-slate-100 dark:bg-slate-800 rounded-xl animate-pulse" />
              ) : resumes.length === 0 ? (
                <p className="text-center text-slate-400 dark:text-slate-500 text-sm py-2">No saved resumes yet — drop one above!</p>
              ) : (
                <select
                  value={selectedResume}
                  onChange={(e) => setSelectedResume(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-3.5 text-slate-900 dark:text-white focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all font-medium"
                >
                  {resumes.map((r) => {
                    const name = r.filename || r.file_name || `Resume #${r.id}`;
                    const date = r.created_at
                      ? new Date(r.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
                      : null;
                    return <option key={r.id} value={r.id}>{name}{date ? ` — ${date}` : ''}</option>;
                  })}
                </select>
              )}
            </div>
          </div>

          {/* ── Step Loading Overlay ── */}
          {loading && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-3xl p-10 w-full max-w-md mx-4 shadow-2xl">
                <div className="text-center mb-8">
                  <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-indigo-500/30">
                    <Brain className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-black text-slate-900 dark:text-white">Analyzing Career Profile</h3>
                  <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Please wait while we process your resume…</p>
                </div>

                <div className="space-y-3">
                  {LOADING_STEPS.map((step, idx) => {
                    const Icon = step.icon;
                    const done    = idx < loadingStep;
                    const active  = idx === loadingStep;
                    const pending = idx > loadingStep;
                    return (
                      <div key={idx} className={`flex items-center gap-4 p-3 rounded-xl transition-all duration-500 ${
                        active  ? 'bg-indigo-500/10 border border-indigo-500/20' :
                        done    ? 'opacity-60' : 'opacity-30'
                      }`}>
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 transition-all ${
                          done   ? 'bg-emerald-500' :
                          active ? 'bg-indigo-500' : 'bg-slate-200 dark:bg-slate-700'
                        }`}>
                          {done ? (
                            <CheckCircle className="w-4 h-4 text-white" />
                          ) : active ? (
                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          ) : (
                            <Icon className="w-4 h-4 text-slate-400" />
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className={`font-semibold text-sm ${
                            done || active ? 'text-slate-900 dark:text-white' : 'text-slate-400 dark:text-slate-600'
                          }`}>{step.label}</p>
                          {active && (
                            <p className="text-xs text-indigo-400 mt-0.5">{step.detail}</p>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Progress bar */}
                <div className="mt-6 h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-700"
                    style={{ width: `${(loadingStep / LOADING_STEPS.length) * 100}%` }}
                  />
                </div>
                <p className="text-center text-xs text-slate-400 dark:text-slate-500 mt-2">
                  Step {Math.min(loadingStep + 1, LOADING_STEPS.length)} of {LOADING_STEPS.length}
                </p>
              </div>
            </div>
          )}

          {/* ── Analyze Button ── */}
          <div className="text-center mb-12 relative">
            <div className="max-w-md mx-auto relative group">
              {selectedResume && (
                <div className="absolute -inset-1.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 rounded-2xl blur opacity-50 dark:opacity-70 group-hover:opacity-100 transition duration-300" />
              )}
              <button
                onClick={handleAnalyze}
                disabled={loading || !selectedResume}
                className={`w-full relative h-16 text-lg font-black tracking-wide rounded-2xl transition-all duration-300 flex items-center justify-center gap-3 ${
                  selectedResume
                    ? 'bg-slate-900 dark:bg-slate-900 border border-transparent dark:border-white/10 text-white hover:bg-slate-800'
                    : 'bg-slate-200 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 border border-transparent dark:border-white/5 cursor-not-allowed'
                }`}
              >
                {loading ? (
                  <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <Sparkles className={`h-6 w-6 ${selectedResume ? 'text-indigo-400' : ''}`} />
                )}
                {loading ? 'Analyzing your career profile…' : 'Analyze My Career'}
                {!loading && selectedResume && <ArrowRight className="h-5 w-5 text-slate-400" />}
              </button>
            </div>
          </div>

          {/* ── Error ── */}
          {error && (
            <div className="mb-8 p-5 bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 rounded-2xl animate-fade-in flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-rose-500 shrink-0 mt-0.5" />
              <p className="text-rose-600 dark:text-rose-400 font-medium">{error}</p>
            </div>
          )}

          {/* ── Results ── */}
          {analysis && (
            <div className="space-y-6 animate-fade-in">

              {/* What We Did Banner */}
              <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-2xl p-5 flex flex-wrap gap-4">
                {[
                  { icon: Brain,      color: 'text-indigo-400 bg-indigo-500/10',  label: 'Scanned your resume text' },
                  { icon: Zap,        color: 'text-yellow-400 bg-yellow-500/10',  label: `Identified ${analysis.skills_summary?.total_skills_found ?? 0} skills` },
                  { icon: Briefcase,  color: 'text-blue-400 bg-blue-500/10',      label: 'Scored 25+ career paths' },
                  { icon: TrendingUp, color: 'text-emerald-400 bg-emerald-500/10',label: 'Ranked by best match %' },
                ].map(({ icon: Icon, color, label }) => (
                  <div key={label} className="flex items-center gap-2">
                    <div className={`w-7 h-7 rounded-lg ${color} flex items-center justify-center`}>
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">{label}</span>
                  </div>
                ))}
              </div>

              {/* Best Fit */}
              {analysis.best_fit && (
                <div className="relative overflow-hidden bg-gradient-to-br from-indigo-600/20 via-purple-600/15 to-pink-600/10 dark:from-indigo-500/20 dark:via-purple-500/15 dark:to-pink-500/10 border border-indigo-500/30 rounded-3xl p-8 shadow-xl">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full -translate-y-32 translate-x-32 blur-3xl" />
                  <div className="relative">
                    <div className="flex items-center gap-2 text-indigo-400 dark:text-indigo-300 text-xs font-bold uppercase tracking-widest mb-3">
                      <Star className="w-4 h-4 fill-current" /> Best Career Match For You
                    </div>
                    <div className="flex flex-col lg:flex-row justify-between items-start gap-6">
                      <div className="flex-1">
                        <h2 className="text-3xl font-black text-slate-900 dark:text-white mb-1">{analysis.best_fit.career_title}</h2>
                        <p className="text-indigo-600 dark:text-indigo-300 font-semibold mb-2">{analysis.best_fit.field}</p>
                        <p className="text-slate-600 dark:text-slate-400 text-sm max-w-xl mb-4">{analysis.best_fit.description}</p>
                        <div className="flex flex-wrap gap-3 text-sm">
                          <span className={`flex items-center gap-1.5 font-semibold ${getDemandColor(analysis.best_fit.market_demand)}`}>
                            <TrendingUp className="w-4 h-4" /> {analysis.best_fit.market_demand} Demand
                          </span>
                          <span className="flex items-center gap-1.5 text-blue-500">
                            <BarChart3 className="w-4 h-4" /> {analysis.best_fit.growth_rate} Growth
                          </span>
                          <span className="flex items-center gap-1.5 text-emerald-500">
                            <DollarSign className="w-4 h-4" /> {analysis.best_fit.salary_range}
                          </span>
                          <span className="flex items-center gap-1.5 text-purple-500">
                            <GraduationCap className="w-4 h-4" /> {analysis.best_fit.experience_level}
                          </span>
                        </div>
                      </div>
                      <div className="text-center shrink-0">
                        <div className={`text-6xl font-black bg-gradient-to-br ${getMatchGradient(analysis.best_fit.match_percentage)} bg-clip-text text-transparent leading-none`}>
                          {analysis.best_fit.match_percentage}%
                        </div>
                        <p className="text-slate-500 dark:text-slate-400 text-xs mt-1 uppercase tracking-wider">Match Score</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 pt-6 border-t border-white/10">
                      <div>
                        <p className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider mb-2">
                          <CheckCircle className="w-3.5 h-3.5" /> Skills You Have ({analysis.best_fit.matched_skills.length})
                        </p>
                        <div className="flex flex-wrap gap-1.5">
                          {analysis.best_fit.matched_skills.map((s, i) => (
                            <span key={i} className="px-2.5 py-0.5 bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 text-xs rounded-full border border-emerald-500/25">{s}</span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <p className="flex items-center gap-1.5 text-rose-500 dark:text-rose-400 text-xs font-bold uppercase tracking-wider mb-2">
                          <XCircle className="w-3.5 h-3.5" /> Skills to Learn ({analysis.best_fit.missing_skills.length})
                        </p>
                        <div className="flex flex-wrap gap-1.5">
                          {analysis.best_fit.missing_skills.slice(0, 12).map((s, i) => (
                            <span key={i} className="px-2.5 py-0.5 bg-rose-500/10 text-rose-500 dark:text-rose-400 text-xs rounded-full border border-rose-500/20">{s}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Stats Row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { icon: Briefcase,    color: 'text-blue-500',   bg: 'bg-blue-500/10',   label: 'Eligible Careers', value: analysis.overall_profile?.total_eligible_careers ?? 0 },
                  { icon: Layers,       color: 'text-purple-500', bg: 'bg-purple-500/10', label: 'Fields Open',       value: analysis.overall_profile?.total_eligible_fields ?? 0 },
                  { icon: Target,       color: 'text-emerald-500',bg: 'bg-emerald-500/10',label: 'Skills Found',      value: analysis.skills_summary?.total_skills_found ?? 0 },
                  { icon: GraduationCap,color: 'text-orange-500', bg: 'bg-orange-500/10', label: 'Your Level',        value: analysis.overall_profile?.career_level ?? 'N/A', small: true },
                ].map(({ icon: Icon, color, bg, label, value, small }) => (
                  <div key={label} className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-2xl p-5 text-center shadow-sm">
                    <div className={`inline-flex p-2 rounded-xl ${bg} mb-3`}>
                      <Icon className={`w-5 h-5 ${color}`} />
                    </div>
                    <p className={`font-black text-slate-900 dark:text-white ${small ? 'text-base' : 'text-3xl'}`}>{value}</p>
                    <p className="text-slate-500 dark:text-slate-400 text-xs mt-1 font-medium">{label}</p>
                  </div>
                ))}
              </div>

              {/* Eligible Fields */}
              {analysis.eligible_fields?.length > 0 && (
                <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-6 shadow-sm">
                  <h3 className="flex items-center gap-2 text-lg font-black text-slate-900 dark:text-white mb-4">
                    <Layers className="w-5 h-5 text-purple-500" /> Fields You Can Enter
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {analysis.eligible_fields.map((f, i) => (
                      <div key={i} className="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/50 rounded-2xl p-4">
                        <h4 className="font-bold text-slate-900 dark:text-white text-sm">{f.field}</h4>
                        <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5 mb-2">{f.description}</p>
                        <div className="flex flex-wrap gap-1">
                          {f.matching_careers.map((c, ci) => (
                            <span key={ci} className="px-2 py-0.5 bg-indigo-500/10 text-indigo-600 dark:text-indigo-300 text-xs rounded-lg border border-indigo-500/20">{c}</span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* All Eligible Careers */}
              {analysis.eligible_careers?.length > 0 && (
                <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-6 shadow-sm">
                  <h3 className="flex items-center gap-2 text-lg font-black text-slate-900 dark:text-white mb-4">
                    <Briefcase className="w-5 h-5 text-blue-500" /> All Careers You're Eligible For
                  </h3>
                  <div className="space-y-2">
                    {analysis.eligible_careers.map((career, idx) => (
                      <div
                        key={idx}
                        className={`border rounded-2xl p-4 cursor-pointer transition-all hover:shadow-md ${getMatchBorder(career.match_percentage)}`}
                        onClick={() => setExpandedCareer(expandedCareer === idx ? null : idx)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className={`text-2xl font-black bg-gradient-to-r ${getMatchGradient(career.match_percentage)} bg-clip-text text-transparent w-16 shrink-0`}>
                              {career.match_percentage}%
                            </span>
                            <div>
                              <p className="font-bold text-slate-900 dark:text-white text-sm">{career.career_title}</p>
                              <p className="text-slate-500 dark:text-slate-400 text-xs">
                                {career.field} • <span className={getDemandColor(career.market_demand)}>{career.market_demand}</span> • {career.salary_range}
                              </p>
                            </div>
                          </div>
                          {expandedCareer === idx ? <ChevronUp className="w-4 h-4 text-slate-400 shrink-0" /> : <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />}
                        </div>

                        {expandedCareer === idx && (
                          <div className="mt-4 pt-4 border-t border-slate-200 dark:border-white/10">
                            <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">{career.description}</p>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                              <div>
                                <p className="text-emerald-600 dark:text-emerald-400 text-xs font-bold mb-1.5">✓ Your Skills ({career.matched_skills.length})</p>
                                <div className="flex flex-wrap gap-1">
                                  {career.matched_skills.map((s, i) => (
                                    <span key={i} className="px-2 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs rounded-full">{s}</span>
                                  ))}
                                </div>
                              </div>
                              <div>
                                <p className="text-rose-500 dark:text-rose-400 text-xs font-bold mb-1.5">✗ To Learn ({career.missing_skills.length})</p>
                                <div className="flex flex-wrap gap-1">
                                  {career.missing_skills.slice(0, 8).map((s, i) => (
                                    <span key={i} className="px-2 py-0.5 bg-rose-500/10 text-rose-500 dark:text-rose-400 text-xs rounded-full">{s}</span>
                                  ))}
                                </div>
                              </div>
                            </div>
                            <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
                              <span>Level: {career.experience_level}</span>
                              <span>Growth: {career.growth_rate}</span>
                              {career.alternate_titles?.length > 0 && (
                                <span>Also: {career.alternate_titles.slice(0, 3).join(', ')}</span>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Future Careers */}
              {analysis.future_careers?.length > 0 && (
                <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-6 shadow-sm">
                  <h3 className="flex items-center gap-2 text-lg font-black text-slate-900 dark:text-white mb-4">
                    <Rocket className="w-5 h-5 text-orange-500" /> Careers You Could Reach
                    <span className="text-slate-400 dark:text-slate-500 text-sm font-normal ml-1">(learn more skills)</span>
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {analysis.future_careers.slice(0, 6).map((career, idx) => (
                      <div key={idx} className="bg-orange-50 dark:bg-orange-500/5 border border-orange-200 dark:border-orange-500/20 rounded-2xl p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <p className="font-bold text-slate-900 dark:text-white text-sm">{career.career_title}</p>
                            <p className="text-slate-500 dark:text-slate-400 text-xs">{career.field}</p>
                          </div>
                          <span className="text-orange-500 font-black text-sm">{career.match_percentage}%</span>
                        </div>
                        <div className="space-y-1">
                          {career.recommendations.map((rec, i) => (
                            <p key={i} className="flex items-start gap-1.5 text-xs text-slate-600 dark:text-slate-400">
                              <Lightbulb className="w-3 h-3 text-yellow-500 mt-0.5 shrink-0" /> {rec}
                            </p>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top Skills to Learn */}
              {analysis.skills_summary?.skills_to_learn?.length > 0 && (
                <div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-6 shadow-sm">
                  <h3 className="flex items-center gap-2 text-lg font-black text-slate-900 dark:text-white mb-4">
                    <BookOpen className="w-5 h-5 text-cyan-500" /> Top Skills to Learn for Career Growth
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis.skills_summary.skills_to_learn.map((skill, i) => (
                      <span key={i} className="px-3 py-1.5 bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-200 dark:border-cyan-500/20 text-cyan-700 dark:text-cyan-300 rounded-xl text-sm font-semibold">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}
        </div>
      </div>
    </>
  );
}
