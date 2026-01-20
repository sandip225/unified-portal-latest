import React, { useState } from 'react';
import { Play, Square, CheckCircle, AlertCircle } from 'lucide-react';

const SimpleRPAController = ({ formData, onComplete, onError }) => {
  const [rpaStatus, setRpaStatus] = useState('idle');
  const [rpaLogs, setRpaLogs] = useState([]);
  const [progress, setProgress] = useState(0);

  const addLog = (message, type = 'info') => {
    const logEntry = {
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString(),
      message,
      type
    };
    setRpaLogs(prev => [...prev, logEntry]);
  };

  const startRPA = async () => {
    try {
      setRpaStatus('starting');
      setRpaLogs([]);
      addLog('🚀 Starting RPA automation...', 'info');
      
      // Simulate RPA process for now
      setRpaStatus('running');
      setProgress(20);
      addLog('📱 Auto-filling mobile number...', 'success');
      
      setTimeout(() => {
        setProgress(40);
        addLog('🏢 Selecting DISCOM...', 'success');
      }, 2000);
      
      setTimeout(() => {
        setProgress(60);
        addLog('⏳ Waiting for manual captcha entry...', 'warning');
      }, 4000);
      
      setTimeout(() => {
        setProgress(80);
        addLog('🔐 Waiting for manual OTP entry...', 'warning');
      }, 6000);
      
      setTimeout(() => {
        setProgress(100);
        addLog('✅ RPA automation completed!', 'success');
        setRpaStatus('success');
        onComplete && onComplete({ success: true });
      }, 8000);
      
    } catch (error) {
      setRpaStatus('error');
      addLog(`❌ RPA failed: ${error.message}`, 'error');
      onError && onError(error);
    }
  };

  const stopRPA = () => {
    setRpaStatus('idle');
    addLog('🛑 RPA automation stopped', 'warning');
  };

  const getStatusColor = () => {
    switch (rpaStatus) {
      case 'idle': return 'bg-gray-100 text-gray-700';
      case 'starting': return 'bg-blue-100 text-blue-700';
      case 'running': return 'bg-yellow-100 text-yellow-700';
      case 'success': return 'bg-green-100 text-green-700';
      case 'error': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 rounded-t-lg">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-lg">
            🤖
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">RPA Automation Controller</h3>
            <p className="text-white/80 text-sm">DGVCL Name Change Automation</p>
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <div className="p-4 border-b border-gray-200">
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium mb-3 ${getStatusColor()}`}>
          {rpaStatus === 'success' ? <CheckCircle className="w-4 h-4" /> : 
           rpaStatus === 'error' ? <AlertCircle className="w-4 h-4" /> : 
           <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>}
          <span className="capitalize">{rpaStatus}</span>
        </div>

        {/* Progress Bar */}
        {progress > 0 && (
          <div className="mb-3">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Control Buttons */}
        <div className="flex gap-3">
          {rpaStatus === 'idle' || rpaStatus === 'error' ? (
            <button
              onClick={startRPA}
              className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              <Play className="w-4 h-4" />
              Start Automation
            </button>
          ) : (
            <button
              onClick={stopRPA}
              className="flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              <Square className="w-4 h-4" />
              Stop Automation
            </button>
          )}
        </div>
      </div>

      {/* Logs Panel */}
      <div className="p-4">
        <h4 className="font-semibold text-gray-800 mb-3">📋 Automation Logs</h4>
        <div className="bg-gray-50 rounded-lg p-3 h-64 overflow-y-auto">
          {rpaLogs.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <div className="text-2xl mb-2">📝</div>
              <p>Logs will appear here when automation starts</p>
            </div>
          ) : (
            <div className="space-y-2">
              {rpaLogs.map((log) => (
                <div key={log.id} className="flex items-start gap-2 text-sm">
                  <span className="text-gray-400 text-xs mt-0.5 font-mono">
                    {log.timestamp}
                  </span>
                  <span className={`flex-1 ${
                    log.type === 'error' ? 'text-red-600' :
                    log.type === 'success' ? 'text-green-600' :
                    log.type === 'warning' ? 'text-orange-600' :
                    'text-gray-700'
                  }`}>
                    {log.message}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="p-4 bg-blue-50 border-t border-blue-200 rounded-b-lg">
        <h5 className="font-semibold text-blue-800 mb-2">📖 How it works:</h5>
        <div className="text-sm text-blue-700 space-y-1">
          <p>1. 🚀 Click "Start Automation" to begin RPA process</p>
          <p>2. 🤖 Bot will auto-fill mobile number and DISCOM</p>
          <p>3. ✋ You'll need to manually enter captcha and OTP</p>
          <p>4. 🔄 Bot will handle rest of the form submission</p>
          <p>5. ✅ Get notified when process completes</p>
        </div>
      </div>
    </div>
  );
};

export default SimpleRPAController;