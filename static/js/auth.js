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