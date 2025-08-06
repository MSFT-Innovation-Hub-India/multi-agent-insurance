# Insurance Customer Communication Agent

A sophisticated AI-powered customer service agent built with Azure AI Projects that handles insurance customer communications through natural language interactions.

## 🚀 Features

### Insurance Communication Operations
- **Policy Number Generation**: Send policy number generation emails to customers
- **Claim Processing Status**: Notify customers about claim processing progress
- **Claim Approval Notifications**: Send claim approval emails with settlement details
- **Claim Rejection Communications**: Inform customers about claim rejections with appeal information

### Insurance Process Stage Management
The agent supports 4 distinct insurance communication stages:
1. **Stage 1: Policy Number Generation** - Send policy number to new customers
2. **Stage 2: Claim In Progress** - Update customers on claim processing status
3. **Stage 3: Claim Approved** - Notify customers of approved claims with settlement amounts
4. **Stage 4: Claim Rejected** - Inform customers of rejected claims with appeal process

### Smart Customer Memory
- Remembers customer ID throughout the conversation
- No need to re-enter customer information for subsequent requests
- Maintains context across multiple interactions

## 📋 Prerequisites

- Python 3.8 or higher
- Azure subscription with AI Projects enabled
- Azure Logic Apps endpoints configured
- Valid Azure credentials

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd Insurance Customer Communication Agent
   ```

2. **Install required dependencies**
   ```bash
   pip install azure-ai-projects~=1.0.0b7
   pip install requests
   ```

3. **Set up environment variables**
   ```bash
   # Azure AI Projects configuration
   export AZURE_AI_PROJECT_CONNECTION_STRING="your_connection_string_here"
   
   # Or alternatively, set individual variables:
   export AZURE_AI_PROJECT_SUBSCRIPTION_ID="your_subscription_id"
   export AZURE_AI_PROJECT_RESOURCE_GROUP="your_resource_group"
   export AZURE_AI_PROJECT_PROJECT_NAME="your_project_name"
   ```

## ⚙️ Configuration

### Azure Logic Apps Integration
The agent integrates with Azure Logic Apps for email sending:

- **Insurance Logic App URL**: Configure in `custom_agent_functions.py`
- **Endpoint**: `https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke`

### Agent Configuration
Update `config.py` with your settings:
```python
# Company information
AGENT_COMPANY_NAME = "Global Secure Shield"

# Agent behavior settings
AGENT_MODEL = "gpt-4o"
AGENT_TEMPERATURE = 0.3
```

## 🚦 Usage

### Running the Agent
```bash
python agent.py
```

### Example Conversation Flow
```
Agent: Hello! I'm your Insurance Customer Communication Agent...

User: Hi, my customer ID is CUST123 and I need Stage 1

Agent: Thank you! I'll send you the policy number generation email for customer ID CUST123.

[Agent sends policy number email via Logic App]

Agent: Thank you for using our insurance services. You will be notified via email about your policy number.
```

### Supported Commands
- **Stage 1**: "I need stage 1" or "policy number generation"
- **Stage 2**: "I need stage 2" or "claim in progress"  
- **Stage 3**: "I need stage 3" or "claim approved"
- **Stage 4**: "I need stage 4" or "claim rejected"

## 📁 Project Structure

```
Insurance Customer Communication Agent/
├── agent.py                      # Main agent orchestration
├── config.py                     # Configuration settings
├── custom_agent_functions.py     # Insurance communication functions
├── custom_agent_tools.py         # Tool definitions for the agent
├── system_instructions.py        # Agent behavior instructions
├── tool_handler.py              # Tool execution management
├── utils.py                      # Utility functions
├── logic_app.json               # Logic App configuration
└── README.md                     # Project documentation
```

## 🔧 Core Components

### 1. Agent Orchestration (`agent.py`)
- Main conversation loop
- Customer memory management
- Tool execution coordination

### 2. Insurance Functions (`custom_agent_functions.py`)
- `send_insurance_policy_number()` - Policy number generation emails
- `send_insurance_claim_in_progress()` - Claim processing status emails
- `send_insurance_claim_approved()` - Claim approval notifications
- `send_insurance_claim_rejected()` - Claim rejection communications

### 3. Tool Definitions (`custom_agent_tools.py`)
- Azure AI Projects tool schemas
- Parameter validation
- Function mapping

### 4. System Instructions (`system_instructions.py`)
- Agent behavior guidelines
- Conversation flow rules
- Tool usage instructions

## 📝 API Documentation

### Function Signatures

```python
# Insurance Communication Functions
send_insurance_policy_number(customer_id: str)
send_insurance_claim_in_progress(customer_id: str)
send_insurance_claim_approved(customer_id: str)
send_insurance_claim_rejected(customer_id: str)
```

## 🔐 Security Considerations

- All API calls use HTTPS encryption
- Customer data is validated before processing
- Azure credentials are managed securely
- No sensitive information is logged

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with additional insurance systems
- [ ] Enhanced customer authentication
- [ ] Real-time notification system
- [ ] Mobile app integration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For technical support or questions:
- Email: support@insurance-agent.com
- Documentation: [Azure AI Projects Docs](https://docs.microsoft.com/azure/ai-services/)
- Issues: GitHub Issues page

---

**Note**: This agent is designed specifically for insurance customer communication. Ensure your Azure Logic Apps endpoints are properly configured for email delivery.
