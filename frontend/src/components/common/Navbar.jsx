import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useState } from 'react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-blue-600">
              AI Resume Optimizer
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <>
                <Link to="/upload" className="text-gray-700 hover:text-blue-600 px-3 py-2">
                  Upload
                </Link>
                <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2">
                  Dashboard
                </Link>
                <div className="relative group">
                  <button className="text-gray-700 hover:text-blue-600 px-3 py-2 flex items-center">
                    {user.full_name}
                    <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition">
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-blue-600 px-3 py-2">
                  Login
                </Link>
                <Link to="/signup">
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Sign Up
                  </button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-blue-600"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4">
            {user ? (
              <>
                <Link to="/upload" className="block px-3 py-2 text-gray-700 hover:text-blue-600">
                  Upload
                </Link>
                <Link to="/dashboard" className="block px-3 py-2 text-gray-700 hover:text-blue-600">
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-3 py-2 text-gray-700 hover:text-blue-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="block px-3 py-2 text-gray-700 hover:text-blue-600">
                  Login
                </Link>
                <Link to="/signup" className="block px-3 py-2 text-gray-700 hover:text-blue-600">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;

