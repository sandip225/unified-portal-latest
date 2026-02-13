import { useState } from 'react';
import { useLocation, useNavigate, useParams, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, Loader, AlertCircle, Play } from 'lucide-react';

const FinalFormPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { serviceType, providerId } = useParams();
  
  const { extractedData, documents } = location.state || {};
  
  const [formData, setFormData] = useState({
    // Pre-filled from documents
    name: extractedData?.identityProof?.name || '',
    address: extractedData?.identityProof?.address || extractedData?.addressProof?.address || '',
    serviceNumber: extractedData?.addressProof?.serviceNumber || '',
    oldName: extractedData?.nameChangeProof?.oldName || '',
    newName: extractedData?.nameChangeProof?.newName || '',
    
    // To be filled by user
    mobile: '',
    email: '',
    confirmEmail: '',
    city: 'Ahmedabad',
    tNumber: ''
  });
  
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user types
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.mobile || formData.mobile.length < 10) {
      newErrors.mobile = 'Valid 10-digit mobile number required';
    }
    
    if (!formData.email || !formData.email.includes('@')) {
      newErrors.email = 'Valid email address required';
    }
    
    if (formData.email !== formData.confirmEmail) {
      newErrors.confirmEmail = 'Email addresses do not match';
    }
    
    if (providerId === 'torrent-power' && !formData.tNumber) {
      newErrors.tNumber = 'T Number is required for Torrent Power';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    // Submit form directly
    navigate('/applications', {
      state: {
        success: true,
        message: 'Application submitted successfully!',
        formData: formData
      }
    });
  };

  // Provider-specific configurations
  const providerNames = {
    'torrent-power': 'Torrent Power',
    'pgvcl': 'PGVCL',
    'ugvcl': 'UGVCL',
    'mgvcl': 'MGVCL',
    'dgvcl': 'DGVCL',
    'gujarat-gas': 'Gujarat Gas',
    'adani-gas': 'Adani Gas',
    'amc-water': 'AMC Water',
    'anyror': 'AnyRoR'
  };

  const providerName = providerNames[providerId] || 'Provider';

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            to={`/utility-services/${serviceType}/${providerId}/document-upload`}
            className="inline-flex items-center gap-2 text-white hover:text-blue-100 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Documents</span>
          </Link>
          
          <h1 className="text-3xl font-bold mb-2">Final Application Form</h1>
          <p className="text-blue-100">{providerName} - Name Change Application</p>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Success Message */}
        <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6 mb-8">
          <div className="flex items-start gap-4">
            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-green-900 mb-2">
                🎉 Documents Processed Successfully!
              </h3>
              <p className="text-sm text-green-700">
                AI has extracted data from your documents. Review the pre-filled information and complete the remaining fields.
              </p>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8">
          {/* Pre-filled Data Section */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              Pre-filled from Documents
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Name */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Current Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  disabled
                  className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg text-gray-600 cursor-not-allowed"
                />
                <p className="text-xs text-green-600 mt-1">✓ Extracted from Identity Proof</p>
              </div>

              {/* New Name */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  New Name
                </label>
                <input
                  type="text"
                  value={formData.newName}
                  disabled
                  className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg text-gray-600 cursor-not-allowed"
                />
                <p className="text-xs text-green-600 mt-1">✓ Extracted from Name Change Proof</p>
              </div>

              {/* Address */}
              <div className="md:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Address
                </label>
                <textarea
                  value={formData.address}
                  disabled
                  rows="2"
                  className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg text-gray-600 cursor-not-allowed resize-none"
                />
                <p className="text-xs text-green-600 mt-1">✓ Extracted from Address Proof</p>
              </div>

              {/* Service Number */}
              {formData.serviceNumber && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Service Number
                  </label>
                  <input
                    type="text"
                    value={formData.serviceNumber}
                    disabled
                    className="w-full px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg text-gray-600 cursor-not-allowed"
                  />
                  <p className="text-xs text-green-600 mt-1">✓ Extracted from Address Proof</p>
                </div>
              )}
            </div>
          </div>

          {/* User Input Section */}
          <div className="mb-8 pt-8 border-t-2 border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-blue-600" />
              Please Fill Remaining Details
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* City (for Torrent Power) */}
              {providerId === 'torrent-power' && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    City <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none"
                  >
                    <option value="Ahmedabad">Ahmedabad</option>
                    <option value="Surat">Surat</option>
                    <option value="Gandhinagar">Gandhinagar</option>
                    <option value="Bhavnagar">Bhavnagar</option>
                  </select>
                </div>
              )}

              {/* T Number (for Torrent Power) */}
              {providerId === 'torrent-power' && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    T Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="tNumber"
                    value={formData.tNumber}
                    onChange={handleChange}
                    placeholder="Enter T Number"
                    className={`w-full px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-blue-100 outline-none ${
                      errors.tNumber ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                    }`}
                  />
                  {errors.tNumber && (
                    <p className="text-xs text-red-500 mt-1">{errors.tNumber}</p>
                  )}
                </div>
              )}

              {/* Mobile Number */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Mobile Number <span className="text-red-500">*</span>
                </label>
                <input
                  type="tel"
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleChange}
                  placeholder="Enter 10-digit mobile number"
                  maxLength="10"
                  className={`w-full px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-blue-100 outline-none ${
                    errors.mobile ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                  }`}
                />
                {errors.mobile && (
                  <p className="text-xs text-red-500 mt-1">{errors.mobile}</p>
                )}
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter email address"
                  className={`w-full px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-blue-100 outline-none ${
                    errors.email ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                  }`}
                />
                {errors.email && (
                  <p className="text-xs text-red-500 mt-1">{errors.email}</p>
                )}
              </div>

              {/* Confirm Email */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Confirm Email <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  name="confirmEmail"
                  value={formData.confirmEmail}
                  onChange={handleChange}
                  placeholder="Re-enter email address"
                  className={`w-full px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-blue-100 outline-none ${
                    errors.confirmEmail ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                  }`}
                />
                {errors.confirmEmail && (
                  <p className="text-xs text-red-500 mt-1">{errors.confirmEmail}</p>
                )}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-6 border-t-2 border-gray-200">
            <Link
              to={`/utility-services/${serviceType}/${providerId}/document-upload`}
              className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Back to Documents
            </Link>
            
            <button
              type="submit"
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-bold hover:from-blue-700 hover:to-purple-700 transition-colors flex items-center gap-2 shadow-lg"
            >
              <Play className="w-5 h-5" />
              Submit Application
            </button>
          </div>
        </form>

        {/* Info Box */}
        <div className="mt-8 bg-blue-50 border-2 border-blue-200 rounded-xl p-6">
          <h4 className="font-semibold text-blue-900 mb-3">🚀 What happens next?</h4>
          <ul className="space-y-2 text-sm text-blue-700">
            <li>✓ Your application will be auto-submitted to {providerName}</li>
            <li>✓ Browser will open and fill the form automatically</li>
            <li>✓ You'll receive a confirmation email with reference number</li>
            <li>✓ Track your application status in "My Applications"</li>
            <li>✓ Processing time: 5-10 business days</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FinalFormPage;

