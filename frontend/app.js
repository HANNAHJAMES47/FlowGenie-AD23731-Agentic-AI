const state = {
    eventId: null,
    recommendations: {},
    selectedVendors: {}, // Map category -> vendor object
    skippedCategories: new Set(),
    budgetPlan: {},
    agentLogs: [],
    runOfShow: [],
    bookedVendors: [],
    auth: {
        token: null,
        user: null,
        isLoggedIn: false,
    },
    user: {
        name: '',
        email: '',
    },
    favorites: {},
    eventHistory: [],
    preferences: {},
    favoritesOnlyMode: false,
};

const views = {
    landing: document.getElementById('landingView'),
    prompt: document.getElementById('promptView'),
    loading: document.getElementById('loadingView'),
    recommendation: document.getElementById('recommendationView'),
    confirmation: document.getElementById('confirmationView'),
    status: document.getElementById('statusView'),
};

const els = {
    eventForm: document.getElementById('eventForm'),
    eventType: document.getElementById('eventType'),
    guestCount: document.getElementById('guestCount'),
    location: document.getElementById('location'),
    eventDate: document.getElementById('eventDate'),
    eventTimeSlot: document.getElementById('eventTimeSlot'),
    eventStartTime: document.getElementById('eventStartTime'),
    cateringMealSlot: document.getElementById('cateringMealSlot'),
    budget: document.getElementById('budget'),
    cuisine: document.getElementById('cuisine'),
    decorStyle: document.getElementById('decorStyle'),
    customNotes: document.getElementById('customNotes'),
    submitPromptBtn: document.getElementById('submitPromptBtn'),
    recommendationContent: document.getElementById('recommendationContent'),
    confirmationContent: document.getElementById('confirmationContent'),
    statusContent: document.getElementById('statusContent'),
    connectionStatus: document.getElementById('connectionStatus'),
    profileBtn: document.getElementById('profileBtn'),
    profileDrawer: document.getElementById('profileDrawer'),
    closeProfileBtn: document.getElementById('closeProfileBtn'),
    userName: document.getElementById('userName'),
    userEmail: document.getElementById('userEmail'),
    saveProfileBtn: document.getElementById('saveProfileBtn'),
    clearDataBtn: document.getElementById('clearDataBtn'),
    preferencesList: document.getElementById('preferencesList'),
    favoritesList: document.getElementById('favoritesList'),
    eventHistoryList: document.getElementById('eventHistoryList'),
    suggestionsCard: document.getElementById('suggestionsCard'),
    suggestionsContent: document.getElementById('suggestionsContent'),
    greetingText: document.getElementById('greetingText'),
    userGreeting: document.getElementById('userGreeting'),
    favToggleBtn: document.getElementById('favToggleBtn'),
    agentConsoleLogs: document.getElementById('agentConsoleLogs'),
    budgetSummaryCard: document.getElementById('budgetSummaryCard'),
    runOfShowTimeline: document.getElementById('runOfShowTimeline'),
    viewLiveStatusBtn: document.getElementById('viewLiveStatusBtn'),
    navHomeTab: document.getElementById('navHomeTab'),
    navPlanTab: document.getElementById('navPlanTab'),
    navStatusTab: document.getElementById('navStatusTab'),
    eventTypeChips: document.getElementById('eventTypeChips'),
    budgetChips: document.getElementById('budgetChips'),
    favCountBadge: document.getElementById('favCountBadge'),

    // Landing Page Elements
    landingGetStartedBtn: document.getElementById('landingGetStartedBtn'),
    landingSignInBtn: document.getElementById('landingSignInBtn'),
    landingDemoBtn: document.getElementById('landingDemoBtn'),
    bottomLandingSignUpBtn: document.getElementById('bottomLandingSignUpBtn'),
    bottomLandingDemoBtn: document.getElementById('bottomLandingDemoBtn'),
    backToLandingBtn: document.getElementById('backToLandingBtn'),
    plannerUserAvatar: document.getElementById('plannerUserAvatar'),
    plannerUserGreeting: document.getElementById('plannerUserGreeting'),

    // Authentication Elements
    authModal: document.getElementById('authModal'),
    authModalHeading: document.getElementById('authModalHeading'),
    authModalEyebrow: document.getElementById('authModalEyebrow'),
    closeAuthModalBtn: document.getElementById('closeAuthModalBtn'),
    tabSignInBtn: document.getElementById('tabSignInBtn'),
    tabSignUpBtn: document.getElementById('tabSignUpBtn'),
    signInForm: document.getElementById('signInForm'),
    signUpForm: document.getElementById('signUpForm'),
    quickDemoLoginBtn: document.getElementById('quickDemoLoginBtn'),
    topbarSignInBtn: document.getElementById('topbarSignInBtn'),
    topbarSignUpBtn: document.getElementById('topbarSignUpBtn'),
    topbarSignOutBtn: document.getElementById('topbarSignOutBtn'),
    drawerSignOutBtn: document.getElementById('drawerSignOutBtn'),
    authLoggedOutGroup: document.getElementById('authLoggedOutGroup'),
    authLoggedInGroup: document.getElementById('authLoggedInGroup'),
    userAvatarCircle: document.getElementById('userAvatarCircle'),
    userBadgeName: document.getElementById('userBadgeName'),
    userBadgeRole: document.getElementById('userBadgeRole'),
    authAlertBanner: document.getElementById('authAlertBanner'),
    // Schedule Customizer Elements
    addMilestoneBtn: document.getElementById('addMilestoneBtn'),
    saveScheduleBtn: document.getElementById('saveScheduleBtn'),
    milestoneModal: document.getElementById('milestoneModal'),
    closeMilestoneModalBtn: document.getElementById('closeMilestoneModalBtn'),
    cancelMilestoneModalBtn: document.getElementById('cancelMilestoneModalBtn'),
    milestoneForm: document.getElementById('milestoneForm'),
    milestoneTime: document.getElementById('milestoneTime'),
    milestoneCategory: document.getElementById('milestoneCategory'),
    milestoneTitle: document.getElementById('milestoneTitle'),
    milestoneDescription: document.getElementById('milestoneDescription'),
    milestoneEditIndex: document.getElementById('milestoneEditIndex'),
    milestoneModalTitle: document.getElementById('milestoneModalTitle'),
    scheduleAlertBanner: document.getElementById('scheduleAlertBanner'),
};

function getCategoryFallbackImage(category) {
    const map = {
        venue: '/static/images/venue_1.svg',
        catering: '/static/images/catering_1.svg',
        decor: '/static/images/decor_1.svg',
        photography: '/static/images/photography_1.svg',
        entertainment: '/static/images/entertainment_1.svg',
        makeup: '/static/images/makeup_1.svg',
        stay: '/static/images/venue_1.svg',
        transport: '/static/images/others_1.svg',
        cake: '/static/images/catering_1.svg',
        emcee: '/static/images/entertainment_1.svg',
        mehendi: '/static/images/makeup_1.svg',
        favors: '/static/images/others_2.svg',
        invites: '/static/images/others_2.svg',
        pyro: '/static/images/entertainment_2.svg',
        others: '/static/images/others_1.svg',
    };
    return map[category] || '/static/images/others_1.svg';
}

function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
    }
}

function showView(name) {
    // Auth gate for event planning requirements form:
    if (name === 'prompt' && (!state.auth || !state.auth.isLoggedIn)) {
        openAuthModal('signin');
        return;
    }

    Object.entries(views).forEach(([key, element]) => {
        if (element) {
            element.classList.toggle('hidden', key !== name);
            element.classList.toggle('active', key === name);
        }
    });

    if (els.navHomeTab) {
        els.navHomeTab.classList.toggle('active', name === 'landing');
    }
    if (els.navPlanTab && els.navStatusTab) {
        els.navPlanTab.classList.toggle('active', name === 'prompt' || name === 'recommendation');
        els.navStatusTab.classList.toggle('active', name === 'status' || name === 'confirmation');
    }

    setTimeout(refreshIcons, 10);
}

// LocalStorage persistence
// LocalStorage persistence & Auth State
function saveToLocalStorage() {
    localStorage.setItem('flowgenie_user', JSON.stringify(state.user));
    localStorage.setItem('flowgenie_favorites', JSON.stringify(state.favorites));
    localStorage.setItem('flowgenie_history', JSON.stringify(state.eventHistory));
    localStorage.setItem('flowgenie_preferences', JSON.stringify(state.preferences));
    if (state.eventId) localStorage.setItem('flowgenie_event_id', state.eventId);
    if (state.bookedVendors && state.bookedVendors.length) {
        localStorage.setItem('flowgenie_booked_vendors', JSON.stringify(state.bookedVendors));
    }
    if (state.auth && state.auth.token) {
        localStorage.setItem('flowgenie_auth_token', state.auth.token);
        localStorage.setItem('flowgenie_auth_user', JSON.stringify(state.auth.user));
    } else {
        localStorage.removeItem('flowgenie_auth_token');
        localStorage.removeItem('flowgenie_auth_user');
    }
}

function loadFromLocalStorage() {
    const savedUser = localStorage.getItem('flowgenie_user');
    const savedFavorites = localStorage.getItem('flowgenie_favorites');
    const savedHistory = localStorage.getItem('flowgenie_history');
    const savedPreferences = localStorage.getItem('flowgenie_preferences');
    const savedEventId = localStorage.getItem('flowgenie_event_id');
    const savedBooked = localStorage.getItem('flowgenie_booked_vendors');
    const savedToken = localStorage.getItem('flowgenie_auth_token');
    const savedAuthUser = localStorage.getItem('flowgenie_auth_user');

    if (savedUser) {
        try { state.user = JSON.parse(savedUser); } catch (e) { }
    }
    if (savedFavorites) {
        try { state.favorites = JSON.parse(savedFavorites); } catch (e) { }
    }
    if (savedHistory) {
        try { state.eventHistory = JSON.parse(savedHistory); } catch (e) { }
    }
    if (savedPreferences) {
        try { state.preferences = JSON.parse(savedPreferences); } catch (e) { }
    }
    if (savedEventId) {
        state.eventId = savedEventId;
    }
    if (savedBooked) {
        try { state.bookedVendors = JSON.parse(savedBooked); } catch (e) { }
    }
    if (savedToken && savedAuthUser) {
        try {
            state.auth.token = savedToken;
            state.auth.user = JSON.parse(savedAuthUser);
            state.auth.isLoggedIn = true;
            state.user.name = state.auth.user.name || state.user.name;
            state.user.email = state.auth.user.email || state.user.email;
        } catch (e) { }
    }
}

