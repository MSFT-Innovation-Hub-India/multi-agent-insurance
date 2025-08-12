# AI-Powered Insurance Policy Generator

A comprehensive insurance policy generation system that combines Azure AI with Model Context Protocol (MCP) PDF generation to create professional insurance documents through conversational interfaces.

## 🌟 Features

- **🤖 Conversational AI Agent**: Interactive insurance policy creation using Azure AI Projects
- **📄 Professional PDF Generation**: High-quality insurance documents with industry-standard formatting
- **🎨 Custom Styling**: Professional insurance document themes and layouts
- **🇮🇳 Indian Market Focus**: Compliance with IRDAI standards and Indian insurance regulations
- **🔄 Multiple Policy Types**: Health, Auto, Life, and other insurance policy generation
- **💡 Smart Document Processing**: AI-powered content generation with local formatting control
- **📋 MCP Integration**: Advanced PDF generation using Model Context Protocol server

## 🏗️ Architecture

The system uses a hybrid architecture combining:

1. **Azure AI Projects**: For intelligent conversation and content generation
2. **Local Python Processing**: For data validation, formatting, and business logic
3. **MCP PDF Server**: For professional PDF document generation with custom styling
4. **Professional Styling System**: Insurance industry-grade document formatting

```
User Input (JSON/Chat) → Azure AI Agent → Python Processing → MCP PDF Server → Professional PDF
```

## 📁 Project Structure

