// Login Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    if (Auth.isLoggedIn()) {
        window.location.href = 'dashboard.html';
        return;
    }

    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const loginBtn = document.getElementById('loginBtn');

    // Password visibility toggle
    passwordToggle.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = passwordToggle.querySelector('.toggle-icon');
        icon.textContent = type === 'password' ? '👁️' : '🙈';
    });

    // Real-time validation
    function validateField(field, errorElement, message) {
        const value = field.value.trim();
        if (!value) {
            showFieldError(field, errorElement, message);
            return false;
        } else {
            hideFieldError(field, errorElement);
            return true;
        }
    }

    function showFieldError(field, errorElement, message) {
        field.style.borderColor = 'var(--error-color)';
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }

    function hideFieldError(field, errorElement) {
        field.style.borderColor = 'var(--border-color)';
        errorElement.textContent = '';
        errorElement.classList.remove('show');
    }

    // Input validation on blur
    usernameInput.addEventListener('blur', function() {
        validateField(
            usernameInput, 
            document.getElementById('usernameError'), 
            'Username is required'
        );
    });

    passwordInput.addEventListener('blur', function() {
        validateField(
            passwordInput, 
            document.getElementById('passwordError'), 
            'Password is required'
        );
    });

    // Clear errors on input
    usernameInput.addEventListener('input', function() {
        if (this.value.trim()) {
            hideFieldError(this, document.getElementById('usernameError'));
        }
    });

    passwordInput.addEventListener('input', function() {
        if (this.value.trim()) {
            hideFieldError(this, document.getElementById('passwordError'));
        }
    });

    // Form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const usernameError = document.getElementById('usernameError');
        const passwordError = document.getElementById('passwordError');

        // Validate fields
        const isUsernameValid = validateField(usernameInput, usernameError, 'Username is required');
        const isPasswordValid = validateField(passwordInput, passwordError, 'Password is required');

        if (!isUsernameValid || !isPasswordValid) {
            // Shake animation for invalid form
            loginForm.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                loginForm.style.animation = '';
            }, 500);
            return;
        }

        // Show loading state
        loginBtn.disabled = true;
        loginBtn.textContent = 'Signing in...';

        // Simulate API call delay
        setTimeout(() => {
            // Attempt login (demo accepts any non-empty credentials)
            const loginSuccess = Auth.login(username, password);

            if (loginSuccess) {
                // Success state
                loginBtn.textContent = '✓ Success!';
                loginBtn.style.background = 'linear-gradient(135deg, var(--success-color), #059669)';
                
                Utils.showNotification('Login successful! Redirecting...', 'success');
                
                // Redirect after short delay
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } else {
                // Reset button state
                loginBtn.disabled = false;
                loginBtn.textContent = 'Sign In';
                
                // Show error
                showFieldError(passwordInput, passwordError, 'Invalid username or password');
                Utils.showNotification('Login failed. Please check your credentials.', 'error');
                
                // Shake animation
                loginForm.style.animation = 'shake 0.5s ease-in-out';
                setTimeout(() => {
                    loginForm.style.animation = '';
                }, 500);
            }
        }, 1500); // Simulate network delay
    });

    // Add shake animation styles
    const shakeStyles = document.createElement('style');
    shakeStyles.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(shakeStyles);

    // Enter key support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && (usernameInput.contains(e.target) || passwordInput.contains(e.target))) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-fill demo credentials (for testing)
    const demoCard = document.querySelector('.demo-card');
    if (demoCard) {
        demoCard.addEventListener('click', function() {
            usernameInput.value = 'demo';
            passwordInput.value = 'password';
            
            // Animate the inputs
            usernameInput.style.transform = 'scale(1.02)';
            passwordInput.style.transform = 'scale(1.02)';
            
            setTimeout(() => {
                usernameInput.style.transform = '';
                passwordInput.style.transform = '';
            }, 200);
            
            Utils.showNotification('Demo credentials filled!', 'info');
        });
    }

    // Parallax effect for background
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        const overlay = document.querySelector('.login-overlay');
        if (overlay) {
            overlay.style.background = `radial-gradient(circle at ${mouseX * 100}% ${mouseY * 100}%, rgba(255, 255, 255, 0.1) 0%, transparent 70%)`;
        }
    });

    // Focus first input on load
    setTimeout(() => {
        usernameInput.focus();
    }, 500);
});