// Authentication Helpers & Modal Controller
function openAuthModal(tab = 'signin') {
    if (!els.authModal) return;
    els.authModal.classList.remove('hidden');
    switchAuthTab(tab);
    clearAuthAlert();
    refreshIcons();
}

function closeAuthModal() {
    if (!els.authModal) return;
    els.authModal.classList.add('hidden');
    clearAuthAlert();
}

function switchAuthTab(tab) {
    const isSignIn = tab === 'signin';
    if (els.tabSignInBtn) els.tabSignInBtn.classList.toggle('active', isSignIn);
    if (els.tabSignUpBtn) els.tabSignUpBtn.classList.toggle('active', !isSignIn);
    if (els.signInForm) els.signInForm.classList.toggle('hidden', !isSignIn);
    if (els.signUpForm) els.signUpForm.classList.toggle('hidden', isSignIn);
    if (els.authModalHeading) {
        els.authModalHeading.textContent = isSignIn ? 'Sign In to FlowGenie' : 'Create Your Account';
    }
    clearAuthAlert();
    refreshIcons();
}

function showAuthAlert(message, isError = true) {
    if (!els.authAlertBanner) return;
    els.authAlertBanner.textContent = message;
    els.authAlertBanner.classList.remove('hidden');
    els.authAlertBanner.style.background = isError ? 'var(--danger-subtle)' : 'var(--sage-subtle)';
    els.authAlertBanner.style.color = isError ? 'var(--danger)' : 'var(--sage)';
    els.authAlertBanner.style.borderColor = isError ? 'var(--danger-border)' : 'var(--sage-border)';
}

function clearAuthAlert() {
    if (!els.authAlertBanner) return;
    els.authAlertBanner.classList.add('hidden');
    els.authAlertBanner.textContent = '';
}

function updateAuthUI() {
    const loggedIn = state.auth && state.auth.isLoggedIn && state.auth.user;
    if (els.authLoggedOutGroup) els.authLoggedOutGroup.style.display = loggedIn ? 'none' : 'flex';
    if (els.authLoggedInGroup) els.authLoggedInGroup.style.display = loggedIn ? 'flex' : 'none';
    if (els.drawerSignOutBtn) els.drawerSignOutBtn.style.display = loggedIn ? 'inline-flex' : 'none';

    if (loggedIn) {
        const name = state.auth.user.name || 'User';
        const initials = name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2) || 'VIP';
        if (els.userAvatarCircle) els.userAvatarCircle.textContent = initials;
        if (els.plannerUserAvatar) els.plannerUserAvatar.textContent = initials;
        if (els.userBadgeName) els.userBadgeName.textContent = name.split(' ')[0];
        if (els.userBadgeRole) els.userBadgeRole.textContent = (state.auth.user.role || 'Host').split(' ')[0];
        if (els.greetingText) els.greetingText.textContent = `${name}`;
        if (els.userGreeting) els.userGreeting.style.display = 'inline-flex';
        if (els.plannerUserGreeting) els.plannerUserGreeting.textContent = `Welcome, ${name}!`;
    } else {
        if (els.userGreeting) els.userGreeting.style.display = 'none';
    }
    refreshIcons();
}

async function handleSignIn(e) {
    if (e) e.preventDefault();
    const emailOrPhone = document.getElementById('loginEmail')?.value.trim();
    const password = document.getElementById('loginPassword')?.value;

    if (!emailOrPhone || !password) {
        showAuthAlert('Please enter your email/phone and password.');
        return;
    }

    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email_or_phone: emailOrPhone, password: password }),
        });
        const data = await res.json();
        if (!res.ok) {
            showAuthAlert(data.detail || 'Sign in failed. Please check your credentials.');
            return;
        }

        state.auth.token = data.token;
        state.auth.user = data.user;
        state.auth.isLoggedIn = true;
        state.user.name = data.user.name;
        state.user.email = data.user.email;

        // Restore user event history if available
        if (Array.isArray(data.user.event_history) && data.user.event_history.length > 0) {
            state.eventHistory = data.user.event_history;
        }

        saveToLocalStorage();
        updateAuthUI();
        renderProfileDrawer();
        closeAuthModal();
        showView('prompt');
        showPersonalizedSuggestions();
        alert(data.message || `Welcome back, ${data.user.name}!`);
    } catch (err) {
        showAuthAlert('Network error while signing in.');
    }
}

async function handleSignUp(e) {
    if (e) e.preventDefault();
    const name = document.getElementById('signupName')?.value.trim();
    const email = document.getElementById('signupEmail')?.value.trim();
    const phone = document.getElementById('signupPhone')?.value.trim();
    const password = document.getElementById('signupPassword')?.value;
    const role = document.getElementById('signupRole')?.value || 'Host & Planner';

    if (!name || !email || !password) {
        showAuthAlert('Please fill in your name, email, and password.');
        return;
    }

    try {
        const res = await fetch('/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, password, role }),
        });
        const data = await res.json();
        if (!res.ok) {
            showAuthAlert(data.detail || 'Account registration failed.');
            return;
        }

        state.auth.token = data.token;
        state.auth.user = data.user;
        state.auth.isLoggedIn = true;
        state.user.name = data.user.name;
        state.user.email = data.user.email;

        saveToLocalStorage();
        updateAuthUI();
        renderProfileDrawer();
        closeAuthModal();
        showView('prompt');
        alert(data.message || `Account created successfully! Welcome to FlowGenie, ${name}.`);
    } catch (err) {
        showAuthAlert('Network error while creating account.');
    }
}

