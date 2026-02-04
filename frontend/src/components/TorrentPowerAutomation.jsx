import { useState } from 'react';
import { Bot, CheckCircle, AlertCircle, Play, ExternalLink, Monitor, Server } from 'lucide-react';
import api from '../api/axios';
import clientRpaService from '../services/clientRpaService';

const TorrentPowerAutomation = ({ userData, onComplete, onClose }) => {
  const [automationStatus, setAutomationStatus] = useState('idle'); // idle, running, completed, failed
  const [result, setResult] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [automationType, setAutomationType] = useState('client'); // 'client' or 'server'

  const startClientAutomation = async () => {
    try {
      setAutomationStatus('running');
      setStatusMessage('🚀 Starting automation on your laptop...');

      console.log('🔍 Debug - userData received:', userData);

      const result = await clientRpaService.startTorrentPowerAutomation(userData);

      console.log('📥 Client RPA Response:', result);

      if (result.success) {
        setAutomationStatus('completed');
        setStatusMessage('🎉 Application submitted successfully on your laptop!');
        setResult(result);
        
        if (onComplete) {
          onComplete(result);
        }
      } else {
        setAutomationStatus('failed');
        setStatusMessage(`❌ Client automation failed: ${result.message}`);
        setResult(result);
      }

    } catch (error) {
      console.error('❌ Client automation error:', error);
      setAutomationStatus('failed');
      setStatusMessage(`❌ Failed to start client automation: ${error.message}`);
      setResult({
        success: false,
        error: error.message,
        message: 'Client Automation Failed'
      });
    }
  };

  const startServerAutomation = async () => {
  const startServerAutomation = async () => {
    try {
      setAutomationStatus('running');
      setStatusMessage('🚀 Starting automation on server...');

      // Debug: Log the userData to see what we're getting
      console.log('🔍 Debug - userData received:', userData);

      // Prepare the request data with proper field mapping
      const requestData = {
        city: userData.city || 'Ahmedabad',
        service_number: userData.serviceNumber || userData.service_number || '',
        t_number: userData.tNumber || userData.t_number || '',
        mobile: userData.mobile || '',
        email: userData.email || '',
        confirm_email: userData.confirmEmail || userData.email || ''
      };

      // Debug: Log the request data
      console.log('📤 Debug - Request data being sent:', requestData);

      // Validate required fields before sending
      if (!requestData.service_number || !requestData.t_number || !requestData.mobile || !requestData.email) {
        throw new Error('Missing required fields: Service Number, T Number, Mobile, or Email');
      }

      const response = await api.post('/torrent-automation/start-automation', requestData);

      console.log('✅ Server automation request sent successfully');
      console.log('📥 Response received:', response.data);

      const automationResult = response.data;

      if (automationResult.success) {
        setAutomationStatus('completed');
        setStatusMessage('🎉 Application submitted successfully on server!');
        setResult(automationResult);
        
        if (onComplete) {
          onComplete(automationResult);
        }
      } else {
        setAutomationStatus('failed');
        setStatusMessage(`❌ Server automation failed: ${automationResult.message}`);
        setResult(automationResult);
      }

    } catch (error) {
      console.error('❌ Server automation error:', error);
      setAutomationStatus('failed');
      
      // Show user-friendly error messages
      let errorMessage = 'Failed to connect to automation service';
      
      if (error.message && error.message.includes('Missing required fields')) {
        errorMessage = error.message;
      } else if (error.response?.status === 400) {
        errorMessage = error.response?.data?.detail || 'Invalid request data. Please check your form inputs.';
      } else if (error.response?.status === 401) {
        errorMessage = 'Authentication required. Please login again.';
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error. Please try again later.';
      }
      
      setStatusMessage(`❌ ${errorMessage}`);
      setResult({
        success: false,
        error: errorMessage,
        message: 'Server Automation Failed'
      });
    }
  };

  const openTorrentPowerManually = () => {
    // Store data in localStorage for potential auto-fill
    const torrentData = {
      city: userData.city || 'Ahmedabad',
      service_number: userData.serviceNumber || userData.service_number || '',
      t_number: userData.tNumber || userData.t_number || '',
      mobile: userData.mobile || '',
      email: userData.email || '',
      timestamp: Date.now()
    };
    
    try {
      localStorage.setItem('torrent_autofill_data', JSON.stringify(torrentData));
      console.log('💾 Data stored in localStorage for manual opening');
    } catch (e) {
      console.warn('Could not store data in localStorage:', e);
    }
    
    // Open the website
    window.open('https://connect.torrentpower.com/tplcp/application/namechangerequest', '_blank');
    setStatusMessage('🌐 Torrent Power website opened manually. Data stored for potential auto-fill.');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-t-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bot className="w-6 h-6 text-white" />
              <h2 className="text-lg font-bold text-white">Torrent Power Automation</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 p-1 rounded transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          
          {/* Automation Type Selection */}
          <div className="mb-4">
            <h3 className="font-semibold text-gray-800 mb-3">Choose Automation Method:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button
                onClick={() => setAutomationType('client')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  automationType === 'client' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Monitor className="w-6 h-6 text-blue-600" />
                  <div className="text-left">
                    <div className="font-semibold text-gray-800">Your Laptop</div>
                    <div className="text-sm text-gray-600">Chrome opens on your computer</div>
                  </div>
                </div>
              </button>
              
              <button
                onClick={() => setAutomationType('server')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  automationType === 'server' 
                    ? 'border-purple-500 bg-purple-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Server className="w-6 h-6 text-purple-600" />
                  <div className="text-left">
                    <div className="font-semibold text-gray-800">Server (EC2)</div>
                    <div className="text-sm text-gray-600">Chrome opens on server</div>
                  </div>
                </div>
              </button>
            </div>
          </div>

          {/* Status Display */}
          <div className="mb-4">
            <div className={`p-4 rounded-lg border ${
              automationStatus === 'idle' ? 'bg-gray-50 border-gray-200' :
              automationStatus === 'running' ? 'bg-blue-50 border-blue-200' :
              automationStatus === 'completed' ? 'bg-green-50 border-green-200' :
              'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center gap-3">
                {automationStatus === 'running' && (
                  <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                )}
                {automationStatus === 'completed' && <CheckCircle className="w-5 h-5 text-green-600" />}
                {automationStatus === 'failed' && <AlertCircle className="w-5 h-5 text-red-600" />}
                {automationStatus === 'idle' && <Bot className="w-5 h-5 text-gray-600" />}
                
                <p className={`font-medium ${
                  automationStatus === 'running' ? 'text-blue-800' :
                  automationStatus === 'completed' ? 'text-green-800' :
                  automationStatus === 'failed' ? 'text-red-800' :
                  'text-gray-800'
                }`}>
                  {statusMessage || 'Ready to start automation'}
                </p>
              </div>
            </div>
          </div>

          {/* Results Display */}
          {result && result.success && (
            <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="font-semibold text-green-800 mb-2">🎉 Application Submitted Successfully!</h3>
              <p className="text-sm text-green-700 mb-3">
                Your name change request has been successfully submitted to Torrent Power!
              </p>
              
              {/* Success Details */}
              <div className="bg-white rounded-lg p-3 mb-3">
                <h4 className="font-medium text-green-800 mb-2">✅ Completed Actions:</h4>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>• Chrome browser opened automatically</li>
                  <li>• Navigated to Torrent Power website</li>
                  <li>• Form fields filled with your data</li>
                  <li>• Application submitted successfully</li>
                </ul>
              </div>

              {/* Next Steps */}
              <div className="bg-blue-50 rounded-lg p-3">
                <h4 className="font-medium text-blue-800 mb-2">📋 What's Next:</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• You will receive a confirmation email shortly</li>
                  <li>• Track your application status on Torrent Power portal</li>
                  <li>• Keep your application reference number safe</li>
                </ul>
              </div>

              {/* Success Stats */}
              {result.total_filled && (
                <div className="mt-3 text-xs text-green-600 bg-green-100 p-2 rounded">
                  📊 Automation Stats: {result.total_filled}/{result.total_fields || 6} fields filled successfully
                </div>
              )}
            </div>
          )}

          {result && !result.success && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="font-semibold text-red-800 mb-2">❌ Automation Failed</h3>
              <p className="text-sm text-red-700">{result.message || result.error}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3">
            {automationStatus === 'idle' && (
              <button
                onClick={automationType === 'client' ? startClientAutomation : startServerAutomation}
                className={`flex-1 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${
                  automationType === 'client' 
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800'
                    : 'bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800'
                }`}
              >
                <Play className="w-4 h-4" />
                {automationType === 'client' ? 'Start Auto-fill on Your Laptop' : 'Start Auto-fill on Server'}
              </button>
            )}
            
            <button
              onClick={openTorrentPowerManually}
              className="flex-1 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
            >
              <ExternalLink className="w-4 h-4" />
              Open Manually
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TorrentPowerAutomation;