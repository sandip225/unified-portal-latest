// Torrent Power Auto-Fill Content Script
// This script runs on the official Torrent Power website

console.log('🤖 Torrent Power Auto-Fill Script Loaded');

// Check if we're on the correct page
if (window.location.hostname.includes('torrentpower.com') &&
    window.location.pathname.includes('namechangerequest')) {

    console.log('✅ On Torrent Power name change page');

    // Wait for page to load completely
    if (document.readyState === 'complete') {
        initializeAutoFill();
    } else {
        window.addEventListener('load', initializeAutoFill);
    }
}

function initializeAutoFill() {
    console.log('🔄 Initializing auto-fill...');

    // Check for stored form data
    const storedData = localStorage.getItem('aiFormData');
    if (storedData) {
        try {
            const userData = JSON.parse(storedData);
            console.log('📦 Found stored form data:', userData);

            // Start auto-fill after 2 seconds
            setTimeout(() => {
                startVisibleAutoFill(userData);
                // Clean up after use
                localStorage.removeItem('aiFormData');
            }, 2000);

        } catch (error) {
            console.error('❌ Error parsing stored data:', error);
        }
    } else {
        console.log('ℹ️ No stored form data found');
    }

    // Listen for messages from parent window
    window.addEventListener('message', function (event) {
        console.log('📨 Message received:', event.data);

        if (event.data.type === 'FILL_FORM') {
            console.log('🔄 Starting form filling from message...');
            startVisibleAutoFill(event.data.data);
        }
    });
}