async function handleDemoLogin() {
    try {
        const res = await fetch('/auth/demo-login', { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error('Demo login failed');

        state.auth.token = data.token;
        state.auth.user = data.user;
        state.auth.isLoggedIn = true;
        state.user.name = data.user.name;
        state.user.email = data.user.email;

        saveToLocalStorage();
        updateAuthUI();
        renderProfileDrawer();
        closeAuthModal();
        showView('prompt');
        showPersonalizedSuggestions();
        alert('Signed in with Demo VIP Account (Ananya Roy)!');
    } catch (err) {
        showAuthAlert('Could not initiate demo login.');
    }
}

async function handleSignOut(e) {
    if (e) e.preventDefault();
    const token = (state.auth && state.auth.token) || localStorage.getItem('flowgenie_auth_token');
    if (token) {
        try {
            await fetch('/auth/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token }),
            });
        } catch (err) { }
    }

    state.auth = { token: null, user: null, isLoggedIn: false };
    state.user = { name: '', email: '' };
    localStorage.removeItem('flowgenie_auth_token');
    localStorage.removeItem('flowgenie_auth_user');
    localStorage.removeItem('flowgenie_user');
    saveToLocalStorage();
    updateAuthUI();
    updateGreeting();
    renderProfileDrawer();
    if (els.profileDrawer) els.profileDrawer.classList.add('hidden');
    showView('landing');
    alert('You have logged out successfully.');
}

async function checkAuthSession() {
    if (!state.auth.token) return;
    try {
        const res = await fetch(`/auth/me?token=${state.auth.token}`);
        if (res.ok) {
            const data = await res.json();
            state.auth.user = data.user;
            state.auth.isLoggedIn = true;
            updateAuthUI();
        } else {
            // Token expired
            state.auth = { token: null, user: null, isLoggedIn: false };
            saveToLocalStorage();
            updateAuthUI();
        }
    } catch (e) { }
}

function updateGreeting() {
    if (state.user && state.user.name) {
        if (els.greetingText) els.greetingText.textContent = `${state.user.name}`;
        if (els.userGreeting) els.userGreeting.style.display = 'inline-flex';
    } else {
        if (els.userGreeting) els.userGreeting.style.display = 'none';
    }
}

function renderProfileDrawer() {
    if (els.userName) els.userName.value = state.user.name || '';
    if (els.userEmail) els.userEmail.value = state.user.email || '';

    // Preferences
    if (els.preferencesList) {
        if (Object.keys(state.preferences).length > 0) {
            els.preferencesList.innerHTML = Object.entries(state.preferences)
                .map(([key, value]) => `<span class="tag">${key}: <strong>${value}</strong></span>`)
                .join('');
        } else {
            els.preferencesList.innerHTML = '<p style="color: var(--text-tertiary); font-size: 13px;">No preferences saved yet.</p>';
        }
    }

    // Favorites
    const favVendors = Object.values(state.favorites);
    if (els.favCountBadge) {
        els.favCountBadge.textContent = `${favVendors.length} Saved`;
    }
    if (els.favoritesList) {
        if (favVendors.length > 0) {
            els.favoritesList.innerHTML = favVendors
                .map((vendor) => `
                    <div class="favorite-item">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong>${vendor.name}</strong>
                            <span style="color: var(--amber); font-weight: 700;">${vendor.rating} ★</span>
                        </div>
                        <small>${vendor.category.toUpperCase()} • INR ${Number(vendor.price).toLocaleString()} • ${vendor.location || 'Bangalore'}</small>
                    </div>
                `)
                .join('');
        } else {
            els.favoritesList.innerHTML = '<p style="color: var(--text-tertiary); font-size: 13px;">No favorite vendors saved yet.</p>';
        }
    }

    // Event History
    if (els.eventHistoryList) {
        if (state.eventHistory.length > 0) {
            els.eventHistoryList.innerHTML = state.eventHistory
                .slice(-5)
                .reverse()
                .map((ev) => `
                    <div class="history-item">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong>${ev.type}</strong>
                            <span style="color: var(--brand-accent); font-weight: 700; font-size: 11.5px;">PLANNED</span>
                        </div>
                        <small>${ev.location} • ${ev.guests} guests • INR ${Number(ev.budget).toLocaleString()}</small>
                    </div>
                `)
                .join('');
        } else {
            els.eventHistoryList.innerHTML = '<p style="color: var(--text-tertiary); font-size: 13px;">No past event plans yet.</p>';
        }
    }
}

function showPersonalizedSuggestions() {
    if (!els.suggestionsCard || !els.suggestionsContent) return;

    if (!state.eventHistory || state.eventHistory.length === 0) {
        els.suggestionsCard.classList.add('hidden');
        return;
    }

    const recent = state.eventHistory.slice(-3);
    const commonCuisine = recent[0]?.cuisine || state.preferences['Preferred Cuisine'] || null;
    const commonDecor = recent[0]?.decor || state.preferences['Preferred Decor'] || null;
    const avgBudget = Math.round(recent.reduce((sum, e) => sum + (e.budget || 0), 0) / recent.length);

    let html = '<div class="suggestions-list">';
    if (commonCuisine) html += `<p>Food Style: <strong>${commonCuisine}</strong></p>`;
    if (commonDecor) html += `<p>Theme: <strong>${commonDecor}</strong></p>`;
    if (avgBudget) html += `<p>Avg Budget: <strong>INR ${avgBudget.toLocaleString()}</strong></p>`;
    html += '</div>';

    els.suggestionsContent.innerHTML = html;
    els.suggestionsCard.classList.remove('hidden');
}

function renderAgentLogs(logs) {
    if (!els.agentConsoleLogs) return;
    if (!logs || !logs.length) {
        els.agentConsoleLogs.innerHTML = '<p style="font-size: 13px; color: var(--text-secondary);">No extra details recorded.</p>';
        return;
    }

    els.agentConsoleLogs.innerHTML = logs
        .map((log) => `
            <div class="audit-row">
                <div class="audit-agent">${log.agent} — <span style="color: var(--brand-accent);">${log.step}</span></div>
                <div>${log.thought}</div>
                <div style="color: var(--text-primary); margin-top: 3px;"><strong>Summary:</strong> ${log.result_summary}</div>
            </div>
        `)
        .join('');
}

function renderBudgetSummary(budgetPlan) {
    if (!els.budgetSummaryCard) return;
    if (!budgetPlan || !budgetPlan.category_allocations) {
        els.budgetSummaryCard.innerHTML = '';
        return;
    }

    const cats = budgetPlan.category_allocations;
    const titles = budgetPlan.category_titles || {};
    const feasibility = budgetPlan.feasibility || {};

    const pills = Object.entries(cats)
        .map(([cat, amt]) => `<span class="cat-pill">${titles[cat] || (cat.charAt(0).toUpperCase() + cat.slice(1))}: <strong>INR ${Number(amt).toLocaleString()}</strong></span>`)
        .join('');

    els.budgetSummaryCard.innerHTML = `
        <div class="budget-stats-grid">
            <div class="budget-stat-item">
                <label>Total Budget</label>
                <value>INR ${Number(budgetPlan.total_budget || 0).toLocaleString()}</value>
            </div>
            <div class="budget-stat-item">
                <label>Guests</label>
                <value>${budgetPlan.guest_count || 50} People</value>
            </div>
            <div class="budget-stat-item">
                <label>Budget Per Guest</label>
                <value>INR ${Number(feasibility.per_guest_spend || 0).toLocaleString()}</value>
            </div>
            <div class="budget-stat-item">
                <label>Estimated Food Cost</label>
                <value style="font-size: 17px; color: var(--sage);">INR ${Number(feasibility.estimated_per_plate_catering || 0).toLocaleString()} / plate</value>
            </div>
        </div>
        <div class="category-tags-row">
            ${pills}
        </div>
    `;
}

function computeLiveTotals() {
    const selectedList = Object.values(state.selectedVendors).filter(Boolean);
    const totalSpend = selectedList.reduce((sum, v) => sum + Number(v.price || 0), 0);
    const totalBudget = Number(state.budgetPlan.total_budget || 0);
    const remaining = Math.max(totalBudget - totalSpend, 0);

    return {
        count: selectedList.length,
        totalSpend,
        remaining,
    };
}

function renderRecommendations(data) {
    state.recommendations = data.recommendations || {};
    state.agentLogs = data.agent_logs || [];
    state.budgetPlan = data.budget_plan || {};
    state.skippedCategories.clear();

    renderAgentLogs(state.agentLogs);
    renderBudgetSummary(state.budgetPlan);

    const categories = Object.entries(state.recommendations);
    if (!categories.length) {
        els.recommendationContent.innerHTML = '<p style="padding: 32px 0; color: var(--text-secondary);">No recommendations found.</p>';
        return;
    }

    // Auto-select #1 recommendation initially
    state.selectedVendors = {};
    categories.forEach(([category, vendors]) => {
        if (vendors && vendors.length > 0) {
            state.selectedVendors[category] = vendors[0];
        }
    });

    renderVendorCards();

    // Immediately render customizable hour-by-hour schedule while selecting vendors!
    renderRunOfShow(data.run_of_show || state.runOfShow || []);
}

function renderVendorCards() {
    const categories = Object.entries(state.recommendations);
    const liveStats = computeLiveTotals();

    let html = categories
        .map(([category, vendors]) => {
            let displayedVendors = vendors;
            if (state.favoritesOnlyMode) {
                displayedVendors = vendors.filter((v) => state.favorites[v.id]);
                if (!displayedVendors.length) return '';
            }

            const isCategorySkipped = state.skippedCategories.has(category);
            const selectedVendorId = state.selectedVendors[category]?.id;

            const cards = displayedVendors
                .map((vendor) => {
                    const isFavorite = !!state.favorites[vendor.id];
                    const isSelected = !isCategorySkipped && selectedVendorId === vendor.id;
                    const fallbackImg = getCategoryFallbackImage(category);

                    // Gallery thumbnails & Primary Image
                    const primaryImg = vendor.image || (vendor.gallery && vendor.gallery[0]) || fallbackImg;
                    const gallery = vendor.gallery && vendor.gallery.length > 0 ? vendor.gallery : [primaryImg];
                    const mainImage = primaryImg;

                    const thumbsHtml = gallery.length > 1 ? `
                        <div class="vendor-gallery-thumbs" id="thumbs-${vendor.id}">
                            ${gallery.map((img, idx) => `
                                <img src="${img}" onerror="this.onerror=null; this.src='${fallbackImg}';" class="gallery-thumb ${idx === 0 ? 'active' : ''}" data-target-img="main-img-${vendor.id}" data-src="${img}" alt="Photo ${idx + 1}" />
                            `).join('')}
                        </div>
                    ` : '';

                    // Key Specs
                    const specsEntries = Object.entries(vendor.specs || {}).slice(0, 4);
                    const specsHtml = specsEntries.length > 0 ? `
                        <div class="specs-preview">
                            ${specsEntries.map(([k, v]) => `
                                <div class="spec-mini-item" title="${k}: ${v}">
                                    <strong>${k}:</strong> ${v}
                                </div>
                            `).join('')}
                        </div>
                    ` : '';

                    // Services / Inclusions
                    const servicesHtml = (vendor.services_offered || [])
                        .slice(0, 3)
                        .map((s) => `<span class="service-item">${s}</span>`)
                        .join('');

                    return `
                        <div class="vendor-card ${isSelected ? 'selected-card' : ''}" id="card-${vendor.id}">
                            <div class="vendor-media-box">
                                <div class="vendor-card-img-wrap">
                                    <img src="${mainImage}" onerror="this.onerror=null; this.src='${fallbackImg}';" id="main-img-${vendor.id}" alt="${vendor.name}" class="vendor-card-img" />
                                    ${vendor.is_top_pick ? '<span class="vendor-top-badge"><i data-lucide="award" class="icon-inline"></i> Top Match</span>' : ''}
                                </div>
                                ${thumbsHtml}
                            </div>

                            <div class="vendor-card-body">
                                <div class="vendor-header-row">
                                    <h4>${vendor.name}</h4>
                                    <span class="vendor-rating-chip"><i data-lucide="star" class="icon-star-sm"></i> ${vendor.rating}</span>
                                </div>

                                ${category.toLowerCase() === 'catering' ? `
                                    <div class="meal-timing-pill" style="margin: 6px 0 10px; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); color: #B45309; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                                        <i data-lucide="sun-medium" class="icon-sm"></i> Meal Timing: ${(state.preferences && state.preferences['Catering Meal Timing']) || (els.cateringMealSlot && els.cateringMealSlot.value) || 'Night (Dinner Buffet)'}
                                    </div>
                                ` : ''}

                                ${category.toLowerCase() === 'venue' ? `
                                    <div class="event-timing-pill" style="margin: 6px 0 10px; background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.3); color: #1D4ED8; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                                        <i data-lucide="clock" class="icon-sm"></i> Event Timing: ${(state.preferences && state.preferences['Event Timing']) || (els.eventTimeSlot && els.eventTimeSlot.value) || 'Evening / Night (5:00 PM - 11:30 PM)'}
                                    </div>
                                ` : ''}
                                
                                <div class="meta-line" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                                    ${vendor.justdial_url ? `
                                        <a href="${vendor.justdial_url}" target="_blank" rel="noopener noreferrer" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;" title="View on Justdial">
                                            <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location} <span style="font-size: 11px; color: var(--brand-accent); font-weight: 600;">[Justdial ↗]</span>
                                        </a>
                                    ` : (vendor.google_maps_url ? `
                                        <a href="${vendor.google_maps_url}" target="_blank" rel="noopener noreferrer" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;" title="View on Google Maps">
                                            <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location}
                                        </a>
                                    ` : `
                                        <span style="color: var(--text-secondary); font-weight: 500;">
                                            <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location}
                                        </span>
                                    `)}
                                    <span style="font-size: 11.5px; color: var(--sage); background: var(--sage-subtle); padding: 2px 6px; border-radius: 4px; font-weight: 600;">
                                        <i data-lucide="phone" class="meta-icon"></i> ${vendor.contact || 'Verified Phone'}
                                    </span>
                                </div>
                                
                                <div class="vendor-price-tag">INR ${Number(vendor.price).toLocaleString()}</div>

                                ${vendor.why_recommended ? `
                                    <div class="why-recommended-box">
                                        <strong>Why we recommend this</strong>
                                        ${vendor.why_recommended}
                                    </div>
                                ` : ''}

                                <div class="vendor-points-box">
                                    <div class="points-label">Key Highlights</div>
                                    <ul class="vendor-points-list">
                                        ${((vendor.points && vendor.points.length > 0) ? vendor.points : [vendor.blurb || 'Verified full-service event package.'])
                                            .slice(0, 3)
                                            .map((pt) => `<li>${pt}</li>`)
                                            .join('')}
                                    </ul>
                                </div>

                                ${specsHtml}

                                ${servicesHtml ? `
                                    <div class="services-section">
                                        <div class="services-label">What's Included</div>
                                        <div class="services-list">${servicesHtml}</div>
                                    </div>
                                ` : ''}

                                <div class="card-actions">
                                    <button data-action="select" data-vendor-id="${vendor.id}" data-category="${category}" class="vendor-select-btn ${isSelected ? 'selected' : ''}">
                                        ${isSelected ? '<i data-lucide="check" class="icon-inline"></i> Selected' : 'Select'}
                                    </button>
                                    <button data-action="favorite" data-vendor-id="${vendor.id}" class="favorite-btn ${isFavorite ? 'is-fav' : ''}" title="${isFavorite ? 'Remove favorite' : 'Save favorite'}">
                                        <i data-lucide="${isFavorite ? 'bookmark-check' : 'bookmark'}" class="fav-icon-svg"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                })
                .join('');

            if (!cards && !isCategorySkipped) return '';

            let catStatus = '<span class="cat-status-badge">None chosen yet</span>';
            if (isCategorySkipped) {
                catStatus = '<span class="cat-status-badge skipped">Skipped (Not needed)</span>';
            } else if (state.selectedVendors[category]) {
                catStatus = `<span class="cat-status-badge selected">Chosen: ${state.selectedVendors[category].name}</span>`;
            }

            const catDisplayName = (state.budgetPlan && state.budgetPlan.category_titles && state.budgetPlan.category_titles[category])
                || (category.charAt(0).toUpperCase() + category.slice(1));

            return `
                <div class="category-block ${isCategorySkipped ? 'is-skipped' : ''}" id="cat-block-${category}">
                    <div class="category-header">
                        <div class="cat-title-group">
                            <h3>${catDisplayName}</h3>
                            ${catStatus}
                        </div>
                        <div>
                            <button data-action="toggle-skip" data-category="${category}" class="skip-category-btn ${isCategorySkipped ? 'is-active' : ''}">
                                ${isCategorySkipped ? '<i data-lucide="plus" class="icon-inline"></i> Include service' : '<i data-lucide="x" class="icon-inline"></i> Skip service'}
                            </button>
                        </div>
                    </div>
                    ${isCategorySkipped ? `
                        <p style="color: var(--text-tertiary); font-size: 13.5px; padding: 12px 0;">
                            This service is skipped. Click "Include this service" or select any vendor below to re-enable it.
                        </p>
                    ` : ''}
                    <div class="vendor-grid">
                        ${cards}
                    </div>
                </div>
            `;
        })
        .join('');

    if (state.favoritesOnlyMode && !html) {
        html = '<p style="color: var(--text-secondary); padding: 32px 0; text-align: center;">No favorite vendors saved yet.</p>';
    }

    els.recommendationContent.innerHTML = html + `
        <div class="approval-actions">
            <div class="live-spend-counter">
                <span>Total Selected: <strong id="liveSelectedSpend">INR ${liveStats.totalSpend.toLocaleString()}</strong></span>
                <span>Budget Remaining: <strong id="liveBudgetRemaining" style="color: #6EE7B7;">INR ${liveStats.remaining.toLocaleString()}</strong></span>
                <span id="liveSelectedCount" class="tag" style="background: rgba(255,255,255,0.15); color: white; padding: 4px 10px; border-radius: 9999px; font-size: 12px;">${liveStats.count} Selected</span>
            </div>
            <div class="action-buttons-group">
                <button id="rejectAllBtn" class="btn btn-outline">Edit Event Details</button>
                <button id="approveAllBtn" class="btn btn-primary">Confirm & Save Booking →</button>
            </div>
        </div>
    `;

    attachRecommendationHandlers();
    refreshIcons();
}

function attachRecommendationHandlers() {
    // Thumbnail switcher
    els.recommendationContent.querySelectorAll('.gallery-thumb').forEach((thumb) => {
        thumb.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = thumb.dataset.targetImg;
            const newSrc = thumb.dataset.src;
            const mainImg = document.getElementById(targetId);
            if (mainImg && newSrc) {
                mainImg.src = newSrc;
                const parentThumbs = thumb.parentElement;
                parentThumbs.querySelectorAll('.gallery-thumb').forEach((t) => t.classList.remove('active'));
                thumb.classList.add('active');
            }
        });
    });

    // Favorite handler
    els.recommendationContent.querySelectorAll('button[data-action="favorite"]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const { vendorId } = btn.dataset;
            const allVendors = Object.values(state.recommendations).flat();
            const vendor = allVendors.find((v) => v.id === vendorId);
            if (!vendor) return;

            if (state.favorites[vendorId]) {
                delete state.favorites[vendorId];
                btn.textContent = '☆';
            } else {
                state.favorites[vendorId] = vendor;
                btn.textContent = '★';
            }
            saveToLocalStorage();
            renderProfileDrawer();
        });
    });

    // Select vendor
    els.recommendationContent.querySelectorAll('button[data-action="select"]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const { vendorId, category } = btn.dataset;
            const vendor = (state.recommendations[category] || []).find((v) => v.id === vendorId);
            if (!vendor) return;

            state.skippedCategories.delete(category);

            if (state.selectedVendors[category]?.id === vendorId) {
                delete state.selectedVendors[category];
            } else {
                state.selectedVendors[category] = vendor;
            }

            renderVendorCards();
        });
    });

    // Skip category
    els.recommendationContent.querySelectorAll('button[data-action="toggle-skip"]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const { category } = btn.dataset;

            if (state.skippedCategories.has(category)) {
                state.skippedCategories.delete(category);
                const topPick = (state.recommendations[category] || [])[0];
                if (topPick) state.selectedVendors[category] = topPick;
            } else {
                state.skippedCategories.add(category);
                delete state.selectedVendors[category];
            }

            renderVendorCards();
        });
    });

    // Approve
    const approveBtn = els.recommendationContent.querySelector('#approveAllBtn');
    if (approveBtn) approveBtn.addEventListener('click', submitApproval);

    // Reject / Modify
    const rejectBtn = els.recommendationContent.querySelector('#rejectAllBtn');
    if (rejectBtn) {
        rejectBtn.addEventListener('click', () => {
            showView('prompt');
            if (els.connectionStatus) els.connectionStatus.textContent = 'Ready';
        });
    }
}

function toggleFavoritesView() {
    state.favoritesOnlyMode = !state.favoritesOnlyMode;
    if (els.favToggleBtn) {
        els.favToggleBtn.textContent = state.favoritesOnlyMode ? 'Show All' : 'Favorites Only';
    }
    renderVendorCards();
}

function renderRunOfShow(milestones) {
    if (!els.runOfShowTimeline) return;
    if (!milestones || !milestones.length) {
        els.runOfShowTimeline.innerHTML = '<p style="color: var(--text-tertiary); font-size: 13.5px;">No schedule generated.</p>';
        return;
    }

    els.runOfShowTimeline.innerHTML = milestones
        .map((m) => `
            <div class="timeline-item-row">
                <div class="timeline-time">${m.time}</div>
                <div class="timeline-details">
                    <strong>${m.title}</strong>
                    <p>${m.description}</p>
                </div>
            </div>
        `)
        .join('');
}

function renderConfirmation(data) {
    const selected = data.booking_summary?.selected || data.curated_package || [];
    const total = data.booking_summary?.total_spend || 0;
    const remaining = data.booking_summary?.budget_remaining || 0;
    state.bookedVendors = selected;

    const cardsHtml = selected
        .map((vendor) => {
            const fallbackImg = getCategoryFallbackImage(vendor.category);
            const img = vendor.image || fallbackImg;

            const servicesHtml = (vendor.services_offered || [])
                .slice(0, 3)
                .map((s) => `<span class="service-item">${s}</span>`)
                .join('');

            const specsEntries = Object.entries(vendor.specs || {}).slice(0, 4);
            const specsHtml = specsEntries.length > 0 ? `
                <div class="specs-preview" style="margin-top: 8px;">
                    ${specsEntries.map(([k, v]) => `
                        <div class="spec-mini-item" title="${k}: ${v}">
                            <strong>${k}:</strong> ${v}
                        </div>
                    `).join('')}
                </div>
            ` : '';

            const catDisplayName = (state.budgetPlan && state.budgetPlan.category_titles && state.budgetPlan.category_titles[vendor.category])
                || (vendor.category ? vendor.category.toUpperCase() : 'SERVICE');

            return `
                <div class="vendor-card">
                    <div class="vendor-card-img-wrap" style="height: 140px;">
                        <img src="${img}" onerror="this.onerror=null; this.src='${fallbackImg}';" alt="${vendor.name}" class="vendor-card-img" />
                        <span class="vendor-top-badge category-badge">${catDisplayName.toUpperCase()}</span>
                    </div>
                    <div class="vendor-card-body">
                        <div class="vendor-header-row">
                            <h4>${vendor.name}</h4>
                            <span class="vendor-rating-chip"><i data-lucide="star" class="icon-star-sm"></i> ${vendor.rating}</span>
                        </div>
                        <div class="meta-line" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                            ${vendor.justdial_url ? `
                                <a href="${vendor.justdial_url}" target="_blank" rel="noopener noreferrer" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;" title="View on Justdial">
                                    <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location} <span style="font-size: 11px; color: var(--brand-accent); font-weight: 600;">[Justdial ↗]</span>
                                </a>
                            ` : (vendor.google_maps_url ? `
                                <a href="${vendor.google_maps_url}" target="_blank" rel="noopener noreferrer" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;" title="View on Google Maps">
                                    <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location}
                                </a>
                            ` : `
                                <span style="color: var(--text-secondary); font-weight: 500;">
                                    <i data-lucide="map-pin" class="meta-icon"></i> ${vendor.location}
                                </span>
                            `)}
                            <span style="font-size: 11.5px; color: var(--sage); background: var(--sage-subtle); padding: 2px 6px; border-radius: 4px; font-weight: 600;">
                                <i data-lucide="phone" class="meta-icon"></i> ${vendor.contact || 'Verified Phone'}
                            </span>
                        </div>
                        <div class="vendor-price-tag">Cost: INR ${Number(vendor.price).toLocaleString()}</div>
                        
                        ${vendor.why_recommended ? `
                            <div class="why-recommended-box">
                                <strong>Service Details</strong>
                                ${vendor.why_recommended}
                            </div>
                        ` : ''}

                        ${specsHtml}

                        ${servicesHtml ? `
                            <div class="services-section">
                                <div class="services-label">What's Included</div>
                                <div class="services-list">${servicesHtml}</div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        })
        .join('');

    els.confirmationContent.innerHTML = `
        <div class="summary-box">
            <div class="budget-stats-grid">
                <div class="budget-stat-item">
                    <label>Total Event Cost</label>
                    <value>INR ${Number(total).toLocaleString()}</value>
                </div>
                <div class="budget-stat-item">
                    <label>Money Saved / Remaining</label>
                    <value style="color: var(--sage);">INR ${Number(remaining).toLocaleString()}</value>
                </div>
                <div class="budget-stat-item">
                    <label>Event Timing</label>
                    <value style="font-size: 15px; color: var(--brand);">${state.preferences['Event Timing'] || (els.eventTimeSlot && els.eventTimeSlot.value) || 'Evening / Night'}</value>
                </div>
                <div class="budget-stat-item">
                    <label>Catering Service</label>
                    <value style="font-size: 15px; color: #B45309;">${state.preferences['Catering Meal Timing'] || (els.cateringMealSlot && els.cateringMealSlot.value) || 'Dinner (Night)'}</value>
                </div>
            </div>

            <div style="display: flex; gap: 12px; margin-top: 14px; margin-bottom: 24px; flex-wrap: wrap;">
                <button class="btn btn-whatsapp btn-sm" id="openRfpModalBtn">
                    <span>📲</span> Send WhatsApp Briefs to All Vendors
                </button>
                <button class="btn btn-outline btn-sm" id="emailPlanBtn">
                    <span>📧</span> Email Plan to Me
                </button>
                <button class="btn btn-outline btn-sm" onclick="window.print()">
                    <span>🖨️</span> Print / Save Event Plan
                </button>
                <button class="btn btn-primary btn-sm" id="jumpToStatusBtn">
                    <span>📡</span> View Live Event Status & Sentinel
                </button>
            </div>

            <div class="vendor-grid">
                ${cardsHtml || '<p style="color: var(--text-tertiary);">No vendors selected.</p>'}
            </div>
        </div>
    `;

    const rfpBtn = document.getElementById('openRfpModalBtn');
    if (rfpBtn) rfpBtn.addEventListener('click', openRfpModal);

    const emailBtn = document.getElementById('emailPlanBtn');
    if (emailBtn) emailBtn.addEventListener('click', dispatchAllEmail);

    const jumpBtn = document.getElementById('jumpToStatusBtn');
    if (jumpBtn) {
        jumpBtn.addEventListener('click', () => {
            fetch(`/status/${state.eventId || 'evt_default'}`)
                .then((res) => res.json())
                .then((statusData) => {
                    renderStatusView(statusData);
                    showView('status');
                    loadSentinelAuditLogs(state.eventId || 'evt_default');
                });
        });
    }

    const confirmedTimelineEl = document.getElementById('confirmedTimelineList');
    if (confirmedTimelineEl) {
        const ros = (state.runOfShow && state.runOfShow.length > 0) ? state.runOfShow : (data.run_of_show || []);
        confirmedTimelineEl.innerHTML = ros
            .map((item) => {
                const cat = (item.category || 'ceremony').toLowerCase();
                return `
                    <div class="timeline-item-editable ${cat}" style="margin-bottom: 8px; padding: 12px 16px;">
                        <div style="flex: 1;">
                            <div class="timeline-meta-row">
                                <span class="timeline-time-badge"><i data-lucide="clock" class="icon-inline"></i> ${item.time || 'TBD'}</span>
                                <span class="milestone-cat-badge">${(item.category || 'Custom').toUpperCase()}</span>
                            </div>
                            <div class="timeline-item-title" style="font-size: 14px;">${item.title}</div>
                            <p class="timeline-item-desc" style="font-size: 12.5px;">${item.description || ''}</p>
                        </div>
                    </div>
                `;
            })
            .join('');
    }

    const editScheduleBtn = document.getElementById('editScheduleInConfirmBtn');
    if (editScheduleBtn) {
        editScheduleBtn.addEventListener('click', () => {
            showView('recommendation');
            const customizer = document.getElementById('scheduleCustomizerCard');
            if (customizer) customizer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    refreshIcons();
}

// ==========================================================================
// Customizable Hour-by-Hour Timeline Schedule & Traditions Engine
// ==========================================================================

function renderRunOfShow(scheduleList) {
    if (Array.isArray(scheduleList) && scheduleList.length > 0) {
        state.runOfShow = scheduleList;
    } else if (!state.runOfShow || state.runOfShow.length === 0) {
        state.runOfShow = [
            { time: "09:00 AM", title: "Venue Access & Decor Setup", description: "Stage floral installations and venue preparation.", category: "decor" },
            { time: "01:00 PM", title: "Bridal Makeup & Groom Styling", description: "Artist session and attire coordination.", category: "makeup" },
            { time: "05:30 PM", title: "Guest Welcome & Refreshments", description: "Welcome drinks and reception.", category: "catering" },
            { time: "06:30 PM", title: "Main Ceremony & Rituals", description: "Solemn customs and sacred vows.", category: "ceremony" },
            { time: "08:30 PM", title: "Grand Dinner Feast", description: "Buffet dining and celebration.", category: "catering" },
            { time: "11:00 PM", title: "Event Wrap & Departure", description: "Farewell and vendor closure.", category: "venue" },
        ];
    }

    if (!els.runOfShowTimeline) return;

    if (!state.runOfShow.length) {
        els.runOfShowTimeline.innerHTML = '<p style="color: var(--text-tertiary); padding: 24px 0; text-align: center;">No milestones in schedule yet. Click "+ Add Custom Milestone / Ritual" to create your first checkpoint.</p>';
        return;
    }

    els.runOfShowTimeline.innerHTML = state.runOfShow
        .map((item, idx) => {
            const cat = (item.category || 'ceremony').toLowerCase();
            return `
                <div class="timeline-item-editable ${cat}">
                    <div style="flex: 1;">
                        <div class="timeline-meta-row">
                            <span class="timeline-time-badge"><i data-lucide="clock" class="icon-inline"></i> ${item.time || 'TBD'}</span>
                            <span class="milestone-cat-badge">${(item.category || 'Custom').toUpperCase()}</span>
                        </div>
                        <div class="timeline-item-title">${item.title}</div>
                        <p class="timeline-item-desc">${item.description || 'Custom milestone checkpoint.'}</p>
                    </div>
                    <div class="timeline-item-actions">
                        ${idx > 0 ? `<button class="timeline-action-btn" onclick="moveMilestone(${idx}, -1)" title="Move Earlier"><i data-lucide="arrow-up" class="icon-inline"></i></button>` : ''}
                        ${idx < state.runOfShow.length - 1 ? `<button class="timeline-action-btn" onclick="moveMilestone(${idx}, 1)" title="Move Later"><i data-lucide="arrow-down" class="icon-inline"></i></button>` : ''}
                        <button class="timeline-action-btn" onclick="openEditMilestoneModal(${idx})" title="Edit Milestone"><i data-lucide="edit-2" class="icon-inline"></i> Edit</button>
                        <button class="timeline-action-btn delete" onclick="deleteMilestone(${idx})" title="Delete Milestone"><i data-lucide="trash-2" class="icon-inline"></i></button>
                    </div>
                </div>
            `;
        })
        .join('');

    refreshIcons();
}

window.openAddMilestoneModal = function () {
    if (!els.milestoneModal) return;
    if (els.milestoneEditIndex) els.milestoneEditIndex.value = '-1';
    if (els.milestoneModalTitle) els.milestoneModalTitle.textContent = 'Add Custom Milestone / Ritual';
    if (els.milestoneTime) els.milestoneTime.value = '';
    if (els.milestoneTitle) els.milestoneTitle.value = '';
    if (els.milestoneDescription) els.milestoneDescription.value = '';
    if (els.milestoneCategory) els.milestoneCategory.value = 'ceremony';
    els.milestoneModal.classList.remove('hidden');
    refreshIcons();
};

window.openEditMilestoneModal = function (idx) {
    if (!els.milestoneModal || !state.runOfShow[idx]) return;
    const item = state.runOfShow[idx];
    if (els.milestoneEditIndex) els.milestoneEditIndex.value = String(idx);
    if (els.milestoneModalTitle) els.milestoneModalTitle.textContent = 'Edit Schedule Milestone';
    if (els.milestoneTime) els.milestoneTime.value = item.time || '';
    if (els.milestoneTitle) els.milestoneTitle.value = item.title || '';
    if (els.milestoneDescription) els.milestoneDescription.value = item.description || '';
    if (els.milestoneCategory) els.milestoneCategory.value = item.category || 'ceremony';
    els.milestoneModal.classList.remove('hidden');
    refreshIcons();
};

window.closeMilestoneModal = function () {
    if (!els.milestoneModal) return;
    els.milestoneModal.classList.add('hidden');
};

window.deleteMilestone = function (idx) {
    if (confirm('Delete this milestone from your schedule?')) {
        state.runOfShow.splice(idx, 1);
        renderRunOfShow(state.runOfShow);
        saveCustomScheduleToBackend();
    }
};

window.moveMilestone = function (idx, direction) {
    const targetIdx = idx + direction;
    if (targetIdx < 0 || targetIdx >= state.runOfShow.length) return;
    const temp = state.runOfShow[idx];
    state.runOfShow[idx] = state.runOfShow[targetIdx];
    state.runOfShow[targetIdx] = temp;
    renderRunOfShow(state.runOfShow);
    saveCustomScheduleToBackend();
};

async function saveMilestoneFromModal(e) {
    if (e) e.preventDefault();
    const idx = parseInt(els.milestoneEditIndex?.value || '-1', 10);
    const time = els.milestoneTime?.value.trim() || 'TBD';
    const title = els.milestoneTitle?.value.trim();
    const description = els.milestoneDescription?.value.trim() || '';
    const category = els.milestoneCategory?.value || 'ceremony';

    if (!title) {
        alert('Please enter a milestone or tradition title.');
        return;
    }

    const milestone = { time, title, description, category };

    if (idx >= 0 && idx < state.runOfShow.length) {
        state.runOfShow[idx] = milestone;
    } else {
        state.runOfShow.push(milestone);
    }

    renderRunOfShow(state.runOfShow);
    closeMilestoneModal();
    await saveCustomScheduleToBackend();
}

async function applySchedulePreset(presetKey) {
    try {
        const res = await fetch('/schedule/presets');
        const presets = await res.json();
        const preset = presets[presetKey];
        if (preset && Array.isArray(preset.milestones)) {
            state.runOfShow = preset.milestones;
            renderRunOfShow(state.runOfShow);
            await saveCustomScheduleToBackend();
            showScheduleAlert(`Applied "${preset.name}" tradition preset! You can customize any milestone.`);
        }
    } catch (e) {
        // Fallback local preset
        renderRunOfShow();
    }
}

async function saveCustomScheduleToBackend() {
    saveToLocalStorage();
    const eventId = state.eventId || 'evt_default';

    try {
        const res = await fetch('/schedule/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: eventId,
                run_of_show: state.runOfShow,
            }),
        });
        const data = await res.json();
        showScheduleAlert(data.message || 'Hour-by-Hour Schedule updated to match your customs!');
    } catch (err) {
        console.error('Schedule save error:', err);
    }
}

function showScheduleAlert(msg) {
    if (!els.scheduleAlertBanner) return;
    els.scheduleAlertBanner.textContent = msg;
    els.scheduleAlertBanner.classList.remove('hidden');
    els.scheduleAlertBanner.style.background = 'var(--sage-subtle)';
    els.scheduleAlertBanner.style.color = 'var(--sage)';
    els.scheduleAlertBanner.style.borderColor = 'var(--sage-border)';
    setTimeout(() => {
        if (els.scheduleAlertBanner) els.scheduleAlertBanner.classList.add('hidden');
    }, 4500);
}

async function openRfpModal() {
    const modal = document.getElementById('rfpModal');
    const container = document.getElementById('rfpVendorList');
    if (!modal || !container) return;

    modal.classList.remove('hidden');
    container.innerHTML = '<p style="padding: 20px; color: var(--text-secondary);">Generating customized briefs for your suppliers...</p>';

    try {
        const response = await fetch('/notify/preview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event_id: state.eventId }),
        });
        const data = await response.json();
        const rfps = data.vendor_rfps || [];

        if (!rfps.length) {
            container.innerHTML = '<p style="color: var(--text-secondary);">No booked vendors found.</p>';
            return;
        }

        container.innerHTML = rfps
            .map((rfp) => `
                <div class="rfp-vendor-item">
                    <div class="rfp-item-header">
                        <div>
                            <h5>${rfp.vendor_name} (${rfp.category})</h5>
                            <span style="font-size: 12px; color: var(--text-tertiary);"><i data-lucide="phone" class="meta-icon"></i> ${rfp.contact}</span>
                        </div>
                        <a href="${rfp.whatsapp_url}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp btn-sm" style="text-decoration: none;">
                            <span>📲</span> Open WhatsApp Chat
                        </a>
                    </div>
                    <div class="rfp-preview-text">${rfp.message}</div>
                </div>
            `)
            .join('');
        refreshIcons();
    } catch (err) {
        container.innerHTML = '<p style="color: var(--danger);">Failed to load briefs.</p>';
    }
}

async function dispatchAllEmail() {
    const email = state.user.email || prompt('Enter your email to receive the event plan:') || 'client@example.com';
    if (!email) return;

    try {
        const response = await fetch('/notify/dispatch-all', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: state.eventId,
                client_email: email,
            }),
        });
        const res = await response.json();
        alert(res.message || 'Event plan sent to your email!');
    } catch (err) {
        alert('Could not dispatch email.');
    }
}

async function loadSentinelAuditLogs(eventId) {
    const container = document.getElementById('sentinelAuditLogList');
    if (!container) return;

    try {
        const res = await fetch(`/sentinel/audit-log/${eventId}`);
        const data = await res.json();
        const logs = data.audit_logs || [];

        if (!logs.length) {
            container.innerHTML = `
                <div class="sentinel-log-row resolved">
                    <span class="log-time">${new Date().toLocaleTimeString()}</span>
                    <span><strong>WATCHDOG_STANDBY:</strong> All 7 supplier contracts active with zero delays. Monitoring active.</span>
                </div>
            `;
            return;
        }

        container.innerHTML = logs
            .slice(-6)
            .reverse()
            .map((log) => `
                <div class="sentinel-log-row ${log.severity.toLowerCase()}">
                    <span class="log-time">${log.timestamp.slice(11, 19)}</span>
                    <div>
                        <strong>[${log.incident_type}]</strong> ${log.message}
                        <div style="font-size: 11.5px; opacity: 0.85; margin-top: 2px;">➔ <em>${log.action_taken}</em></div>
                    </div>
                </div>
            `)
            .join('');
        refreshIcons();
    } catch (err) {
        console.error(err);
    }
}

async function toggleSentinelWatchdog() {
    const badge = document.getElementById('watchdogBadge');
    const btn = document.getElementById('toggleWatchdogBtn');
    const isCurrentlyActive = badge?.textContent.includes('Active');

    try {
        const res = await fetch('/sentinel/watchdog/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: state.eventId || 'evt_default',
                enable: !isCurrentlyActive,
            }),
        });
        const data = await res.json();

        if (data.watchdog_active) {
            if (badge) {
                badge.innerHTML = '<span class="status-indicator"></span> Active';
                badge.style.background = 'var(--brand-accent-subtle)';
                badge.style.color = 'var(--brand-accent)';
            }
            if (btn) btn.textContent = 'Pause Watchdog';
        } else {
            if (badge) {
                badge.innerHTML = '<span style="width: 7px; height: 7px; background: var(--text-tertiary); border-radius: 50%;"></span> Paused';
                badge.style.background = 'var(--bg-card-warm)';
                badge.style.color = 'var(--text-tertiary)';
            }
            if (btn) btn.textContent = 'Resume Watchdog';
        }
        loadSentinelAuditLogs(state.eventId || 'evt_default');
        refreshIcons();
    } catch (err) {
        console.error(err);
    }
}

async function simulateSentinelAutoRecover() {
    if (!state.eventId) {
        alert('Please plan and save an event first.');
        return;
    }

    const category = 'catering';
    try {
        const res = await fetch('/sentinel/auto-recover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: state.eventId,
                category: category,
                reason: 'Supplier power outage simulation by Sentinel Watchdog',
            }),
        });
        const data = await res.json();
        alert(data.message || 'Auto-recovery executed.');
        loadSentinelAuditLogs(state.eventId);

        // Refresh status view
        fetch(`/status/${state.eventId}`)
            .then((r) => r.json())
            .then(renderStatusView);
    } catch (err) {
        alert('Auto recovery failed.');
    }
}

function renderStatusView(data) {
    const timeline = data.timeline || [];
    const booked = data.booked_vendors || state.bookedVendors || [];

    const timelineHtml = timeline
        .map((step) => `
            <div class="timeline-step-row">
                <span><strong>${step.step.replace(/_/g, ' ')}</strong></span>
                <span class="status-pill">${step.complete ? 'Completed' : 'Pending'}</span>
            </div>
        `)
        .join('');

    const vendorRows = booked
        .map((v) => {
            const fallbackImg = getCategoryFallbackImage(v.category);
            const img = v.image || fallbackImg;
            return `
                <div class="contingency-vendor-row">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <img src="${img}" onerror="this.onerror=null; this.src='${fallbackImg}';" style="width: 48px; height: 48px; border-radius: 8px; object-fit: cover;" />
                        <div>
                            <strong>${v.name}</strong>
                            <div class="meta-line" style="margin-bottom: 0;">${v.category.toUpperCase()} • INR ${Number(v.price).toLocaleString()}</div>
                        </div>
                    </div>
                    <button class="btn btn-outline btn-sm" data-category="${v.category}">
                        <span>⚡</span> Test: Vendor Cancels
                    </button>
                </div>
            `;
        })
        .join('');

    els.statusContent.innerHTML = `
        ${data.alert ? `<div class="alert-banner">${data.alert}</div>` : ''}
        
        <div id="replanRecommendationsContainer"></div>

        <div class="status-timeline-box">
            <h3 style="font-family: var(--font-heading); font-size: 18px; font-weight: 800; margin-bottom: 14px;">Event Status: ${data.status || 'Active'}</h3>
            <div>${timelineHtml}</div>
        </div>

        <div class="summary-box">
            <h3 style="font-family: var(--font-heading); font-size: 18px; font-weight: 800; margin-bottom: 6px;">Your Booked Vendors</h3>
            <p style="color: var(--text-secondary); font-size: 13.5px; margin-bottom: 18px;">
                Test what happens if a vendor cancels unexpectedly—we automatically search and recommend immediate backup replacements:
            </p>
            <div>${vendorRows || '<p style="color: var(--text-tertiary);">No booked vendors.</p>'}</div>
        </div>
    `;

    els.statusContent.querySelectorAll('.contingency-vendor-row button').forEach((btn) => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            simulateCancellation(category);
        });
    });

    refreshIcons();
}

function pickReplacement(category, vendorName, vendorPrice, vendorLocation, vendorImage) {
    const updatedVendor = {
        id: `${category}-replacement-${Date.now()}`,
        category: category,
        name: vendorName,
        price: Number(vendorPrice) || 50000,
        location: vendorLocation || 'Bangalore',
        image: vendorImage || getCategoryFallbackImage(category),
        rating: 4.8,
        contact: '+91 98450 12345',
        blurb: 'Verified replacement supplier confirmed.',
    };

    if (!state.bookedVendors) state.bookedVendors = [];
    const idx = state.bookedVendors.findIndex((v) => (v.category || '').toLowerCase() === category.toLowerCase());
    if (idx >= 0) {
        state.bookedVendors[idx] = updatedVendor;
    } else {
        state.bookedVendors.push(updatedVendor);
    }
    state.selectedVendors[category] = updatedVendor;
    saveToLocalStorage();

    const statusData = {
        status: 'Active (Sentinel Recovered)',
        alert: `Replacement Confirmed: Successfully switched to ${vendorName} for ${category.toUpperCase()} within budget!`,
        booked_vendors: state.bookedVendors,
        timeline: [
            { step: 'requirements_analyzed', complete: true },
            { step: 'budget_allocated', complete: true },
            { step: 'vendors_shortlisted', complete: true },
            { step: 'emergency_replan_triggered', complete: true },
            { step: 'replacement_contract_confirmed', complete: true },
        ],
    };

    renderStatusView(statusData);

    const container = document.getElementById('replanRecommendationsContainer');
    if (container) {
        container.innerHTML = `
            <div class="alert-banner" style="background: var(--sage-subtle); border: 1.5px solid var(--sage); color: var(--sage); margin-bottom: 24px; padding: 18px 22px; border-radius: 12px;">
                <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px; display: flex; align-items: center; gap: 8px;">
                    <i data-lucide="check-circle" class="icon-inline"></i> Replacement Contract Confirmed
                </div>
                <div style="font-size: 13.5px; color: var(--text-primary);">
                    Successfully booked <strong>${vendorName}</strong> (${category.toUpperCase()}) for INR ${Number(vendorPrice).toLocaleString()}. Run-of-show schedule and supplier dispatch updated.
                </div>
            </div>
        `;
        refreshIcons();
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

async function simulateCancellation(category) {
    const eventId = state.eventId || 'evt_default';
    const container = document.getElementById('replanRecommendationsContainer');

    if (container) {
        container.innerHTML = `
            <div class="suggestions-card" style="margin-bottom: 24px; border: 1.5px solid var(--amber); background: var(--bg-card); padding: 22px 24px; border-radius: var(--radius-lg); box-shadow: var(--shadow-md);">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <i data-lucide="loader-2" class="meta-icon animate-spin" style="width: 24px; height: 24px; color: var(--amber);"></i>
                    <div>
                        <h4 style="color: var(--text-primary); font-weight: 800; margin: 0; font-size: 16px;">
                            Searching Emergency Backup Suppliers for ${category.toUpperCase()}...
                        </h4>
                        <span style="font-size: 13px; color: var(--text-secondary);">
                            The Sentinel Agent is screening available verified vendors matching your budget...
                        </span>
                    </div>
                </div>
            </div>
        `;
        refreshIcons();
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (els.connectionStatus) els.connectionStatus.textContent = 'Finding Backup Vendors...';

    try {
        const response = await fetch('/replan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: eventId,
                category: category,
            }),
        });

        if (!response.ok) throw new Error('Replan failed');

        const result = await response.json();
        const replacementCategory = (result.recommendations && result.recommendations[category])
            ? result.recommendations[category]
            : (Object.values(result.recommendations || {})[0] || []);

        if (container) {
            if (!replacementCategory.length) {
                container.innerHTML = `
                    <div class="suggestions-card" style="margin-bottom: 24px; padding: 20px;">
                        <p style="color: var(--text-secondary);">No immediate replacements found for ${category}. Contacting human concierge...</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = `
                <div class="suggestions-card" style="margin-bottom: 28px; border: 1.5px solid var(--amber); background: var(--bg-card); padding: 24px; border-radius: var(--radius-lg); box-shadow: var(--shadow-md);">
                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
                        <h4 style="color: var(--text-primary); font-family: var(--font-heading); font-size: 18px; font-weight: 800;">
                            <i data-lucide="shield-alert" class="icon-inline" style="color: var(--amber);"></i> Emergency Backup Options for ${category.toUpperCase()}
                        </h4>
                        <span style="font-size: 11.5px; font-weight: 700; color: var(--amber); background: var(--amber-subtle); padding: 4px 10px; border-radius: 20px; border: 1px solid var(--amber-border);">
                            Sentinel Self-Healing
                        </span>
                    </div>
                    <p style="font-size: 13.5px; color: var(--text-secondary); margin-bottom: 20px;">
                        The previous supplier cancelled. We instantly scanned and ranked top verified replacements within your budget:
                    </p>
                    <div class="vendor-grid">
                        ${replacementCategory.map((v) => {
                            const fallbackImg = getCategoryFallbackImage(category);
                            const img = v.image || fallbackImg;
                            return `
                                <div class="vendor-card" style="border: 1px solid var(--border);">
                                    <div class="vendor-card-img-wrap" style="height: 140px;">
                                        <img src="${img}" onerror="this.onerror=null; this.src='${fallbackImg}';" alt="${v.name}" class="vendor-card-img" />
                                        <span class="vendor-top-badge backup-badge"><i data-lucide="shield-check" class="icon-inline"></i> Backup Ready</span>
                                    </div>
                                    <div class="vendor-card-body">
                                        <div class="vendor-header-row">
                                            <h4>${v.name}</h4>
                                            <span class="vendor-rating-chip"><i data-lucide="star" class="icon-star-sm"></i> ${v.rating}</span>
                                        </div>
                                        <div class="meta-line">
                                            <span><i data-lucide="map-pin" class="meta-icon"></i> ${v.location || 'Bangalore'}</span>
                                            <span style="font-size: 11px; color: var(--sage); font-weight: 600;">
                                                <i data-lucide="phone" class="meta-icon"></i> ${v.contact || 'Verified'}
                                            </span>
                                        </div>
                                        <div class="vendor-price-tag">INR ${Number(v.price).toLocaleString()}</div>
                                        <p class="vendor-blurb" style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">${v.blurb || 'Verified emergency replacement package.'}</p>
                                        <button class="btn btn-primary btn-sm full-width" data-action="pick-replacement" data-category="${category}" data-name="${v.name}" data-price="${v.price}" data-location="${v.location || 'Bangalore'}" data-img="${img}">
                                            <i data-lucide="check-circle" class="btn-icon"></i> Pick this Replacement
                                        </button>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;

            container.querySelectorAll('button[data-action="pick-replacement"]').forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const d = btn.dataset;
                    pickReplacement(d.category, d.name, d.price, d.location, d.img);
                });
            });

            refreshIcons();
            container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        if (els.connectionStatus) els.connectionStatus.textContent = 'Backup Ready';
    } catch (err) {
        console.error(err);
        if (container) {
            container.innerHTML = `
                <div class="alert-banner" style="margin-bottom: 20px;">
                    Could not fetch replacements automatically. Please check connection.
                </div>
            `;
        }
        if (els.connectionStatus) els.connectionStatus.textContent = 'Ready';
    }
}

