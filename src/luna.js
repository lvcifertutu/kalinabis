let lunaData = null;

const DEITY_COLORS = {
  isis:'#c4824a', afrodita:'#b8a0cc', lilith:'#5a9bc4',
  artemisa:'#7aad6a', tutu:'#c4a96a', kali:'#8a7a8a'
};
const ZODIAC_SYMS = ['\u2648','\u2649','\u264A','\u264B','\u264C','\u264D','\u264E','\u264F','\u2650','\u2651','\u2652','\u2653'];
const ZODIAC_NAMES = ['Aries','Tauro','G\u00E9minis','C\u00E1ncer','Leo','Virgo','Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis'];

async function cargarLuna() {
  try {
    const res = await fetchAPI('/api/luna');
    lunaData  = await res.json();
    renderLuna(lunaData);
    setTimeout(cargarLuna, 60 * 60 * 1000);
  } catch(e) {
    document.getElementById('luna-fase-sub').textContent = 'sin conexi\u00F3n';
  }
}

function renderLuna(d) {
  const f  = d.fase;
  const s  = d.signo;
  const n  = d.nodos;
  const di = d.distancia;
  const se = d.sephirah;
  const m  = d.marea;
  const v  = d.voc;

  document.getElementById('luna-emoji').textContent      = f.emoji;
  document.getElementById('luna-fase-nombre').textContent = f.nombre;
  document.getElementById('luna-fase-sub').textContent    = 'd\u00EDa ' + f.dia_ciclo + ' \u00B7 ' + f.iluminacion + '% \u00B7 ' + f.energia;

  document.getElementById('luna-marea-fill').style.width = m.pct * 100 + '%';
  document.getElementById('luna-marea-pct').textContent  = Math.round(m.valor) + '% \u00B7 ' + m.intensidad + ' \u00B7 ' + m.direccion;

  document.getElementById('luna-signo').textContent    = s.signo + ' ' + s.simbolo + ' ' + s.grado + '\u00B0';
  document.getElementById('luna-mansion').textContent  = s.mansion_n + ' \u00B7 ' + s.mansion_nombre;
  document.getElementById('luna-rahu').textContent     = n.rahu.signo + ' ' + n.rahu.simbolo;
  document.getElementById('luna-ketu').textContent     = n.ketu.signo + ' ' + n.ketu.simbolo;
  document.getElementById('luna-distancia').textContent= di.distancia_km.toLocaleString() + ' km \u00B7 ' + di.estado;
  document.getElementById('luna-celta').textContent    = d.celta.ogham + ' \u00B7 ' + d.celta.arbol;
  document.getElementById('luna-haab').textContent     = d.haab.dia + ' ' + d.haab.mes;

  document.getElementById('luna-seph-nombre').textContent = se.nombre + ' \u00B7 ' + se.desc;
  document.getElementById('luna-seph-desc').textContent   = se.conexion;

  const vocEl = document.getElementById('luna-voc');
  if (v.activo) {
    vocEl.classList.add('activo');
    vocEl.textContent = '\u26A0 Void of Course \u00B7 ' + v.descripcion;
  }

  const eventosEl = document.getElementById('luna-eventos');
  eventosEl.innerHTML = (d.proximos || []).map(e => [
    '<div class="luna-evento">',
    '  <span class="luna-evento-emoji">' + e.emoji + '</span>',
    '  <div class="luna-evento-info">',
    '    <div class="luna-evento-nombre">' + e.nombre + '</div>',
    '    <div class="luna-evento-fecha">' + e.tema + '</div>',
    '  </div>',
    '  <div class="luna-evento-dias">' + e.fecha + '<br><span style="color:var(--dim);font-size:10px">' + e.dias + 'd</span></div>',
    '</div>',
  ].join('')).join('');

  const DEIDADES_ORD = ['isis','afrodita','lilith','artemisa','tutu','kali'];
  const mods = d.modificaciones || {};
  const modGrid = document.getElementById('luna-mod-grid');
  modGrid.innerHTML = DEIDADES_ORD.map(nombre => {
    const mod = mods[nombre] || {estado:'neutral'};
    const col = DEITY_COLORS[nombre];
    return '<div class="luna-mod-item ' + mod.estado + '" style="color:' + col + '">' +
      '<span class="luna-mod-nombre">' + nombre.toUpperCase() + '</span>' +
      '<span class="luna-mod-estado">' + mod.estado + '</span></div>';
  }).join('');

  actualizarDotsDeidades(mods);

  const tag = document.getElementById('luna-deidad-tag');
  tag.textContent = '\u263D  ' + (d.deidad_resonante || '').toUpperCase() + '  resuena hoy';
  tag.className   = 'luna-deidad-tag ' + (d.deidad_resonante || '');

  dibujarRuedaZodiacal(d);
  const hdrFase = document.getElementById('hdr-luna-fase');
  if (hdrFase) hdrFase.textContent = f.emoji;
}

function actualizarDotsDeidades(mods) {
  Object.entries(mods).forEach(([nombre, datos]) => {
    const dot = document.getElementById('amp-' + nombre);
    if (dot) {
      dot.style.color  = DEITY_COLORS[nombre];
      dot.classList.toggle('on', datos.estado === 'amplificada');
    }
  });
}

