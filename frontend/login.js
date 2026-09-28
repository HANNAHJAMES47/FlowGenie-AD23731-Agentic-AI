/**
 * Standalone Login & Account Creation Controller for FlowGenie.
 */

function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
    }
}

const tabSignInBtn = document.getElementById('tabSignInBtn');
const tabSignUpBtn = document.getElementById('tabSignUpBtn');
const signInForm = document.getElementById('signInForm');
const signUpForm = document.getElementById('signUpForm');
const authAlertBanner = document.getElementById('authAlertBanner');
const authPageTitle = document.getElementById('authPageTitle');
const authPageSubtitle = document.getElementById('authPageSubtitle');
const authModeLabel = document.getElementById('authModeLabel');
const quickDemoLoginBtn = document.getElementById('quickDemoLoginBtn');

function switchTab(tab) {
    const isSignIn = tab === 'signin';
    if (tabSignInBtn) tabSignInBtn.classList.toggle('active', isSignIn);
    if (tabSignUpBtn) tabSignUpBtn.classList.toggle('active', !isSignIn);
    if (signInForm) signInForm.classList.toggle('hidden', !isSignIn);
    if (signUpForm) signUpForm.classList.toggle('hidden', isSignIn);

    if (authPageTitle) {
        authPageTitle.textContent = isSignIn ? 'Sign In to Your Account' : 'Create Your FlowGenie Account';
    }
    if (authPageSubtitle) {
        authPageSubtitle.textContent = isSignIn
            ? 'Access your saved event plans and vendor packages.'
            : 'Start orchestrating your event with 5 autonomous AI agents.';
    }
    if (authModeLabel) {
        authModeLabel.textContent = isSignIn ? 'WELCOME BACK' : 'GET STARTED';
    }

    clearAlert();
    refreshIcons();
}

function showAlert(message, isError = true) {
    if (!authAlertBanner) return;
    authAlertBanner.textContent = message;
    authAlertBanner.classList.remove('hidden');
    authAlertBanner.style.background = isError ? 'var(--danger-subtle)' : 'var(--sage-subtle)';
    authAlertBanner.style.color = isError ? 'var(--danger)' : 'var(--sage)';
    authAlertBanner.style.borderColor = isError ? 'var(--danger-border)' : 'var(--sage-border)';
}

function clearAlert() {
    if (!authAlertBanner) return;
    authAlertBanner.classList.add('hidden');
    authAlertBanner.textContent = '';
}

async function handleSignIn(e) {
    if (e) e.preventDefault();
    const emailOrPhone = document.getElementById('loginEmail')?.value.trim();
    const password = document.getElementById('loginPassword')?.value;

    if (!emailOrPhone || !password) {
        showAlert('Please enter your email/phone and password.');
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
            showAlert(data.detail || 'Sign in failed. Please check your credentials.');
            return;
        }

        // Store session in localStorage
        localStorage.setItem('flowgenie_auth_token', data.token);
        localStorage.setItem('flowgenie_auth_user', JSON.stringify(data.user));
        localStorage.setItem('flowgenie_user', JSON.stringify({ name: data.user.name, email: data.user.email }));

        if (Array.isArray(data.user.event_history) && data.user.event_history.length > 0) {
            localStorage.setItem('flowgenie_history', JSON.stringify(data.user.event_history));
        }

        showAlert(`Welcome back, ${data.user.name}! Redirecting to event planner...`, false);
        setTimeout(() => {
            window.location.href = '/';
        }, 600);
    } catch (err) {
        showAlert('Network error while signing in.');
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
        showAlert('Please fill in your name, email, and password.');
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
            showAlert(data.detail || 'Account registration failed.');
            return;
        }

        localStorage.setItem('flowgenie_auth_token', data.token);
        localStorage.setItem('flowgenie_auth_user', JSON.stringify(data.user));
        localStorage.setItem('flowgenie_user', JSON.stringify({ name: data.user.name, email: data.user.email }));

        showAlert(`Account created successfully! Welcome to FlowGenie, ${name}. Redirecting...`, false);
        setTimeout(() => {
            window.location.href = '/';
        }, 600);
    } catch (err) {
        showAlert('Network error while creating account.');
    }
}

async function handleDemoLogin() {
    try {
        const res = await fetch('/auth/demo-login', { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error('Demo login failed');

        localStorage.setItem('flowgenie_auth_token', data.token);
        localStorage.setItem('flowgenie_auth_user', JSON.stringify(data.user));
        localStorage.setItem('flowgenie_user', JSON.stringify({ name: data.user.name, email: data.user.email }));

        showAlert('Signed in as VIP Demo Planner (Ananya Roy)! Redirecting...', false);
        setTimeout(() => {
            window.location.href = '/';
        }, 500);
    } catch (err) {
        showAlert('Could not initiate demo login.');
    }
}

// Event Listeners
if (tabSignInBtn) tabSignInBtn.addEventListener('click', () => switchTab('signin'));
if (tabSignUpBtn) tabSignUpBtn.addEventListener('click', () => switchTab('signup'));
if (signInForm) signInForm.addEventListener('submit', handleSignIn);
if (signUpForm) signUpForm.addEventListener('submit', handleSignUp);
if (quickDemoLoginBtn) quickDemoLoginBtn.addEventListener('click', handleDemoLogin);

// Check URL param ?mode=signup or ?mode=signin
const urlParams = new URLSearchParams(window.location.search);
const modeParam = urlParams.get('mode') || 'signin';
switchTab(modeParam);
setTimeout(refreshIcons, 50);
