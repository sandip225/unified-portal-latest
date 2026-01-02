import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { ArrowLeft, RefreshCw, Building } from 'lucide-react';
import { gujaratData } from '../data/gujaratServices';

const PropertyForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    district: 'Ahmedabad',
    taluka: '',
    village: '',
    survey_number: '',
    property_id: '',
    current_owner_name: '',
    new_owner_name: '',
    property_type: 'Residential',
    property_address: '',
    mobile: '',
    email: '',
    aadhaar_number: '',
    application_type: 'mutation',
    captcha_answer: ''
  });
  const [captcha, setCaptcha] = useState({ num1: 0, num2: 0 });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const propertyTypes = ['Residential', 'Commercial', 'Agricultural', 'Industrial', 'Mixed Use'];
  const applicationTypes = [
    { value: 'mutation', label: 'Mutation / Name Transfer (नाम स्थानांतरण)' },
    { value: 'noc', label: 'NOC Request' },
    { value: '7_12_extract', label: '7/12 Extract (7/12 निकालना)' },
    { value: 'property_tax', label: 'Property Tax Name Change' }
  ];

  useEffect(() => {
    fetchPrefillData();
    generateCaptcha();
  }, []);

  const generateCaptcha = () => {
    setCaptcha({
      num1: Math.floor(Math.random() * 10),
      num2: Math.floor(Math.random() * 10)
    });
    setFormData(prev => ({ ...prev, captcha_answer: '' }));
  };

  const fetchPrefillData = async () => {
    setLoading(true);
    try {
      const response = await api.get('/applications/prefill/property/name_change');
      setFormData(prev => ({
        ...prev,
        survey_number: response.data.survey_number || '',
        property_id: response.data.property_id || '',
        current_owner_name: response.data.owner_name || response.data.full_name || '',
        property_address: response.data.property_address || response.data.address || '',
        mobile: response.data.mobile || '',
        email: response.data.email || '',
        aadhaar_number: response.data.aadhaar_number || '',
        district: response.data.city || 'Ahmedabad'
      }));
    } catch (error) {
      console.error('Failed to fetch prefill data');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (parseInt(formData.captcha_answer) !== captcha.num1 + captcha.num2) {
      setMessage('Invalid captcha answer');
      generateCaptcha();
      return;
    }

    setSubmitting(true);
    try {
      const appResponse = await api.post('/applications/', {
        service_type: 'property',
        application_type: formData.application_type,
        form_data: formData
      });
      await api.post(`/applications/${appResponse.data.id}/submit`);
      setMessage('Application submitted successfully!');
      setTimeout(() => navigate('/applications'), 2000);
    } catch (error) {
      setMessage('Failed to submit application');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
      >
        <ArrowLeft className="w-5 h-5" /> Back to Dashboard
      </button>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-gradient-to-r from-green-600 to-green-500 p-4">
          <div className="flex items-center gap-3">
            <div className="bg-white p-2 rounded-lg">
              <Building className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h1 className="text-white text-xl font-bold">Property / Revenue Service</h1>
              <p className="text-green-100 text-sm">Gujarat State - Land Administration</p>
            </div>
          </div>
        </div>

        <div className="p-6">
          <h2 className="text-xl font-bold text-gray-800 text-center mb-2">
            Property Name Transfer / Mutation Application
          </h2>
          <p className="text-gray-500 text-center text-sm mb-6">
            Revenue Department, Government of Gujarat
          </p>

          {message && (
            <div className={`p-3 rounded-lg mb-4 text-center ${
              message.includes('success') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Application Type */}
            <div>
              <label className="block text-gray-700 mb-1">Application Type<span className="text-red-500">*</span></label>
              <select
                name="application_type"
                value={formData.application_type}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              >
                {applicationTypes.map(type => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))}
              </select>
            </div>

            {/* District */}
            <div>
              <label className="block text-gray-700 mb-1">District (जिला)<span className="text-red-500">*</span></label>
              <select
                name="district"
                value={formData.district}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              >
                {gujaratData.districts.map(district => (
                  <option key={district} value={district}>{district}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 mb-1">Taluka (तहसील)<span className="text-red-500">*</span></label>
                <input
                  type="text"
                  name="taluka"
                  value={formData.taluka}
                  onChange={handleChange}
                  placeholder="Enter Taluka"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 mb-1">Village (गांव)<span className="text-red-500">*</span></label>
                <input
                  type="text"
                  name="village"
                  value={formData.village}
                  onChange={handleChange}
                  placeholder="Enter Village"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 mb-1">Survey Number (सर्वे संख्या)<span className="text-red-500">*</span></label>
                <input
                  type="text"
                  name="survey_number"
                  value={formData.survey_number}
                  onChange={handleChange}
                  placeholder="Enter Survey Number"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 mb-1">Property ID / Khata Number</label>
                <input
                  type="text"
                  name="property_id"
                  value={formData.property_id}
                  onChange={handleChange}
                  placeholder="Enter Property ID"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Property Type<span className="text-red-500">*</span></label>
              <select
                name="property_type"
                value={formData.property_type}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              >
                {propertyTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Current Owner Name (वर्तमान मालिक का नाम)<span className="text-red-500">*</span></label>
              <input
                type="text"
                name="current_owner_name"
                value={formData.current_owner_name}
                onChange={handleChange}
                placeholder="Enter current owner name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-1">New Owner Name (नए मालिक का नाम)<span className="text-red-500">*</span></label>
              <input
                type="text"
                name="new_owner_name"
                value={formData.new_owner_name}
                onChange={handleChange}
                placeholder="Enter new owner name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Property Address<span className="text-red-500">*</span></label>
              <textarea
                name="property_address"
                value={formData.property_address}
                onChange={handleChange}
                placeholder="Enter complete property address"
                rows={2}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Aadhaar Number<span className="text-red-500">*</span></label>
              <input
                type="text"
                name="aadhaar_number"
                value={formData.aadhaar_number}
                onChange={handleChange}
                placeholder="Enter 12-digit Aadhaar Number"
                maxLength={12}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 mb-1">Mobile Number<span className="text-red-500">*</span></label>
                <input
                  type="tel"
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleChange}
                  placeholder="Enter Mobile Number"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 mb-1">Email<span className="text-red-500">*</span></label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter Email"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-gray-700 mb-1">Please confirm you are not robot</label>
              <div className="flex items-center gap-3">
                <span className="text-gray-700 font-medium">{captcha.num1} + {captcha.num2} =</span>
                <input
                  type="text"
                  name="captcha_answer"
                  value={formData.captcha_answer}
                  onChange={handleChange}
                  className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-center"
                  required
                />
                <button type="button" onClick={generateCaptcha} className="flex items-center gap-1 text-green-600">
                  Re-generate <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Government Portal Links */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-2">Official Gujarat Government Portals:</p>
              <div className="flex flex-wrap gap-2 text-xs">
                <a href="https://anyror.gujarat.gov.in" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">AnyRoR Gujarat</a>
                <span>•</span>
                <a href="https://revenuedepartment.gujarat.gov.in" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Revenue Department</a>
                <span>•</span>
                <a href="https://enagar.gujarat.gov.in" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">e-Nagar Gujarat</a>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-green-600 text-white py-3 rounded-full font-semibold hover:bg-green-700 disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Application'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PropertyForm;