function dibujarRuedaZodiacal(d) {
  const svg    = document.getElementById('luna-rueda');
  const r      = 80;
  const rInner = 55;
  const rLuna  = 68;
  const rNodos = 74;

  let html = '';
  const COLORES_ELEM = { fire:'#c4824a22', earth:'#7aad6a22', air:'#b8a0cc22', water:'#5a9bc422' };
  const ELEMS = ['fire','earth','air','water','fire','earth','air','water','fire','earth','air','water'];

  for (let i = 0; i < 12; i++) {
    const a1 = ((i * 30 - 90) * Math.PI) / 180;
    const a2 = (((i + 1) * 30 - 90) * Math.PI) / 180;
    const x1 = Math.cos(a1) * rInner, y1 = Math.sin(a1) * rInner;
    const x2 = Math.cos(a2) * rInner, y2 = Math.sin(a2) * rInner;
    const x3 = Math.cos(a2) * r,      y3 = Math.sin(a2) * r;
    const x4 = Math.cos(a1) * r,      y4 = Math.sin(a1) * r;
    const fill = COLORES_ELEM[ELEMS[i]];
    html += '<path d="M' + x1 + ',' + y1 + ' A' + rInner + ',' + rInner + ' 0 0,1 ' + x2 + ',' + y2 + ' L' + x3 + ',' + y3 + ' A' + r + ',' + r + ' 0 0,0 ' + x4 + ',' + y4 + ' Z" fill="' + fill + '" stroke="#2e2a2533" stroke-width="0.5"/>';
    const aMid = ((i * 30 + 15 - 90) * Math.PI) / 180;
    const sx = Math.cos(aMid) * ((r + rInner) / 2);
    const sy = Math.sin(aMid) * ((r + rInner) / 2);
    html += '<text x="' + sx + '" y="' + sy + '" text-anchor="middle" dominant-baseline="middle" font-size="8" fill="#7a706088">' + ZODIAC_SYMS[i] + '</text>';
  }

  html += '<circle cx="0" cy="0" r="' + r + '" fill="none" stroke="#3d382f" stroke-width="0.8"/>';
  html += '<circle cx="0" cy="0" r="' + rInner + '" fill="none" stroke="#2e2a2544" stroke-width="0.5"/>';
  html += '<circle cx="0" cy="0" r="2" fill="#c4a96a44"/>';

  const GUARDIANS = [
    {a:-90, color:'#c4824a', sym:'\uD83D\uDD02', label:'ISIS'},
    {a:0,   color:'#b8a0cc', sym:'\uD83D\uDD01', label:'AFR'},
    {a:90,  color:'#5a9bc4', sym:'\uD83D\uDD04', label:'LIL'},
    {a:180, color:'#7aad6a', sym:'\uD83D\uDD03', label:'ART'},
  ];
  GUARDIANS.forEach(g => {
    const ar = (g.a * Math.PI) / 180;
    const gx = Math.cos(ar) * 44, gy = Math.sin(ar) * 44;
    html += '<text x="' + gx + '" y="' + gy + '" text-anchor="middle" dominant-baseline="middle" font-size="11" fill="' + g.color + '" opacity="0.7">' + g.sym + '</text>';
  });

  const lunaGrado = d.signo.grado_total;
  const lunaAng   = ((lunaGrado - 90) * Math.PI) / 180;
  const lx = Math.cos(lunaAng) * rLuna;
  const ly = Math.sin(lunaAng) * rLuna;
  const deityColor = DEITY_COLORS[d.deidad_resonante] || '#c4a96a';
  html += '<circle cx="' + lx + '" cy="' + ly + '" r="5" fill="' + deityColor + '" opacity="0.9"/>';
  html += '<circle cx="' + lx + '" cy="' + ly + '" r="8" fill="none" stroke="' + deityColor + '" stroke-width="0.8" opacity="0.4"/>';
  html += '<text x="' + lx + '" y="' + (ly - 11) + '" text-anchor="middle" font-size="8" fill="' + deityColor + '">' + d.fase.emoji + '</text>';

  const rahuGrado = d.nodos.rahu.grado;
  const rahuAng   = ((rahuGrado - 90) * Math.PI) / 180;
  const rx = Math.cos(rahuAng) * rNodos;
  const ry = Math.sin(rahuAng) * rNodos;
  html += '<text x="' + rx + '" y="' + ry + '" text-anchor="middle" dominant-baseline="middle" font-size="9" fill="#c4a96a77">\u260A</text>';

  const ketuGrado = (rahuGrado + 180) % 360;
  const ketuAng   = ((ketuGrado - 90) * Math.PI) / 180;
  const kx = Math.cos(ketuAng) * rNodos;
  const ky = Math.sin(ketuAng) * rNodos;
  html += '<text x="' + kx + '" y="' + ky + '" text-anchor="middle" dominant-baseline="middle" font-size="9" fill="#8a7a8a77">\u260B</text>';

  svg.innerHTML = html;
}

function abrirLunaModal() {
  document.getElementById('luna-modal').classList.add('open');
  if (!lunaData) cargarLuna();
}

function cerrarLunaModal() {
  document.getElementById('luna-modal').classList.remove('open');
}
