const API = '/api';

function getToken() { return localStorage.getItem('token'); }
function setToken(t) { localStorage.setItem('token', t); }
function removeToken() { localStorage.removeItem('token'); }
function getUser() { try { return JSON.parse(localStorage.getItem('user')); } catch { return null; } }
function setUser(u) { localStorage.setItem('user', JSON.stringify(u)); }
function removeUser() { localStorage.removeItem('user'); }

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API + path, { ...options, headers });
  if (res.status === 401) {
    removeToken(); removeUser();
    window.location.href = 'login.html';
    return;
  }
  return res;
}

function requireAuth() {
  if (!getToken()) { window.location.href = 'login.html'; }
}

function showError(elId, message) {
  const el = document.getElementById(elId);
  if (el) { el.textContent = message; el.classList.remove('hidden'); }
}

function hideError(elId) {
  const el = document.getElementById(elId);
  if (el) { el.classList.add('hidden'); }
}
