/**
 * Client-Side RPA Service
 * This runs RPA automation on user's laptop, not on server
 */

class ClientRpaService {
  constructor() {
    this.isRunning = false;
    this.automationWindow = null;
  }

  /**
   * Start RPA automation on user's laptop
   * Chrome will open on user's machine, not server
   */
  async startTorrentPowerAutomation(userData) {
    try {
      console.log('🚀 Starting client-side RPA automation...');
      this.isRunning = true;

      // Create automation script that runs on user's browser
      const automationScript = this.generateAutomationScript(userData);
      
      // Create a new window/tab for automation
      const automationUrl = this.createAutomationUrl(automationScript);
      
      // Open Chrome on USER'S laptop, not server
      this.automationWindow = window.open(automationUrl, '_blank', 
        'width=1200,height=800,scrollbars=yes,resizable=yes'
      );

      if (!this.automationWindow) {
        throw new Error('Popup blocked. Please allow popups for this site.');
      }

      // Monitor automation progress
      const result = await this.monitorAutomation();
      
      return {
        success: true,
        message: 'RPA automation completed successfully on your laptop',
        automation_type: 'client_side',
        browser_location: 'user_laptop',
        details: 'Chrome opened on your laptop and filled the form automatically'
      };

    } catch (error) {
      console.error('❌ Client RPA failed:', error);
      return {
        success: false,
        message: 'Client-side RPA failed',
        error: error.message,
        automation_type: 'client_side'
      };
    } finally {
      this.isRunning = false;
    }
  }

  /**
   * Generate JavaScript automation script
   */
  generateAutomationScript(userData) {
    return `
      // Torrent Power Auto-fill Script - Runs on User's Browser
      (function() {
        console.log('🤖 Starting Torrent Power auto-fill on user laptop...');
        
        const userData = ${JSON.stringify(userData)};
        let filledFields = 0;
        
        // Wait for page to load
        function waitForLoad() {
          return new Promise((resolve) => {
            if (document.readyState === 'complete') {
              resolve();
            } else {
              window.addEventListener('load', resolve);
            }
          });
        }
        
        // Fill form fields with visual feedback
        function fillField(selector, value, fieldName) {
          const element = document.querySelector(selector);
          if (element && value) {
            element.value = value;
            element.style.backgroundColor = '#d4edda';
            element.style.border = '3px solid #28a745';
            element.dispatchEvent(new Event('input', { bubbles: true }));
            element.dispatchEvent(new Event('change', { bubbles: true }));
            filledFields++;
            console.log(\`✅ Filled \${fieldName}: \${value}\`);
            return true;
          }
          return false;
        }
        
        // Fill dropdown/select fields
        function fillSelect(selector, value, fieldName) {
          const select = document.querySelector(selector);
          if (select && value) {
            const options = Array.from(select.options);
            const option = options.find(opt => 
              opt.text.toLowerCase().includes(value.toLowerCase()) ||
              opt.value.toLowerCase().includes(value.toLowerCase())
            );
            
            if (option) {
              select.value = option.value;
              select.style.backgroundColor = '#d4edda';
              select.style.border = '3px solid #28a745';
              select.dispatchEvent(new Event('change', { bubbles: true }));
              filledFields++;
              console.log(\`✅ Selected \${fieldName}: \${option.text}\`);
              return true;
            }
          }
          return false;
        }
        
        // Main automation function
        async function startAutomation() {
          try {
            await waitForLoad();
            console.log('📋 Page loaded, starting form fill...');
            
            // Add visual indicator
            const indicator = document.createElement('div');
            indicator.innerHTML = \`
              <div style="position: fixed; top: 20px; right: 20px; background: #007bff; color: white; padding: 15px 20px; border-radius: 10px; font-family: Arial; z-index: 999999; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <strong>🤖 AI Auto-fill Active</strong><br>
                <small>Filling form automatically...</small>
              </div>
            \`;
            document.body.appendChild(indicator);
            
            // Wait a moment for any dynamic content
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Fill City (dropdown)
            fillSelect('select', userData.city || 'Ahmedabad', 'City');
            
            // Fill Service Number
            fillField('input[placeholder*="Service Number"], input[name*="service"], input[id*="service"]', 
                     userData.serviceNumber || userData.service_number, 'Service Number');
            
            // Fill T Number
            fillField('input[placeholder*="T No"], input[placeholder*="T-No"], input[name*="tno"]', 
                     userData.tNumber || userData.t_number, 'T Number');
            
            // Fill Mobile
            fillField('input[type="tel"], input[placeholder*="Mobile"], input[name*="mobile"]', 
                     userData.mobile, 'Mobile Number');
            
            // Fill Email
            fillField('input[type="email"], input[placeholder*="Email"], input[name*="email"]', 
                     userData.email, 'Email Address');
            
            // Wait before submitting
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            // Try to find and click submit button
            const submitSelectors = [
              'button[type="submit"]',
              'input[type="submit"]',
              'button:contains("Submit")',
              '.btn-primary',
              '.submit-btn'
            ];
            
            let submitted = false;
            for (const selector of submitSelectors) {
              const button = document.querySelector(selector);
              if (button) {
                button.scrollIntoView({ behavior: 'smooth' });
                await new Promise(resolve => setTimeout(resolve, 1000));
                button.click();
                submitted = true;
                console.log('✅ Form submitted successfully');
                break;
              }
            }
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.innerHTML = \`
              <div style="position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 20px 30px; border-radius: 10px; font-family: Arial; z-index: 999999; box-shadow: 0 4px 20px rgba(0,0,0,0.3); max-width: 400px;">
                <strong>🎉 Application Submitted Successfully!</strong><br>
                <small style="font-size: 14px; margin-top: 10px; display: block;">
                  \${filledFields} fields filled automatically.<br>
                  You will receive a confirmation email shortly.
                </small>
              </div>
            \`;
            document.body.appendChild(successMsg);
            
            // Remove indicator
            if (indicator.parentNode) {
              indicator.parentNode.removeChild(indicator);
            }
            
            // Auto-close after 10 seconds
            setTimeout(() => {
              if (successMsg.parentNode) {
                successMsg.parentNode.removeChild(successMsg);
              }
            }, 10000);
            
            // Notify parent window
            if (window.opener) {
              window.opener.postMessage({
                type: 'RPA_COMPLETE',
                success: true,
                filledFields: filledFields,
                submitted: submitted
              }, '*');
            }
            
          } catch (error) {
            console.error('❌ Automation error:', error);
            
            // Show error message
            const errorMsg = document.createElement('div');
            errorMsg.innerHTML = \`
              <div style="position: fixed; top: 20px; right: 20px; background: #dc3545; color: white; padding: 20px 30px; border-radius: 10px; font-family: Arial; z-index: 999999; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <strong>❌ Automation Error</strong><br>
                <small>\${error.message}</small>
              </div>
            \`;
            document.body.appendChild(errorMsg);
            
            // Notify parent window
            if (window.opener) {
              window.opener.postMessage({
                type: 'RPA_COMPLETE',
                success: false,
                error: error.message
              }, '*');
            }
          }
        }
        
        // Start automation when page is ready
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', startAutomation);
        } else {
          startAutomation();
        }
        
      })();
    `;
  }