async function startVisibleAutoFill(userData) {
    try {
        console.log('🤖 Starting visible auto-fill with data:', userData);

        let currentStep = 0;
        const totalSteps = 8;

        // Show progress indicator
        function showProgress(step, message) {
            const existing = document.querySelector('.ai-progress-indicator');
            if (existing) existing.remove();

            const progressDiv = document.createElement('div');
            progressDiv.className = 'ai-progress-indicator';
            progressDiv.innerHTML = `
                <div style="position: fixed; top: 20px; left: 20px; background: #3B82F6; color: white; padding: 15px 25px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); z-index: 10000; font-family: Arial, sans-serif; min-width: 300px;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <div style="width: 24px; height: 24px; border: 3px solid #60A5FA; border-top: 3px solid white; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                        <div style="font-weight: bold; font-size: 16px;">🤖 AI Auto-Filling Form</div>
                    </div>
                    <div style="font-size: 14px; margin-bottom: 10px;">Step ${step}/${totalSteps}: ${message}</div>
                    <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: white; height: 100%; width: ${(step / totalSteps) * 100}%; transition: width 0.5s ease; border-radius: 3px;"></div>
                    </div>
                </div>
                <style>
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                </style>
            `;
            document.body.appendChild(progressDiv);
        }

        // Animated field filling
        function fillFieldWithAnimation(field, value, fieldName) {
            return new Promise((resolve) => {
                if (!field || !value) {
                    resolve();
                    return;
                }

                // Scroll to field
                field.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Highlight field
                field.style.border = '3px solid #3B82F6';
                field.style.boxShadow = '0 0 15px rgba(59, 130, 246, 0.5)';
                field.style.backgroundColor = '#EBF8FF';

                // Clear and focus
                field.value = '';
                field.focus();

                // Type animation
                let i = 0;
                const typeInterval = setInterval(() => {
                    if (i < value.length) {
                        field.value += value[i];
                        field.dispatchEvent(new Event('input', { bubbles: true }));
                        i++;
                    } else {
                        clearInterval(typeInterval);

                        // Final events
                        field.dispatchEvent(new Event('change', { bubbles: true }));
                        field.dispatchEvent(new Event('blur', { bubbles: true }));

                        // Success styling
                        field.style.border = '3px solid #10B981';
                        field.style.boxShadow = '0 0 15px rgba(16, 185, 129, 0.5)';
                        field.style.backgroundColor = '#ECFDF5';

                        // Add checkmark
                        const checkmark = document.createElement('span');
                        checkmark.innerHTML = '✅';
                        checkmark.style.position = 'absolute';
                        checkmark.style.right = '10px';
                        checkmark.style.top = '50%';
                        checkmark.style.transform = 'translateY(-50%)';
                        checkmark.style.fontSize = '18px';
                        checkmark.style.zIndex = '1000';

                        // Position checkmark
                        if (field.parentElement.style.position !== 'relative') {
                            field.parentElement.style.position = 'relative';
                        }
                        field.parentElement.appendChild(checkmark);

                        console.log(`✅ ${fieldName} filled with: ${value}`);

                        setTimeout(() => {
                            field.style.border = '';
                            field.style.boxShadow = '';
                            field.style.backgroundColor = '';
                            resolve();
                        }, 800);
                    }
                }, 150); // Slower typing for better visibility
            });
        }

        // Find field helper
        function findField(selectors) {
            for (const selector of selectors) {
                const field = document.querySelector(selector);
                if (field) {
                    console.log(`✅ Found field with selector: ${selector}`);
                    return field;
                }
            }
            console.log(`❌ No field found for selectors:`, selectors);
            return null;
        }

        // Step 1: City
        currentStep = 1;
        showProgress(currentStep, 'Selecting City...');
        const cityField = findField([
            'select[name*="city"]',
            'select[id*="city"]',
            'select[aria-label*="City"]',
            'div[role="combobox"] input', // Modern frameworks often hide native selects
            'select' // If logical first select
        ]);

        // Handle select specifically (setting value and dispatching change)
        if (cityField) {
            // Try to find matching option
            let foundOption = false;
            if (cityField.tagName === 'SELECT') {
                // Try exact match
                for (let i = 0; i < cityField.options.length; i++) {
                    if (cityField.options[i].text.toLowerCase() === userData.city.toLowerCase() ||
                        cityField.options[i].value.toLowerCase() === userData.city.toLowerCase()) {
                        cityField.selectedIndex = i;
                        foundOption = true;
                        break;
                    }
                }
                // If not found, try contains
                if (!foundOption) {
                    for (let i = 0; i < cityField.options.length; i++) {
                        if (cityField.options[i].text.toLowerCase().includes(userData.city.toLowerCase())) {
                            cityField.selectedIndex = i;
                            foundOption = true;
                            break;
                        }
                    }
                }
            } else {
                // Input based city (searchable dropdown)
                await fillFieldWithAnimation(cityField, userData.city, 'City');
            }

            if (foundOption || cityField.tagName !== 'SELECT') {
                cityField.dispatchEvent(new Event('change', { bubbles: true }));
                // Highlight success
                cityField.style.border = '3px solid #10B981';
                console.log(`✅ City selected: ${userData.city}`);
            }
        }
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 2: Service Number
        currentStep = 2;
        showProgress(currentStep, 'Filling Service/Consumer Number...');
        const serviceField = findField([
            'input[placeholder*="Service"]',
            'input[placeholder*="Consumer"]',
            'input[name*="service"]',
            'input[name*="consumer"]',
            'input[name*="connection"]'
        ]);
        await fillFieldWithAnimation(serviceField, userData.connection_id, 'Service Number');
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 3: Transaction Number
        currentStep = 3;
        showProgress(currentStep, 'Filling Transaction/Reference ID...');
        const transactionField = findField([
            'input[placeholder*="Transaction"]',
            'input[placeholder*="Reference"]',
            'input[name*="transaction"]',
            'input[name*="reference"]',
            'input[name*="tno"]',
            'input[name*="t_no"]' // Common variations
        ]);
        await fillFieldWithAnimation(transactionField, userData.t_number || userData.transaction_number, 'Transaction Number');
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 4: Mobile Number
        currentStep = 4;
        showProgress(currentStep, 'Filling Mobile Number...');
        const mobileField = findField([
            'input[placeholder*="Mobile"]',
            'input[placeholder*="mobile"]',
            'input[type="tel"]',
            'input[name*="mobile"]'
        ]);
        await fillFieldWithAnimation(mobileField, userData.mobile, 'Mobile Number');
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 5: Email
        currentStep = 5;
        showProgress(currentStep, 'Filling Email Address...');
        const emailField = findField([
            'input[type="email"]',
            'input[placeholder*="Email"]',
            'input[placeholder*="email"]',
            'input[name*="email"]'
        ]);
        await fillFieldWithAnimation(emailField, userData.email, 'Email Address');
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 6: Confirm Email
        currentStep = 6;
        showProgress(currentStep, 'Confirming Email Address...');
        const confirmEmailField = findField([
            'input[placeholder*="Confirm"]',
            'input[placeholder*="confirm"]',
            'input[name*="confirm"]',
            'input[name*="verify"]'
        ]);
        await fillFieldWithAnimation(confirmEmailField, userData.email, 'Confirm Email');
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 7: Generate Captcha
        currentStep = 7;
        showProgress(currentStep, 'Generating Captcha...');
        const regenerateBtn = findField([
            'a[onclick*="regenerate"]',
            'button[onclick*="regenerate"]',
            '.regenerate',
            'a[href*="regenerate"]'
        ]);
        if (regenerateBtn) {
            regenerateBtn.click();
            console.log('✅ Captcha regenerated');
        }
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Step 8: Secure Form
        currentStep = 8;
        showProgress(currentStep, 'Securing form - Please enter captcha...');

        // Disable submit button for safety
        const submitButtons = document.querySelectorAll(
            'input[type="submit"], button[type="submit"], input[value*="Submit"], button[onclick*="submit"]'
        );

        submitButtons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
            btn.title = 'Form filled by AI - Please enter captcha and review before submitting';

            // Add indicator
            if (!btn.querySelector('.ai-filled-indicator')) {
                const indicator = document.createElement('span');
                indicator.className = 'ai-filled-indicator';
                indicator.innerHTML = ' 🤖 AI Filled - Enter Captcha';
                indicator.style.fontSize = '12px';
                indicator.style.color = '#666';
                indicator.style.marginLeft = '8px';
                btn.appendChild(indicator);
            }
        });

        // Show completion message
        setTimeout(() => {
            const existing = document.querySelector('.ai-progress-indicator');
            if (existing) existing.remove();

            const completionDiv = document.createElement('div');
            completionDiv.innerHTML = `
                <div style="position: fixed; top: 20px; left: 20px; background: #10B981; color: white; padding: 20px 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); z-index: 10000; font-family: Arial, sans-serif; min-width: 350px;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                        <span style="font-size: 24px;">🎉</span>
                        <div>
                            <div style="font-weight: bold; font-size: 18px; margin-bottom: 4px;">Form Filled Successfully!</div>
                            <div style="font-size: 14px; opacity: 0.9;">Please complete the remaining steps</div>
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; margin-top: 12px;">
                        <div style="font-size: 13px; font-weight: bold; margin-bottom: 6px;">⚠️ Next Steps:</div>
                        <div style="font-size: 12px; line-height: 1.4;">
                            1. Enter the captcha code<br>
                            2. Review all filled information<br>
                            3. Click Submit to complete your application
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(completionDiv);

            // Remove after 15 seconds
            setTimeout(() => {
                if (completionDiv.parentNode) {
                    completionDiv.parentNode.removeChild(completionDiv);
                }
            }, 15000);
        }, 1000);

        console.log('🎉 Auto-fill completed successfully!');

    } catch (error) {
        console.error('❌ Auto-fill error:', error);

        // Show error message
        const errorDiv = document.createElement('div');
        errorDiv.innerHTML = `
            <div style="position: fixed; top: 20px; left: 20px; background: #EF4444; color: white; padding: 15px 25px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); z-index: 10000; font-family: Arial, sans-serif;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">❌</span>
                    <div>
                        <div style="font-weight: bold; margin-bottom: 4px;">Auto-Fill Failed</div>
                        <div style="font-size: 12px; opacity: 0.9;">Error: ${error.message}</div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(errorDiv);

        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

console.log('✅ Torrent Power Auto-Fill Script Ready!');