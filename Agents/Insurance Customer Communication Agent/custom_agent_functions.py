"""
Custom Agent Functions Module for Insurance Customer Communication

This module contains functions that can be called by an AI agent to perform
specific operations related to insurance customer communication by integrating 
with Azure Logic Apps. Each function represents a capability that can be exposed 
as a tool to the agent.
"""

import os
import requests
import json
import time
from typing import Dict, Any, Optional, List


def send_insurance_policy_number(customer_id: str) -> Dict[str, Any]:
    """
    Sends policy number generation email to insurance customers via Logic App.
    This function is used by the Insurance Customer Communication Agent to notify customers
    about their policy number generation.

    :param customer_id (str): The unique ID of the insurance customer
    :return: A dictionary containing the status and message about the email send operation
    :rtype: Dict[str, Any]
    """
    # Logic App endpoint for insurance customer communication
    api_url = "https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=SnPAbyaqajdIX8V-V4MHttI0DFq0yF5wrk_dWzXE1VI"
    
    print(f"Sending policy number generation email for customer {customer_id}...")

    try:
        # Email template for policy number generation
        subject = f"Your Insurance Policy Number Has Been Generated"
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Policy Number Generated</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #2c3e50;
            margin-bottom: 25px;
        }}
        .policy-info {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #667eea;
        }}
        .policy-number {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            background-color: white;
            padding: 15px;
            border-radius: 6px;
            border: 2px solid #667eea;
            letter-spacing: 1px;
        }}
        .benefits {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .benefits h3 {{
            color: #495057;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .benefit-item {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            color: #6c757d;
        }}
        .benefit-item::before {{
            content: "✓";
            color: #28a745;
            font-weight: bold;
            margin-right: 10px;
            font-size: 16px;
        }}
        .contact-info {{
            background-color: #e8f4fd;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
        }}
        .contact-info h3 {{
            color: #0066cc;
            margin-bottom: 10px;
        }}
        .footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 25px;
            font-size: 14px;
        }}
        .footer .company-name {{
            font-weight: bold;
            color: #667eea;
        }}
        @media (max-width: 600px) {{
            .container {{
                margin: 10px;
                border-radius: 5px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .policy-number {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">🛡️</div>
            <h1>Policy Successfully Generated!</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Dear Valued Customer,
            </div>
            
            <p>We are pleased to inform you that your insurance policy number has been successfully generated and your coverage is now active!</p>
            
            <div class="policy-info">
                <h3 style="text-align: center; margin-bottom: 15px; color: #495057;">Your Policy Number</h3>
                <div class="policy-number">
                    GSS-12-8372-9721-1245-55
                </div>
            </div>
            
            <div class="benefits">
                <h3>🎉 Your Coverage is Now Active!</h3>
                <div class="benefit-item">Comprehensive insurance protection</div>
                <div class="benefit-item">24/7 customer support available</div>
                <div class="benefit-item">Easy claims process</div>
                <div class="benefit-item">Digital policy management</div>
            </div>
            
            <p>You can now start enjoying the full benefits of your insurance coverage. Keep your policy number safe as you'll need it for any future communications or claims.</p>
            
            <div class="contact-info">
                <h3>Need Assistance? 📞</h3>
                <p>Our customer service team is ready to help with any questions about your policy or coverage.</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>
            <span class="company-name">Global Secure Shield</span><br>
            Your trusted insurance partner</p>
        </div>
    </div>
</body>
</html>"""
        
        # Make the HTTP POST API call with subject and body
        response = requests.post(
            api_url,
            json={
                "subject": subject,
                "body": body
            },
            headers={"Content-Type": "application/json"},
        )
        
        # Return a standard response
        result = {
            "status": "submitted",
            "customer_id": customer_id,
            "stage": "policy_number_generation",
            "message": "Thank you for using our insurance services. You will be notified via mail about your policy number."
        }
        
        print(f"Policy number generation email sent successfully for customer {customer_id}")
        return result
        
    except Exception as e:
        print(f"Error sending policy number generation email: {str(e)}")
        return {
            "status": "error",
            "customer_id": customer_id,
            "message": "There was an issue sending the policy number generation email. Please try again later or contact customer support."
        }


def send_insurance_claim_in_progress(customer_id: str) -> Dict[str, Any]:
    """
    Sends claim process in progress email to insurance customers via Logic App.
    This function is used by the Insurance Customer Communication Agent to notify customers
    that their claim is being processed.

    :param customer_id (str): The unique ID of the insurance customer
    :return: A dictionary containing the status and message about the email send operation
    :rtype: Dict[str, Any]
    """
    # Logic App endpoint for insurance customer communication
    api_url = "https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=SnPAbyaqajdIX8V-V4MHttI0DFq0yF5wrk_dWzXE1VI"
    
    print(f"Sending claim in progress email for customer {customer_id}...")

    try:
        # Email template for claim in progress
        subject = f"Your Insurance Claim is Being Processed"
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claim Processing Update</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #2c3e50;
            margin-bottom: 25px;
        }}
        .claim-info {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #3498db;
        }}
        .claim-id {{
            font-size: 20px;
            font-weight: bold;
            color: #2980b9;
            text-align: center;
            background-color: white;
            padding: 12px;
            border-radius: 6px;
            border: 2px solid #3498db;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }}
        .status-badge {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            display: inline-block;
            margin: 10px 0;
        }}
        .timeline {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .timeline h3 {{
            color: #495057;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .timeline-item {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            color: #6c757d;
        }}
        .timeline-item.active {{
            color: #3498db;
            font-weight: bold;
        }}
        .timeline-item::before {{
            content: "●";
            margin-right: 12px;
            font-size: 14px;
        }}
        .timeline-item.active::before {{
            color: #3498db;
        }}
        .contact-info {{
            background-color: #e8f4fd;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
        }}
        .contact-info h3 {{
            color: #0066cc;
            margin-bottom: 10px;
        }}
        .footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 25px;
            font-size: 14px;
        }}
        .footer .company-name {{
            font-weight: bold;
            color: #3498db;
        }}
        @media (max-width: 600px) {{
            .container {{
                margin: 10px;
                border-radius: 5px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .claim-id {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">🔄</div>
            <h1>Claim Processing Update</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Dear Valued Customer,
            </div>
            
            <p>We want to provide you with an update on your insurance claim status.</p>
            
            <div class="claim-info">
                <div class="claim-id">
                    Claim ID: 107834789210
                </div>
                <div style="text-align: center;">
                    <span class="status-badge">🔄 IN PROGRESS</span>
                </div>
            </div>
            
            <div class="timeline">
                <h3>📋 Claim Processing Timeline</h3>
                <div class="timeline-item">Claim submitted</div>
                <div class="timeline-item">Initial review completed</div>
                <div class="timeline-item active">Processing in progress</div>
                <div class="timeline-item">Final review</div>
                <div class="timeline-item">Decision notification</div>
            </div>
            
            <p>Your claim is currently being reviewed by our experienced claims processing team. We are working diligently to process your claim as quickly as possible while ensuring all necessary documentation and requirements are thoroughly evaluated.</p>
            
            <p>We will keep you updated on any developments throughout the process. Rest assured that we are committed to providing you with timely and fair claim resolution.</p>
            
            <div class="contact-info">
                <h3>Need to Submit Additional Documents? 📄</h3>
                <p>If you need to provide additional information or have questions about your claim, please contact our claims department immediately.</p>
            </div>
            
            <p style="margin-top: 25px;"><strong>Thank you for your patience and for choosing our insurance services.</strong></p>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>
            <span class="company-name">Insurance Claims Department</span><br>
            Global Secure Shield</p>
        </div>
    </div>
</body>
</html>"""
        
        # Make the HTTP POST API call with subject and body
        response = requests.post(
            api_url,
            json={
                "subject": subject,
                "body": body
            },
            headers={"Content-Type": "application/json"},
        )
        
        # Return a standard response
        result = {
            "status": "submitted",
            "customer_id": customer_id,
            "stage": "claim_in_progress",
            "message": "Thank you for using our insurance services. You will be notified via mail about your claim status."
        }
        
        print(f"Claim in progress email sent successfully for customer {customer_id}")
        return result
        
    except Exception as e:
        print(f"Error sending claim in progress email: {str(e)}")
        return {
            "status": "error",
            "customer_id": customer_id,
            "message": "There was an issue sending the claim status email. Please try again later or contact customer support."
        }


def send_insurance_claim_approved(customer_id: str) -> Dict[str, Any]:
    """
    Sends insurance claim approved email to customers via Logic App.
    This function is used by the Insurance Customer Communication Agent to notify customers
    that their claim has been approved.

    :param customer_id (str): The unique ID of the insurance customer
    :return: A dictionary containing the status and message about the email send operation
    :rtype: Dict[str, Any]
    """
    # Logic App endpoint for insurance customer communication
    api_url = "https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=SnPAbyaqajdIX8V-V4MHttI0DFq0yF5wrk_dWzXE1VI"
    
    print(f"Sending claim approved email for customer {customer_id}...")

    try:
        # Email template for claim approved
        subject = f"🎉 Great News! Your Insurance Claim Has Been Approved"
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claim Approved</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #2c3e50;
            margin-bottom: 25px;
        }}
        .approval-banner {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid #27ae60;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            margin: 25px 0;
        }}
        .approval-banner h2 {{
            color: #155724;
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        .claim-details {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #27ae60;
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        .detail-label {{
            font-weight: bold;
            color: #495057;
        }}
        .detail-value {{
            color: #6c757d;
        }}
        .amount {{
            font-size: 28px;
            font-weight: bold;
            color: #27ae60;
            text-align: center;
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #27ae60;
            margin: 15px 0;
        }}
        .settlement-info {{
            background: linear-gradient(135deg, #e8f5e8 0%, #d1ecf1 100%);
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .settlement-info h3 {{
            color: #0c5460;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .info-item {{
            margin-bottom: 10px;
            color: #495057;
        }}
        .info-item strong {{
            color: #2c3e50;
        }}
        .next-steps {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .next-steps h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        .step {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            color: #856404;
        }}
        .step-number {{
            background-color: #ffc107;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 12px;
            flex-shrink: 0;
            font-size: 12px;
        }}
        .contact-info {{
            background-color: #e8f4fd;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
        }}
        .contact-info h3 {{
            color: #0066cc;
            margin-bottom: 10px;
        }}
        .footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 25px;
            font-size: 14px;
        }}
        .footer .company-name {{
            font-weight: bold;
            color: #27ae60;
        }}
        @media (max-width: 600px) {{
            .container {{
                margin: 10px;
                border-radius: 5px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .amount {{
                font-size: 24px;
            }}
            .detail-row {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">🎉</div>
            <h1>Claim Approved!</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Dear Valued Customer,
            </div>
            
            <div class="approval-banner">
                <h2>✅ Congratulations!</h2>
                <p style="margin: 0; font-size: 16px; color: #155724;">Your insurance claim has been successfully approved and processed.</p>
            </div>
            
            <div class="claim-details">
                <div class="detail-row">
                    <span class="detail-label">Claim ID:</span>
                    <span class="detail-value">CLM-{customer_id}-{hash(customer_id) % 10000:04d}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span class="detail-value" style="color: #27ae60; font-weight: bold;">APPROVED ✅</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Processing Date:</span>
                    <span class="detail-value">{time.strftime('%B %d, %Y')}</span>
                </div>
            </div>
            
            <div style="text-align: center; margin: 25px 0;">
                <h3 style="color: #495057; margin-bottom: 10px;">💰 Approved Settlement Amount</h3>
                <div class="amount">₹3,50,000</div>
            </div>
            
            <div class="settlement-info">
                <h3>💳 Settlement Details</h3>
                <div class="info-item"><strong>Payment Method:</strong> Direct Bank Transfer</div>
                <div class="info-item"><strong>Expected Transfer:</strong> 3-5 Business Days</div>
                <div class="info-item"><strong>Reference Number:</strong> REF-{customer_id}-{hash(customer_id) % 10000:04d}</div>
            </div>
            
            <div class="next-steps">
                <h3>📝 What Happens Next?</h3>
                <div class="step">
                    <div class="step-number">1</div>
                    <div>Settlement amount will be transferred to your registered bank account</div>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div>You'll receive a confirmation SMS/email once the transfer is completed</div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div>Your claim case will be marked as closed in our system</div>
                </div>
            </div>
            
            <p style="margin-top: 25px;">We appreciate your patience throughout the claims process. Our team has carefully reviewed your claim and determined it meets all policy requirements for full approval.</p>
            
            <div class="contact-info">
                <h3>Questions About Your Settlement? 📞</h3>
                <p>If you have any questions about your settlement or need assistance with future claims, our customer service team is here to help.</p>
            </div>
            
            <p style="margin-top: 25px; text-align: center;"><strong>Thank you for choosing our insurance services. We're here when you need us!</strong></p>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>
            <span class="company-name">Insurance Claims Department</span><br>
            Global Secure Shield</p>
        </div>
    </div>
</body>
</html>"""
        
        # Make the HTTP POST API call with subject and body
        response = requests.post(
            api_url,
            json={
                "subject": subject,
                "body": body
            },
            headers={"Content-Type": "application/json"},
        )
        
        # Return a standard response
        result = {
            "status": "submitted",
            "customer_id": customer_id,
            "stage": "claim_approved",
            "message": "Thank you for using our insurance services. You will be notified via mail about your claim approval."
        }
        
        print(f"Claim approved email sent successfully for customer {customer_id}")
        return result
        
    except Exception as e:
        print(f"Error sending claim approved email: {str(e)}")
        return {
            "status": "error",
            "customer_id": customer_id,
            "message": "There was an issue sending the claim approval email. Please try again later or contact customer support."
        }


def send_insurance_claim_rejected(customer_id: str) -> Dict[str, Any]:
    """
    Sends insurance claim rejected email to customers via Logic App.
    This function is used by the Insurance Customer Communication Agent to notify customers
    that their claim has been rejected.

    :param customer_id (str): The unique ID of the insurance customer
    :return: A dictionary containing the status and message about the email send operation
    :rtype: Dict[str, Any]
    """
    # Logic App endpoint for insurance customer communication
    api_url = "https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=SnPAbyaqajdIX8V-V4MHttI0DFq0yF5wrk_dWzXE1VI"
    
    print(f"Sending claim rejected email for customer {customer_id}...")

    try:
        # Email template for claim rejected
        subject = f"Important Update Regarding Your Insurance Claim"
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claim Decision Update</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #2c3e50;
            margin-bottom: 25px;
        }}
        .decision-banner {{
            background: linear-gradient(135deg, #fadbd8 0%, #f1948a 100%);
            border: 2px solid #e74c3c;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            margin: 25px 0;
        }}
        .decision-banner h2 {{
            color: #a93226;
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        .claim-details {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #e74c3c;
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        .detail-label {{
            font-weight: bold;
            color: #495057;
        }}
        .detail-value {{
            color: #6c757d;
        }}
        .reason-section {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .reason-section h3 {{
            color: #856404;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .reason-item {{
            margin-bottom: 10px;
            color: #856404;
            padding-left: 20px;
            position: relative;
        }}
        .reason-item::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #856404;
            font-weight: bold;
        }}
        .appeal-info {{
            background-color: #e8f4fd;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .appeal-info h3 {{
            color: #0066cc;
            margin-bottom: 15px;
        }}
        .appeal-item {{
            margin-bottom: 10px;
            color: #495057;
        }}
        .appeal-item strong {{
            color: #2c3e50;
        }}
        .contact-info {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
        }}
        .contact-info h3 {{
            color: #495057;
            margin-bottom: 10px;
        }}
        .footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 25px;
            font-size: 14px;
        }}
        .footer .company-name {{
            font-weight: bold;
            color: #e74c3c;
        }}
        @media (max-width: 600px) {{
            .container {{
                margin: 10px;
                border-radius: 5px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .detail-row {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">📋</div>
            <h1>Claim Decision Update</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Dear Valued Customer,
            </div>
            
            <p>We have completed the review of your insurance claim and want to provide you with an update on the decision.</p>
            
            <div class="decision-banner">
                <h2>⚠️ Claim Decision</h2>
                <p style="margin: 0; font-size: 16px; color: #a93226;">After careful review, we regret to inform you that your claim has been declined.</p>
            </div>
            
            <div class="claim-details">
                <div class="detail-row">
                    <span class="detail-label">Claim ID:</span>
                    <span class="detail-value">CLM-{customer_id}-{hash(customer_id) % 10000:04d}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span class="detail-value" style="color: #e74c3c; font-weight: bold;">DECLINED ❌</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Review Date:</span>
                    <span class="detail-value">{time.strftime('%B %d, %Y')}</span>
                </div>
            </div>
            
            <div class="reason-section">
                <h3>📝 Reason for Decline</h3>
                <div class="reason-item">The submitted claim does not meet the policy coverage requirements</div>
                <div class="reason-item">Insufficient documentation provided to support the claim</div>
                <div class="reason-item">The incident falls outside the coverage period or scope</div>
            </div>
            
            <p>We understand this decision may be disappointing. Our claims review team has carefully evaluated all submitted documentation and policy terms before reaching this conclusion.</p>
            
            <div class="appeal-info">
                <h3>⚖️ Have Questions or Want to Appeal?</h3>
                <div class="appeal-item"><strong>Appeal Deadline:</strong> You have 30 days from this notice to file an appeal</div>
                <div class="appeal-item"><strong>Required Documents:</strong> Additional evidence supporting your claim</div>
                <div class="appeal-item"><strong>Review Process:</strong> Independent review by senior claims specialists</div>
            </div>
            
            <p style="margin-top: 25px;">If you believe this decision was made in error or you have additional information that supports your claim, please don't hesitate to contact our claims review department.</p>
            
            <div class="contact-info">
                <h3>📞 Claims Review Department</h3>
                <p>Email: claims-review@insurance.com<br>
                Phone: 1-800-CLAIMS-1<br>
                Available: Monday-Friday, 8 AM - 6 PM</p>
            </div>
            
            <p style="margin-top: 25px; text-align: center;"><strong>Thank you for your understanding and for choosing our insurance services.</strong></p>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>
            <span class="company-name">Insurance Claims Department</span><br>
            Global Secure Shield</p>
        </div>
    </div>
</body>
</html>"""
        
        # Make the HTTP POST API call with subject and body
        response = requests.post(
            api_url,
            json={
                "subject": subject,
                "body": body
            },
            headers={"Content-Type": "application/json"},
        )
        
        # Return a standard response
        result = {
            "status": "submitted",
            "customer_id": customer_id,
            "stage": "claim_rejected",
            "message": "Thank you for using our insurance services. You will be notified via mail about your claim decision."
        }
        
        print(f"Claim rejected email sent successfully for customer {customer_id}")
        return result
        
    except Exception as e:
        print(f"Error sending claim rejected email: {str(e)}")
        return {
            "status": "error",
            "customer_id": customer_id,
            "message": "There was an issue sending the claim decision email. Please try again later or contact customer support."
        }


# List of available functions that can be used as agent tools
available_functions = [send_insurance_policy_number, send_insurance_claim_in_progress, send_insurance_claim_approved, send_insurance_claim_rejected]