function setupPresetChips() {
    // Event Type Chips
    document.querySelectorAll('#eventTypeChips .preset-chip').forEach((chip) => {
        chip.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('#eventTypeChips .preset-chip').forEach((c) => c.classList.remove('active'));
            chip.classList.add('active');
            const val = chip.dataset.value;
            const hiddenInput = document.getElementById('eventType');
            if (hiddenInput) hiddenInput.value = val;
        });
    });

    // Budget Chips
    document.querySelectorAll('#budgetChips .budget-chip').forEach((chip) => {
        chip.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('#budgetChips .budget-chip').forEach((c) => c.classList.remove('active'));
            chip.classList.add('active');
            const amount = chip.dataset.amount;
            const budgetInput = document.getElementById('budget');
            if (budgetInput && amount) budgetInput.value = amount;
        });
    });
}

async function submitPrompt(e) {
    if (e) e.preventDefault();

    const eventTypeEl = document.getElementById('eventType');
    const guestCountEl = document.getElementById('guestCount');
    const locationEl = document.getElementById('location');
    const eventDateEl = document.getElementById('eventDate');
    const eventTimeSlotEl = document.getElementById('eventTimeSlot');
    const eventStartTimeEl = document.getElementById('eventStartTime');
    const cateringMealSlotEl = document.getElementById('cateringMealSlot');
    const budgetEl = document.getElementById('budget');
    const cuisineEl = document.getElementById('cuisine');
    const decorStyleEl = document.getElementById('decorStyle');
    const customNotesEl = document.getElementById('customNotes');

    const activeTypeChip = document.querySelector('#eventTypeChips .preset-chip.active');

    const timeSlotVal = (eventTimeSlotEl && eventTimeSlotEl.value) || 'Evening / Night (5:00 PM - 11:30 PM)';
    const startTimeVal = (eventStartTimeEl && eventStartTimeEl.value.trim()) || '06:00 PM';
    const mealSlotVal = (cateringMealSlotEl && cateringMealSlotEl.value) || 'Night (Dinner Buffet / Reception Banquet)';

    state.preferences['Event Timing'] = timeSlotVal;
    state.preferences['Event Start Time'] = startTimeVal;
    state.preferences['Catering Meal Timing'] = mealSlotVal;
    state.preferences['Cuisine'] = (cuisineEl && cuisineEl.value) || 'Multi-Cuisine';
    const notesVal = (customNotesEl && customNotesEl.value.trim()) || '';
    if (notesVal) {
        state.preferences['Special Requirements'] = notesVal;
    }

    const payload = {
        event_type: (eventTypeEl && eventTypeEl.value) || (activeTypeChip && activeTypeChip.dataset.value) || 'Wedding',
        guest_count: Number(guestCountEl ? guestCountEl.value : 150) || 150,
        location: (locationEl && locationEl.value.trim()) || 'Bangalore',
        date: (eventDateEl && eventDateEl.value) || new Date().toISOString().slice(0, 10),
        event_time_slot: timeSlotVal,
        event_start_time: startTimeVal,
        catering_meal_slot: mealSlotVal,
        budget: Number(budgetEl ? budgetEl.value : 350000) || 350000,
        custom_notes: notesVal,
        preferences: {
            cuisine: (cuisineEl && cuisineEl.value) || 'Multi-Cuisine',
            decor_style: (decorStyleEl && decorStyleEl.value) || 'Modern',
            event_time_slot: timeSlotVal,
            event_start_time: startTimeVal,
            catering_meal_slot: mealSlotVal,
            custom_notes: notesVal,
        },
    };

    showView('loading');
    if (els.connectionStatus) els.connectionStatus.textContent = 'Finding Vendors...';

    ['step1', 'step2', 'step3', 'step4'].forEach((id) => document.getElementById(id)?.classList.remove('active'));
    document.getElementById('step1')?.classList.add('active');
    setTimeout(() => { document.getElementById('step2')?.classList.add('active'); }, 250);
    setTimeout(() => { document.getElementById('step3')?.classList.add('active'); }, 600);
    setTimeout(() => { document.getElementById('step4')?.classList.add('active'); }, 950);

    try {
        const response = await fetch('/plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error('Planning failed');

        const result = await response.json();
        state.eventId = result.event_id;

        renderRecommendations(result);
        showView('recommendation');
        if (els.connectionStatus) els.connectionStatus.textContent = 'Ready for Review';
    } catch (err) {
        console.error(err);
        alert('Could not generate recommendations.');
        showView('prompt');
        if (els.connectionStatus) els.connectionStatus.textContent = 'Ready';
    }
}

async function submitApproval() {
    const selectedList = Object.values(state.selectedVendors).filter(Boolean);
    if (!selectedList.length) {
        alert('Please select at least one vendor before confirming.');
        return;
    }

    showView('loading');
    if (els.connectionStatus) els.connectionStatus.textContent = 'Saving Your Booking...';

    try {
        const response = await fetch('/approve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: state.eventId,
                decision: 'approve',
                approved_vendors: selectedList,
                run_of_show: state.runOfShow,
            }),
        });

        if (!response.ok) throw new Error('Booking failed');

        const result = await response.json();

        const eventEntry = {
            id: state.eventId,
            type: els.eventType.value,
            guests: parseInt(els.guestCount.value),
            location: els.location.value,
            date: els.eventDate.value,
            budget: parseInt(els.budget.value),
            cuisine: els.cuisine.value,
            decor: els.decorStyle.value,
            vendors: selectedList,
            bookedDate: new Date().toISOString(),
        };
        state.eventHistory.push(eventEntry);

        state.preferences['Preferred Cuisine'] = els.cuisine.value;
        state.preferences['Preferred Decor'] = els.decorStyle.value;
        state.preferences['Typical Budget'] = `INR ${parseInt(els.budget.value).toLocaleString()}`;
        saveToLocalStorage();

        renderConfirmation(result);
        showView('confirmation');
        if (els.connectionStatus) els.connectionStatus.textContent = 'Confirmed';
    } catch (err) {
        console.error(err);
        alert('Could not confirm booking.');
        showView('recommendation');
        if (els.connectionStatus) els.connectionStatus.textContent = 'Ready';
    }
}

