const ARCANOS_SVG = {
  0: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="45" r="12"/><path d="M50 57 L50 100"/><path d="M50 70 L32 88 M50 70 L68 88"/><path d="M50 100 L38 130 M50 100 L62 130"/><circle cx="72" cy="95" r="5"/><path d="M72 95 L80 80"/><path d="M30 38 L35 30 L40 38" /><circle cx="50" cy="20" r="3" fill="#c4a96a"/><path d="M20 135 Q50 125 80 135" stroke-width="0.7" opacity="0.4"/></g></svg>',
  1: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="40" r="11"/><path d="M50 51 L50 95"/><path d="M50 60 L30 50 M50 60 L70 50"/><path d="M30 50 L28 42 M70 50 L72 42"/><rect x="32" y="100" width="36" height="6"/><circle cx="40" cy="103" r="2" fill="#c4a96a"/><path d="M55 100 L62 96"/><path d="M50 18 Q44 12 50 8 Q56 12 50 18"/><text x="50" y="130" font-size="14" fill="#c4a96a" text-anchor="middle" stroke="none">\u221e</text></g></svg>',
  2: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="38" r="11"/><path d="M38 50 L38 110 L62 110 L62 50"/><path d="M38 50 Q50 44 62 50"/><path d="M30 60 L30 115 M70 60 L70 115"/><circle cx="50" cy="75" r="8"/><path d="M50 67 L50 83 M42 75 L58 75"/><path d="M44 25 L50 18 L56 25"/><circle cx="50" cy="14" r="3"/></g></svg>',
  3: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="38" r="11"/><path d="M35 52 Q50 46 65 52 L68 115 L32 115 Z"/><path d="M40 25 L44 18 L48 25 L52 18 L56 25 L60 18"/><circle cx="50" cy="75" r="9"/><path d="M50 66 L50 84 M41 75 L59 75 M44 69 L56 81 M56 69 L44 81" stroke-width="0.8"/><path d="M30 125 Q50 118 70 125" stroke-width="0.7" opacity="0.5"/></g></svg>',
  4: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="38" r="11"/><path d="M36 52 L64 52 L66 115 L34 115 Z"/><rect x="40" y="22" width="20" height="8"/><path d="M42 22 L44 16 M50 22 L50 14 M58 22 L56 16"/><circle cx="50" cy="80" r="7"/><path d="M30 60 L30 115 L36 115 M70 60 L70 115 L64 115"/></g></svg>',
  5: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="36" r="10"/><path d="M37 48 L63 48 L66 115 L34 115 Z"/><path d="M50 20 L50 10 M44 16 L56 16 M44 22 L56 22"/><path d="M50 55 L50 100 M42 65 L58 65 M44 78 L56 78"/><path d="M38 122 L44 116 M50 122 L50 116 M62 122 L56 116" stroke-width="0.8"/></g></svg>',
  6: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="34" cy="50" r="9"/><circle cx="66" cy="50" r="9"/><path d="M34 59 L34 100 M66 59 L66 100"/><path d="M34 70 L66 70" stroke-width="0.8"/><path d="M50 25 Q44 18 40 24 Q44 30 50 34 Q56 30 60 24 Q56 18 50 25" fill="#c4a96a" opacity="0.3"/><circle cx="50" cy="15" r="4"/><path d="M50 19 L50 28" stroke-width="0.8"/></g></svg>',
  7: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="36" r="10"/><rect x="32" y="62" width="36" height="30" rx="2"/><circle cx="38" cy="100" r="9"/><circle cx="62" cy="100" r="9"/><path d="M38 100 L38 100 M50 70 L50 84"/><path d="M40 25 L44 18 L48 25 L52 18 L56 25"/><path d="M32 70 L20 64 M68 70 L80 64"/></g></svg>',
  8: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="36" r="10"/><path d="M50 46 L50 120"/><path d="M30 60 L70 60"/><path d="M30 60 L24 75 L36 75 Z" /><path d="M70 60 L64 75 L76 75 Z"/><path d="M50 50 L58 70" stroke-width="0.8"/><path d="M44 24 L50 18 L56 24"/><path d="M40 120 L60 120"/></g></svg>',
  9: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="40" r="11"/><path d="M34 54 Q50 48 66 54 L64 118 L36 118 Z"/><circle cx="68" cy="62" r="7"/><path d="M68 55 L68 47" stroke-width="0.8"/><circle cx="68" cy="62" r="2" fill="#c4a96a"/><path d="M32 70 L32 118" /><path d="M44 30 Q50 24 56 30" stroke-width="0.8"/></g></svg>',
  10: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="80" r="32"/><circle cx="50" cy="80" r="20"/><circle cx="50" cy="80" r="4" fill="#c4a96a"/><path d="M50 48 L50 112 M18 80 L82 80 M27 57 L73 103 M73 57 L27 103" stroke-width="0.8"/><path d="M50 30 L44 38 L56 38 Z"/></g></svg>',
  11: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="42" cy="44" r="10"/><path d="M30 56 Q42 50 54 56 L52 110 L34 110 Z"/><circle cx="65" cy="80" r="14"/><path d="M58 74 L52 70 M58 86 L52 90" stroke-width="0.8"/><path d="M42 22 Q48 16 42 12 Q36 16 42 22"/><text x="42" y="28" font-size="10" fill="#c4a96a" text-anchor="middle" stroke="none">\u221e</text></g></svg>',
  12: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><path d="M20 30 L80 30 M30 30 L30 120 M70 30 L70 45"/><path d="M70 45 L62 50"/><circle cx="55" cy="62" r="9"/><path d="M55 71 L55 100"/><path d="M55 82 L42 92 M55 82 L68 92"/><path d="M55 100 L48 88 M55 100 L62 115"/><circle cx="55" cy="55" r="16" stroke-width="0.6" opacity="0.4"/></g></svg>',
  13: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="44" r="13"/><path d="M44 42 L46 46 M56 42 L54 46" stroke-width="2"/><path d="M42 50 Q50 54 58 50" /><path d="M44 50 L44 56 M50 51 L50 57 M56 50 L56 56"/><path d="M38 60 L62 60 L60 115 L40 115 Z"/><path d="M30 95 L70 78" stroke-width="0.8"/><path d="M65 72 L72 70 L70 78 Z" fill="#c4a96a" opacity="0.4"/></g></svg>',
  14: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="36" r="10"/><path d="M36 50 Q50 44 64 50 L62 112 L38 112 Z"/><path d="M30 65 L42 72 M70 80 L58 73" /><ellipse cx="28" cy="62" rx="6" ry="8"/><ellipse cx="72" cy="83" rx="6" ry="8"/><path d="M42 72 Q50 76 58 73" stroke-width="0.7" opacity="0.5"/><path d="M44 24 L50 18 L56 24"/></g></svg>',
  15: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="42" r="12"/><path d="M40 34 L34 24 M60 34 L66 24"/><path d="M44 44 L48 48 L52 44 M54 44 L56 48"/><path d="M40 54 L60 54 L58 100 L42 100 Z"/><circle cx="36" cy="115" r="6"/><circle cx="64" cy="115" r="6"/><path d="M36 109 L36 100 M64 109 L64 100" stroke-width="0.7"/><path d="M50 54 L50 100"/></g></svg>',
  16: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><path d="M38 50 L38 120 L62 120 L62 50"/><path d="M34 50 L66 50 L62 40 L38 40 Z"/><path d="M48 30 L44 18 L52 24 L50 12" stroke-width="0.9"/><circle cx="50" cy="70" r="4"/><rect x="45" y="90" width="10" height="14"/><path d="M30 60 L20 70 M70 65 L80 78" stroke-width="0.8" opacity="0.6"/><path d="M40 35 L36 28 M60 35 L64 28"/></g></svg>',
  17: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><path d="M50 18 L54 34 L70 30 L58 42 L70 52 L54 50 L50 66 L46 50 L30 52 L42 42 L30 30 L46 34 Z"/><circle cx="50" cy="42" r="3" fill="#c4a96a"/><circle cx="30" cy="80" r="9"/><circle cx="70" cy="80" r="9"/><path d="M30 89 Q50 84 70 89 L66 115 L34 115 Z"/><path d="M22 70 L26 64 M78 70 L74 64" stroke-width="0.7" opacity="0.5"/></g></svg>',
  18: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><path d="M58 22 Q40 30 40 50 Q40 70 58 78 Q46 70 46 50 Q46 30 58 22" fill="#c4a96a" opacity="0.3"/><path d="M58 22 Q40 30 40 50 Q40 70 58 78 Q46 70 46 50 Q46 30 58 22"/><path d="M30 100 L36 115 L44 100 L40 88 M56 100 L60 88 L64 100 L70 115" stroke-width="0.9"/><path d="M40 130 Q50 124 60 130" stroke-width="0.7"/><circle cx="28" cy="60" r="2" fill="#c4a96a"/><circle cx="72" cy="68" r="2" fill="#c4a96a"/></g></svg>',
  19: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><circle cx="50" cy="50" r="20"/><circle cx="50" cy="50" r="4" fill="#c4a96a"/><path d="M50 20 L50 10 M50 80 L50 90 M20 50 L10 50 M80 50 L90 50 M29 29 L22 22 M71 29 L78 22 M29 71 L22 78 M71 71 L78 78" stroke-width="0.9"/><path d="M38 105 Q50 100 62 105 L60 125 L40 125 Z"/></g></svg>',
  20: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><path d="M40 20 Q50 14 60 20 L60 26 L40 26 Z"/><path d="M50 26 L50 44" /><circle cx="50" cy="30" r="3" fill="#c4a96a" opacity="0.5"/><circle cx="50" cy="58" r="10"/><path d="M36 72 Q50 66 64 72 L62 115 L38 115 Z"/><path d="M30 80 L24 88 M70 80 L76 88" stroke-width="0.7" opacity="0.5"/><path d="M42 44 L58 44" stroke-width="0.8"/></g></svg>',
  21: '<svg viewBox="0 0 100 160"><g fill="none" stroke="#c4a96a" stroke-width="1.3" opacity="0.85"><ellipse cx="50" cy="75" rx="26" ry="42"/><circle cx="50" cy="75" r="9"/><path d="M50 66 L50 84 M41 75 L59 75" stroke-width="0.8"/><path d="M28 40 L22 32 M72 40 L78 32 M28 110 L22 118 M72 110 L78 118" stroke-width="0.8"/><circle cx="22" cy="30" r="2" fill="#c4a96a"/><circle cx="78" cy="30" r="2" fill="#c4a96a"/><circle cx="22" cy="120" r="2" fill="#c4a96a"/><circle cx="78" cy="120" r="2" fill="#c4a96a"/></g></svg>',
};

