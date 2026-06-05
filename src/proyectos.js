async function initProyecto() {
  proyectoCodigo = localStorage.getItem('kalinabis_codigo');
  if (proyectoCodigo) {
    try {
      const res = await fetch('/api/proyecto/verificar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Project-Code': proyectoCodigo },
      });
      const data = await res.json();
      if (!data.existe) { proyectoCodigo = null; localStorage.removeItem('kalinabis_codigo'); }
    } catch(e) { /* mantener código existente y reintentar */ }
  }
  if (!proyectoCodigo) {
    try {
      const res = await fetch('/api/proyecto/nuevo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      if (data.ok && data.codigo) {
        proyectoCodigo = data.codigo;
        localStorage.setItem('kalinabis_codigo', proyectoCodigo);
      }
    } catch(e) { console.warn('No se pudo crear proyecto:', e.message); }
  }
  mostrarCodigoProyecto();
}

function mostrarCodigoProyecto() {
  const el = document.getElementById('project-code-display');
  if (el && proyectoCodigo) {
    el.textContent = proyectoCodigo;
    el.title = 'Tu código de proyecto — guárdalo para no perder tu acceso';
  }
}

function copiarCodigo() {
  if (!proyectoCodigo) return;
  navigator.clipboard.writeText(proyectoCodigo).then(() => {
    const el = document.getElementById('project-code-display');
    if (el) { el.style.background = 'var(--artemisa)'; setTimeout(() => el.style.background = '', 800); }
  });
}

async function fetchAPI(url, options = {}) {
  const headers = { ...options.headers };
  if (proyectoCodigo) headers['X-Project-Code'] = proyectoCodigo;
  if (options.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json';
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    proyectoCodigo = null;
    localStorage.removeItem('kalinabis_codigo');
    await initProyecto();
    headers['X-Project-Code'] = proyectoCodigo;
    return fetch(url, { ...options, headers });
  }
  return response;
}