// Setup Event Listeners
const formElement = document.getElementById('eventForm');
if (formElement) {
    formElement.addEventListener('submit', submitPrompt);
}
const submitButton = document.getElementById('submitPromptBtn');
if (submitButton) {
    submitButton.addEventListener('click', (e) => {
        const form = document.getElementById('eventForm');
        if (form && typeof form.requestSubmit === 'function') {
            form.requestSubmit();
        } else {
            submitPrompt(e);
        }
    });
}

if (els.profileBtn && els.profileDrawer) {
    els.profileBtn.addEventListener('click', () => {
        els.profileDrawer.classList.toggle('hidden');
        renderProfileDrawer();
    });
}

if (els.closeProfileBtn && els.profileDrawer) {
    els.closeProfileBtn.addEventListener('click', () => {
        els.profileDrawer.classList.add('hidden');
    });
}

if (els.saveProfileBtn) {
    els.saveProfileBtn.addEventListener('click', () => {
        if (els.userName) state.user.name = els.userName.value.trim();
        if (els.userEmail) state.user.email = els.userEmail.value.trim();
        saveToLocalStorage();
        updateGreeting();
        renderProfileDrawer();
        alert('Profile saved.');
    });
}

if (els.clearDataBtn) {
    els.clearDataBtn.addEventListener('click', () => {
        if (confirm('Reset your saved preferences and past event plans?')) {
            state.user = { name: '', email: '' };
            state.favorites = {};
            state.eventHistory = [];
            state.preferences = {};
            localStorage.clear();
            renderProfileDrawer();
            updateGreeting();
            showPersonalizedSuggestions();
            alert('Saved data reset.');
        }
    });
}