let arcanosData = [];
let posicionesData = [];
let tiradaActual = [];
let entropia = 0;
let entropiaPool = [];

async function abrirTarot() {
  document.getElementById('camara-tarot').classList.add('open');
  document.getElementById('tarot-deidad-nombre').textContent = selectedDeidad.charAt(0).toUpperCase() + selectedDeidad.slice(1);
  if (!arcanosData.length) {
    try {
      const res = await fetchAPI('/api/tarot/arcanos');
      const d = await res.json();
      arcanosData = d.arcanos;
      posicionesData = d.posiciones;
    } catch(e) {}
  }
  if (lunaData) {
    const f = lunaData.fase, s = lunaData.signo;
    document.getElementById('tarot-luna-info').textContent = f.emoji + ' ' + f.nombre + ' \u00B7 Luna en ' + s.signo + ' ' + s.simbolo + ' \u00B7 ' + f.energia;
  }
  actualizarEstadoNatal();
  nuevaTirada();
}

function cerrarTarot() {
  document.getElementById('camara-tarot').classList.remove('open');
}

function construirMazo() {
  const mazo = document.getElementById('tarot-mazo');
  mazo.innerHTML = '';
  entropia = 0; entropiaPool = [];
  document.getElementById('tarot-entropia-val').textContent = '0';
  for (let i=0; i<7; i++) {
    const carta = document.createElement('div');
    carta.className = 'mazo-carta';
    const ang = (i - 3) * 8;
    const x = (i - 3) * 38;
    carta.style.transform = 'translateX(' + x + 'px) rotate(' + ang + 'deg)';
    carta.onmousemove = (e) => sembrarEntropia(e, carta, x, ang);
    mazo.appendChild(carta);
  }
}

