import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useState } from 'react';
import { Menu, X, User, LogOut, Upload, BarChart3, Home } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  return (
    <nav className="bg-white shadow-lg border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-primary-600 rounded-lg p-2">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">AI Resume Optimizer</span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium">
              <Home className="h-4 w-4" />
              <span>Home</span>
            </Link>

            {user ? (
              <>
                <Link to="/upload" className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium">
                  <Upload className="h-4 w-4" />
                  <span>Upload</span>
                </Link>
                <Link to="/dashboard" className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium">
                  <BarChart3 className="h-4 w-4" />
                  <span>Dashboard</span>
                </Link>
                <div className="relative group">
                  <button className="flex items-center space-x-2 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium">
                    <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <User className="h-4 w-4 text-primary-600" />
                    </div>
                    <span>{user.full_name || user.email}</span>
                    <svg className="ml-1 h-4 w-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 border border-gray-100">
                    <button
                      onClick={handleLogout}
                      className="flex items-center space-x-2 w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors duration-200 rounded-lg"
                    >
                      <LogOut className="h-4 w-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-primary-600 px-4 py-2 transition-colors duration-200 font-medium">
                  Login
                </Link>
                <Link to="/signup">
                  <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors duration-200 shadow-md hover:shadow-lg font-semibold">
                    Get Started
                  </button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-primary-600 transition-colors duration-200 p-2"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 border-t border-gray-100">
            <div className="pt-4 space-y-2">
              <Link to="/" className="flex items-center space-x-2 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium" onClick={() => setMobileMenuOpen(false)}>
                <Home className="h-4 w-4" />
                <span>Home</span>
              </Link>

              {user ? (
                <>
                  <Link to="/upload" className="flex items-center space-x-2 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium" onClick={() => setMobileMenuOpen(false)}>
                    <Upload className="h-4 w-4" />
                    <span>Upload</span>
                  </Link>
                  <Link to="/dashboard" className="flex items-center space-x-2 text-gray-700 hover:text-primary-600 px-3 py-2 transition-colors duration-200 font-medium" onClick={() => setMobileMenuOpen(false)}>
                    <BarChart3 className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                  <div className="border-t border-gray-100 pt-2 mt-2">
                    <div className="px-3 py-2 text-sm text-gray-500">
                      Signed in as {user.full_name || user.email}
                    </div>
                    <button
                      onClick={() => {
                        handleLogout();
                        setMobileMenuOpen(false);
                      }}
                      className="flex items-center space-x-2 w-full text-left px-3 py-2 text-gray-700 hover:text-primary-600 transition-colors duration-200 font-medium"
                    >
                      <LogOut className="h-4 w-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <Link to="/login" className="block px-3 py-2 text-gray-700 hover:text-primary-600 transition-colors duration-200 font-medium" onClick={() => setMobileMenuOpen(false)}>
                    Login
                  </Link>
                  <Link to="/signup" className="block px-3 py-2" onClick={() => setMobileMenuOpen(false)}>
                    <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors duration-200 shadow-md font-semibold">
                      Get Started
                    </button>
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;

