# CUA-2 - Global Secure Shield Insurance Portal

A comprehensive full-stack application combining automated risk analysis capabilities with a modern web-based management portal for insurance claims processing.

## 🏗️ Project Overview

This project consists of two main components:

1. **Backend**: An AI-powered browser automation system for risk score analysis using Azure OpenAI
2. **Frontend**: A modern web-based portal for insurance claims management and monitoring

## 📁 Project Structure

```
CUA-2/
├── Backend/                # AI-powered automation engine
│   ├── agent.py           # Main automation script
│   ├── requirements.txt   # Python dependencies
│   ├── README.md          # Backend documentation
│   ├── config/            # Configuration modules
│   ├── core/              # Core automation logic
│   ├── handlers/          # Action and safety handlers
│   └── utils/             # Utility functions
│
├── Frontend/              # Web-based management portal
│   ├── *.html            # Application pages
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript modules
│   └── README.md         # Frontend documentation
│
└── README.md             # This file - Project overview
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for Backend)
- **Modern web browser** (for Frontend)
- **Azure OpenAI access** (for automation features)

### Backend Setup

1. Navigate to the Backend directory:
   ```powershell
   cd Backend
   ```

2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```powershell
   playwright install chromium
   ```

4. Configure Azure OpenAI credentials (optional - defaults provided):
   ```powershell
   copy .env.example .env
   # Edit .env with your credentials
   ```

5. Run the automation system:
   ```powershell
   python backup.py
   ```

### Frontend Setup

1. Navigate to the Frontend directory:
   ```powershell
   cd Frontend
   ```

2. Start a local web server:
   ```powershell
   # Using Python
   python -m http.server 8000
   ```

3. Access the application:
   - Open browser to `http://localhost:8000`
   - Start with `login.html`

## 🌟 Key Features

### Backend Capabilities
- **AI-Powered Automation**: Uses Azure OpenAI for intelligent browser automation
- **Risk Analysis**: Automated risk score calculation and analysis
- **Safety Handling**: Built-in safety checks and user confirmations
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Robust Error Handling**: Comprehensive exception handling and retry logic

### Frontend Features
- **User Authentication**: Secure login system with session management
- **Dashboard Overview**: Visual metrics and key performance indicators
- **Risk Scoring Interface**: Interactive risk assessment tools
- **Rules Management**: Business rules configuration and validation
- **Workflow Automation**: Process design and monitoring capabilities
- **Responsive Design**: Modern, professional UI that adapts to different screen sizes

## 🔗 Component Integration

The Backend and Frontend components work together to provide a complete insurance claims management solution:

- **Backend** handles the automated risk analysis and data processing
- **Frontend** provides the user interface for monitoring, configuration, and manual oversight
- Both components can operate independently or in conjunction

## 📚 Detailed Documentation

For detailed information about each component:

- **Backend Documentation**: See [`Backend/README.md`](Backend/README.md)
- **Frontend Documentation**: See [`Frontend/README.md`](Frontend/README.md)

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Azure OpenAI API**
- **Playwright** (Browser automation)
- **Asyncio** (Asynchronous programming)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Responsive Design**
- **Local Storage** (Session management)
- **Modern ES6+ JavaScript**

## 🔒 Security Considerations

### Backend Security
- Azure OpenAI API key management
- Safe browser automation practices
- Comprehensive safety check system
- Session termination on security concerns

### Frontend Security
⚠️ **Important**: The frontend currently uses dummy authentication for demonstration purposes.

For production deployment:
1. Implement proper backend authentication
2. Use HTTPS for all communications
3. Implement secure session management
4. Add input validation and sanitization
5. Use token-based authentication

## 🚀 Deployment

### Development Environment
1. Run Backend automation system on localhost
2. Serve Frontend using local web server
3. Test integration between components

### Production Considerations
- Deploy Backend on secure server infrastructure
- Host Frontend on web server with HTTPS
- Implement proper authentication and authorization
- Configure monitoring and logging
- Set up backup and disaster recovery

## 📞 Support and Maintenance

This project is designed with modularity and maintainability in mind:

- **Modular Architecture**: Easy to extend and modify individual components
- **Comprehensive Documentation**: Each component has detailed documentation
- **Error Handling**: Robust error handling and logging throughout
- **Configuration Management**: Centralized configuration for easy updates

## 🤝 Contributing

When contributing to this project:

1. Follow the existing code structure and patterns
2. Update relevant README files for significant changes
3. Test both Backend and Frontend components
4. Ensure security best practices are maintained

## 📄 License

This project is part of the Global Secure Shield insurance management system. Please refer to the main project license for usage terms.

---

**Note**: This project combines advanced AI automation capabilities with a user-friendly web interface to provide a comprehensive solution for insurance claims processing and risk management.
