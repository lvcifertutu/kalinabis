let _bosquePrevFocus = null;
let _bosqueSalud = null;
let _bosqueMapa = null;

function abrirBosque() {
  _bosquePrevFocus = document.activeElement;
  document.getElementById('panel-bosque').classList.add('open');
  cargarBosque();
}

function cerrarBosque() {
  document.getElementById('panel-bosque').classList.remove('open');
  if (_bosquePrevFocus) _bosquePrevFocus.focus();
}

document.addEventListener('keydown', function(e){
  if (e.key === 'Escape' && document.getElementById('panel-bosque').classList.contains('open')) {
    cerrarBosque();
  }
});

async function cargarBosque() {
  await Promise.all([cargarBosqueSalud(), cargarBosqueMapa()]);
}

async function cargarBosqueSalud() {
  try {
    const res = await fetchAPI('/api/bosque/salud');
    if (!res.ok) return;
    _bosqueSalud = await res.json();
    renderBosqueSalud(_bosqueSalud);
  } catch(e) { console.warn('No se pudo cargar salud del bosque:', e); }
}

function renderBosqueSalud(d) {
  document.getElementById('bosque-total').textContent      = d.total_esferas;
  document.getElementById('bosque-activas').textContent    = d.activas;
  document.getElementById('bosque-letargo').textContent    = d.en_letargo;
  document.getElementById('bosque-disolviendo').textContent= d.disolviendo;
  const amp = Math.min(1, d.promedio_amplitud || 0);
  document.getElementById('bosque-amp-fill').style.width = (amp * 100) + '%';
  document.getElementById('bosque-amp-valor').textContent = ((d.promedio_amplitud || 0) * 100).toFixed(1) + '%';
  const dist = d.distribucion_por_tipo || {};
  const distEl = document.getElementById('bosque-distribucion');
  const tipos = Object.keys(dist);
  if (!tipos.length) {
    distEl.innerHTML = '<div class="bosque-vacio">Sin esferas activas</div>';
  } else {
    distEl.innerHTML = tipos.map(t =>
      `<div class="bosque-distribucion-item">
        <span class="bosque-distribucion-tipo">${t}</span>
        <span class="bosque-distribucion-cant">${dist[t]}</span>
      </div>`).join('');
  }
  const fuertes = d.esferas_mas_fuertes || [];
  const fuertesEl = document.getElementById('bosque-fuertes');
  if (!fuertes.length) {
    fuertesEl.innerHTML = '<div class="bosque-vacio">Sin esferas todavía</div>';
  } else {
    fuertesEl.innerHTML = fuertes.map(e => `
      <div class="bosque-fuerte-item">
        <span class="bosque-fuerte-label" title="${e.label}">${e.label}</span>
        <div class="bosque-fuerte-bar"><div class="bosque-fuerte-bar-fill" style="width:${Math.min(100, (e.amplitud || 0) * 100)}%"></div></div>
        <span class="bosque-fuerte-amp">${((e.amplitud || 0) * 100).toFixed(0)}%</span>
      </div>`).join('');
  }
}

async function cargarBosqueMapa() {
  try {
    const res = await fetchAPI('/api/bosque/mapa');
    if (!res.ok) return;
    _bosqueMapa = await res.json();
    renderBosqueMapa(_bosqueMapa);
  } catch(e) { console.warn('No se pudo cargar mapa del bosque:', e); }
}

function renderBosqueMapa(d) {
  const svg = document.getElementById('bosque-mapa-svg');
  if (!svg) return;
  const COLORES = {
    geografica:'#c4824a', geo:'#c4824a', elemental:'#7aad6a',
    tematica:'#b8a0cc', resonancia:'#5a9bc4', esfera:'#c4a96a',
  };
  const nodosRaw = d.nodos || [];
  const enlaces = d.links || d.enlaces || [];
  const W = 800, H = 500;
  const cx = W / 2, cy = H / 2;
  const radio = Math.min(W, H) * 0.35;
  const nodos = nodosRaw.map((n, i) => {
    const ang = (i / Math.max(1, nodosRaw.length)) * Math.PI * 2 - Math.PI / 2;
    return { ...n, _x: nodosRaw.length === 1 ? cx : cx + Math.cos(ang) * radio, _y: nodosRaw.length === 1 ? cy : cy + Math.sin(ang) * radio };
  });
  let html = '';
  enlaces.forEach(e => {
    const origen = nodos.find(n => n.id === e.origen || n.id === e.from);
    const destino = nodos.find(n => n.id === e.destino || n.id === e.to);
    if (origen && destino) {
      const midX = (origen._x + destino._x) / 2;
      const midY = (origen._y + destino._y) / 2 - 20;
      html += `<path d="M${origen._x},${origen._y} Q${midX},${midY} ${destino._x},${destino._y}" stroke="#3d382f" stroke-width="0.8" fill="none" opacity="0.5"/>`;
    }
  });
  nodos.forEach(n => {
    const x = n._x, y = n._y;
    const amp = Math.min(1.5, n.amplitud || 0.5);
    const r = Math.max(8, Math.min(28, amp * 18));
    const color = COLORES[n.subtipo] || COLORES[n.tipo] || '#c4a96a';
    const fase = n.fase || 'activa';
    const opacidad = fase === 'activa' ? 1 : fase === 'letargo' ? 0.5 : 0.3;
    html += `<circle cx="${x}" cy="${y}" r="${r * 1.8}" fill="${color}" opacity="${opacidad * 0.08}"/>`;
    html += `<circle cx="${x}" cy="${y}" r="${r}" fill="${color}" opacity="${opacidad * 0.3}"/>`;
    html += `<circle cx="${x}" cy="${y}" r="${r * 0.5}" fill="${color}" opacity="${opacidad}"/>`;
    if (n.label) {
      html += `<text x="${x}" y="${y + r + 14}" text-anchor="middle" font-size="10" fill="#7a7060" opacity="0.85">${n.label}</text>`;
    }
  });
  if (!nodosRaw.length) {
    html = '<text x="400" y="250" text-anchor="middle" fill="#3d3830" font-family="Cinzel,serif" font-size="14">El bosque está vacío. Invoca deidades para poblarlo.</text>';
  }
  svg.innerHTML = html;
  const subtipos = [...new Set(nodosRaw.map(n => n.subtipo || n.tipo))];
  document.getElementById('bosque-leyenda').innerHTML = subtipos.map(t =>
    `<div class="bosque-leyenda-item">
      <span class="bosque-leyenda-punto" style="background:${COLORES[t] || '#c4a96a'}"></span>
      <span>${t}</span>
    </div>`).join('');
}
