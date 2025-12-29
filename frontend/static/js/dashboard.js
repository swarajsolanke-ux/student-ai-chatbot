// dashboard.js - Dashboard functionality
document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return;
    }

    // Load user data
    await loadUserData();
    await loadRecommendations();

    // Setup event listeners
    setupEventListeners();
});

async function loadUserData() {
    try {
        const response = await authenticatedFetch('/auth/me');

        if (response.ok) {
            const data = await response.json();

            // Update UI with user data
            const userName = data.profile?.full_name || data.user?.email || 'Student';
            document.getElementById('userName').textContent = userName.split(' ')[0];

            // Update avatar initial
            const initial = userName.charAt(0).toUpperCase();
            document.getElementById('userInitial').textContent = initial;

            // Store user data
            window.currentUser = data;
        }
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

async function loadRecommendations() {
    const container = document.getElementById('recommendedUniversities');

    try {
        // Get user ID from stored data
        const userResponse = await authenticatedFetch('/auth/me');
        const userData = await userResponse.json();
        const userId = userData.user.id;

        // Get recommendations
        const response = await authenticatedFetch('/universities/recommend', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                max_results: 5
            })
        });

        if (response.ok) {
            const data = await response.json();
            const universities = data.recommendations || [];

            if (universities.length === 0) {
                container.innerHTML = '<div class="loading">No recommendations yet. Complete your assessment to get personalized recommendations!</div>';
                return;
            }

            // Update recommendations count
            document.getElementById('recommendations').textContent = universities.length;

            // Render universities
            container.innerHTML = universities.map(uni => `
                <div class="university-item" onclick="viewUniversity(${uni.id})">
                    <div class="university-logo">${uni.name.substring(0, 2)}</div>
                    <div class="university-info">
                        <h3>${uni.name}</h3>
                        <div class="university-meta">
                            <span>📍 ${uni.country}</span>
                            <span>💰 $${uni.tuition_fee.toLocaleString()}</span>
                            <span class="match-score">${Math.round(uni.recommendation_score * 100)}% Match</span>
                        </div>
                    </div>
                </div>
            `).join('');

        } else {
            container.innerHTML = '<div class="loading">Complete your profile to get recommendations</div>';
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
        container.innerHTML = '<div class="loading">Unable to load recommendations</div>';
    }
}

function setupEventListeners() {
    // User dropdown
    const userBtn = document.getElementById('userBtn');
    const userDropdown = document.getElementById('userDropdown');

    userBtn.addEventListener('click', () => {
        userDropdown.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!userBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('show');
        }
    });

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });

    // Assessment button
    document.getElementById('startAssessment').addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/assessment';
    });
}

function viewUniversity(id) {
    window.location.href = `/universities/${id}`;
}

// Load notifications count
async function loadNotifications() {
    try {
        const response = await authenticatedFetch('/notifications');
        if (response.ok) {
            const data = await response.json();
            const unreadCount = data.unread_count || 0;
            document.getElementById('notificationBadge').textContent = unreadCount;
        }
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

// Call loadNotifications periodically
setInterval(loadNotifications, 30000); // Every 30 seconds
