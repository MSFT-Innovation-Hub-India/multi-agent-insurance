# Risk Score Analysis System

A modular browser automation system using Azure OpenAI's computer use capabilities with Playwright for automated risk analysis.

## Project Structure

```
Backend/
├── agent.py                   # Main automation script (refactored)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env.example               # Environment variables template
├── config/
│   ├── __init__.py
│   ├── settings.py            # Configuration settings
│   └── system_instructions.py # System instructions and prompts
├── core/
│   ├── __init__.py
│   ├── azure_client.py        # Azure OpenAI client management
│   ├── browser_manager.py     # Browser and page management
│   └── automation_engine.py   # Core automation logic
├── handlers/
│   ├── __init__.py
│   ├── action_handler.py      # Action execution handlers
│   └── safety_handler.py      # Safety check handlers
└── utils/
    ├── __init__.py
    ├── api_utils.py           # API utilities and retry logic
    ├── screenshot_utils.py    # Screenshot utilities
    └── user_interaction.py    # User input/output utilities
```

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Safety Handling**: Built-in safety check acknowledgment system
- **Retry Logic**: Robust API call handling with exponential backoff
- **Automated Execution**: Runs with predefined settings, no user input required
- **Browser Automation**: Comprehensive browser action handling (click, scroll, type, etc.)
- **Screenshot Management**: Automated screenshot capture and encoding

## Installation and Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```
4. Copy `.env.example` to `.env` and configure your Azure OpenAI credentials (optional - defaults are provided)

## Usage

Run the automation script:

```bash
python backup.py
```

The system will automatically start the risk analysis process with predefined settings.

## Modules Overview

### Core Modules

- **azure_client.py**: Manages Azure OpenAI client initialization and configuration
- **browser_manager.py**: Handles browser lifecycle and page management
- **automation_engine.py**: Contains the main automation loop logic

### Handler Modules

- **action_handler.py**: Executes different types of browser actions
- **safety_handler.py**: Manages safety check acknowledgments

### Utility Modules

- **api_utils.py**: Provides retry logic and safe API calls
- **screenshot_utils.py**: Handles screenshot capture and encoding
- **user_interaction.py**: Manages output formatting and minimal user interactions

### Configuration

- **settings.py**: Centralized configuration management
- **system_instructions.py**: Contains system prompts and instructions

## Safety Features

The system includes comprehensive safety handling:
- Automatic detection of safety warnings
- User confirmation for potentially risky actions (when required)
- Session termination on user decline
- Safety check acknowledgment tracking

## Error Handling

- Exponential backoff for API rate limits
- Comprehensive exception handling
- Graceful degradation on failures
- User-friendly error messages

## Contributing

1. Follow the modular structure
2. Add proper error handling
3. Include docstrings for all functions
4. Test thoroughly before committing

## License

This project is for internal use only.
