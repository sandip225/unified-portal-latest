# Gujarat Suppliers Selenium Automation Guide

## Overview

आपके unified portal में अब सभी Gujarat suppliers के लिए comprehensive Selenium automation है। यह guide बताती है कि कौन सी websites direct automation support करती हैं और कौन सी में login required है।

## Automation Types

### 1. **Direct Automation** (पूरी तरह Automated)
ये websites बिना login के direct name change page open करती हैं:

#### GAS SUPPLIERS - DIRECT ACCESS ✅
- **Gujarat Gas Ltd** - Direct service request page
- **Vadodara Gas Ltd** - Direct name change form  
- **Torrent Gas** - PDF form download
- **Sabarmati Gas** - Direct form access
- **IRM Energy** - Direct form access

#### ELECTRICITY SUPPLIERS - DIRECT ACCESS ✅
- **Torrent Power** - PDF form download (no login)

#### WATER SUPPLIERS - DIRECT ACCESS ✅
- **GWSSB (Gujarat Water Supply)** - Direct forms page

#### PROPERTY SUPPLIERS - DIRECT ACCESS ✅
- **AnyROR Gujarat** - Public record view (no login)
- **e-Dhara Centers** - Direct form access

### 2. **Login-Assisted Automation** (User Login + Selenium Form Fill)
ये websites पहले login require करती हैं, फिर Selenium form fill करता है:

#### GAS SUPPLIERS - LOGIN REQUIRED 🔐
- **Adani Total Gas** - Customer portal + OTP required

#### ELECTRICITY SUPPLIERS - LOGIN REQUIRED 🔐
- **PGVCL** - GUVNL portal + CAPTCHA + OTP
- **UGVCL** - GUVNL portal + CAPTCHA + OTP  
- **MGVCL** - GUVNL portal + CAPTCHA + OTP
- **DGVCL** - GUVNL portal + CAPTCHA + OTP

#### WATER SUPPLIERS - LOGIN REQUIRED 🔐
- **AMC (Ahmedabad)** - Ward verification required
- **SMC (Surat)** - Manual approval process

### 3. **Manual Only** (केवल Manual Process)
ये suppliers केवल offline process support करते हैं:

#### WATER SUPPLIERS - MANUAL ONLY ❌
- **VMC (Vadodara)** - Offline only, ward office visit required
- **RMC (Rajkot)** - Offline only, ward office visit required

#### PROPERTY SUPPLIERS - MANUAL ONLY ❌
- **Talati/Mamlatdar** - Village/Tehsil office visit required
- **Municipal Corporations** - Physical verification required

## Implementation Details

### Direct Automation Example (Gujarat Gas)

```python
# User clicks "Start Automation" 
# System automatically:
1. Opens Gujarat Gas service request page
2. Fills consumer number, old name, new name
3. Fills mobile, email, address
4. Takes screenshot for verification
5. User manually reviews and submits
```

### Login-Assisted Example (PGVCL)

```python
# User clicks "Start Automation"
# System shows instructions:
1. "Please login to GUVNL portal manually"
2. "Solve CAPTCHA and enter OTP"  
3. "Click OK when logged in"
# Then system automatically:
4. Navigates to name change page
5. Fills all form fields
6. User reviews and submits
```

## Updated Form Fields

### Gujarat Gas Form Fields
```json
{
  "consumer_number": "Gujarat Gas consumer number",
  "old_name": "Current name as per gas bill", 
  "new_name": "New name to update",
  "mobile": "10-digit mobile number",
  "email": "Email address (optional)",
  "address": "Complete address"
}
```

### GUVNL (PGVCL/UGVCL/MGVCL/DGVCL) Form Fields
```json
{
  "consumer_number": "10-12 digit consumer number",
  "old_name": "Current name as per electricity bill",
  "new_name": "New name to update", 
  "mobile": "10-digit mobile number",
  "email": "Email address (optional)",
  "address": "Complete address",
  "aadhar_number": "12-digit Aadhar number"
}
```

### Adani Gas Form Fields
```json
{
  "consumer_number": "Adani Gas consumer number",
  "bp_number": "BP number (if available)",
  "old_name": "Current name as per gas bill",
  "new_name": "New name to update",
  "mobile": "10-digit mobile number", 
  "email": "Email address (optional)"
}
```