if (els.favToggleBtn) {
    els.favToggleBtn.addEventListener('click', toggleFavoritesView);
}

if (els.viewLiveStatusBtn) {
    els.viewLiveStatusBtn.addEventListener('click', () => {
        fetch(`/status/${state.eventId || 'evt_default'}`)
            .then((res) => res.json())
            .then((data) => {
                renderStatusView(data);
                showView('status');
                loadSentinelAuditLogs(state.eventId || 'evt_default');
            });
    });
}

// Modal controls
const closeRfpModalBtn = document.getElementById('closeRfpModalBtn');
const doneRfpModalBtn = document.getElementById('doneRfpModalBtn');
const rfpModal = document.getElementById('rfpModal');
const dispatchAllEmailBtn = document.getElementById('dispatchAllEmailBtn');

if (closeRfpModalBtn && rfpModal) {
    closeRfpModalBtn.addEventListener('click', () => rfpModal.classList.add('hidden'));
}
if (doneRfpModalBtn && rfpModal) {
    doneRfpModalBtn.addEventListener('click', () => rfpModal.classList.add('hidden'));
}
if (dispatchAllEmailBtn) {
    dispatchAllEmailBtn.addEventListener('click', dispatchAllEmail);
}

// Sentinel Watchdog controls
const toggleWatchdogBtn = document.getElementById('toggleWatchdogBtn');
const simulateAutoRecoverBtn = document.getElementById('simulateAutoRecoverBtn');

