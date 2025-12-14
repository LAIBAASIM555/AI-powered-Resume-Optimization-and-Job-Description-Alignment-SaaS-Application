import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import Footer from '../components/common/Footer';
import CustomerReviews from '../components/common/CustomerReviews';
import AnimatedCounter from '../components/common/AnimatedCounter';
import { TrendingDown, Users, Target, Zap, FileText, CheckCircle, Lightbulb, Search, BarChart3, Shield } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/5 rounded-full blur-3xl"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="mb-8">
            <span className="inline-block bg-white/20 text-white px-4 py-2 rounded-full text-sm font-medium mb-4">
              🚀 AI-Powered Resume Optimization
            </span>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Get Your Resume Past
              <span className="block text-yellow-300">ATS Systems</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100 max-w-3xl mx-auto leading-relaxed">
              Transform your resume with AI-powered analysis, skill matching, and personalized recommendations to land more interviews
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Link to="/signup">
              <button className="bg-white text-primary-600 hover:bg-primary-50 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 transform">
                Get Started Free
              </button>
            </Link>
            <Link to="/login">
              <button className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 hover:scale-105 transform">
                Login
              </button>
            </Link>
          </div>
          <div className="text-primary-200 text-sm">
            ✓ No credit card required • ✓ Instant results • ✓ 100% Free to start
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
                <TrendingDown className="h-8 w-8 text-red-600" />
              </div>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                <AnimatedCounter value={75} suffix="%" duration={2000} />
              </div>
              <div className="text-gray-600 font-medium">Resumes Rejected by ATS</div>
              <div className="text-sm text-gray-500 mt-1">Industry average</div>
            </div>
            <div className="text-center bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <Users className="h-8 w-8 text-green-600" />
              </div>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                <AnimatedCounter value={10000} suffix="+" duration={2500} />
              </div>
              <div className="text-gray-600 font-medium">Users Optimized</div>
              <div className="text-sm text-gray-500 mt-1">And growing daily</div>
            </div>
            <div className="text-center bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <Target className="h-8 w-8 text-blue-600" />
              </div>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                <AnimatedCounter value={3} suffix="x" duration={1500} />
              </div>
              <div className="text-gray-600 font-medium">More Interviews</div>
              <div className="text-sm text-gray-500 mt-1">Average improvement</div>
            </div>
            <div className="text-center bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
                <Zap className="h-8 w-8 text-purple-600" />
              </div>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                <AnimatedCounter value={95} suffix="%" duration={2000} />
              </div>
              <div className="text-gray-600 font-medium">Success Rate</div>
              <div className="text-sm text-gray-500 mt-1">ATS compatibility</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get your resume optimized in three simple steps with our AI-powered platform
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <span className="text-3xl font-bold text-white">1</span>
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-gray-900">Upload Your Resume</h3>
              <p className="text-gray-600 text-lg leading-relaxed">
                Upload your resume in PDF or DOCX format. Our AI securely processes your document instantly.
              </p>
            </div>
            <div className="text-center group">
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <span className="text-3xl font-bold text-white">2</span>
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-gray-900">Paste Job Description</h3>
              <p className="text-gray-600 text-lg leading-relaxed">
                Copy and paste the job description you're interested in. We'll analyze the requirements.
              </p>
            </div>
            <div className="text-center group">
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <span className="text-3xl font-bold text-white">3</span>
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-gray-900">Get Instant Analysis</h3>
              <p className="text-gray-600 text-lg leading-relaxed">
                Receive your ATS score, skill matching analysis, and actionable recommendations within seconds.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Powerful Features</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to optimize your resume and beat ATS systems
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: FileText, title: 'ATS Score Analysis', desc: 'Get detailed compatibility scores with ATS systems and major job boards' },
              { icon: CheckCircle, title: 'Skill Matching', desc: 'Advanced AI matching of your skills with job requirements' },
              { icon: Lightbulb, title: 'Smart Recommendations', desc: 'Actionable, personalized tips to improve your resume effectiveness' },
              { icon: Search, title: 'Keyword Optimization', desc: 'Optimize keyword usage for better search visibility' },
              { icon: Shield, title: 'Format Validation', desc: 'Ensure your resume follows ATS-friendly formatting standards' },
              { icon: BarChart3, title: 'Progress Tracking', desc: 'Monitor your resume improvements over time with detailed analytics' },
            ].map((feature, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 animate-fade-in" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="inline-flex items-center justify-center w-14 h-14 bg-primary-100 rounded-lg mb-6">
                  <feature.icon className="h-7 w-7 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Customer Reviews */}
      <CustomerReviews />

      {/* Final CTA */}
      <section className="py-20 bg-primary-600 text-white text-center">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-4">Ready to Optimize Your Resume?</h2>
          <p className="text-xl mb-8 text-primary-100">Start getting more interviews today</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup">
              <button className="bg-white text-primary-600 hover:bg-primary-50 px-8 py-4 rounded-lg font-semibold text-lg transition-colors duration-200 shadow-lg hover:shadow-xl">
                Get Started Now
              </button>
            </Link>
            <Link to="/login">
              <button className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg transition-colors duration-200">
                Login
              </button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default HomePage;

