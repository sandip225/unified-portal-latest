import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, LogIn, Shield, Eye, EyeOff } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    const result = await login(email, password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        
        {/* Header with Ashoka Emblem */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 mx-auto mb-4">
            <img 
              src="/portal/ashoka-emblem.webp" 
              alt="Government of India" 
              className="w-full h-full object-contain"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
            <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center" style={{display: 'none'}}>
              <Shield className="w-10 h-10 text-orange-600" />
            </div>
          </div>
          
          {/* Service Icons */}
          <div className="flex justify-center gap-3 mb-4">
            <div className="w-8 h-8 bg-yellow-500 rounded flex items-center justify-center">
              <span className="text-white text-xs">⚡</span>
            </div>
            <div className="w-8 h-8 bg-orange-500 rounded flex items-center justify-center">
              <span className="text-white text-xs">🔥</span>
            </div>
            <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center">
              <span className="text-white text-xs">💧</span>
            </div>
            <div className="w-8 h-8 bg-green-500 rounded flex items-center justify-center">
              <span className="text-white text-xs">🏢</span>
            </div>
          </div>
          
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Unified Services Portal</h1>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          
          {/* Card Header */}
          <div className="bg-blue-600 px-6 py-6 text-white text-center">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-3">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-xl font-bold mb-1">Citizen Login</h2>
            <p className="text-blue-100 text-sm">नागरिक लॉगिन</p>
          </div>

          {/* Form */}
          <div className="p-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg mb-4 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              
              {/* Email Field */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-colors"
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-colors"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-all flex items-center justify-center gap-2 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Logging in...</span>
                  </>
                ) : (
                  <>
                    <LogIn className="w-4 h-4" />
                    <span>Login to Portal</span>
                  </>
                )}
              </button>

              {/* Register Link */}
              <div className="text-center pt-4 border-t border-gray-100 mt-6">
                <p className="text-gray-600 text-sm">
                  Don't have an account?{' '}
                  <Link 
                    to="/register" 
                    className="text-blue-600 font-medium hover:text-blue-700 transition-colors hover:underline"
                  >
                    Register Now
                  </Link>
                </p>
              </div>
            </form>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-xs text-gray-500">
          <p>Government of India | भारत सरकार</p>
          <p className="mt-1">Unified Services Portal for Citizens</p>
        </div>
      </div>
    </div>
  );
};

export default Login;