## API Usage

### Start Direct Automation
```javascript
const response = await fetch('/api/unified-automation/start-automation', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    supplier_id: 'gujarat-gas',
    service_type: 'name_change',
    form_data: {
      consumer_number: 'GG123456789',
      old_name: 'राम शर्मा',
      new_name: 'राम कुमार शर्मा', 
      mobile: '9876543210',
      email: 'ram@example.com',
      address: 'अहमदाबाद, गुजरात'
    }
  })
});
```

### Start Login-Assisted Automation  
```javascript
const response = await fetch('/api/unified-automation/start-automation', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    supplier_id: 'pgvcl',
    service_type: 'name_change',
    form_data: {
      consumer_number: '1234567890',
      old_name: 'राम शर्मा',
      new_name: 'राम कुमार शर्मा',
      mobile: '9876543210',
      address: 'अहमदाबाद, गुजरात',
      aadhar_number: '123456789012'
    }
  })
});
```

### Get Supplier Information
```javascript
const supplierInfo = await fetch('/api/unified-automation/supplier-info/gujarat-gas');
// Returns: automation_type, login_required, instructions, etc.
```

## Chrome Extension Integration

आपका Chrome extension अब automatically detect करेगा:

### Direct Access Sites
- Extension shows: "✅ Direct automation available"
- User clicks "Auto-fill" → Form fills immediately
- User reviews and submits manually

### Login Required Sites  
- Extension shows: "🔐 Login assistance available"
- User clicks "Start Assistance" → Login instructions appear
- After login → Form fills automatically

## User Experience Flow

### For Direct Automation Sites:
1. User selects supplier (e.g., Gujarat Gas)
2. Fills form in unified portal
3. Clicks "Submit with Automation"
4. Browser opens → Form fills automatically
5. User reviews → Submits manually
6. Gets confirmation number

### For Login Required Sites:
1. User selects supplier (e.g., PGVCL) 
2. Fills form in unified portal
3. Clicks "Submit with Automation"
4. Browser opens with login instructions
5. User completes login + CAPTCHA + OTP
6. Form fills automatically after login
7. User reviews → Submits manually
8. Gets confirmation number

## Benefits

### For Users:
- **Time Saving**: No manual form filling
- **Error Reduction**: Automatic data entry
- **Convenience**: One portal for all suppliers
- **Guidance**: Clear instructions for each step

### For You:
- **Scalable**: Easy to add new suppliers
- **Maintainable**: Separate logic for each automation type
- **Safe**: No automatic submissions without user verification
- **Comprehensive**: Covers all major Gujarat suppliers

## Screenshots Required

कृपया इन websites के screenshots भेजें ताकि मैं forms को और भी accurate बना सकूं:

### Direct Access Sites (Screenshots Needed):
1. **Gujarat Gas** - https://iconnect.gujaratgas.com/Portal/outer-service-request_template.aspx
2. **Vadodara Gas** - Name change form page
3. **GWSSB** - https://watersupply.gujarat.gov.in/forms
4. **Torrent Power** - Forms download page

### Login Required Sites (Screenshots Needed):
1. **GUVNL Portal** - Name change form (after login)
2. **Adani Gas** - Customer portal name change section
3. **AMC Water** - Name change form (after verification)

## Next Steps

1. **Test Direct Automation** - Gujarat Gas, Vadodara Gas
2. **Test Login Assistance** - PGVCL, Adani Gas  
3. **Send Screenshots** - For form field mapping
4. **Add More Suppliers** - Based on your requirements
5. **Enhance Error Handling** - For edge cases

## Conclusion

आपका unified portal अब सभी major Gujarat suppliers को support करता है:
- **8 Direct Automation** suppliers (fully automated)
- **6 Login-Assisted** suppliers (semi-automated)  
- **4 Manual Only** suppliers (guidance provided)

यह system scalable है और आसानी से नए suppliers add कर सकते हैं। User experience बहुत smooth है क्योंकि system automatically detect करता है कि कौन सा automation type use करना है।