function sembrarEntropia(e, carta, baseX, baseAng) {
  entropiaPool.push((e.clientX * 31 + e.clientY * 17 + performance.now()) % 997);
  if (entropiaPool.length > 200) entropiaPool.shift();
  entropia = Math.min(100, Math.floor(entropiaPool.length / 2));
  document.getElementById('tarot-entropia-val').textContent = entropia;
  carta.style.transform = 'translateX(' + baseX + 'px) rotate(' + baseAng + 'deg) translateY(-12px)';
  clearTimeout(carta._t);
  carta._t = setTimeout(() => {
    carta.style.transform = 'translateX(' + baseX + 'px) rotate(' + baseAng + 'deg)';
  }, 200);
  if (sonidoOn && Math.random() < 0.04) campanilla();
}

function azarReal(max) {
  const buf = new Uint32Array(1);
  crypto.getRandomValues(buf);
  const semilla = entropiaPool.reduce((a,b) => (a + b) % 999983, 0);
  return (buf[0] ^ Math.floor(semilla * 7919)) % max;
}

function extraerTirada() {
  const indices = [...Array(22).keys()];
  for (let i = indices.length - 1; i > 0; i--) {
    const j = azarReal(i + 1);
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }
  tiradaActual = [];
  for (let p = 0; p < 3; p++) {
    const n = indices[p];
    tiradaActual.push({ n, invertida: false, posicion: p });
  }
  mostrarTirada();
}

