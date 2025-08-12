"""
Generate a professional Global Secure Shield Health Insurance Policy document.
This creates a comprehensive insurance policy with authentic Indian insurance formatting.
"""

import asyncio
from mcp_client import MCPPDFClient

async def generate_insurance_policy_document():
    """Generate a professional Indian health insurance policy document"""
    
    # Create client instance
    client = MCPPDFClient("src/index.js")
    
    try:
        # Start the server
        await client.start_server()
        
        # First, create a custom insurance policy style
        print("🏥 Creating Global Secure Shield Insurance Policy Style...")
        
        insurance_style_css = """
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Noto+Sans:wght@400;600&display=swap');
        
        body {
            font-family: 'Roboto', 'Noto Sans', Arial, sans-serif;
            line-height: 1.5;
            color: #2c3e50;
            font-size: 11pt;
            margin: 0;
            padding: 20px;
        }
        
        .policy-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 25px;
            margin: -20px -20px 30px -20px;
            text-align: center;
            border-radius: 0 0 15px 15px;
        }
        
        .company-logo {
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .company-tagline {
            font-size: 12pt;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .policy-title {
            background-color: #f8fafc;
            border: 2px solid #e2e8f0;
            border-left: 6px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            font-size: 16pt;
            font-weight: 600;
            color: #1e40af;
            text-align: center;
        }
        
        .section-header {
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            color: white;
            padding: 12px 20px;
            margin: 25px 0 15px 0;
            font-weight: 600;
            font-size: 13pt;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        
        .info-card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .info-label {
            font-weight: 600;
            color: #4b5563;
            font-size: 10pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-weight: 500;
            color: #1f2937;
            font-size: 12pt;
        }
        
        .coverage-highlight {
            background: linear-gradient(135deg, #10b981, #34d399);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .coverage-amount {
            font-size: 24pt;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .coverage-text {
            font-size: 12pt;
            opacity: 0.9;
        }
        
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .benefit-item {
            background-color: #f0f9ff;
            border: 1px solid #bae6fd;
            border-left: 4px solid #0ea5e9;
            padding: 12px;
            border-radius: 6px;
        }
        
        .benefit-title {
            font-weight: 600;
            color: #0c4a6e;
            margin-bottom: 5px;
        }
        
        .benefit-detail {
            color: #475569;
            font-size: 10pt;
        }
        
        .exclusions-box {
            background-color: #fef2f2;
            border: 2px solid #fecaca;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .exclusions-title {
            color: #dc2626;
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 12pt;
        }
        
        .claim-process {
            background-color: #f0fdf4;
            border: 2px solid #bbf7d0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .claim-steps {
            counter-reset: step-counter;
        }
        
        .claim-step {
            counter-increment: step-counter;
            margin: 10px 0;
            padding-left: 30px;
            position: relative;
        }
        
        .claim-step::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            background-color: #22c55e;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9pt;
            font-weight: 600;
        }
        
        .premium-details {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .premium-amount {
            font-size: 20pt;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(135deg, #6b7280, #9ca3af);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        tr:nth-child(even) {
            background-color: #f9fafb;
        }
        
        .signature-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #d1d5db;
        }
        
        .regulatory-info {
            background-color: #f3f4f6;
            border: 1px solid #d1d5db;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 10pt;
            color: #4b5563;
        }
        
        .important-notice {
            background-color: #fef3c7;
            border: 2px solid #fcd34d;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .exclusions-section {
            background-color: #fef2f2;
            border: 1px solid #fca5a5;
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .contact-info {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .contact-info h3 {
            margin-top: 0;
            color: white;
            font-size: 16pt;
            margin-bottom: 15px;
        }
        
        .contact-info strong {
            color: #fbbf24;
            font-weight: 600;
        }
        
        .footer-disclaimer {
            font-size: 9pt;
            color: #6b7280;
            text-align: center;
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
        }
        """
        
        style_result = await client.create_custom_style(
            style_name="global_secure_shield_policy",
            description="Professional Health Insurance Policy Document for Global Secure Shield",
            prompt="Create a comprehensive insurance policy document with modern professional styling",
            theme="professional",
            format="A4",
            page_numbers=True,
            custom_css=insurance_style_css,
            header='<div style="text-align: center; font-size: 10px; color: #666; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Global Secure Shield - Health Insurance Policy Document</div>',
            footer='<div style="text-align: center; font-size: 9px; color: #666;">Page {pageNumber} | Confidential Document | IRDAI Reg. No.: 123456</div>'
        )
        
        print(f"✅ Insurance policy style created: {style_result['style_name']}")
        
        # Create the comprehensive insurance policy document content
        policy_content = """<div class="policy-header">
    <div class="company-logo">🛡️ GLOBAL SECURE SHIELD</div>
    <div class="company-tagline">Your Health, Our Priority | Comprehensive Insurance Solutions</div>
</div>

<div class="policy-title">
    HEALTH INSURANCE POLICY CERTIFICATE<br>
    <span style="font-size: 12pt; font-weight: 400;">(IRDAI Registration No.: 123456)</span>
</div>

---

## 1. Policy & Customer Information

<div class="section-header">📋 POLICY & CUSTOMER DETAILS</div>

<div class="info-grid">
    <div class="info-card">
        <div class="info-label">Policyholder Name</div>
        <div class="info-value">Rajesh Kumar Sharma</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy Number</div>
        <div class="info-value">GSS-2025-123456</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy Start Date</div>
        <div class="info-value">15 May 2023</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy End Date</div>
        <div class="info-value">14 May 2026 (3-year policy)</div>
    </div>
    <div class="info-card">
        <div class="info-label">Contact Address</div>
        <div class="info-value">Block A-123, Sector 15<br>New Delhi, India - 110025</div>
    </div>
    <div class="info-card">
        <div class="info-label">Contact Details</div>
        <div class="info-value">📱 +91-9876543254<br>📧 rajesh.sharma@gmail.com</div>
    </div>
</div>

### Insurer Information
**Company:** Global Secure Shield Insurance Company Limited  
**Licensed Office:** Global Secure Shield Tower, Plot No. 45, Financial District, Bandra Kurla Complex, Mumbai - 400051  
**Customer Service:** 1800-12-4567 (Toll Free)  
**Website:** www.globalsecureshield.com

---

## 2. Coverage Details

<div class="section-header">🏥 COMPREHENSIVE COVERAGE INFORMATION</div>

<div class="coverage-highlight">
    <div class="coverage-amount">₹5,00,000</div>
    <div class="coverage-text">Sum Insured (Individual Coverage)</div>
</div>

### Policy Type
**Comprehensive Health Insurance** - Individual Family Floater Plan

### Coverage Inclusions

<div class="benefits-grid">
    <div class="benefit-item">
        <div class="benefit-title">🏨 Hospitalization</div>
        <div class="benefit-detail">In-patient treatment for minimum 24 hours</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🏥 Room Rent</div>
        <div class="benefit-detail">Up to ₹5,000 per day (Private AC Room)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🚑 Ambulance Services</div>
        <div class="benefit-detail">Up to ₹3,000 per claim incident</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🔬 ICU Charges</div>
        <div class="benefit-detail">Intensive Care Unit expenses covered</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">💉 Day Care Treatments</div>
        <div class="benefit-detail">Same day discharge procedures</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🏥 Pre & Post Hospitalization</div>
        <div class="benefit-detail">30 days before, 60 days after</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">👶 Maternity Cover</div>
        <div class="benefit-detail">Up to ₹50,000 (after waiting period)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🩺 Annual Health Check-up</div>
        <div class="benefit-detail">Up to ₹2,000 per policy year</div>
    </div>
</div>

### Waiting Periods

| Condition Type | Waiting Period | Coverage Details |
|----------------|----------------|------------------|
| **General Illnesses** | 30 days | All acute conditions after policy inception |
| **Pre-existing Diseases** | 2 years | Conditions existing before policy start |
| **Maternity & Newborn** | 3 years | Pregnancy, delivery, and infant care |
| **Specific Diseases** | 2 years | Heart disease, cancer, kidney ailments |

---

## 3. Premium Details

<div class="section-header">💰 PREMIUM & PAYMENT INFORMATION</div>

<div class="premium-details">
    <div class="premium-amount">₹22,500</div>
    <div style="text-align: center; opacity: 0.9;">Total Annual Premium (Including 18% GST)</div>
</div>

### Payment Information
- **Base Premium:** ₹19,068
- **GST (18%):** ₹3,432
- **Total Premium:** ₹22,500
- **Payment Frequency:** Annual
- **Payment Mode:** Online Bank Transfer (NEFT/RTGS)
- **Payment Date:** 12 May 2023
- **Transaction ID:** GSS230512789456
- **Next Renewal Due:** 15 May 2026

### Premium Breakdown by Coverage

| Coverage Component | Premium Amount | Percentage |
|-------------------|----------------|------------|
| Base Health Cover | ₹15,000 | 66.7% |
| Maternity Benefit | ₹2,500 | 11.1% |
| Critical Illness | ₹1,568 | 7.0% |
| Service Tax & Fees | ₹3,432 | 15.2% |
| **Total** | **₹22,500** | **100%** |

---

## 4. Claim Process

<div class="section-header">📋 CURRENT CLAIM INFORMATION</div>

<div class="important-notice">
    <strong>🚨 Active Claim Details</strong><br>
    <strong>Claim Reference Number:</strong> HCL-2025-00458<br>
    <strong>Claim Amount:</strong> ₹1,85,000<br>
    <strong>Claim Date:</strong> 8 August 2025<br>
    <strong>Hospital:</strong> Apollo Hospital, New Delhi<br>
    <strong>Treatment:</strong> Cardiac Surgery (Angioplasty)<br>
    <strong>Status:</strong> Under Process - Pre-authorization Approved
</div>

### 📋 How to File a Claim

**Step-by-Step Claim Process:**

1. **Inform Immediately:** Call our 24x7 helpline within 24 hours of hospitalization
2. **Pre-authorization:** For cashless treatment, get pre-approval from network hospital  
3. **Submit Documents:** Provide all required documents within 15 days of discharge
4. **Claim Processing:** Our team will process your claim within 30 working days
5. **Settlement:** Approved amount will be settled directly to hospital or reimbursed

### Required Documents for Claims

#### For Hospitalization Claims:
- ✅ Duly filled and signed claim form
- ✅ Original hospital bills and payment receipts
- ✅ Doctor's prescription and discharge summary
- ✅ Diagnostic reports and test results
- ✅ Photo ID proof and policy document
- ✅ Bank account details for reimbursement

#### Additional Documents (if applicable):
- 📄 Police FIR (for accident cases)
- 📄 Employer certificate (for group policies)
- 📄 Death certificate (for nominee claims)

### Claim Submission Channels

| Method | Details | Processing Time |
|--------|---------|----------------|
| **Online Portal** | www.globalsecureshield.com/claims | 24-48 hours |
| **Mobile App** | GSS Claims App (Android/iOS) | 24-48 hours |
| **Email** | claims@globalsecureshield.com | 48-72 hours |
| **Toll-Free** | 1800-12-4567 | Immediate assistance |
| **Branch Visit** | Any GSS branch office | Same day |

---

## 5. Exclusions & Limitations

<div class="section-header">🚫 POLICY EXCLUSIONS</div>

<div class="exclusions-section">

### ⚠️ What's NOT Covered

**General Exclusions:**
- Cosmetic and plastic surgery (unless medically necessary)
- Self-inflicted injuries and attempted suicide
- Treatment outside India (except emergency)
- War, nuclear risks, and acts of terrorism
- Experimental or unproven treatments

**Treatment Exclusions:**
- Dental treatment (except due to accident)
- Eye glasses, contact lenses, hearing aids
- Naturopathy, homeopathy (unless specified)
- Routine check-ups and preventive care
- Obesity and weight control programs

**Condition-Based Exclusions:**
- Congenital diseases and birth defects
- Mental illness and psychiatric disorders
- Alcohol or drug-related treatments
- HIV/AIDS related treatments
- Genetic disorders

</div>

### Sub-limits and Co-payments

| Service | Limit/Co-payment | Notes |
|---------|------------------|-------|
| Room Rent | ₹5,000/day max | Private AC room category |
| ICU Charges | No sub-limit | Full coverage within sum insured |
| Ambulance | ₹3,000/claim | Ground ambulance only |
| Pre-Post Hospitalization | 30+60 days | Connected to main treatment |
| Annual Health Check | ₹2,000/year | Preventive care package |

---

## 6. Terms & Conditions

<div class="section-header">📋 IMPORTANT TERMS & CONDITIONS</div>

### General Terms

1. **Grace Period:** 30 days from due date for premium payment
2. **Free Look Period:** 15 days from policy receipt to review and return
3. **Renewal:** Lifetime renewability guaranteed (subject to terms)
4. **Age Limits:** Entry age 18-65 years, renewable up to 80 years
5. **Network Hospitals:** 8,500+ hospitals across India

### Policy Conditions

#### Medical Examination
- Not required for sum insured up to ₹5 lakhs for age below 45 years
- Pre-medical screening required for higher sum insured or older age

#### Pre-existing Diseases
- Must be declared at the time of proposal
- Covered after completion of 2-year waiting period
- Medical records may be verified before claim settlement

#### Modifications and Endorsements
- Policy can be modified subject to underwriting guidelines
- Endorsements require additional premium payment
- Changes effective from next policy anniversary

### Claim Settlement Process

#### Cashless Treatment
- Available at 8,500+ network hospitals
- Pre-authorization required for planned treatments
- Emergency cases: intimation within 24 hours

#### Reimbursement Claims
- Submit complete documents within 15 days of discharge
- Processing time: 30 working days from receipt of complete documents
- Settlement through NEFT/RTGS to registered bank account

---

## 7. Regulatory & Contact Information

<div class="section-header">📞 REGULATORY COMPLIANCE & CONTACT DETAILS</div>

<div class="regulatory-info">
    <strong>🏛️ Regulatory Information</strong><br>
    <strong>IRDAI Registration No.:</strong> 123456<br>
    <strong>Valid until:</strong> 31 March 2026<br>
    <strong>Category:</strong> General Insurance Company<br>
    <strong>License Date:</strong> 15 April 2001<br>
    <strong>Complaint Reference:</strong> IRDAI Complaint Portal - www.irdai.gov.in
</div>



### Branch Offices

| City | Address | Contact |
|------|---------|---------|
| **New Delhi** | Connaught Place, CP Metro Station | +91-11-2341-5678 |
| **Mumbai** | Nariman Point, Near RBI Building | +91-22-6789-0123 |
| **Bangalore** | MG Road, Brigade Center | +91-80-4567-8901 |
| **Chennai** | Anna Salai, Express Towers | +91-44-2890-1234 |
| **Kolkata** | Park Street, AJC Bose Road | +91-33-5678-9012 |

---

<div class="signature-section">

### Digital Signatures & Validation

<table style="border: none;">
<tr style="border: none;">
<td style="border: none; width: 50%; text-align: center; padding: 20px;">
<strong>Policy Issued By:</strong><br><br>
<strong>Amit Kumar Singh</strong><br>
Senior Underwriting Manager<br>
Global Secure Shield Insurance<br>
Employee ID: GSS001234<br>
<em>Digital Signature Applied</em><br>
<em>Date: 15 May 2023</em>
</td>
<td style="border: none; width: 50%; text-align: center; padding: 20px;">
<strong>Verified By:</strong><br><br>
<strong>Dr. Priya Sharma</strong><br>
Chief Medical Officer<br>
Global Secure Shield Insurance<br>
Employee ID: GSS001567<br>
<em>Medical Approval Applied</em><br>
<em>Date: 15 May 2023</em>
</td>
</tr>
</table>

</div>

<div class="important-notice">
    <strong>🔒 Important Security Information</strong><br>
    This policy certificate is generated electronically and is valid without physical signature. 
    Policy authenticity can be verified online at www.globalsecureshield.com using policy number GSS-2025-123456.
    Any alterations or modifications to this document will render it invalid.
</div>

<div class="footer-disclaimer">
    <strong>Disclaimer:</strong> This policy is subject to terms, conditions, and exclusions mentioned in the policy wordings. 
    For complete terms and conditions, please refer to the policy document. In case of any dispute, 
    the English version of the policy shall prevail. This policy is regulated by the Insurance Regulatory 
    and Development Authority of India (IRDAI).<br><br>
    
### Important Disclaimer

**Beware of Spurious/Fake Calls:** IRDAI clarifies to public that IRDAI or its officials do not involve in activities like sale of any kind of insurance or investment products nor invest premium or deposits. Public receiving such phone calls are requested to lodge a police complaint along with details of phone call, number.
</div>"""
        
        # Generate the insurance policy document
        print("🏥 Generating Global Secure Shield Insurance Policy Document...")
        
        output_path = client.get_pdf_path("global_secure_shield_health_policy.pdf")
        
        pdf_result = await client.generate_pdf_with_style(
            style_name="global_secure_shield_policy",
            content=policy_content,
            output_path=output_path
        )
        
        print(f"✅ Insurance policy document generated successfully!")
        print(f"📄 File location: {pdf_result['output_path']}")
        print(f"📊 File size: {pdf_result['file_size']:,} bytes")
        print(f"📋 Total pages: {pdf_result['page_count']}")
        print(f"⏱️ Generation time: {pdf_result['generation_time_ms']}ms")
        
        if pdf_result.get('warnings'):
            print(f"⚠️ Warnings: {pdf_result['warnings']}")
        
        print(f"\n🎨 Document Style: {pdf_result.get('style_used', 'Global Secure Shield Policy Style')}")
        
    except Exception as e:
        print(f"❌ Error generating insurance policy: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.close()

if __name__ == "__main__":
    print("🛡️ Global Secure Shield - Health Insurance Policy Generator")
    print("=" * 70)
    asyncio.run(generate_insurance_policy_document())
    print("\n🎉 Insurance policy document generation completed!")
    print("\nThe document includes:")
    print("✓ Professional insurance company branding and styling")
    print("✓ Complete policy information with all required sections")
    print("✓ Authentic Indian insurance formatting and terminology")
    print("✓ Realistic coverage details, premiums, and claim information")
    print("✓ Regulatory compliance information (IRDAI)")
    print("✓ Professional layout with modern design elements")
    print("✓ Contact information and customer service details")
