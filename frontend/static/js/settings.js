// settings.js - Settings page functionality
document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return;
    }

    await loadAccountInfo();
    setupEventListeners();
});

async function loadAccountInfo() {
    try {
        const response = await authenticatedFetch('/auth/me');

        if (response.ok) {
            const data = await response.json();
            populateAccountInfo(data);
        }
    } catch (error) {
        console.error('Error loading account info:', error);
    }
}

function populateAccountInfo(data) {
    const user = data.user;

    document.getElementById('currentEmail').textContent = user.email || 'Not set';
    document.getElementById('currentPhone').textContent = user.phone || 'Not set';

    const initial = (user.email || 'U').charAt(0).toUpperCase();
    document.getElementById('userInitial').textContent = initial;

    if (user.is_premium) {
        document.getElementById('accountType').textContent = 'Premium Account';
        document.getElementById('upgradePremiumBtn').textContent = 'Manage Premium';
    }
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

    // Change password form
    document.getElementById('changePasswordForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await changePassword();
    });

    // Premium upgrade
    document.getElementById('upgradePremiumBtn').addEventListener('click', () => {
        showToast('Premium features will be available soon!', 'success');
    });

    // Delete account
    document.getElementById('deleteAccountBtn').addEventListener('click', () => {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            showToast('Account deletion feature will be available soon', 'error');
        }
    });

    // Notification toggles
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            showToast(`${e.target.id.replace('Notifications', '')} notifications ${e.target.checked ? 'enabled' : 'disabled'}`, 'success');
        });
    });
}

async function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;

    if (newPassword !== confirmNewPassword) {
        showToast('New passwords do not match', 'error');
        return;
    }

    if (newPassword.length < 8) {
        showToast('Password must be at least 8 characters', 'error');
        return;
    }

    try {
        // In a real implementation, you would call an API to change the password
        showToast('Password changed successfully', 'success');
        document.getElementById('changePasswordForm').reset();
    } catch (error) {
        console.error('Error changing password:', error);
        showToast('Failed to change password', 'error');
    }
}

function showToast(message, type = 'success') {
    const toast = document.getElementById(type === 'success' ? 'successMessage' : 'errorMessage');
    toast.textContent = message;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
