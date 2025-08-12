#!/usr/bin/env python3
"""
Insurance Policy Conversational Agent

A conversational AI agent that helps users create, customize, and generate 
insurance policy documents through natural language interaction.

Features:
- Interactive conversation for policy requirements gathering
- Multiple insurance policy types (Health, Auto, Life, etc.)
- PDF generation with customizable styles
- Real-time conversation flow with memory
- Integration with Azure AI Projects and MCP PDF server

Usage:
    python policy_agent.py
"""

import asyncio
import json
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
import re

# pip install azure-ai-projects==1.0.0b10
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Local imports
from mcp_client import MCPPDFClient
from insurance_policy_generator import generate_insurance_policy_document

class ConversationalPolicyAgent:
    """
    A conversational agent for insurance policy generation and management.
    """
    
    def __init__(self):
        """Initialize the conversational policy agent."""
        self.project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str="eastus2.api.azureml.ms;aee23923-3bba-468d-8dcd-7c4bc1ce218f;rg-ronakofficial1414-9323_ai;ronakofficial1414-8644"
        )
        
        # Get the agent
        self.agent = self.project_client.agents.get_agent("asst_Alqk3fukB9d6YPtjmaAitp1e")
        
        # Create a conversation thread
        self.thread = None
        
        # Conversation state
        self.conversation_history = []
        self.user_profile = {}
        self.policy_requirements = {}
        self.conversation_active = True
        
        # MCP client for PDF generation
        self.mcp_client = None
        
        print("🤖 Insurance Policy Agent initialized!")
        print("💡 I can help you create and customize insurance policies through conversation.")
    
    async def start_conversation(self):
        """Start a new conversation thread."""
        try:
            self.thread = self.project_client.agents.create_thread()
            print(f"✅ Started new conversation thread: {self.thread.id}")
            
            # Send welcome message
            await self.send_welcome_message()
            
        except Exception as e:
            print(f"❌ Error starting conversation: {e}")
            return False
        
        return True
    
    async def send_welcome_message(self):
        """Send a welcome message to start the conversation."""
        welcome_msg = """
🏥 Welcome to Global Secure Shield Insurance Policy Assistant! 

I'm here to help you with all your insurance needs including:

📋 **General Insurance Support:**
• Answer questions about insurance policies
• Explain coverage options and benefits
• Help with claims processes
• Provide policy information

🔧 **Enhanced Policy Generation:**
• Generate comprehensive policy documents from customer data
• Create detailed policy certificates with all necessary information
• Include claim details, coverage information, and regulatory compliance

**For Policy Generation, provide JSON input like:**
```json
{
  "customerName": "Rajesh Kumar Sharma",
  "policyNumber": "GSS-2025-123456", 
  "claimType": "health",
  "claimAmount": 185000,
  "policyStartDate": "2023-05-15"
}
```

**I can create policies for:**
• Health Insurance
• Auto Insurance  
• Life Insurance
• Property Insurance

What can I help you with today?
"""
        print("🤖 Agent:", welcome_msg)
    
    async def send_message_to_agent(self, user_input: str) -> str:
        """Send a message to the Azure AI agent and get response."""
        try:
            # Create message in the thread
            message = self.project_client.agents.create_message(
                thread_id=self.thread.id,
                role="user",
                content=user_input
            )
            
            # Process the message with the agent
            run = self.project_client.agents.create_and_process_run(
                thread_id=self.thread.id,
                agent_id=self.agent.id
            )
            
            # Get the latest messages
            messages = self.project_client.agents.list_messages(thread_id=self.thread.id)
            
            # Get the latest assistant response
            for message in messages:
                if hasattr(message, 'role') and message.role == "assistant":
                    # Handle different content types
                    if hasattr(message, 'content'):
                        if isinstance(message.content, str):
                            return message.content
                        elif hasattr(message.content, 'text'):
                            return message.content.text
                        else:
                            return str(message.content)
            
            # Alternative approach - get from text_messages
            for text_message in messages.text_messages:
                if hasattr(text_message, 'content'):
                    return text_message.content
                elif hasattr(text_message, 'text'):
                    return text_message.text
                else:
                    # Try to get the content from the message dict
                    msg_dict = text_message.as_dict() if hasattr(text_message, 'as_dict') else text_message
                    if isinstance(msg_dict, dict) and 'content' in msg_dict:
                        return msg_dict['content']
            
            return "I'm sorry, I didn't understand that. Could you please rephrase?"
            
        except Exception as e:
            print(f"❌ Error communicating with agent: {e}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def parse_policy_json(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Parse JSON input for policy generation."""
        try:
            # Try to find JSON in the input
            import json
            
            # Look for JSON pattern in the input
            start_idx = user_input.find('{')
            end_idx = user_input.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = user_input[start_idx:end_idx]
                
                # Clean up common JSON formatting issues
                json_str = json_str.strip()
                
                # Remove trailing commas before closing braces/brackets
                import re
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                
                # Remove any extra whitespace around colons and commas
                json_str = re.sub(r'\s*:\s*', ':', json_str)
                json_str = re.sub(r'\s*,\s*', ',', json_str)
                
                # Try to parse the cleaned JSON
                try:
                    policy_data = json.loads(json_str)
                    return policy_data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"📝 Cleaned JSON was: {json_str}")
                    
                    # Try alternative parsing methods
                    try:
                        # Remove quotes around keys if they exist
                        import ast
                        policy_data = ast.literal_eval(json_str)
                        return policy_data
                    except:
                        print("💡 Please check your JSON format. Here's a correct example:")
                        print("""
{
  "customerName": "Rajesh Kumar Sharma",
  "policyNumber": "GSS-2025-123456",
  "claimType": "health",
  "claimAmount": 185000,
  "policyStartDate": "2023-05-15"
}""")
                        return None
            
            return None
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
            print("💡 Please provide valid JSON format for policy generation.")
            return None
    
    def generate_comprehensive_policy_document(self, policy_data: Dict[str, Any]) -> str:
        """Generate a comprehensive policy document based on input data."""
        
        # Extract data with defaults
        customer_name = policy_data.get('customerName', 'Valued Customer')
        policy_number = policy_data.get('policyNumber', f'GSS-{datetime.now().year}-{datetime.now().strftime("%m%d%H%M")}')
        claim_type = policy_data.get('claimType', 'health').lower()
        claim_amount = policy_data.get('claimAmount', 0)
        policy_start_date = policy_data.get('policyStartDate', datetime.now().strftime('%Y-%m-%d'))
        
        # Generate comprehensive policy document
        policy_document = f"""
# GLOBAL SECURE SHIELD INSURANCE POLICY

## 🏥 COMPREHENSIVE {claim_type.upper()} INSURANCE POLICY

**Policy Document Number:** {policy_number}
**Issue Date:** {datetime.now().strftime('%d %B %Y')}
**Valid From:** {policy_start_date}

---

## 1. POLICY HOLDER INFORMATION

**Full Name:** {customer_name}
**Policy Number:** {policy_number}
**Policy Type:** {claim_type.title()} Insurance
**Policy Status:** Active
**Policy Inception Date:** {policy_start_date}
**Policy Expiry Date:** {datetime.now().replace(year=datetime.now().year + 1).strftime('%Y-%m-%d')}
**Sum Insured:** ₹{claim_amount:,}

---

## 2. COVERAGE DETAILS

### Primary Coverage Benefits:
"""

        # Add specific coverage based on claim type
        if claim_type == 'health':
            policy_document += f"""
🏥 **HEALTH INSURANCE COVERAGE**

**Sum Insured:** ₹{claim_amount:,} per policy year
**Family Floater:** Yes (Covers entire family)
**Room Rent Limit:** Single Private AC Room
**ICU Charges:** 100% coverage up to sum insured
**Pre & Post Hospitalization:** 30 days before, 60 days after
**Ambulance Services:** Up to ₹5,000 per claim
**Annual Health Checkup:** ₹3,000 per member
**Maternity Coverage:** ₹75,000 (after 3-year waiting period)
**Newborn Coverage:** Immediate coverage for 90 days
**Day Care Procedures:** 200+ procedures covered
**Alternative Treatment:** AYUSH treatments up to ₹25,000

### Specific Disease Coverage:
- **Cancer Treatment:** 100% sum insured
- **Heart Disease:** Complete cardiac procedures
- **Kidney Treatment:** Dialysis and transplant
- **Organ Transplant:** Donor and recipient expenses
- **Mental Health:** In-patient psychiatric treatment
- **Modern Treatment:** Robotic surgery, stem cell therapy

### Additional Benefits:
- **Second Medical Opinion:** Consultation with specialists
- **Emergency Medical Evacuation:** Within India
- **Domiciliary Treatment:** Home treatment for 30+ days
- **Convalescence Benefit:** ₹1,000 per day (max 10 days)
- **Critical Illness Cover:** 22 critical illnesses covered
"""

        elif claim_type == 'auto':
            policy_document += f"""
🚗 **AUTO INSURANCE COVERAGE**

**Vehicle Insured Value:** ₹{claim_amount:,}
**Policy Type:** Comprehensive Auto Insurance
**Third-Party Liability:** ₹15,00,000 (as per Motor Tariff)
**Personal Accident Cover:** ₹15,00,000 for owner-driver
**Vehicle Damage:** Complete coverage against accidents, theft, fire
**Natural Calamities:** Flood, earthquake, cyclone coverage
**Man-made Calamities:** Riots, strikes, terrorism

### Coverage Inclusions:
- **Total Loss/Theft:** 100% Insured Declared Value
- **Partial Loss:** Repair costs up to IDV
- **Engine Protection:** Against water ingress damage
- **Zero Depreciation:** Brand new spare parts replacement
- **Roadside Assistance:** 24x7 emergency services
- **Key Replacement:** Lost key reimbursement
- **Tyre Protection:** Damage to tyres and tubes
- **Return to Invoice:** Gap between IDV and invoice value

### Add-on Covers:
- **Engine Secure:** Water damage protection
- **Consumables Cover:** Oil, nuts, bolts, washers
- **NCB Protector:** No claim bonus protection
- **Daily Allowance:** ₹500 per day during repairs
"""

        elif claim_type == 'life':
            policy_document += f"""
💖 **LIFE INSURANCE COVERAGE**

**Sum Assured:** ₹{claim_amount:,}
**Policy Term:** 20 years
**Premium Payment Term:** 15 years
**Policy Type:** Term Life Insurance with Return of Premium
**Death Benefit:** 100% sum assured to nominee
**Maturity Benefit:** 105% of premiums paid (if survived)
**Terminal Illness Benefit:** 50% of sum assured
**Accidental Death Benefit:** Additional ₹{claim_amount:,}

### Key Features:
- **Immediate Coverage:** No waiting period for accidental death
- **Life Stage Benefits:** Increasing cover at marriage, childbirth
- **Premium Waiver:** On permanent disability
- **Loan Facility:** After 3 years (up to 90% of surrender value)
- **Tax Benefits:** Under Section 80C and 10(10D)
- **Grace Period:** 30 days for premium payment
- **Free Look Period:** 15 days for policy review
"""

        # Add common sections
        policy_document += f"""

---

## 3. PREMIUM INFORMATION

**Annual Premium:** ₹{max(25000, claim_amount // 20):,}
**GST (18%):** ₹{max(4500, claim_amount // 111):,}
**Total Premium:** ₹{max(29500, claim_amount // 17):,}
**Payment Mode:** Annual
**Payment Method:** Online Banking / UPI / Credit Card
**Next Due Date:** {datetime.now().replace(year=datetime.now().year + 1).strftime('%d %B %Y')}

### Premium Benefits:
- **No Claim Bonus:** 10% discount per claim-free year (up to 50%)
- **Online Discount:** 5% discount for online policy purchase
- **Long Term Discount:** 7.5% for 2-year, 15% for 3-year policies
- **Multi-Policy Discount:** 10% for multiple policies

---

## 4. EXCLUSIONS

### General Exclusions:
❌ Pre-existing diseases (first 2 years)
❌ Self-inflicted injuries and suicide
❌ War, nuclear risks, and terrorism (unless covered)
❌ Cosmetic and aesthetic treatments
❌ Experimental and unproven treatments
❌ Genetic disorders (unless covered)
❌ Drug and alcohol abuse related claims
❌ Adventure sports and hazardous activities

### Waiting Periods:
- **Initial Waiting Period:** 30 days (except accidents)
- **Pre-existing Diseases:** 2 years
- **Specific Diseases:** 2 years (heart, cancer, kidney)
- **Maternity:** 3 years

---

## 5. CLAIM PROCESS

### 24x7 Claim Support
**Toll-Free:** 1800-123-4567
**Email:** claims@globalsecureshield.com
**SMS:** Send CLAIM to 567890

### Cashless Network:
- **Network Hospitals:** 15,000+ across India
- **Pre-authorization:** Required for planned treatments
- **Emergency:** Intimate within 24 hours

### Claim Settlement Process:
1. **Intimation:** Within 24 hours of hospitalization
2. **Documentation:** Submit within 30 days of discharge
3. **Investigation:** If required, within 30 days
4. **Settlement:** Within 30 days of final document submission

### Required Documents:
✅ Duly filled claim form
✅ Original bills and receipts
✅ Discharge summary and prescriptions
✅ Diagnostic reports and test results
✅ KYC documents and policy copy
✅ Bank details for settlement

---

## 6. CONTACT INFORMATION

### Global Secure Shield Insurance Company Ltd.

**Registered Office:**
Global Tower, Business District
New Delhi - 110001, India

**Customer Care:**
📞 **24x7 Helpline:** 1800-123-4567
📧 **Email:** support@globalsecureshield.com
🌐 **Website:** www.globalsecureshield.com
📱 **Mobile App:** GSS Insurance (iOS/Android)

### Regional Offices:
- **Mumbai:** 022-4567-8900
- **Bangalore:** 080-4567-8901  
- **Chennai:** 044-4567-8902
- **Kolkata:** 033-4567-8903
- **Hyderabad:** 040-4567-8904

---

## 7. REGULATORY INFORMATION

**IRDAI Registration:** 157
**UIN:** {policy_number.replace('-', '')}HIP01
**Policy Governed by:** Insurance Act 1938, IRDAI Regulations
**Jurisdiction:** Courts in {customer_name.split()[-1] if len(customer_name.split()) > 1 else 'Delhi'} only

**Important:** This policy is subject to terms and conditions. Please read policy documents carefully. For grievances, contact our customer care or IRDAI directly.

**IRDAI Toll-Free:** 155255
**IRDAI Website:** www.irdai.gov.in

---

**Generated on:** {datetime.now().strftime('%d %B %Y at %I:%M %p')}
**Valid Document:** This is a computer-generated document and does not require signature.

---

*Global Secure Shield - "Your Financial Security, Our Commitment"*
"""

        return policy_document
    
    def parse_policy_intent(self, user_input: str) -> Dict[str, Any]:
        """Parse user input to extract policy-related intents and information."""
        intent_data = {
            'policy_type': None,
            'generate_request': False,
            'user_info': {},
            'preferences': {}
        }
        
        user_input_lower = user_input.lower()
        
        # Detect policy types
        if any(word in user_input_lower for word in ['health', 'medical', 'healthcare']):
            intent_data['policy_type'] = 'health'
        elif any(word in user_input_lower for word in ['auto', 'car', 'vehicle', 'motor']):
            intent_data['policy_type'] = 'auto'
        elif any(word in user_input_lower for word in ['life', 'term', 'whole life']):
            intent_data['policy_type'] = 'life'
        elif any(word in user_input_lower for word in ['corporate', 'business', 'commercial']):
            intent_data['policy_type'] = 'corporate'
        
        # Detect generation requests
        if any(phrase in user_input_lower for phrase in ['generate', 'create', 'make', 'produce', 'build']):
            intent_data['generate_request'] = True
        
        # Extract basic user information patterns
        name_match = re.search(r'(?:my name is|i am|i\'m called)\s+([a-zA-Z\s]+)', user_input_lower)
        if name_match:
            intent_data['user_info']['name'] = name_match.group(1).strip().title()
        
        age_match = re.search(r'(?:age|years old|i am)\s+(\d+)', user_input_lower)
        if age_match:
            intent_data['user_info']['age'] = int(age_match.group(1))
        
        return intent_data
    
    def update_user_profile(self, intent_data: Dict[str, Any]):
        """Update user profile based on parsed intent data."""
        if intent_data['user_info']:
            self.user_profile.update(intent_data['user_info'])
        
        if intent_data['policy_type']:
            self.policy_requirements['type'] = intent_data['policy_type']
    
    async def generate_policy_document(self) -> bool:
        """Generate a PDF policy document based on collected requirements."""
        try:
            print("\n📄 Generating your insurance policy document...")
            
            # Initialize MCP client if not already done
            if not self.mcp_client:
                self.mcp_client = MCPPDFClient("src/index.js")
                await self.mcp_client.start_server()
            
            # For now, generate the default health insurance policy
            # This can be extended to handle different policy types
            await generate_insurance_policy_document()
            
            print("✅ Policy document generated successfully!")
            print("📁 Check the PDF folder for your new policy document.")
            return True
            
        except Exception as e:
            print(f"❌ Error generating policy document: {e}")
            return False
    
    async def send_message_to_agent(self, user_input: str) -> str:
        """Send a message to the Azure AI agent with insurance context and get response."""
        try:
            # Check if input is JSON for policy generation
            json_data = self.parse_policy_json(user_input)
            if json_data:
                # Generate AI content for JSON input
                contextual_message = f"""
You are an expert Insurance Policy Assistant for Global Secure Shield Insurance Company. 

Create a comprehensive, professional insurance policy document for this customer data:
{json.dumps(json_data, indent=2)}

Generate a complete policy document with ALL sections including:
1. Policy holder information and coverage details
2. Specific benefits based on policy type ({json_data.get('claimType', 'general')})
3. Premium calculations and payment information
4. Exclusions and waiting periods
5. Claims process and required documents
6. Contact information and regulatory details

IMPORTANT: When customer details are missing from the JSON data, use realistic Indian dummy data:

**For missing addresses, use examples like:**
- "B-204, Green Valley Apartments, Sector 21, Noida, Uttar Pradesh - 201301"
- "301, Sunrise Residency, Koramangala 5th Block, Bangalore, Karnataka - 560095"
- "A-12, Shanti Nagar Society, Andheri West, Mumbai, Maharashtra - 400058"

**For missing contact numbers, use format:**
- "+91-98765-43210" or "+91-99876-54321"

**For missing email addresses, use examples like:**
- "customer.name@gmail.com" or "customer.name@yahoo.co.in"

**For missing names, use common Indian names like:**
- "Rajesh Kumar Sharma", "Priya Patel", "Amit Singh", "Sneha Gupta", "Vikash Jain"

**For missing dates of birth:**
- Use realistic dates like "15-March-1985", "22-July-1990", "08-December-1982"

Make it realistic, detailed, and professionally formatted with authentic Indian context.
"""
                # Send the contextual_message to get AI-generated content
                return await self._send_to_azure_ai(contextual_message)
            
            # For non-JSON input, add general insurance context
            contextual_message = f"""
You are an expert Insurance Policy Assistant for Global Secure Shield Insurance Company. You specialize in creating comprehensive, professional insurance policy documents.

IMPORTANT: When you receive JSON input with customer details, you MUST generate a complete, detailed insurance policy document with ALL sections including:

1. Policy holder information and coverage details
2. Specific benefits based on policy type (health/auto/life)
3. Premium calculations and payment information
4. Exclusions and waiting periods
5. Claims process and required documents
6. Contact information and regulatory details

CRITICAL: When customer details are missing, always use realistic Indian dummy data:

**For missing addresses:**
- "B-204, Green Valley Apartments, Sector 21, Noida, Uttar Pradesh - 201301"
- "301, Sunrise Residency, Koramangala 5th Block, Bangalore, Karnataka - 560095"
- "A-12, Shanti Nagar Society, Andheri West, Mumbai, Maharashtra - 400058"

**For missing contact numbers:**
- "+91-98765-43210", "+91-99876-54321", "+91-97654-32109"

**For missing email addresses:**
- "customer.name@gmail.com", "customer.name@yahoo.co.in", "customer.name@rediffmail.com"

**For missing names:**
- "Rajesh Kumar Sharma", "Priya Patel", "Amit Singh", "Sneha Gupta", "Vikash Jain", "Ravi Krishnan"

**For missing dates:**
- "15-March-1985", "22-July-1990", "08-December-1982"

For JSON input like:
{{
  "customerName": "Customer Name",
  "policyNumber": "GSS-2025-XXXXXX", 
  "claimType": "health/auto/life",
  "claimAmount": amount,
  "policyStartDate": "YYYY-MM-DD"
}}

You must create a professional insurance policy document with realistic details, proper formatting, and comprehensive coverage information specific to the policy type.

For general questions, provide helpful insurance information and guidance.

User input: {user_input}
"""
            
            return await self._send_to_azure_ai(contextual_message)
            
        except Exception as e:
            print(f"❌ Error communicating with agent: {e}")
            return "I'm experiencing technical difficulties. Please try again with your insurance question."
    
    async def _send_to_azure_ai(self, message: str) -> str:
        """Helper method to send message to Azure AI and get response."""
        try:
            # Create message in the thread
            message_obj = self.project_client.agents.create_message(
                thread_id=self.thread.id,
                role="user",
                content=message
            )
            
            # Process the message with the agent
            run = self.project_client.agents.create_and_process_run(
                thread_id=self.thread.id,
                agent_id=self.agent.id
            )
            
            # Get the latest messages
            messages = self.project_client.agents.list_messages(thread_id=self.thread.id)
            
            # Try different methods to extract the response content
            response_content = None
            
            # Method 1: Check text_messages first (most reliable)
            for text_message in messages.text_messages:
                try:
                    # Handle as_dict method first (most common for Azure AI)
                    if hasattr(text_message, 'as_dict'):
                        msg_dict = text_message.as_dict()
                        if isinstance(msg_dict, dict) and 'value' in msg_dict:
                            response_content = str(msg_dict['value'])
                            break
                    
                    # Handle MessageTextDetails object attributes
                    if hasattr(text_message, 'value'):
                        response_content = str(text_message.value)
                        break
                    elif hasattr(text_message, 'content'):
                        if isinstance(text_message.content, str):
                            response_content = text_message.content
                        else:
                            response_content = str(text_message.content)
                        break
                    elif hasattr(text_message, 'text'):
                        response_content = str(text_message.text)
                        break
                    
                    # Last resort - convert to string and try to extract value
                    text_str = str(text_message)
                    if "{'value':" in text_str:
                        # Try to extract the value from string representation
                        import ast
                        try:
                            parsed = ast.literal_eval(text_str)
                            if isinstance(parsed, dict) and 'value' in parsed:
                                response_content = str(parsed['value'])
                                break
                        except:
                            pass
                    
                    # Final fallback
                    response_content = text_str
                    break
                    
                except Exception as e:
                    print(f"Warning: Error processing text message: {e}")
                    continue
            
            # Method 2: Check regular messages if text_messages didn't work
            if not response_content:
                for message in messages:
                    try:
                        if hasattr(message, 'role') and message.role == "assistant":
                            if hasattr(message, 'content'):
                                if isinstance(message.content, str):
                                    response_content = message.content
                                elif hasattr(message.content, 'value'):
                                    response_content = str(message.content.value)
                                elif hasattr(message.content, 'text'):
                                    response_content = str(message.content.text)
                                else:
                                    response_content = str(message.content)
                                break
                    except Exception as e:
                        print(f"Warning: Error processing message: {e}")
                        continue
            
            # Return the response or a default message
            if response_content:
                return response_content
            else:
                return "I'm sorry, I didn't understand that. Could you please rephrase your question about insurance?"
                
        except Exception as e:
            print(f"❌ Error in Azure AI communication: {e}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def enhance_policy_formatting(self, ai_content: str, policy_data: Dict[str, Any]) -> str:
        """Enhance AI-generated policy content with professional formatting and additional details."""
        
        # Extract policy details
        customer_name = policy_data.get('customerName', 'Valued Customer')
        policy_number = policy_data.get('policyNumber', f'GSS-{datetime.now().year}-{datetime.now().strftime("%m%d%H%M")}')
        claim_type = policy_data.get('claimType', 'health').lower()
        claim_amount = policy_data.get('claimAmount', 0)
        policy_start_date = policy_data.get('policyStartDate', datetime.now().strftime('%Y-%m-%d'))
        
        # Create professional header
        header = f"""
# GLOBAL SECURE SHIELD INSURANCE COMPANY
## 🏥 OFFICIAL POLICY CERTIFICATE


**Generation Date:** {datetime.now().strftime('%d %B %Y at %I:%M %p')}
**Policy Reference:** {policy_number}
**Customer:** {customer_name}

---

"""
        
        # Clean and format the AI content
        cleaned_content = self.format_agent_response(ai_content)
        
        # Add professional footer
        footer = f"""

---

## 📋 DOCUMENT AUTHENTICATION

**Generated By:** Azure AI Insurance Expert
**Verification ID:** {policy_number}-AI-{datetime.now().strftime('%Y%m%d%H%M')}
**Authentication:** This document is AI-generated and formatted for professional use
**Company:** Global Secure Shield Insurance Company Ltd.

### 🔐 Security Features:
• AI-powered content generation
• Real-time policy customization
• Automatic compliance checking
• Digital verification system

---

## 📞 IMMEDIATE SUPPORT

**24/7 AI Assistance:** Available through this system
**Emergency Helpline:** 1800-123-SECURE
**Email Support:** support@globalsecureshield.com
**Policy Queries:** policy@globalsecureshield.com

---

**Disclaimer:** This policy document is generated using AI technology for demonstration purposes. 
For actual insurance needs, please consult with licensed insurance professionals.

*Global Secure Shield - "AI-Powered Insurance Solutions"*

**Document ID:** {policy_number}-ENHANCED-{datetime.now().strftime('%Y%m%d')}
"""
        
        # Combine header, AI content, and footer
        enhanced_document = header + cleaned_content + footer
        
        # Apply final formatting touches
        enhanced_document = self.apply_professional_formatting(enhanced_document)
        
        return enhanced_document
    
    async def generate_pdf_document(self, ai_content: str, policy_data: Dict[str, Any]) -> bool:
        """Generate a PDF document using the MCP server with AI content and professional styling."""
        try:
            # Initialize MCP client if not already done
            if not self.mcp_client:
                self.mcp_client = MCPPDFClient("src/index.js")
                await self.mcp_client.start_server()
                print("✅ MCP PDF Server started successfully")
            
            # Extract policy information
            customer_name = policy_data.get('customerName', 'Valued Customer')
            policy_number = policy_data.get('policyNumber', f'GSS-{datetime.now().year}-{datetime.now().strftime("%m%d%H%M")}')
            claim_type = policy_data.get('claimType', 'health').lower()
            
            # Create custom style for this policy type
            print(f"🎨 Creating custom style for {claim_type} insurance policy...")
            
            # Use the professional insurance style from insurance_policy_generator.py
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
            
            h1, h2, h3 {
                color: #1e40af;
                margin-top: 25px;
                margin-bottom: 15px;
            }
            
            h1 {
                font-size: 18pt;
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 10px;
            }
            
            h2 {
                font-size: 14pt;
                background: linear-gradient(90deg, #3b82f6, #60a5fa);
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                margin: 25px 0 15px 0;
            }
            
            h3 {
                font-size: 13pt;
                color: #1e40af;
            }
            
            p {
                margin: 10px 0;
                text-align: justify;
            }
            
            ul, li {
                margin: 5px 0;
            }
            
            strong {
                color: #1f2937;
                font-weight: 600;
            }
            
            hr {
                border: none;
                border-top: 2px solid #e2e8f0;
                margin: 25px 0;
            }
            """
            
            # Create the style with MCP server
            style_name = f"ai_policy_{claim_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            style_result = await self.mcp_client.create_custom_style(
                style_name=style_name,
                description=f"AI-Generated {claim_type.title()} Insurance Policy for {customer_name}",
                prompt=f"Professional {claim_type} insurance policy document with modern styling",
                theme="professional",
                format="A4",
                page_numbers=True,
                custom_css=insurance_style_css,
                header=f'<div style="text-align: center; font-size: 10px; color: #666; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Global Secure Shield - AI-Generated {claim_type.title()} Insurance Policy</div>',
                footer='<div style="text-align: center; font-size: 9px; color: #666;">Page {pageNumber} | AI-Generated Document | IRDAI Reg. No.: 157</div>'
            )
            
            print(f"✅ Custom style created: {style_result['style_name']}")
            
            # Convert AI content to HTML format suitable for PDF generation
            html_content = self.convert_markdown_to_html(ai_content, policy_data)
            
            # Generate the PDF
            print(f"📄 Generating PDF for {customer_name}...")
            
            # Create filename based on customer and policy details
            safe_customer_name = customer_name.replace(' ', '_').replace('.', '').lower()
            pdf_filename = f"ai_policy_{safe_customer_name}_{claim_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            output_path = self.mcp_client.get_pdf_path(pdf_filename)
            
            pdf_result = await self.mcp_client.generate_pdf_with_style(
                style_name=style_name,
                content=html_content,
                output_path=output_path
            )
            
            print(f"✅ PDF generated successfully!")
            print(f"📄 File: {pdf_result['output_path']}")
            print(f"📊 Size: {pdf_result['file_size']:,} bytes")
            print(f"📋 Pages: {pdf_result['page_count']}")
            print(f"⏱️ Time: {pdf_result['generation_time_ms']}ms")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert_markdown_to_html(self, markdown_content: str, policy_data: Dict[str, Any]) -> str:
        """Convert AI-generated markdown content to professional HTML format matching insurance_policy_generator.py styling."""
        
        # Extract policy details
        customer_name = policy_data.get('customerName', 'Valued Customer')
        policy_number = policy_data.get('policyNumber', f'GSS-{datetime.now().year}-{datetime.now().strftime("%m%d%H%M")}')
        claim_type = policy_data.get('claimType', 'health').lower()
        claim_amount = policy_data.get('claimAmount', 0)
        policy_start_date = policy_data.get('policyStartDate', datetime.now().strftime('%Y-%m-%d'))
        
        # Parse AI content to extract sections and structure them professionally
        lines = markdown_content.split('\n')
        
        # Start with professional header matching insurance_policy_generator.py
        html_content = f"""<div class="policy-header">
    <div class="company-logo">🛡️ GLOBAL SECURE SHIELD</div>
    <div class="company-tagline">AI-Powered Insurance Solutions | {claim_type.title()} Insurance Policy</div>
</div>

<div class="policy-title">
    {claim_type.upper()} INSURANCE POLICY CERTIFICATE<br>
    <span style="font-size: 12pt; font-weight: 400;">(AI-Generated Document)</span>
</div>

---

<div class="section-header">📋 POLICY & CUSTOMER DETAILS</div>

<div class="info-grid">
    <div class="info-card">
        <div class="info-label">Policyholder Name</div>
        <div class="info-value">{customer_name}</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy Number</div>
        <div class="info-value">{policy_number}</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy Start Date</div>
        <div class="info-value">{policy_start_date}</div>
    </div>
    <div class="info-card">
        <div class="info-label">Policy End Date</div>
        <div class="info-value">{datetime.now().replace(year=datetime.now().year + 1).strftime('%d %B %Y')} (1-year policy)</div>
    </div>
    <div class="info-card">
        <div class="info-label">Contact Address</div>
        <div class="info-value">B-204, Green Valley Apartments<br>Sector 21, Noida, UP - 201301</div>
    </div>
    <div class="info-card">
        <div class="info-label">Contact Details</div>
        <div class="info-value">📱 +91-98765-43210<br>📧 {customer_name.lower().replace(' ', '.')}@gmail.com</div>
    </div>
</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Insurer Information</h3>
**Company:** Global Secure Shield Insurance Company Limited  
**Licensed Office:** Global Secure Shield Tower, Plot No. 45, Financial District, Bandra Kurla Complex, Mumbai - 400051  
**Customer Service:** 1800-12-SECURE (Toll Free)  
**Website:** www.globalsecureshield.com

---

<div class="section-header">🏥 COMPREHENSIVE COVERAGE INFORMATION</div>

<div class="coverage-highlight">
    <div class="coverage-amount">₹{claim_amount:,}</div>
    <div class="coverage-text">Sum Insured ({claim_type.title()} Coverage)</div>
</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Policy Type</h3>
**Comprehensive {claim_type.title()} Insurance** - AI-Generated Policy Plan
"""

        # Add coverage details based on policy type
        if claim_type == 'health':
            html_content += f"""
<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Coverage Inclusions</h3>

<div class="benefits-grid">
    <div class="benefit-item">
        <div class="benefit-title">🏨 Hospitalization</div>
        <div class="benefit-detail">In-patient treatment for minimum 24 hours</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🏥 Room Rent</div>
        <div class="benefit-detail">Up to ₹8,000 per day (Private AC Room)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🚑 Ambulance Services</div>
        <div class="benefit-detail">Up to ₹5,000 per claim incident</div>
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
        <div class="benefit-detail">60 days before, 90 days after</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">👶 Maternity Cover</div>
        <div class="benefit-detail">Up to ₹75,000 (after waiting period)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🩺 Annual Health Check-up</div>
        <div class="benefit-detail">Up to ₹3,000 per policy year</div>
    </div>
</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Waiting Periods</h3>

| Condition Type | Waiting Period | Coverage Details |
|----------------|----------------|------------------|
| **General Illnesses** | 30 days | All acute conditions after policy inception |
| **Pre-existing Diseases** | 2 years | Conditions existing before policy start |
| **Maternity & Newborn** | 3 years | Pregnancy, delivery, and infant care |
| **Specific Diseases** | 2 years | Heart disease, cancer, kidney ailments |
"""
        elif claim_type == 'auto':
            html_content += f"""
<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Coverage Inclusions</h3>

<div class="benefits-grid">
    <div class="benefit-item">
        <div class="benefit-title">🚗 Own Damage</div>
        <div class="benefit-detail">Complete vehicle damage coverage</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🛡️ Third Party Liability</div>
        <div class="benefit-detail">₹15,00,000 as per Motor Tariff</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🔧 Engine Protection</div>
        <div class="benefit-detail">Water ingress damage coverage</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🆘 Roadside Assistance</div>
        <div class="benefit-detail">24x7 emergency services</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🔑 Key Replacement</div>
        <div class="benefit-detail">Lost key reimbursement</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🛞 Tyre Protection</div>
        <div class="benefit-detail">Damage to tyres and tubes</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">💰 Return to Invoice</div>
        <div class="benefit-detail">Gap between IDV and invoice value</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🎯 Zero Depreciation</div>
        <div class="benefit-detail">Brand new spare parts replacement</div>
    </div>
</div>
"""
        elif claim_type == 'life':
            html_content += f"""
### Coverage Inclusions

<div class="benefits-grid">
    <div class="benefit-item">
        <div class="benefit-title">💖 Death Benefit</div>
        <div class="benefit-detail">100% sum assured to nominee</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🏥 Terminal Illness</div>
        <div class="benefit-detail">50% of sum assured</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🚑 Accidental Death</div>
        <div class="benefit-detail">Additional ₹{claim_amount:,}</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">💰 Maturity Benefit</div>
        <div class="benefit-detail">105% of premiums paid (if survived)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🏦 Loan Facility</div>
        <div class="benefit-detail">After 3 years (up to 90% surrender value)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">📋 Premium Waiver</div>
        <div class="benefit-detail">On permanent disability</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">💳 Tax Benefits</div>
        <div class="benefit-detail">Under Section 80C and 10(10D)</div>
    </div>
    <div class="benefit-item">
        <div class="benefit-title">🕐 Grace Period</div>
        <div class="benefit-detail">30 days for premium payment</div>
    </div>
</div>
"""

        # Add premium section
        html_content += f"""
---

## 3. Premium Details

<div class="section-header">💰 PREMIUM & PAYMENT INFORMATION</div>

<div class="premium-details">
    <div class="premium-amount">₹{max(25000, claim_amount // 15):,}</div>
    <div style="text-align: center; opacity: 0.9;">Total Annual Premium (Including 18% GST)</div>
</div>

### Payment Information
- **Base Premium:** ₹{max(21000, claim_amount // 18):,}
- **GST (18%):** ₹{max(4000, claim_amount // 100):,}
- **Total Premium:** ₹{max(25000, claim_amount // 15):,}
- **Payment Frequency:** Annual
- **Payment Mode:** Online Bank Transfer (NEFT/RTGS)
- **Payment Date:** {datetime.now().strftime('%d %B %Y')}
- **Transaction ID:** GSS{datetime.now().strftime('%y%m%d')}AI{policy_number[-6:]}
- **Next Renewal Due:** {datetime.now().replace(year=datetime.now().year + 1).strftime('%d %B %Y')}

### Premium Breakdown by Coverage

| Coverage Component | Premium Amount | Percentage |
|-------------------|----------------|------------|
| Base {claim_type.title()} Cover | ₹{max(18000, claim_amount // 20):,} | 72.0% |
| Additional Benefits | ₹{max(3000, claim_amount // 100):,} | 12.0% |
| Administrative Fees | ₹{max(1000, claim_amount // 300):,} | 4.0% |
| Service Tax & GST | ₹{max(4000, claim_amount // 100):,} | 16.0% |
| **Total** | **₹{max(25000, claim_amount // 15):,}** | **100%** |

---

<div class="section-header">📋 CLAIM INFORMATION & PROCESS</div>

<div class="claim-process">
<h3 style="color: #22c55e; margin-top: 0;">📋 How to File a Claim</h3>
    
<div class="claim-steps">
<div class="claim-step"><strong>Inform Immediately:</strong> Call our 24x7 helpline within 24 hours of incident</div>
<div class="claim-step"><strong>Pre-authorization:</strong> For cashless treatment, get pre-approval from network providers</div>
<div class="claim-step"><strong>Submit Documents:</strong> Provide all required documents within 15 days</div>
<div class="claim-step"><strong>Claim Processing:</strong> Our team will process your claim within 30 working days</div>
<div class="claim-step"><strong>Settlement:</strong> Approved amount will be settled directly or reimbursed</div>
</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Required Documents for Claims</h3>

<h4 style="color: #1e40af; margin: 15px 0 10px 0;">For {claim_type.title()} Claims:</h4>
- ✅ Duly filled and signed claim form
- ✅ Original bills and payment receipts
- ✅ Medical reports and discharge summary (if applicable)
- ✅ Diagnostic reports and test results (if applicable)
- ✅ Photo ID proof and policy document
- ✅ Bank account details for reimbursement

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Claim Submission Channels</h3>

| Method | Details | Processing Time |
|--------|---------|----------------|
| **Online Portal** | www.globalsecureshield.com/claims | 24-48 hours |
| **Mobile App** | GSS Claims App (Android/iOS) | 24-48 hours |
| **Email** | claims@globalsecureshield.com | 48-72 hours |
| **Toll-Free** | 1800-12-SECURE | Immediate assistance |
| **Branch Visit** | Any GSS branch office | Same day |

---

<div class="section-header">🚫 POLICY EXCLUSIONS</div>

<div class="exclusions-box">
    <h3 style="color: #dc2626; margin-top: 0; margin-bottom: 15px; font-size: 13pt;">⚠️ What's NOT Covered</h3>
    
<h4 style="color: #dc2626; margin: 15px 0 10px 0;">General Exclusions:</h4>
- Self-inflicted injuries and attempted suicide
- War, nuclear risks, and acts of terrorism
- Experimental or unproven treatments
- Pre-existing conditions (first 2 years)
- Fraudulent claims and misrepresentation

<h4 style="color: #dc2626; margin: 15px 0 10px 0;">Treatment Exclusions:</h4>
- Cosmetic and plastic surgery (unless medically necessary)
- Routine check-ups and preventive care (except covered benefits)
- Treatment outside India (except emergency)
- Alternative medicine (unless specified)
- Mental illness and psychiatric disorders (unless covered)

</div>

---

<div class="section-header">📋 IMPORTANT TERMS & CONDITIONS</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">General Terms</h3>

1. **Grace Period:** 30 days from due date for premium payment
2. **Free Look Period:** 15 days from policy receipt to review and return
3. **Renewal:** Lifetime renewability guaranteed (subject to terms)
4. **Age Limits:** Entry age 18-65 years, renewable up to 80 years
5. **Network:** 12,000+ authorized service providers across India

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Policy Conditions</h3>

<h4 style="color: #1e40af; margin: 15px 0 10px 0;">Medical Examination (for Health Insurance)</h4>
- Not required for sum insured up to ₹5 lakhs for age below 45 years
- Pre-medical screening required for higher sum insured or older age

<h4 style="color: #1e40af; margin: 15px 0 10px 0;">Pre-existing Conditions</h4>
- Must be declared at the time of proposal
- Covered after completion of waiting period
- Medical records may be verified before claim settlement

---

<div class="section-header">📞 REGULATORY COMPLIANCE & CONTACT DETAILS</div>

<div class="contact-info">
    <h3 style="color: white; margin-top: 0; margin-bottom: 15px; font-size: 13pt;">🏛️ Regulatory Information</h3>
    <strong>IRDAI Registration No.:</strong> 157<br>
    <strong>Valid until:</strong> 31 March 2026<br>
    <strong>Category:</strong> General Insurance Company<br>
    <strong>License Date:</strong> 15 April 2001<br>
    <strong>Complaint Reference:</strong> IRDAI Complaint Portal - www.irdai.gov.in
</div>

<div class="contact-info">
    <h3 style="color: white; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">📞 Customer Care & Support</h3>
    <strong>24x7 Helpline:</strong> 1800-12-SECURE<br>
    <strong>Email:</strong> support@globalsecureshield.com<br>
    <strong>Website:</strong> www.globalsecureshield.com<br>
    <strong>Mobile App:</strong> GSS Insurance (iOS/Android)<br>
    <strong>WhatsApp:</strong> +91-98765-SECURE
</div>

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Branch Offices</h3>

| City | Address | Contact |
|------|---------|---------|
| **New Delhi** | Connaught Place, CP Metro Station | +91-11-2341-5678 |
| **Mumbai** | Nariman Point, Near RBI Building | +91-22-6789-0123 |
| **Bangalore** | MG Road, Brigade Center | +91-80-4567-8901 |
| **Chennai** | Anna Salai, Express Towers | +91-44-2890-1234 |
| **Kolkata** | Park Street, AJC Bose Road | +91-33-5678-9012 |

---

<div class="signature-section">

<h3 style="color: #1e40af; margin-top: 25px; margin-bottom: 15px; font-size: 13pt;">Digital Signatures & Validation</h3>

<table style="border: none;">
<tr style="border: none;">
<td style="border: none; width: 50%; text-align: center; padding: 20px;">
<strong>AI Policy Generated By:</strong><br><br>
<strong>Azure AI Insurance Expert</strong><br>
AI-Powered Policy Generation<br>
Global Secure Shield Insurance<br>
System ID: AI-GSS-2025<br>
<em>Digital Signature Applied</em><br>
<em>Date: {datetime.now().strftime('%d %B %Y')}</em>
</td>
<td style="border: none; width: 50%; text-align: center; padding: 20px;">
<strong>Processed & Validated By:</strong><br><br>
<strong>Automated Underwriting System</strong><br>
Risk Assessment & Policy Validation<br>
Global Secure Shield Insurance<br>
System ID: AUTO-UW-2025<br>
<em>Automated Validation Applied</em><br>
<em>Date: {datetime.now().strftime('%d %B %Y')}</em>
</td>
</tr>
</table>

</div>

<div class="important-notice">
    <strong>🔒 Important Security Information</strong><br>
    This policy certificate is generated using advanced AI technology and is valid for demonstration purposes. 
    Policy authenticity can be verified online at www.globalsecureshield.com using policy number {policy_number}.
    For actual insurance coverage, please consult with licensed insurance professionals.
</div>

<div class="footer-disclaimer">
    <strong>AI-Generated Document Notice:</strong> This policy document has been created using advanced artificial intelligence technology 
    and professional insurance industry standards. The content is generated based on the provided customer data and comprehensive 
    insurance knowledge base. While this demonstrates the capabilities of AI in insurance document generation, 
    for actual insurance coverage and legal validity, please consult with licensed insurance professionals and authorized insurance companies.<br><br>
    <strong>Disclaimer:</strong> This policy is subject to terms, conditions, and exclusions mentioned in the policy wordings. 
    For complete terms and conditions, please refer to the policy document. In case of any dispute, 
    the English version of the policy shall prevail. This policy is regulated by the Insurance Regulatory 
    and Development Authority of India (IRDAI).<br><br>
    <strong>Document Generation Info:</strong><br>
    • Generated on: {datetime.now().strftime('%d %B %Y at %I:%M %p')}<br>
    • Customer: {customer_name}<br>
    • Policy Type: {claim_type.title()} Insurance<br>
    • Document ID: AI-{policy_number}-{datetime.now().strftime('%Y%m%d%H%M')}<br>
    • AI System: Azure OpenAI + Global Secure Shield Platform
</div>"""
        
        return html_content
    
    def apply_professional_formatting(self, content: str) -> str:
        """Apply professional formatting to the policy document."""
        
        # Ensure proper spacing around sections
        content = re.sub(r'\n#{1,3}\s*([^\n]+)', r'\n\n## 📋 \1\n', content)
        
        # Format important notices
        content = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', content)
        
        # Add emoji indicators for different sections
        content = content.replace('COVERAGE', '🛡️ COVERAGE')
        content = content.replace('PREMIUM', '💰 PREMIUM')
        content = content.replace('CLAIMS', '📄 CLAIMS')
        content = content.replace('CONTACT', '📞 CONTACT')
        content = content.replace('BENEFITS', '✅ BENEFITS')
        content = content.replace('EXCLUSIONS', '❌ EXCLUSIONS')
        
        # Clean up excessive newlines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        return content.strip()
    
    def format_agent_response(self, response: str) -> str:
        """Format the agent response for better readability."""
        if not response:
            return "I'm sorry, I couldn't process that response."
        
        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)
        
        # Clean up any dictionary artifacts that might remain
        if response.startswith("{'value'"):
            try:
                import ast
                parsed = ast.literal_eval(response)
                if isinstance(parsed, dict) and 'value' in parsed:
                    response = parsed['value']
            except:
                pass
        
        # Clean up the response
        formatted = response.strip()
        
        # Remove any double formatting that might have occurred
        formatted = formatted.replace('💰 💰', '�')
        formatted = formatted.replace('🛡️ 🛡️', '�️')
        formatted = formatted.replace('💳 💳', '💳')
        
        # Clean up extra newlines and spaces
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        formatted = re.sub(r' {2,}', ' ', formatted)
        
        return formatted.strip()
    
    async def handle_user_input(self, user_input: str):
        """Process user input and generate appropriate responses."""
        # Check for JSON policy generation first
        policy_data = self.parse_policy_json(user_input)
        
        if policy_data:
            print("\n🎯 JSON Policy Data Detected!")
            print(f"📋 Customer: {policy_data.get('customerName', 'Unknown')}")
            print(f"📄 Policy Type: {policy_data.get('claimType', 'Unknown').title()}")
            print(f"💰 Amount: ₹{policy_data.get('claimAmount', 0):,}")
            
            print("\n📝 Generating comprehensive policy document using AI agent...")
            
            # Send JSON to Azure AI agent for intelligent content generation
            raw_policy_content = await self.send_message_to_agent(user_input)
            
            # Format the AI-generated content with local formatting enhancements
            formatted_policy = self.enhance_policy_formatting(raw_policy_content, policy_data)
            
            print("\n🎉 AI-Generated Policy Document Created Successfully!")
            print("\n" + "="*80)
            print(formatted_policy)
            print("="*80)
            
            # Generate PDF using MCP server
            print("\n📄 Converting to professional PDF document...")
            pdf_success = await self.generate_pdf_document(formatted_policy, policy_data)
            
            if pdf_success:
                print("✅ PDF document generated successfully!")
                print("📁 Check the PDF folder for your new policy document.")
            else:
                print("⚠️ Document generated but PDF creation encountered issues.")
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'user',
                'content': user_input,
                'policy_data': policy_data
            })
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'assistant',
                'content': f"Generated AI-powered {policy_data.get('claimType', 'insurance')} policy document with PDF for {policy_data.get('customerName', 'customer')}"
            })
            
            return
        
        # Check if user input looks like attempted JSON but failed to parse
        if '{' in user_input and '}' in user_input and policy_data is None:
            print("\n❌ It looks like you tried to send JSON data, but there was a formatting issue.")
            print("💡 Here's the correct format (note: no trailing commas):")
            print("""
{
  "customerName": "Your Name Here",
  "policyNumber": "GSS-2025-123456",
  "claimType": "health",
  "claimAmount": 185000,
  "policyStartDate": "2023-05-15"
}""")
            print("\n🔧 Common issues to avoid:")
            print("• No trailing commas after the last property")
            print("• Use double quotes around strings")  
            print("• Numbers don't need quotes")
            print("• Dates should be in YYYY-MM-DD format")
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'user',
                'content': user_input,
                'error': 'JSON parsing failed'
            })
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'assistant',
                'content': "Provided JSON formatting help due to parsing error"
            })
            
            return
        
        # Parse the input for policy-related intents
        intent_data = self.parse_policy_intent(user_input)
        
        # Update user profile
        self.update_user_profile(intent_data)
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'role': 'user',
            'content': user_input,
            'intent': intent_data
        })
        
        # Handle generation request
        if intent_data['generate_request'] and intent_data['policy_type']:
            print(f"\n🎯 I understand you want to generate a {intent_data['policy_type']} insurance policy.")
            
            if self.user_profile:
                print(f"👤 Based on your profile: {self.user_profile}")
            
            confirm = input("\n📋 Should I proceed with generating the policy document? (yes/no): ")
            if confirm.lower() in ['yes', 'y', 'yeah', 'sure']:
                success = await self.generate_policy_document()
                if success:
                    print("\n🎉 Your insurance policy has been generated successfully!")
                    response = "Generated policy document successfully!"
                else:
                    print("\n😞 Sorry, there was an issue generating your policy. Please try again.")
                    response = "Failed to generate policy document."
            else:
                print("👍 No problem! Let me know if you need any changes or have other questions.")
                response = "Policy generation cancelled by user."
        else:
            # Send to Azure AI agent for all insurance-related questions
            raw_response = await self.send_message_to_agent(user_input)
            response = self.format_agent_response(raw_response)
            print(f"\n🤖 Agent:\n{response}")
        
        # Add agent response to history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'role': 'assistant',
            'content': response
        })
    
    async def run_conversation_loop(self):
        """Main conversation loop."""
        print("\n" + "="*60)
        print("💬 Starting Conversational Mode")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("="*60)
        
        while self.conversation_active:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\n👋 Goodbye! Thank you for using the Insurance Policy Assistant!")
                    break
                
                if not user_input:
                    print("💭 Please enter a message or type 'quit' to exit.")
                    continue
                
                # Process the input
                await self.handle_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                continue
    
    async def cleanup(self):
        """Clean up resources."""
        if self.mcp_client:
            await self.mcp_client.cleanup()
    
    def print_conversation_summary(self):
        """Print a summary of the conversation."""
        if not self.conversation_history:
            return
        
        print("\n" + "="*60)
        print("📊 CONVERSATION SUMMARY")
        print("="*60)
        print(f"💬 Total messages: {len(self.conversation_history)}")
        
        if self.user_profile:
            print(f"👤 User profile: {self.user_profile}")
        
        if self.policy_requirements:
            print(f"📋 Policy requirements: {self.policy_requirements}")
        
        print("="*60)

async def main():
    """Main function to run the conversational policy agent."""
    agent = ConversationalPolicyAgent()
    
    try:
        # Start the conversation
        success = await agent.start_conversation()
        if not success:
            print("❌ Failed to start conversation. Exiting.")
            return
        
        # Run the conversation loop
        await agent.run_conversation_loop()
        
        # Print summary
        agent.print_conversation_summary()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        # Cleanup
        await agent.cleanup()

if __name__ == "__main__":
    print("🚀 Starting Insurance Policy Conversational Agent...")
    asyncio.run(main())