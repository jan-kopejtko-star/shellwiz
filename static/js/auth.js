// Auth-related JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Get modal elements
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    
    // Get button elements
    const loginBtn = document.querySelector('.login-btn');
    const registerBtn = document.querySelector('.register-btn');
    
    // Get close buttons
    const closeBtns = document.querySelectorAll('.close');
    
    // Get links to switch between modals
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    
    // Login button click event
    loginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.style.display = 'flex';
    });
    
    // Register button click event
    registerBtn.addEventListener('click', function(e) {
        e.preventDefault();
        registerModal.style.display = 'flex';
    });
    
    // Close button click events
    closeBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            loginModal.style.display = 'none';
            registerModal.style.display = 'none';
        });
    });
    
    // Switch to register modal
    showRegisterLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.style.display = 'none';
        registerModal.style.display = 'flex';
    });
    
    // Switch to login modal
    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        registerModal.style.display = 'none';
        loginModal.style.display = 'flex';
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (e.target === registerModal) {
            registerModal.style.display = 'none';
        }
    });
    
    // Form submission handling
    const loginForm = loginModal.querySelector('form');
    const registerForm = registerModal.querySelector('form');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form input values
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        // In a real implementation, you would send these values to your backend
        console.log('Login attempt with:', { email });
        
        // For demo purposes, simulate successful login
        alert('Login functionality would be implemented with a backend. Demo mode: login successful!');
        loginModal.style.display = 'none';
    });
    
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form input values
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const confirmPassword = document.getElementById('register-confirm').value;
        
        // Simple validation
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // In a real implementation, you would send these values to your backend
        console.log('Registration attempt with:', { username, email });
        
        // For demo purposes, simulate successful registration
        alert('Registration functionality would be implemented with a backend. Demo mode: registration successful!');
        registerModal.style.display = 'none';
    });
});

// In your auth.js file
document.addEventListener('DOMContentLoaded', function() {
    // Registration form handling
    const registerForm = document.querySelector('#registerModal form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('register-username').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const confirmPassword = document.getElementById('register-confirm').value;
            
            // Create request data
            const data = {
                username: username,
                email: email,
                password: password,
                confirm_password: confirmPassword
            };
            
            // Send API request
            fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Display success message
                    showMessage('success', data.message);
                    
                    // Close register modal and open login modal
                    document.getElementById('registerModal').style.display = 'none';
                    document.getElementById('loginModal').style.display = 'block';
                } else {
                    // Display error message
                    showMessage('error', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('error', 'An error occurred. Please try again.');
            });
        });
    }
    
    // Helper function to show messages
    function showMessage(type, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('flash-message', type);
        messageDiv.textContent = message;
        
        const closeBtn = document.createElement('span');
        closeBtn.classList.add('close-flash');
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = function() {
            messageDiv.remove();
        };
        
        messageDiv.appendChild(closeBtn);
        document.querySelector('.flash-messages').appendChild(messageDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
});