```
MCP/
├── policy_agent.py              # Main conversational AI agent
├── insurance_policy_generator.py # Standard policy generation
├── mcp_client.py               # MCP PDF server client
├── README.md                   # This file
├── PDF/                        # Generated PDF output directory
│   ├── example_basic.pdf
│   ├── example_corporate.pdf
│   ├── global_secure_shield_health_policy.pdf
│   └── indian_policy_document_2025.pdf
|   -github:FabianGenell/pdf-mcp-server (this is the MCP pdf server)
└── __pycache__/              # Python cache files
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with the following packages:
   ```bash
   pip install azure-ai-projects==1.0.0b10
   pip install azure-identity
   ```

2. **Node.js 16+** for the MCP PDF server:
   ```bash
   cd pdf-mcp-server
   npm install
   ```

3. **Azure AI Projects Setup**: 
   - Azure subscription with AI Projects resource
   - Proper authentication credentials configured

### Basic Usage

#### 1. Conversational Policy Generation

```bash
python policy_agent.py
```

The agent will guide you through an interactive conversation to create insurance policies:

```python
# Example JSON input for the agent:
{
    "customerName": "Rajesh Kumar Sharma",
    "claimType": "health",
    "claimAmount": 500000,
    "policyStartDate": "2025-01-15",
    "policyNumber": "GSS-2025-123456"
}
```

#### 2. Direct Policy Generation

```bash
python insurance_policy_generator.py
```

This generates a sample professional insurance policy document.

## 🔧 Configuration

### Azure AI Setup

Update the connection string in `policy_agent.py`:

```python
self.project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="YOUR_AZURE_AI_CONNECTION_STRING"
)
```

### PDF Output Directory

By default, PDFs are generated in the `PDF/` directory. You can change this in `mcp_client.py`:

```python
self.default_pdf_dir = r"C:\Your\Custom\Path\PDF"
```

## 📋 Usage Examples

### Health Insurance Policy

```python
# Input JSON
{
    "customerName": "Priya Sharma",
    "claimType": "health",
    "claimAmount": 750000,
    "policyStartDate": "2025-08-12",
    "age": 32,
    "occupation": "Software Engineer"
}
```

### Auto Insurance Policy

```python
# Input JSON
{
    "customerName": "Amit Patel",
    "claimType": "auto",
    "claimAmount": 1200000,
    "policyStartDate": "2025-08-12",
    "vehicleType": "Car",
    "vehicleModel": "Honda City"
}
```

## 🎨 Document Styling

The system includes professional insurance document styling with:

- **Company Branding**: Global Secure Shield Insurance branding
- **Gradient Headers**: Professional blue gradient section headers
- **Responsive Grids**: Information and benefits in organized grids
- **Coverage Highlights**: Prominent sum insured displays
- **Claim Process Steps**: Numbered step-by-step claim procedures
- **IRDAI Compliance**: Standard insurance document formatting

### Custom Styles

Custom styles are stored in `pdf-mcp-server/custom-styles/`:

- `global_secure_shield_policy.json` - Main insurance policy style
- `indian_government_policy.json` - Government compliance style
- `corporate_report.json` - Corporate document style

## 🤖 AI Agent Features

The conversational agent provides:

- **Natural Language Processing**: Understands insurance queries in plain English
- **Context Awareness**: Maintains conversation context across multiple exchanges
- **Smart Data Generation**: Automatically fills missing information with realistic Indian data
- **Policy Validation**: Ensures generated policies meet regulatory requirements
- **Multi-format Support**: Supports both JSON input and conversational interaction

### Agent Capabilities

- Policy requirement gathering
- Coverage recommendation
- Premium calculation
- Claims process explanation
- Document generation
- Regulatory compliance checking

## 📄 Generated Documents

Each generated policy includes:

### 1. Policy Information
- Customer details and contact information
- Policy number and validity dates
- Insurer information and licensing details

### 2. Coverage Details
- Sum insured and policy type
- Comprehensive coverage inclusions
- Waiting periods and conditions

### 3. Premium Information
- Detailed premium breakdown
- Payment terms and schedules
- GST and tax calculations

### 4. Claims Process
- Step-by-step claiming procedures
- Required documentation lists
- Submission channels and timelines

### 5. Terms & Conditions
- Policy exclusions and limitations
- General terms and conditions
- Medical examination requirements

### 6. Regulatory Compliance
- IRDAI registration details
- Contact information for complaints
- Branch office locations

## 🔍 Technical Details

### Azure AI Integration

The system uses Azure AI Projects SDK for:
- Intelligent conversation management
- Content generation and enhancement
- Context-aware responses
- Multi-turn conversation support

### MCP PDF Server

The PDF generation server provides:
- Professional document layouts
- Custom CSS styling support
- Template-based generation
- High-quality PDF output

### Error Handling

Comprehensive error handling for:
- Azure AI connection issues
- PDF generation failures
- Invalid input data
- Server communication errors

## 🛠️ Development

### Adding New Policy Types

1. Update the agent instructions in `policy_agent.py`
2. Add coverage details in `convert_markdown_to_html()`
3. Create custom styles in `pdf-mcp-server/custom-styles/`

### Customizing Document Styles

1. Modify CSS in the style creation functions
2. Update templates in `pdf-mcp-server/templates/`
3. Test with sample data

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security & Compliance

- **Data Privacy**: No sensitive data is stored permanently
- **IRDAI Compliance**: Documents follow Indian insurance regulations
- **Secure Communication**: Encrypted connections for Azure AI
- **Audit Trail**: Document generation tracking and logging

## 📞 Support

For issues and questions:

1. Check the error logs in the terminal output
2. Verify Azure AI credentials and permissions
3. Ensure Node.js dependencies are installed
4. Review PDF output directory permissions

## 📈 Future Enhancements

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Integration with actual insurance APIs
- [ ] Advanced risk assessment algorithms
- [ ] Mobile app integration
- [ ] Blockchain-based policy verification
- [ ] OCR for document scanning
- [ ] Automated compliance checking

## 📄 License

This project is for demonstration and educational purposes. For production use, ensure proper insurance licensing and regulatory compliance.

---

**Generated on:** August 12, 2025  
**Project Version:** 2.0  
**AI Model:** Azure OpenAI + Custom Insurance Agent  
**MCP Version:** Latest
