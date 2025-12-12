export const API_URL = 'http://localhost:8000/api';

export async function fetchDashboardStats() {
  const res = await fetch(`${API_URL}/dashboard/stats`);
  if (!res.ok) {
    throw new Error('Failed to fetch stats');
  }
  return res.json();
}

export async function fetchRecentCalls() {
  const res = await fetch(`${API_URL}/dashboard/calls`);
  if (!res.ok) {
    throw new Error('Failed to fetch calls');
  }
  return res.json();
}

export async function fetchScripts() {
    const res = await fetch(`${API_URL}/scripts`);
    if (!res.ok) {
      throw new Error('Failed to fetch scripts');
    }
    return res.json();
  }