function mostrarTirada() {
  document.getElementById('tarot-fase-barajar').style.display = 'none';
  document.getElementById('tarot-fase-tirada').style.display = 'flex';
  document.getElementById('tarot-lectura').textContent = '';
  document.getElementById('tarot-btn-leer').style.display = 'none';
  const cont = document.getElementById('tarot-tirada');
  cont.innerHTML = '';
  tiradaActual.forEach((c, idx) => {
    const pos = posicionesData[c.posicion];
    const wrap = document.createElement('div');
    wrap.className = 'tarot-carta-pos';
    wrap.innerHTML = [
      '<div class="tarot-pos-label">' + pos.nombre + '</div>',
      '<div class="tarot-carta" id="carta-' + idx + '" onclick="revelarCarta(' + idx + ')">',
      '  <div class="tarot-carta-cara tarot-carta-dorso"></div>',
      '  <div class="tarot-carta-cara tarot-carta-frente" id="frente-' + idx + '"></div>',
      '</div>',
      '<div class="tarot-carta-sig" id="sig-' + idx + '"></div>',
    ].join('');
    cont.appendChild(wrap);
  });
}

function revelarCarta(idx) {
  const c = tiradaActual[idx];
  if (c.revelada) return;
  c.revelada = true;
  const arc = arcanosData.find(a => a.n === c.n);
  const frente = document.getElementById('frente-' + idx);
  const svg = ARCANOS_SVG[c.n] || '';
  frente.className = 'tarot-carta-cara tarot-carta-frente';
  frente.innerHTML = '<div class="carta-svg">' + svg + '</div><div class="carta-nombre">' + arc.n + ' \u00B7 ' + arc.nombre + '</div>';
  document.getElementById('carta-' + idx).classList.add('revelada');
  if (sonidoOn) campanilla();
  setTimeout(() => {
    const sigEl = document.getElementById('sig-' + idx);
    sigEl.textContent = arc.derecho;
    sigEl.classList.add('visible');
  }, 500);
  if (tiradaActual.every(t => t.revelada)) {
    setTimeout(() => {
      document.getElementById('tarot-btn-leer').style.display = 'inline-block';
    }, 700);
  }
}

async function pedirLecturaDeidad() {
  const lectura = document.getElementById('tarot-lectura');
  lectura.style.color = DEIDADES_META[selectedDeidad].color;
  lectura.textContent = 'La deidad contempla la tirada...';
  try {
    const res = await fetchAPI('/api/tarot/leer/' + selectedDeidad, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ cartas: tiradaActual }),
    });
    const d = await res.json();
    lectura.textContent = d.respuesta || 'El humo se dispersa.';
    if (sonidoOn) campanilla();
  } catch(e) {
    lectura.textContent = 'El humo se dispersa. Intenta de nuevo.';
  }
}

function nuevaTirada() {
  tiradaActual = [];
  document.getElementById('tarot-fase-tirada').style.display = 'none';
  document.getElementById('tarot-fase-barajar').style.display = 'flex';
  construirMazo();
}

async function abrirNatalModal() {
  document.getElementById('natal-modal').classList.add('open');
  const sel = document.getElementById('natal-ciudad');
  if (sel.options.length === 0) {
    try {
      const res = await fetchAPI('/api/astral/ciudades');
      const d = await res.json();
      sel.innerHTML = '<option value="">\u2014 elige una ciudad \u2014</option>';
      Object.keys(d.ciudades).forEach(nombre => {
        const o = document.createElement('option');
        o.value = nombre;
        o.textContent = nombre;
        o.dataset.lat = d.ciudades[nombre].lat;
        o.dataset.lng = d.ciudades[nombre].lng;
        o.dataset.tz = d.ciudades[nombre].tz;
        sel.appendChild(o);
      });
      const manual = document.createElement('option');
      manual.value = '__manual__';
      manual.textContent = 'Otro lugar (coordenadas manuales)';
      sel.appendChild(manual);
    } catch(e) {}
  }
  cargarNatalGuardada();
}

