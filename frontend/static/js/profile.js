// profile.js - Profile page functionality
document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return;
    }

    await loadProfileData();
    setupEventListeners();
});

async function loadProfileData() {
    try {
        const response = await authenticatedFetch('/auth/me');

        if (response.ok) {
            const data = await response.json();
            populateProfile(data);
            await loadAssessmentHistory();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        showToast('Failed to load profile data', 'error');
    }
}

function populateProfile(data) {
    const user = data.user;
    const profile = data.profile || {};

    // Header info
    const fullName = profile.full_name || user.email || 'User';
    document.getElementById('profileName').textContent = fullName;
    document.getElementById('profileEmail').textContent = user.email || '';

    // Avatar
    const initial = fullName.charAt(0).toUpperCase();
    document.getElementById('avatarInitial').textContent = initial;
    document.getElementById('userInitial').textContent = initial;

    // Premium badge
    if (user.is_premium) {
        document.getElementById('premiumBadge').textContent = 'Premium Account';
        document.getElementById('premiumBadge').classList.add('success');
    }

    // Personal Information
    document.getElementById('fullName').value = profile.full_name || '';
    document.getElementById('nationality').value = profile.nationality || '';
    document.getElementById('dateOfBirth').value = profile.date_of_birth || '';
    document.getElementById('phone').value = user.phone || '';
    document.getElementById('bio').value = profile.bio || '';

    // Academic Profile
    document.getElementById('gpa').value = profile.gpa || '';
    document.getElementById('budget').value = profile.budget || '';
    document.getElementById('preferredCountry').value = profile.preferred_country || '';
    document.getElementById('preferredMajor').value = profile.preferred_major || '';
    document.getElementById('learningStyle').value = profile.learning_style || '';
    document.getElementById('careerGoal').value = profile.career_goal || '';
}

function setupEventListeners() {
    // User dropdown
    const userBtn = document.getElementById('userBtn');
    const userDropdown = document.getElementById('userDropdown');

    userBtn.addEventListener('click', () => {
        userDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!userBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('show');
        }
    });

    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });

    // Edit buttons
    document.getElementById('editPersonalBtn').addEventListener('click', () => {
        toggleEditMode('personal');
    });

    document.getElementById('editAcademicBtn').addEventListener('click', () => {
        toggleEditMode('academic');
    });

    // Cancel buttons
    document.getElementById('cancelPersonalBtn').addEventListener('click', () => {
        toggleEditMode('personal', false);
        loadProfileData();
    });

    document.getElementById('cancelAcademicBtn').addEventListener('click', () => {
        toggleEditMode('academic', false);
        loadProfileData();
    });

    // Form submissions
    document.getElementById('personalInfoForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await savePersonalInfo();
    });

    document.getElementById('academicProfileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveAcademicProfile();
    });
}

function toggleEditMode(formType, enable = true) {
    const form = formType === 'personal' ? 'personalInfoForm' : 'academicProfileForm';
    const inputs = document.querySelectorAll(`#${form} input, #${form} select, #${form} textarea`);
    const actions = document.querySelector(`#${form} .form-actions`);

    inputs.forEach(input => {
        input.disabled = !enable;
    });

    actions.style.display = enable ? 'flex' : 'none';
}

async function savePersonalInfo() {
    const data = {
        full_name: document.getElementById('fullName').value,
        nationality: document.getElementById('nationality').value,
        date_of_birth: document.getElementById('dateOfBirth').value,
        bio: document.getElementById('bio').value
    };

    try {
        const response = await authenticatedFetch('/auth/profile/create', {
            method: 'POST',
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showToast('Personal information updated successfully', 'success');
            toggleEditMode('personal', false);
            await loadProfileData();
        } else {
            showToast('Failed to update personal information', 'error');
        }
    } catch (error) {
        console.error('Error saving personal info:', error);
        showToast('An error occurred', 'error');
    }
}

async function saveAcademicProfile() {
    const data = {
        gpa: parseFloat(document.getElementById('gpa').value) || null,
        budget: parseInt(document.getElementById('budget').value) || null,
        preferred_country: document.getElementById('preferredCountry').value,
        preferred_major: document.getElementById('preferredMajor').value,
        learning_style: document.getElementById('learningStyle').value,
        career_goal: document.getElementById('careerGoal').value
    };

    try {
        const response = await authenticatedFetch('/auth/profile/create', {
            method: 'POST',
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showToast('Academic profile updated successfully', 'success');
            toggleEditMode('academic', false);
            await loadProfileData();
        } else {
            showToast('Failed to update academic profile', 'error');
        }
    } catch (error) {
        console.error('Error saving academic profile:', error);
        showToast('An error occurred', 'error');
    }
}

async function loadAssessmentHistory() {
    try {
        const response = await authenticatedFetch('/assessment/my-results');

        if (response.ok) {
            const data = await response.json();
            displayAssessmentHistory(data.results);
        }
    } catch (error) {
        console.error('Error loading assessment history:', error);
    }
}

function displayAssessmentHistory(assessments) {
    const container = document.getElementById('assessmentHistory');

    if (!assessments || assessments.length === 0) {
        container.innerHTML = '<p class="empty-state">No assessments completed yet</p>';
        return;
    }

    container.innerHTML = assessments.map(assessment => {
        const date = new Date(assessment.completed_at).toLocaleDateString();
        return `
            <div class="assessment-item">
                <div class="assessment-info">
                    <h4>${assessment.test_type} Assessment</h4>
                    <p>Personality: ${assessment.personality_type} • Completed: ${date}</p>
                </div>
                <a href="/assessment/results/${assessment.id}" class="link-btn">View Results</a>
            </div>
        `;
    }).join('');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById(type === 'success' ? 'successMessage' : 'errorMessage');
    toast.textContent = message;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
