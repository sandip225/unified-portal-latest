/**
 * Selenium Bridge for Chrome Extension
 * Bridges communication between Chrome Extension and Selenium automation
 */

class SeleniumBridge {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.isConnected = false;
        this.automationStatus = 'idle';
    }

    /**
     * Initialize the bridge connection
     */
    async initialize() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            this.isConnected = response.ok;
            console.log('Selenium Bridge initialized:', this.isConnected);
            return this.isConnected;
        } catch (error) {
            console.error('Failed to initialize Selenium Bridge:', error);
            this.isConnected = false;
            return false;
        }
    }

    /**
     * Extract form data from current page
     */
    extractFormData() {
        const formData = {};
        
        // Extract input fields
        const inputs = document.querySelectorAll('input[name], input[id]');
        inputs.forEach(input => {
            const key = input.name || input.id;
            if (key && input.type !== 'submit' && input.type !== 'button') {
                formData[key] = input.value;
            }
        });

        // Extract select fields
        const selects = document.querySelectorAll('select[name], select[id]');
        selects.forEach(select => {
            const key = select.name || select.id;
            if (key) {
                formData[key] = select.value;
            }
        });

        // Extract textarea fields
        const textareas = document.querySelectorAll('textarea[name], textarea[id]');
        textareas.forEach(textarea => {
            const key = textarea.name || textarea.id;
            if (key) {
                formData[key] = textarea.value;
            }
        });

        return formData;
    }

    /**
     * Detect the current government website
     */
    detectGovernmentSite() {
        const hostname = window.location.hostname.toLowerCase();
        const url = window.location.href.toLowerCase();

        // Government site detection patterns
        const sitePatterns = {
            'torrent_power': ['torrentpower.com', 'connect.torrentpower'],
            'adani_gas': ['adanigas.com', 'adani-gas'],
            'amc_water': ['amcwater.com', 'amc-water'],
            'anyror_gujarat': ['anyror.gujarat.gov.in', 'anyror'],
            'dgvcl': ['dgvcl.com', 'dgvcl.co.in'],
            'guvnl': ['guvnl.com', 'guvnl.co.in'],
            'gujarat_gas': ['gujaratgas.com', 'gujarat-gas']
        };

        for (const [service, patterns] of Object.entries(sitePatterns)) {
            if (patterns.some(pattern => hostname.includes(pattern) || url.includes(pattern))) {
                return service;
            }
        }

        return 'unknown';
    }

    /**
     * Send automation request to backend
     */
    async requestAutomation(serviceType, formData) {
        try {
            this.automationStatus = 'running';
            
            const response = await fetch(`${this.apiBase}/api/rpa/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    service_type: serviceType,
                    form_data: formData,
                    source: 'chrome_extension'
                })
            });

            const result = await response.json();
            this.automationStatus = result.success ? 'completed' : 'failed';
            
            return result;
        } catch (error) {
            console.error('Automation request failed:', error);
            this.automationStatus = 'failed';
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Monitor automation progress
     */
    async getAutomationStatus(taskId) {
        try {
            const response = await fetch(`${this.apiBase}/api/rpa/status/${taskId}`);
            return await response.json();
        } catch (error) {
            console.error('Failed to get automation status:', error);
            return { status: 'error', error: error.message };
        }
    }

    /**
     * Auto-fill form with provided data
     */
    autoFillForm(data) {
        let filledFields = 0;

        // Fill input fields
        Object.entries(data).forEach(([key, value]) => {
            if (!value) return;

            // Try multiple selector strategies
            const selectors = [
                `input[name="${key}"]`,
                `input[id="${key}"]`,
                `select[name="${key}"]`,
                `select[id="${key}"]`,
                `textarea[name="${key}"]`,
                `textarea[id="${key}"]`
            ];

            for (const selector of selectors) {
                const element = document.querySelector(selector);
                if (element) {
                    if (element.tagName === 'SELECT') {
                        // Handle select elements
                        const option = Array.from(element.options).find(opt => 
                            opt.value === value || opt.text.includes(value)
                        );
                        if (option) {
                            element.value = option.value;
                            element.dispatchEvent(new Event('change', { bubbles: true }));
                            filledFields++;
                        }
                    } else {
                        // Handle input and textarea elements
                        element.value = value;
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                        element.dispatchEvent(new Event('change', { bubbles: true }));
                        filledFields++;
                    }
                    break;
                }
            }
        });

        return filledFields;
    }

    /**
     * Highlight form fields that can be automated
     */
    highlightAutomatableFields() {
        const style = document.createElement('style');
        style.textContent = `
            .selenium-automatable {
                border: 2px solid #4CAF50 !important;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.5) !important;
            }
            .selenium-tooltip {
                position: absolute;
                background: #4CAF50;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 10000;
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);

        // Highlight automatable fields
        const automatableFields = document.querySelectorAll('input[name], input[id], select[name], select[id], textarea[name], textarea[id]');
        automatableFields.forEach(field => {
            if (field.type !== 'submit' && field.type !== 'button') {
                field.classList.add('selenium-automatable');
                
                // Add tooltip
                field.addEventListener('mouseenter', (e) => {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'selenium-tooltip';
                    tooltip.textContent = 'Can be automated with Selenium';
                    tooltip.style.left = e.pageX + 'px';
                    tooltip.style.top = (e.pageY - 30) + 'px';
                    document.body.appendChild(tooltip);
                    
                    field.addEventListener('mouseleave', () => {
                        tooltip.remove();
                    }, { once: true });
                });
            }
        });
    }

    /**
     * Create automation control panel
     */
    createControlPanel() {
        // Remove existing panel
        const existingPanel = document.getElementById('selenium-control-panel');
        if (existingPanel) {
            existingPanel.remove();
        }

        const panel = document.createElement('div');
        panel.id = 'selenium-control-panel';
        panel.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                width: 300px;
                background: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                font-family: Arial, sans-serif;
            ">
                <h3 style="margin: 0 0 12px 0; color: #4CAF50;">🤖 Selenium Automation</h3>
                <div style="margin-bottom: 12px;">
                    <strong>Site:</strong> <span id="detected-site">Detecting...</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <strong>Status:</strong> <span id="automation-status">${this.automationStatus}</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <button id="extract-data-btn" style="
                        background: #2196F3;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-right: 8px;
                    ">Extract Data</button>
                    <button id="auto-fill-btn" style="
                        background: #FF9800;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-right: 8px;
                    ">Auto Fill</button>
                </div>
                <div style="margin-bottom: 12px;">
                    <button id="start-automation-btn" style="
                        background: #4CAF50;
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 4px;
                        cursor: pointer;
                        width: 100%;
                        font-weight: bold;
                    ">Start Automation</button>
                </div>
                <button id="close-panel-btn" style="
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #666;
                ">×</button>
            </div>
        `;

        document.body.appendChild(panel);

        // Add event listeners
        this.attachPanelEventListeners();
        
        // Update detected site
        const detectedSite = this.detectGovernmentSite();
        document.getElementById('detected-site').textContent = detectedSite;
    }

    /**
     * Attach event listeners to control panel
     */
    attachPanelEventListeners() {
        // Close panel
        document.getElementById('close-panel-btn').addEventListener('click', () => {
            document.getElementById('selenium-control-panel').remove();
        });

        // Extract data
        document.getElementById('extract-data-btn').addEventListener('click', () => {
            const data = this.extractFormData();
            console.log('Extracted form data:', data);
            alert(`Extracted ${Object.keys(data).length} form fields. Check console for details.`);
        });

        // Auto fill (demo data)
        document.getElementById('auto-fill-btn').addEventListener('click', () => {
            const demoData = {
                'applicant_name': 'John Doe',
                'mobile': '9876543210',
                'email': 'john.doe@example.com',
                'city': 'Ahmedabad'
            };
            const filled = this.autoFillForm(demoData);
            alert(`Auto-filled ${filled} form fields with demo data.`);
        });

        // Start automation
        document.getElementById('start-automation-btn').addEventListener('click', async () => {
            const serviceType = this.detectGovernmentSite();
            const formData = this.extractFormData();
            
            if (serviceType === 'unknown') {
                alert('This website is not supported for automation yet.');
                return;
            }

            document.getElementById('automation-status').textContent = 'running';
            const result = await this.requestAutomation(serviceType, formData);
            
            if (result.success) {
                alert(`Automation completed successfully! Confirmation: ${result.confirmation_number}`);
            } else {
                alert(`Automation failed: ${result.error}`);
            }
            
            document.getElementById('automation-status').textContent = this.automationStatus;
        });
    }
}

// Initialize Selenium Bridge
const seleniumBridge = new SeleniumBridge();

// Auto-initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        seleniumBridge.initialize();
    });
} else {
    seleniumBridge.initialize();
}

// Export for use in other scripts
window.seleniumBridge = seleniumBridge;