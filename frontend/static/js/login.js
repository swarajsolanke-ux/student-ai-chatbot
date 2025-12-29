// login.js - Login page functionality
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.auth-form');
    const emailForm = document.getElementById('emailLoginForm');
    const phoneForm = document.getElementById('phoneLoginForm');
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    const verifyOtpBtn = document.getElementById('verifyOtpBtn');
    const resendOtpBtn = document.getElementById('resendOtpBtn');
    const otpSection = document.getElementById('otpSection');
    const otpInputs = document.querySelectorAll('.otp-input');

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(`${tabName}LoginForm`).classList.add('active');

            clearMessages();
        });
    });

    // Email login
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        showLoading(emailForm.querySelector('button[type="submit"]'));

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Store token
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);

                showSuccess('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showError(data.detail || 'Invalid email or password');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            hideLoading(emailForm.querySelector('button[type="submit"]'));
        }
    });

    // Send OTP
    sendOtpBtn.addEventListener('click', async () => {
        const phone = document.getElementById('phone').value;

        if (!phone) {
            showError('Please enter your phone number');
            return;
        }

        showLoading(sendOtpBtn);

        try {
            const response = await fetch('/auth/send-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone })
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess('OTP sent successfully! Check your phone.');
                otpSection.style.display = 'block';
                otpInputs[0].focus();
            } else {
                showError(data.detail || 'Failed to send OTP');
            }
        } catch (error) {
            console.error('OTP error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            hideLoading(sendOtpBtn);
        }
    });

    // OTP input handling
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            if (e.target.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });

        // Only allow digits
        input.addEventListener('keypress', (e) => {
            if (!/[0-9]/.test(e.key)) {
                e.preventDefault();
            }
        });
    });

    // Verify OTP
    verifyOtpBtn.addEventListener('click', async () => {
        const phone = document.getElementById('phone').value;
        const otp = Array.from(otpInputs).map(input => input.value).join('');

        if (otp.length !== 6) {
            showError('Please enter the complete OTP');
            return;
        }

        showLoading(verifyOtpBtn);

        try {
            const response = await fetch('/auth/verify-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone, otp_code: otp })
            });

            const data = await response.json();

            if (response.ok) {
                // Store token
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);

                showSuccess('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showError(data.detail || 'Invalid OTP');
                otpInputs.forEach(input => input.value = '');
                otpInputs[0].focus();
            }
        } catch (error) {
            console.error('Verify error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            hideLoading(verifyOtpBtn);
        }
    });

    // Resend OTP
    resendOtpBtn.addEventListener('click', () => {
        sendOtpBtn.click();
    });

    // Social login handlers
    document.querySelector('.google-btn').addEventListener('click', () => {
        showError('Google Sign-In will be available soon');
    });

    document.querySelector('.apple-btn').addEventListener('click', () => {
        showError('Apple Sign-In will be available soon');
    });
});