if (toggleWatchdogBtn) {
    toggleWatchdogBtn.addEventListener('click', toggleSentinelWatchdog);
}
if (simulateAutoRecoverBtn) {
    simulateAutoRecoverBtn.addEventListener('click', simulateSentinelAutoRecover);
}

if (els.navPlanTab) {
    els.navPlanTab.addEventListener('click', () => showView('prompt'));
}

if (els.navStatusTab) {
    els.navStatusTab.addEventListener('click', () => {
        fetch(`/status/${state.eventId || 'evt_default'}`)
            .then((res) => res.json())
            .then((data) => {
                renderStatusView(data);
                showView('status');
                loadSentinelAuditLogs(state.eventId || 'evt_default');
            });
    });
}

// Landing Page Controls
if (els.landingGetStartedBtn) {
    els.landingGetStartedBtn.addEventListener('click', () => {
        if (state.auth && state.auth.isLoggedIn) {
            showView('prompt');
        } else {
            openAuthModal('signup');
        }
    });
}
if (els.landingSignInBtn) {
    els.landingSignInBtn.addEventListener('click', () => openAuthModal('signin'));
}
if (els.landingDemoBtn) {
    els.landingDemoBtn.addEventListener('click', handleDemoLogin);
}
if (els.bottomLandingSignUpBtn) {
    els.bottomLandingSignUpBtn.addEventListener('click', () => openAuthModal('signup'));
}
if (els.bottomLandingDemoBtn) {
    els.bottomLandingDemoBtn.addEventListener('click', handleDemoLogin);
}
if (els.backToLandingBtn) {
    els.backToLandingBtn.addEventListener('click', () => showView('landing'));
}
if (els.navHomeTab) {
    els.navHomeTab.addEventListener('click', () => showView('landing'));
}