function cerrarNatalModal() {
  document.getElementById('natal-modal').classList.remove('open');
}

function onCiudadChange() {
  const sel = document.getElementById('natal-ciudad');
  const manual = document.getElementById('natal-manual');
  manual.style.display = sel.value === '__manual__' ? 'block' : 'none';
}

async function calcularNatal() {
  const sel = document.getElementById('natal-ciudad');
  let lat, lng, tz, lugar;
  if (sel.value === '__manual__') {
    lat = parseFloat(document.getElementById('natal-lat').value);
    lng = parseFloat(document.getElementById('natal-lng').value);
    tz  = document.getElementById('natal-tz').value.trim();
    lugar = lat + ', ' + lng;
  } else if (sel.value) {
    const o = sel.selectedOptions[0];
    lat = parseFloat(o.dataset.lat);
    lng = parseFloat(o.dataset.lng);
    tz  = o.dataset.tz;
    lugar = sel.value;
  } else {
    document.getElementById('natal-resultado').innerHTML = '<div style="color:var(--isis);text-align:center;font-style:italic">Elige un lugar de nacimiento.</div>';
    return;
  }
  const payload = {
    nombre: document.getElementById('natal-nombre').value || 'Consultante',
    dia:  parseInt(document.getElementById('natal-dia').value),
    mes:  parseInt(document.getElementById('natal-mes').value),
    anio: parseInt(document.getElementById('natal-anio').value),
    hora: parseInt(document.getElementById('natal-hora').value),
    minuto: parseInt(document.getElementById('natal-minuto').value),
    lat, lng, tz, lugar,
  };
  if (!payload.dia || !payload.mes || !payload.anio || isNaN(payload.hora) || isNaN(payload.minuto)) {
    document.getElementById('natal-resultado').innerHTML = '<div style="color:var(--isis);text-align:center;font-style:italic">Completa la fecha y hora.</div>';
    return;
  }
  document.getElementById('natal-resultado').innerHTML = '<div style="text-align:center;color:var(--muted);font-style:italic">Calculando el cielo de ese momento...</div>';
  try {
    const res = await fetchAPI('/api/astral/calcular', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload),
    });
    const d = await res.json();
    if (d.error) {
      document.getElementById('natal-resultado').innerHTML = '<div style="color:var(--isis);text-align:center">' + d.error + '</div>';
      return;
    }
    renderNatal(d);
    actualizarEstadoNatal();
  } catch(e) {
    document.getElementById('natal-resultado').innerHTML = '<div style="color:var(--isis);text-align:center">Error al calcular.</div>';
  }
}

function renderNatal(d) {
  let html = '<div class="natal-res-cabecera">\u2609 Sol en ' + d.sol + ' \u00B7 \u263D Luna en ' + d.luna + '<br>\u2191 Ascendente ' + d.asc + '</div>';
  Object.values(d.planetas).forEach(p => {
    html += '<div class="natal-planeta"><span class="natal-planeta-nombre">' + p.simbolo + ' ' + p.nombre + '</span><span class="natal-planeta-pos">' + p.signo + ' ' + p.grado + '\u00B0' + (p.casa ? ' \u00B7 casa '+p.casa : '') + (p.retro ? ' R' : '') + '</span></div>';
  });
  document.getElementById('natal-resultado').innerHTML = html;
}

async function cargarNatalGuardada() {
  try {
    const res = await fetchAPI('/api/astral/guardada');
    const d = await res.json();
    if (d.existe && d.datos && d.datos.planetas) {
      renderNatal(d.datos);
    }
  } catch(e) {}
}

async function actualizarEstadoNatal() {
  try {
    const res = await fetchAPI('/api/astral/guardada');
    const d = await res.json();
    const btn = document.querySelector('.tarot-natal-btn');
    if (d.existe) {
      btn.classList.add('activa');
      btn.textContent = '\u2726 ' + d.nombre + ' \u00B7 \u2609' + d.datos.sol;
    }
  } catch(e) {}
}
