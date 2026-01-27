import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const DirectAutomationDemo = () => {
  const { t } = useTranslation();
  const [selectedSupplier, setSelectedSupplier] = useState('');
  const [supplierData, setSupplierData] = useState(null);
  const [formData, setFormData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [automationResult, setAutomationResult] = useState(null);

  // Direct access suppliers
  const directSuppliers = [
    {
      id: 'gujarat-gas',
      name: 'Gujarat Gas Ltd',
      type: 'Gas',
      description: 'Direct customer service form access',
      icon: '🔥',
      status: 'active'
    },
    {
      id: 'vadodara-gas',
      name: 'Vadodara Gas Ltd', 
      type: 'Gas',
      description: 'Direct name change form',
      icon: '🔥',
      status: 'active'
    },
    {
      id: 'torrent-power',
      name: 'Torrent Power',
      type: 'Electricity',
      description: 'PDF form download available',
      icon: '⚡',
      status: 'active'
    },
    {
      id: 'gwssb',
      name: 'GWSSB Water Supply',
      type: 'Water',
      description: 'Direct forms access',
      icon: '💧',
      status: 'active'
    },
    {
      id: 'anyror',
      name: 'AnyROR Gujarat',
      type: 'Property',
      description: 'Public record view (mutation required)',
      icon: '🏠',
      status: 'view_only'
    }
  ];

  useEffect(() => {
    if (selectedSupplier) {
      fetchSupplierData(selectedSupplier);
    }
  }, [selectedSupplier]);

  const fetchSupplierData = async (supplierId) => {
    try {
      const response = await fetch(`/api/services/supplier/${supplierId}`);
      const data = await response.json();
      setSupplierData(data);
      
      // Initialize form data
      const initialFormData = {};
      data.form_fields?.forEach(field => {
        initialFormData[field.name] = '';
      });
      setFormData(initialFormData);
    } catch (error) {
      console.error('Failed to fetch supplier data:', error);
    }
  };

  const handleFormDataChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const startDirectAutomation = async () => {
    if (!selectedSupplier || !supplierData) {
      alert('Please select a supplier first');
      return;
    }

    // Validate required fields
    const requiredFields = supplierData.form_fields?.filter(field => field.required) || [];
    const missingFields = requiredFields.filter(field => !formData[field.name]?.trim());
    
    if (missingFields.length > 0) {
      alert(`Please fill required fields: ${missingFields.map(f => f.label).join(', ')}`);
      return;
    }

    setIsLoading(true);
    setAutomationResult(null);

    try {
      const response = await fetch('/api/unified-automation/start-automation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          supplier_id: selectedSupplier,
          service_type: 'name_change',
          form_data: formData,
          automation_preference: 'direct'
        })
      });

      const result = await response.json();
      setAutomationResult(result);

      if (result.success) {
        // Show success message with next steps
        const nextStepsText = result.next_steps?.join('\n• ') || 'Please complete the process manually';
        alert(`✅ Automation Started Successfully!\n\n• ${nextStepsText}`);
      } else {
        alert(`❌ Automation Failed: ${result.message}`);
      }

    } catch (error) {
      console.error('Automation failed:', error);
      alert('Automation request failed. Please try again.');
      setAutomationResult({
        success: false,
        message: 'Network error occurred'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderFormField = (field) => {
    const commonProps = {
      id: field.name,
      value: formData[field.name] || '',
      onChange: (e) => handleFormDataChange(field.name, e.target.value),
      placeholder: field.placeholder,
      required: field.required,
      className: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
    };

    switch (field.type) {
      case 'select':
        return (
          <select {...commonProps}>
            <option value="">Select {field.label}</option>
            {field.options?.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      
      case 'textarea':
        return (
          <textarea 
            {...commonProps}
            rows={3}
          />
        );
      
      case 'tel':
        return (
          <input 
            {...commonProps}
            type="tel"
            pattern="[6-9][0-9]{9}"
            maxLength={10}
          />
        );
      
      case 'email':
        return (
          <input 
            {...commonProps}
            type="email"
          />
        );
      
      default:
        return (
          <input 
            {...commonProps}
            type="text"
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🤖 Direct Automation - Name Change
          </h1>
          <p className="text-gray-600 mb-4">
            These suppliers allow direct form access without login. Selenium will automatically fill forms.
          </p>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="font-semibold text-green-800 mb-2">✅ Direct Access Benefits:</h3>
            <ul className="text-green-700 text-sm space-y-1">
              <li>• No login required</li>
              <li>• Automatic form filling</li>
              <li>• Instant processing</li>
              <li>• Manual verification before submit</li>
            </ul>
          </div>
        </div>

        {/* Supplier Selection */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Select Supplier</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {directSuppliers.map((supplier) => (
              <div
                key={supplier.id}
                className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                  selectedSupplier === supplier.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedSupplier(supplier.id)}
              >
                <div className="flex items-center mb-2">
                  <span className="text-2xl mr-2">{supplier.icon}</span>
                  <div>
                    <h3 className="font-semibold text-gray-900">{supplier.name}</h3>
                    <span className="text-xs bg-gray-100 px-2 py-1 rounded">{supplier.type}</span>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-2">{supplier.description}</p>
                <div className="flex items-center justify-between">
                  <span className={`text-xs px-2 py-1 rounded ${
                    supplier.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {supplier.status === 'active' ? 'Full Automation' : 'View Only'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Form Fields */}
        {supplierData && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">
              Name Change Form - {supplierData.name}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {supplierData.form_fields?.map((field) => (
                <div key={field.name} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                    {field.required && <span className="text-red-500 ml-1">*</span>}
                  </label>
                  {field.label_hindi && (
                    <p className="text-xs text-gray-500 mb-1">{field.label_hindi}</p>
                  )}
                  {renderFormField(field)}
                  {field.validation && (
                    <p className="text-xs text-gray-500 mt-1">
                      Format: {field.validation}
                    </p>
                  )}
                </div>
              ))}
            </div>

            {/* Special Instructions */}
            {supplierData.instructions && (
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="font-semibold text-blue-800 mb-2">📋 Instructions:</h3>
                <ul className="text-blue-700 text-sm space-y-1">
                  {supplierData.instructions.map((instruction, index) => (
                    <li key={index}>• {instruction}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action Button */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={startDirectAutomation}
                disabled={isLoading}
                className={`px-8 py-3 rounded-lg font-semibold text-white transition-colors ${
                  isLoading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {isLoading ? (
                  <>
                    <span className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>
                    Starting Automation...
                  </>
                ) : (
                  <>
                    🚀 Start Direct Automation
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Automation Result */}
        {automationResult && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Automation Result</h2>
            
            <div className={`p-4 rounded-lg border ${
              automationResult.success 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-2">
                  {automationResult.success ? '✅' : '❌'}
                </span>
                <h3 className={`font-semibold ${
                  automationResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {automationResult.success ? 'Automation Successful' : 'Automation Failed'}
                </h3>
              </div>
              
              <p className={`mb-4 ${
                automationResult.success ? 'text-green-700' : 'text-red-700'
              }`}>
                {automationResult.message}
              </p>

              {automationResult.next_steps && (
                <div>
                  <h4 className="font-semibold mb-2">Next Steps:</h4>
                  <ul className="space-y-1">
                    {automationResult.next_steps.map((step, index) => (
                      <li key={index} className="text-sm">• {step}</li>
                    ))}
                  </ul>
                </div>
              )}

              {automationResult.screenshot_path && (
                <div className="mt-4">
                  <p className="text-sm">
                    📸 Screenshot saved: {automationResult.screenshot_path}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Help Section */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">How Direct Automation Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">🔄 Process Flow:</h3>
              <ol className="text-sm text-gray-600 space-y-2">
                <li>1. Select supplier from list</li>
                <li>2. Fill form with your details</li>
                <li>3. Click "Start Direct Automation"</li>
                <li>4. Browser opens automatically</li>
                <li>5. Form fills with your data</li>
                <li>6. Review and submit manually</li>
                <li>7. Save confirmation number</li>
              </ol>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">⚡ Supported Suppliers:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Gujarat Gas - Customer service form</li>
                <li>• Vadodara Gas - Direct name change</li>
                <li>• Torrent Power - PDF form download</li>
                <li>• GWSSB - Water supply forms</li>
                <li>• AnyROR - Land record view</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DirectAutomationDemo;