// Auth Modal Listeners
if (els.closeAuthModalBtn) {
    els.closeAuthModalBtn.addEventListener('click', closeAuthModal);
}
if (els.tabSignInBtn) {
    els.tabSignInBtn.addEventListener('click', () => switchAuthTab('signin'));
}
if (els.tabSignUpBtn) {
    els.tabSignUpBtn.addEventListener('click', () => switchAuthTab('signup'));
}
if (els.signInForm) {
    els.signInForm.addEventListener('submit', handleSignIn);
}
if (els.signUpForm) {
    els.signUpForm.addEventListener('submit', handleSignUp);
}
if (els.quickDemoLoginBtn) {
    els.quickDemoLoginBtn.addEventListener('click', handleDemoLogin);
}
if (els.topbarSignInBtn) {
    els.topbarSignInBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openAuthModal('signin');
    });
}
if (els.topbarSignUpBtn) {
    els.topbarSignUpBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openAuthModal('signup');
    });
}

// Close auth modal when clicking background overlay
if (els.authModal) {
    els.authModal.addEventListener('click', (e) => {
        if (e.target === els.authModal) {
            closeAuthModal();
        }
    });
}

// Auth Event Listeners
if (els.topbarSignOutBtn) els.topbarSignOutBtn.addEventListener('click', handleSignOut);
if (els.drawerSignOutBtn) els.drawerSignOutBtn.addEventListener('click', handleSignOut);

// Delegated Fallback Click Listener for Log Out buttons
document.addEventListener('click', (e) => {
    const btn = e.target.closest('#topbarSignOutBtn, #drawerSignOutBtn');
    if (btn) {
        e.preventDefault();
        handleSignOut(e);
    }
});

// Schedule Customizer Listeners
if (els.addMilestoneBtn) els.addMilestoneBtn.addEventListener('click', openAddMilestoneModal);
if (els.saveScheduleBtn) els.saveScheduleBtn.addEventListener('click', saveCustomScheduleToBackend);
if (els.closeMilestoneModalBtn) els.closeMilestoneModalBtn.addEventListener('click', closeMilestoneModal);
if (els.cancelMilestoneModalBtn) els.cancelMilestoneModalBtn.addEventListener('click', closeMilestoneModal);
if (els.milestoneForm) els.milestoneForm.addEventListener('submit', saveMilestoneFromModal);

// Tradition Preset Chips
document.querySelectorAll('.schedule-preset-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
        const preset = chip.dataset.preset;
        if (preset) applySchedulePreset(preset);
    });
});

const defaultDate = new Date();
defaultDate.setDate(defaultDate.getDate() + 45);
if (els.eventDate) {
    els.eventDate.value = defaultDate.toISOString().slice(0, 10);
}

setupPresetChips();
loadFromLocalStorage();
updateAuthUI();
updateGreeting();
checkAuthSession();
showPersonalizedSuggestions();
showView(state.auth && state.auth.isLoggedIn ? 'prompt' : 'landing');
setTimeout(refreshIcons, 50);


