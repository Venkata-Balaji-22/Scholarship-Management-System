const apiBase = window.location.origin;
function getCookie(name){
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchWithAuth(url, options={}) {
  const token = getCookie('access_token_js');
  const headers = { 'Content-Type': 'application/json', ...(options.headers||{}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(url, {
    credentials: 'include',
    headers,
    ...options,
  });
  if (res.status === 401) {
    alert('Please login first (opens in new tab).');
    window.open(`${window.location.origin}/login`, '_blank');    throw new Error('Unauthorized');
  }
  return res;
}

document.getElementById('logoutBtn').addEventListener('click', () => {
  window.open(`${window.location.origin}/logout`, '_blank');});

document.getElementById('scholarshipForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const payload = {
    track: form.get('track'),
    tenth_cgpa: Number(form.get('tenth_cgpa')),
    inter_cgpa: form.get('inter_cgpa') ? Number(form.get('inter_cgpa')) : 0,
    btech_cgpa: form.get('btech_cgpa') ? Number(form.get('btech_cgpa')) : 0,
    family_income: form.get('family_income') ? Number(form.get('family_income')) : 999999999,
    category: form.get('category') || 'GEN',
    state: (form.get('state') || 'ALL').toUpperCase(),
    use_llm: (form.get('use_llm') === 'true')
  };
  try {
    const res = await fetchWithAuth(`${apiBase}/recommend`, { method:'POST', body: JSON.stringify(payload) });
    const data = await res.json();
    const list = document.getElementById('list');
    const llm = document.getElementById('llm');
    list.innerHTML = '';
    llm.innerHTML = '';
    if (data.llm_summary) {
      const box = document.createElement('div');
      box.className = 'card';
      box.innerHTML = `<h3>AI Summary</h3><p>${data.llm_summary}</p>`;
      llm.appendChild(box);
    }
    if (!data.matches || data.matches.length === 0) {
      list.innerHTML = '<p>No scholarships found for the provided details.</p>';
      return;
    }
    data.matches.forEach(item => {
      const posted = item.posted_at ? new Date(item.posted_at).toLocaleString() : '—';
      const card = document.createElement('div');
      card.className = 'card';
      const eligible = item.eligible === true ? '<span style="color:#34D399;font-weight:700">Eligible</span>' : '<span style="color:#FCA5A5;font-weight:700">Not Eligible</span>';
      const reasons = (item.reasons && item.reasons.length) ? `<ul>${item.reasons.map(r=>`<li>${r}</li>`).join('')}</ul>` : '';
      card.innerHTML = `<h3>${item.name}</h3>
        <p>Track: ${item.track.toUpperCase()} · ${eligible}</p>
        <p>Posted: ${posted}</p>
        ${reasons}
        <a href="${item.url}" target="_blank" rel="noopener noreferrer">Go to Application</a>`;
      list.appendChild(card);
    });
  } catch(err) {
    console.error(err);
  }
});
