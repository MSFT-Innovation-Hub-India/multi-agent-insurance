# Frontend - Global Secure Shield

A modern web-based frontend for the Global Secure Shield Insurance Claims Management Portal.

## 📁 Project Structure

```
Frontend/
├── css/                    # Stylesheets
│   ├── main.css           # Global styles and layout
│   ├── login.css          # Login page specific styles
│   ├── dashboard.css      # Dashboard page styles
│   ├── risk-score.css     # Risk scoring page styles
│   ├── rules.css          # Rules management styles
│   └── workflow.css       # Workflow page styles
├── js/                     # JavaScript files
│   ├── main.js            # Core utilities and authentication
│   ├── login.js           # Login page functionality
│   ├── dashboard.js       # Dashboard interactive features
│   ├── risk-score.js      # Risk scoring calculations
│   ├── risk-analysis-data.js # Risk analysis data models
│   ├── rules.js           # Rules management logic
│   └── workflow.js        # Workflow automation controls
├── login.html             # Login/authentication page
├── dashboard.html         # Main dashboard overview
├── risk-score.html        # Risk scoring interface
├── rules.html             # Rules configuration page
├── workflow.html          # Workflow management page
└── README.md              # This file
```

## 🌟 Features

### Authentication System
- **Secure Login**: Username/password authentication with validation
- **Session Management**: Local storage based session handling
- **Auto-redirect**: Automatic redirection for authenticated/unauthenticated users

### Dashboard
- **Claims Overview**: Visual dashboard showing key metrics
- **Navigation Menu**: Intuitive navigation between different modules
- **User Profile**: Display current user information and logout functionality

### Risk Scoring
- **Risk Assessment**: Calculate and display risk scores for insurance claims
- **Visual Indicators**: Color-coded risk levels and scoring charts
- **Data Analysis**: Comprehensive risk analysis tools

### Rules Management
- **Rule Configuration**: Create and manage business rules
- **Rule Engine**: Interactive rule builder interface
- **Validation**: Rule validation and testing capabilities

### Workflow Management
- **Process Automation**: Manage automated workflows
- **Workflow Designer**: Visual workflow creation tools
- **Status Tracking**: Monitor workflow execution status

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Web server (for local development)

### Local Development

1. **Clone or download** the frontend files to your local machine

2. **Serve the files** using a local web server:
   
   **Option 1: Using Python**
   ```bash
   # Navigate to the Frontend directory
   cd Frontend
   
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   ```
   
   **Option 2: Using Node.js**
   ```bash
   # Install a simple server
   npm install -g http-server
   
   # Navigate to Frontend directory and serve
   cd Frontend
   http-server -p 8000
   ```
   
   **Option 3: Using Live Server (VS Code)**
   - Install the "Live Server" extension in VS Code
   - Right-click on `login.html` and select "Open with Live Server"

3. **Access the application**:
   - Open your browser and navigate to `http://localhost:8000`
   - Start with `login.html` for the login page

### Default Login Credentials
For development/testing purposes:
- **Username**: Any non-empty string
- **Password**: Any non-empty string

*Note: The current implementation uses dummy authentication for demo purposes.*

## 📱 Page Navigation

### Login Page (`login.html`)
- Entry point to the application
- Username and password validation
- Redirects to dashboard on successful login

### Dashboard (`dashboard.html`)
- Main overview page after login
- Key metrics and statistics
- Quick access to all modules

### Risk Scoring (`risk-score.html`)
- Risk assessment tools
- Scoring algorithms and visualization
- Risk level indicators

### Rules Management (`rules.html`)
- Business rules configuration
- Rule creation and editing interface
- Rule validation tools

### Workflow Management (`workflow.html`)
- Automated workflow controls
- Process design and monitoring
- Workflow status tracking

## 🎨 Styling and Themes

The application uses a modern, professional design with:
- **Responsive Layout**: Adapts to different screen sizes
- **Color Scheme**: Professional blue and white theme with accent colors
- **Icons**: Emoji-based icons for visual clarity
- **Typography**: Clean, readable fonts
- **Animations**: Smooth transitions and hover effects

## 🔧 Browser Compatibility

- **Chrome**: 80+
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+

## 📚 JavaScript Modules

### Auth Module (`main.js`)
- User authentication
- Session management
- Login/logout functionality

### UI Utilities (`main.js`)
- Common UI functions
- Form validation
- Notification system

### Page-Specific Scripts
- Each page has dedicated JavaScript for specific functionality
- Modular approach for better maintainability

## 🛠️ Customization

### Adding New Pages
1. Create HTML file in the root Frontend directory
2. Create corresponding CSS file in `css/` folder
3. Create JavaScript file in `js/` folder
4. Update navigation in existing pages

### Modifying Styles
- Global styles: Edit `css/main.css`
- Page-specific styles: Edit respective CSS files
- Maintain consistent color scheme and spacing

### Extending Functionality
- Add new JavaScript modules in `js/` folder
- Follow existing naming conventions
- Maintain modular structure

## 🚨 Security Notes

⚠️ **Important**: This frontend currently uses dummy authentication for demonstration purposes. For production use:

1. Implement proper backend authentication
2. Use HTTPS for all communications
3. Implement proper session management
4. Add input validation and sanitization
5. Use secure token-based authentication

## 📞 Support

For technical support or questions about this frontend implementation, please refer to the main project documentation or contact the development team.

## 📄 License

This frontend is part of the Global Secure Shield project. Please refer to the main project license for usage terms.
