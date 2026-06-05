let _modalPrevFocus = null;

function openModal() {
  _modalPrevFocus = document.activeElement;
  document.getElementById('modal').classList.add('open');
  cargarGrimorio();
  cargarDecisiones();
  setTimeout(() => {
    const firstTab = document.querySelector('.grimorio-tab');
    if (firstTab) firstTab.focus();
  }, 50);
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  if (_modalPrevFocus) _modalPrevFocus.focus();
}

document.getElementById('modal').addEventListener('click', function(e){ if(e.target===this) closeModal(); });
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape' && document.getElementById('modal').classList.contains('open')) closeModal();
});

document.getElementById('modal').addEventListener('keydown', function(e){
  if (e.key !== 'Tab') return;
  const focusables = this.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  if (!focusables.length) return;
  const first = focusables[0], last = focusables[focusables.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

function grimorioTab(tab, btn) {
  document.querySelectorAll('.grimorio-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.grimorio-panel').forEach(p => p.style.display = 'none');
  document.getElementById(`grimorio-${tab}`).style.display = '';
}

async function cargarGrimorio() {
  const el = document.getElementById('grimorio-lista');
  el.innerHTML = '<div class="grimorio-vacio">Cargando...</div>';
  try {
    const res = await fetchAPI('/api/grimorio');
    const datos = await res.json();
    if (!datos.length) { el.innerHTML = '<div class="grimorio-vacio">El grimorio está vacío. Escribe tu primera entrada.</div>'; return; }
    const COLORES = { isis:'var(--isis)', afrodita:'var(--afrodita)', lilith:'var(--lilith)', artemisa:'var(--artemisa)', tutu:'var(--tutu)', kali:'var(--kali)' };
    el.innerHTML = datos.map(e => {
      const col = e.entidad ? (COLORES[e.entidad] || 'var(--muted)') : 'var(--dim)';
      const entidadTag = e.entidad ? `<span class="grimorio-item-entidad" style="border:1px solid ${col};color:${col}">${e.entidad}</span>` : '';
      const fecha = e.timestamp ? new Date(e.timestamp).toLocaleDateString('es',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}) : '';
      return `<div class="grimorio-item">
        <div class="grimorio-item-titulo">${e.titulo || 'Sin título'}</div>
        <div class="grimorio-item-meta">${entidadTag}<span>${e.tipo || 'entrada'}</span> · ${fecha}</div>
        <div class="grimorio-item-contenido">${(e.contenido || '').substring(0,200)}${e.contenido && e.contenido.length > 200 ? '...' : ''}</div>
      </div>`;
    }).join('');
  } catch(e) { el.innerHTML = '<div class="grimorio-vacio">Error al cargar.</div>'; }
}

async function cargarDecisiones() {
  const el = document.getElementById('decisiones-lista');
  el.innerHTML = '<div class="grimorio-vacio">Cargando...</div>';
  try {
    const res = await fetchAPI('/api/decisiones');
    const datos = await res.json();
    if (!datos.length) { el.innerHTML = '<div class="grimorio-vacio">Aún no hay decisiones registradas.</div>'; return; }
    const COLORES = { isis:'var(--isis)', afrodita:'var(--afrodita)', lilith:'var(--lilith)', artemisa:'var(--artemisa)', tutu:'var(--tutu)', kali:'var(--kali)' };
    el.innerHTML = datos.map(d => {
      const col = COLORES[d.entidad] || 'var(--muted)';
      const fecha = d.timestamp ? new Date(d.timestamp).toLocaleDateString('es',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}) : '';
      return `<div class="decision-item" style="border-left-color:${col}">
        <div class="decision-item-entidad" style="color:${col}">${(d.entidad||'?').toUpperCase()} · ${d.modo||''}</div>
        <div class="decision-item-razon">${d.razon || ''}</div>
        <div class="decision-item-meta">${d.mensaje ? '"' + d.mensaje.substring(0,60) + '"...' : ''} · ${fecha}</div>
      </div>`;
    }).join('');
  } catch(e) { el.innerHTML = '<div class="grimorio-vacio">Error al cargar.</div>'; }
}

async function guardarEntrada() {
  const titulo = document.getElementById('m-titulo').value.trim();
  const contenido = document.getElementById('m-contenido').value.trim();
  const tipo = document.getElementById('m-tipo').value;
  const entidad = document.getElementById('m-entidad').value;
  if (!titulo || !contenido) { mostrarToast('Escribe un título y contenido', 'error'); return; }
  try {
    await fetchAPI('/api/grimorio', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ titulo, contenido, entidad: entidad || null, tipo }),
    });
    document.getElementById('m-titulo').value = '';
    document.getElementById('m-contenido').value = '';
    mostrarToast('Entrada guardada en el grimorio', 'success');
    grimorioTab('entradas', document.querySelector('.grimorio-tab'));
    cargarGrimorio();
  } catch(e) { mostrarToast('Error al guardar', 'error'); }
}
