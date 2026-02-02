import { useState } from 'react';
import { Bot, Zap, CheckCircle, AlertCircle, ExternalLink, Play, Pause } from 'lucide-react';
import api from '../api/axios';

const TorrentPowerAutomation = ({ userData, onComplete, onClose }) => {
  const [automationStatus, setAutomationStatus] = useState('idle'); // idle, running, completed, failed
  const [result, setResult] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');

  const startAutomation = async () => {
    try {
      setAutomationStatus('running');
      setStatusMessage('🚀 Starting production-ready Torrent Power automation...');

      const response = await api.post('/torrent-automation/start-automation', {
        city: userData.city || 'Ahmedabad',
        service_number: userData.serviceNumber || userData.service_number,
        t_number: userData.tNumber || userData.t_number,
        mobile: userData.mobile,
        email: userData.email
      });

      const automationResult = response.data;

      if (automationResult.success) {
        setAutomationStatus('completed');
        setStatusMessage('✅ Automation completed successfully!');
        setResult(automationResult);
        
        if (onComplete) {
          onComplete(automationResult);
        }
      } else {
        setAutomationStatus('failed');
        setStatusMessage(`❌ Automation failed: ${automationResult.message}`);
        setResult(automationResult);
      }

    } catch (error) {
      console.error('Automation error:', error);
      setAutomationStatus('failed');
      setStatusMessage(`❌ Network error: ${error.message}`);
      setResult({
        success: false,
        error: error.message,
        message: 'Failed to connect to automation service'
      });
    }
  };

  const openTorrentPowerManually = () => {
    window.open('https://connect.torrentpower.com/tplcp/application/namechangerequest', '_blank');
    setStatusMessage('🌐 Torrent Power website opened manually. Please fill the form yourself.');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 rounded-t-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-white/20 p-2 rounded-lg">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Production-Ready AI Automation</h2>
                <p className="text-blue-100 text-sm">Torrent Power Name Change - Live Automation</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          
          {/* Status Display */}
          <div className="mb-6">
            <div className={`p-4 rounded-lg border-2 ${
              automationStatus === 'idle' ? 'bg-gray-50 border-gray-200' :
              automationStatus === 'running' ? 'bg-blue-50 border-blue-200' :
              automationStatus === 'completed' ? 'bg-green-50 border-green-200' :
              'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center gap-3">
                {automationStatus === 'running' && (
                  <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                )}
                {automationStatus === 'completed' && <CheckCircle className="w-6 h-6 text-green-600" />}
                {automationStatus === 'failed' && <AlertCircle className="w-6 h-6 text-red-600" />}
                {automationStatus === 'idle' && <Zap className="w-6 h-6 text-gray-600" />}
                
                <div>
                  <p className={`font-medium ${
                    automationStatus === 'running' ? 'text-blue-800' :
                    automationStatus === 'completed' ? 'text-green-800' :
                    automationStatus === 'failed' ? 'text-red-800' :
                    'text-gray-800'
                  }`}>
                    {statusMessage || 'Ready to start automation'}
                  </p>
                  
                  {automationStatus === 'running' && (
                    <p className="text-sm text-blue-600 mt-1">
                      AI is controlling the browser automatically - watch the process!
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* User Data Preview */}
          <div className="mb-6 bg-gray-50 rounded-lg p-4">
            <h3 className="font-semibold text-gray-800 mb-3">📋 Data to be Auto-filled:</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="font-medium">City:</span> {userData.city || 'Ahmedabad'}</div>
              <div><span className="font-medium">Service Number:</span> {userData.serviceNumber || userData.service_number}</div>
              <div><span className="font-medium">T Number:</span> {userData.tNumber || userData.t_number}</div>
              <div><span className="font-medium">Mobile:</span> {userData.mobile}</div>
              <div className="col-span-2"><span className="font-medium">Email:</span> {userData.email}</div>
            </div>
          </div>

          {/* Automation Features */}
          <div className="mb-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
            <h3 className="font-semibold text-blue-800 mb-3">🤖 Production-Ready Features:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-blue-700">
              <div>✅ AI-assisted field mapping</div>
              <div>✅ Intelligent form filling</div>
              <div>✅ Screenshot audit trail</div>
              <div>✅ Fallback strategies</div>
              <div>✅ Visible browser process</div>
              <div>✅ Production error handling</div>
            </div>
          </div>

          {/* Results Display */}
          {result && (
            <div className="mb-6">
              {result.success ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-semibold text-green-800 mb-3">✅ Automation Completed Successfully!</h3>
                  
                  {result.fields_filled && (
                    <div className="mb-3">
                      <p className="text-green-700">
                        <strong>Fields Filled:</strong> {result.fields_filled}/{result.total_fields} ({result.success_rate})
                      </p>
                    </div>
                  )}

                  {result.next_steps && (
                    <div className="mb-3">
                      <p className="font-medium text-green-800 mb-2">Next Steps:</p>
                      <ul className="text-sm text-green-700 space-y-1">
                        {result.next_steps.map((step, index) => (
                          <li key={index}>{step}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex items-center gap-2 mt-4">
                    <ExternalLink className="w-4 h-4" />
                    <a 
                      href={result.portal_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-green-600 hover:text-green-800 underline"
                    >
                      Open Torrent Power Website
                    </a>
                  </div>
                </div>
              ) : (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h3 className="font-semibold text-red-800 mb-3">❌ Automation Failed</h3>
                  <p className="text-red-700 mb-3">{result.message}</p>
                  
                  {result.troubleshooting && (
                    <div>
                      <p className="font-medium text-red-800 mb-2">Troubleshooting:</p>
                      <ul className="text-sm text-red-700 space-y-1">
                        {result.troubleshooting.map((step, index) => (
                          <li key={index}>{step}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center gap-4">
            {automationStatus === 'idle' && (
              <>
                <button
                  onClick={startAutomation}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium"
                >
                  <Play className="w-5 h-5" />
                  Start AI Automation
                  <span className="text-xs opacity-75 ml-1">(Production Ready)</span>
                </button>
                
                <button
                  onClick={openTorrentPowerManually}
                  className="flex items-center gap-2 px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <ExternalLink className="w-5 h-5" />
                  Open Manually
                </button>
              </>
            )}

            {automationStatus === 'running' && (
              <div className="flex items-center gap-2 px-6 py-3 bg-blue-100 text-blue-800 rounded-lg">
                <Pause className="w-5 h-5" />
                Automation in Progress...
              </div>
            )}

            {(automationStatus === 'completed' || automationStatus === 'failed') && (
              <button
                onClick={() => {
                  setAutomationStatus('idle');
                  setResult(null);
                  setStatusMessage('');
                }}
                className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Play className="w-5 h-5" />
                Run Again
              </button>
            )}
          </div>

          {/* Workflow Info */}
          <div className="mt-6 bg-gray-50 rounded-lg p-4">
            <h3 className="font-semibold text-gray-800 mb-3">🔄 Automation Workflow:</h3>
            <div className="text-sm text-gray-600 space-y-1">
              <div>1. 📋 Data validation and session storage</div>
              <div>2. 🌐 Navigate to official Torrent Power website</div>
              <div>3. 🤖 AI-assisted field identification and mapping</div>
              <div>4. ✍️ Intelligent form filling with fallback strategies</div>
              <div>5. 📸 Screenshot audit trail generation</div>
              <div>6. ⏹️ Stop before submission for user control</div>
              <div>7. 📊 Provide completion summary and next steps</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TorrentPowerAutomation;