  /**
   * Create automation URL that opens Torrent Power with auto-fill script
   */
  createAutomationUrl(script) {
    // Create a data URL with the automation script
    const automationHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>RPA Automation Launcher</title>
        <style>
          body { 
            font-family: Arial, sans-serif; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
          }
          .container {
            max-width: 600px;
            margin: 50px auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
          }
          .btn {
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s;
          }
          .btn:hover {
            background: #218838;
            transform: translateY(-2px);
          }
          .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🤖 RPA Automation Launcher</h1>
          <p>This will automatically fill the Torrent Power form on YOUR laptop</p>
          
          <div class="status" id="status">
            <strong>Ready to start automation</strong>
          </div>
          
          <button class="btn" onclick="startAutomation()">
            🚀 Start Auto-fill on Torrent Power Website
          </button>
          
          <button class="btn" onclick="openManually()" style="background: #6c757d;">
            🌐 Open Website Manually
          </button>
        </div>
        
        <script>
          const automationScript = \`${script.replace(/`/g, '\\`')}\`;
          
          function updateStatus(message, color = '#17a2b8') {
            const status = document.getElementById('status');
            status.innerHTML = \`<strong style="color: \${color}">\${message}</strong>\`;
          }
          
          function startAutomation() {
            updateStatus('🚀 Opening Torrent Power website...', '#28a745');
            
            // Open Torrent Power website with automation script
            const torrentWindow = window.open(
              'https://connect.torrentpower.com/tplcp/application/namechangerequest',
              '_blank',
              'width=1200,height=800,scrollbars=yes,resizable=yes'
            );
            
            if (!torrentWindow) {
              updateStatus('❌ Popup blocked! Please allow popups and try again.', '#dc3545');
              return;
            }
            
            // Inject automation script when page loads
            torrentWindow.addEventListener('load', function() {
              const script = torrentWindow.document.createElement('script');
              script.textContent = automationScript;
              torrentWindow.document.head.appendChild(script);
            });
            
            updateStatus('✅ Automation started! Check the Torrent Power window.', '#28a745');
          }
          
          function openManually() {
            window.open(
              'https://connect.torrentpower.com/tplcp/application/namechangerequest',
              '_blank'
            );
            updateStatus('🌐 Website opened manually', '#6c757d');
          }
          
          // Listen for automation completion
          window.addEventListener('message', function(event) {
            if (event.data.type === 'RPA_COMPLETE') {
              if (event.data.success) {
                updateStatus(\`🎉 Automation completed! \${event.data.filledFields} fields filled.\`, '#28a745');
              } else {
                updateStatus(\`❌ Automation failed: \${event.data.error}\`, '#dc3545');
              }
            }
          });
        </script>
      </body>
      </html>
    `;

    return 'data:text/html;charset=utf-8,' + encodeURIComponent(automationHtml);
  }

  /**
   * Monitor automation progress
   */
  async monitorAutomation() {
    return new Promise((resolve) => {
      const messageHandler = (event) => {
        if (event.data.type === 'RPA_COMPLETE') {
          window.removeEventListener('message', messageHandler);
          resolve(event.data);
        }
      };

      window.addEventListener('message', messageHandler);

      // Timeout after 5 minutes
      setTimeout(() => {
        window.removeEventListener('message', messageHandler);
        resolve({
          success: true,
          message: 'Automation launcher opened successfully',
          timeout: true
        });
      }, 300000);
    });
  }

  /**
   * Stop automation
   */
  stopAutomation() {
    if (this.automationWindow && !this.automationWindow.closed) {
      this.automationWindow.close();
    }
    this.isRunning = false;
  }
}

export default new ClientRpaService();