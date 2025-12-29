// register.js - Registration page functionality
let registrationData = {};
let currentStep = 1;

document.addEventListener('DOMContentLoaded', () => {
    const step1Next = document.getElementById('step1Next');
    const step2Next = document.getElementById('step2Next');
    const step2Back = document.getElementById('step2Back');
    const step3Back = document.getElementById('step3Back');
    const step3Form = document.getElementById('step3Form');

    // Step 1 validation and navigation
    step1Next.addEventListener('click', () => {
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const terms = document.getElementById('terms').checked;

        if (!fullName || !email || !password || !confirmPassword) {
            showError('Please fill in all fields');
            return;
        }

        if (password.length < 8) {
            showError('Password must be at least 8 characters');
            return;
        }

        if (password !== confirmPassword) {
            showError('Passwords do not match');
            return;
        }

        if (!terms) {
            showError('Please accept the terms and conditions');
            return;
        }

        registrationData = {
            full_name: fullName,
            email: email,
            password: password
        };

        goToStep(2);
    });

    // Step 2 navigation
    step2Next.addEventListener('click', () => {
        registrationData.nationality = document.getElementById('nationality').value;
        registrationData.gpa = parseFloat(document.getElementById('gpa').value) || null;
        registrationData.budget = parseInt(document.getElementById('budget').value) || null;
        registrationData.career_goal = document.getElementById('careerGoal').value;

        goToStep(3);
    });

    step2Back.addEventListener('click', () => {
        goToStep(1);
    });

    step3Back.addEventListener('click', () => {
        goToStep(2);
    });

    // Final registration
    step3Form.addEventListener('submit', async (e) => {
        e.preventDefault();

        registrationData.preferred_country = document.getElementById('preferredCountry').value;
        registrationData.preferred_major = document.getElementById('preferredMajor').value;
        registrationData.learning_style = document.getElementById('learningStyle').value;

        showLoading(document.getElementById('registerBtn'));

        try {
            // Register user
            const registerResponse = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: registrationData.email,
                    password: registrationData.password,
                    full_name: registrationData.full_name,
                    auth_provider: 'email'
                })
            });

            const registerData = await registerResponse.json();

            if (!registerResponse.ok) {
                showError(registerData.detail || 'Registration failed');
                hideLoading(document.getElementById('registerBtn'));
                return;
            }

            // Store token
            localStorage.setItem('access_token', registerData.access_token);
            localStorage.setItem('refresh_token', registerData.refresh_token);

            // Create profile
            const profileResponse = await authenticatedFetch('/auth/profile/create', {
                method: 'POST',
                body: JSON.stringify({
                    full_name: registrationData.full_name,
                    nationality: registrationData.nationality,
                    gpa: registrationData.gpa,
                    budget: registrationData.budget,
                    preferred_country: registrationData.preferred_country,
                    preferred_major: registrationData.preferred_major,
                    learning_style: registrationData.learning_style,
                    career_goal: registrationData.career_goal
                })
            });

            if (profileResponse.ok) {
                showSuccess('Registration successful! Redirecting to dashboard...');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                // Registration successful but profile creation failed
                showSuccess('Registration successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            }

        } catch (error) {
            console.error('Registration error:', error);
            showError('An error occurred. Please try again.');
            hideLoading(document.getElementById('registerBtn'));
        }
    });
});

function goToStep(step) {
    currentStep = step;

    // Update step indicators
    document.querySelectorAll('.step').forEach(s => {
        const stepNum = parseInt(s.dataset.step);
        if (stepNum < step) {
            s.classList.add('completed');
            s.classList.remove('active');
        } else if (stepNum === step) {
            s.classList.add('active');
            s.classList.remove('completed');
        } else {
            s.classList.remove('active', 'completed');
        }
    });

    // Show/hide forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    document.getElementById(`step${step}Form`).classList.add('active');

    clearMessages();
}
