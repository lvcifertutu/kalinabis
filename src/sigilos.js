const SIGILOS_DEIDAD = {
  isis: '<svg viewBox="0 0 200 200"><g fill="none" stroke="#c4824a" stroke-width="2">\n    <circle cx="100" cy="60" r="22" opacity="0.8"/>\n    <line x1="100" y1="82" x2="100" y2="160" opacity="0.8"/>\n    <line x1="68" y1="115" x2="132" y2="115" opacity="0.8"/>\n    <circle cx="100" cy="60" r="34" opacity="0.3"/>\n    <path d="M100,38 L108,52 L100,48 L92,52 Z" fill="#c4824a" opacity="0.6"/>\n    <line x1="100" y1="160" x2="85" y2="178" opacity="0.5"/>\n    <line x1="100" y1="160" x2="115" y2="178" opacity="0.5"/>\n  </g></svg>',
  afrodita: '<svg viewBox="0 0 200 200"><g fill="none" stroke="#b8a0cc" stroke-width="2">\n    <circle cx="100" cy="80" r="30" opacity="0.8"/>\n    <line x1="100" y1="110" x2="100" y2="165" opacity="0.8"/>\n    <line x1="78" y1="140" x2="122" y2="140" opacity="0.8"/>\n    <g opacity="0.6"><line x1="100" y1="50" x2="100" y2="38"/><line x1="100" y1="110" x2="100" y2="122"/>\n    <line x1="70" y1="80" x2="58" y2="80"/><line x1="130" y1="80" x2="142" y2="80"/>\n    <line x1="79" y1="59" x2="71" y2="51"/><line x1="121" y1="59" x2="129" y2="51"/>\n    <line x1="79" y1="101" x2="71" y2="109"/><line x1="121" y1="101" x2="129" y2="109"/></g>\n  </g></svg>',
  lilith: '<svg viewBox="0 0 200 200"><g fill="none" stroke="#5a9bc4" stroke-width="2">\n    <line x1="100" y1="30" x2="100" y2="170" opacity="0.8"/>\n    <line x1="100" y1="55" x2="70" y2="35" opacity="0.7"/>\n    <line x1="100" y1="55" x2="130" y2="35" opacity="0.7"/>\n    <line x1="100" y1="95" x2="65" y2="80" opacity="0.7"/>\n    <line x1="100" y1="95" x2="135" y2="80" opacity="0.7"/>\n    <line x1="100" y1="140" x2="72" y2="160" opacity="0.6"/>\n    <line x1="100" y1="140" x2="128" y2="160" opacity="0.6"/>\n    <line x1="100" y1="140" x2="100" y2="175" opacity="0.6"/>\n    <circle cx="100" cy="100" r="14" opacity="0.5"/>\n  </g></svg>',
  artemisa: '<svg viewBox="0 0 200 200"><g fill="none" stroke="#7aad6a" stroke-width="2">\n    <line x1="100" y1="40" x2="100" y2="160" opacity="0.8"/>\n    <line x1="40" y1="100" x2="160" y2="100" opacity="0.8"/>\n    <circle cx="100" cy="100" r="12" opacity="0.7"/>\n    <circle cx="100" cy="40" r="6" opacity="0.6"/>\n    <circle cx="100" cy="160" r="6" opacity="0.6"/>\n    <circle cx="40" cy="100" r="6" opacity="0.6"/>\n    <circle cx="160" cy="100" r="6" opacity="0.6"/>\n    <path d="M100,100 L130,70 M100,100 L70,70 M100,100 L130,130 M100,100 L70,130" opacity="0.3"/>\n  </g></svg>',
  tutu: '<svg viewBox="0 0 200 200"><g fill="none" stroke="#c4a96a" stroke-width="2">\n    <path d="M100,100 Q115,85 118,65 Q120,40 100,32 Q72,25 55,48 Q38,75 55,105 Q78,138 118,128 Q158,115 158,72" opacity="0.7"/>\n    <circle cx="100" cy="100" r="8" opacity="0.8"/>\n    <circle cx="100" cy="100" r="3" fill="#c4a96a"/>\n  </g></svg>',
};

let camaraSigCtx = null, camaraRuedaCtx = null;
let dibujando = false, trazoActual = [], trazos = [];
let grosorPincel = 4, colorPincel = '#c4a96a';

function abrirCamaraSigilos() {
  document.getElementById('camara-sigilos').classList.add('open');
  document.getElementById('camara-deidad-sub').textContent = 'el espacio de ' + selectedDeidad.charAt(0).toUpperCase() + selectedDeidad.slice(1);
  document.getElementById('sig-deidad-nombre').textContent = selectedDeidad.charAt(0).toUpperCase() + selectedDeidad.slice(1);
  const hex = DEIDADES_META[selectedDeidad].hex;
  colorPincel = hex;
  document.getElementById('pincel-color').value = hex;
  initLienzo();
  cargarGaleria();
}

function cerrarCamaraSigilos() {
  document.getElementById('camara-sigilos').classList.remove('open');
}

function initLienzo() {
  const lienzo = document.getElementById('sigilo-lienzo');
  const rueda  = document.getElementById('sigilo-rueda');
  camaraSigCtx   = lienzo.getContext('2d');
  camaraRuedaCtx = rueda.getContext('2d');
  lienzo.onmousedown = e => iniciarTrazo(e);
  lienzo.onmousemove = e => continuarTrazo(e);
  lienzo.onmouseup   = () => finalizarTrazo();
  lienzo.onmouseleave= () => finalizarTrazo();
  lienzo.ontouchstart = e => { e.preventDefault(); iniciarTrazo(e.touches[0]); };
  lienzo.ontouchmove  = e => { e.preventDefault(); continuarTrazo(e.touches[0]); };
  lienzo.ontouchend   = e => { e.preventDefault(); finalizarTrazo(); };
  redibujarLienzo();
}

function coordsLienzo(e) {
  const lienzo = document.getElementById('sigilo-lienzo');
  const rect = lienzo.getBoundingClientRect();
  return { x: (e.clientX - rect.left) / rect.width * 600, y: (e.clientY - rect.top) / rect.height * 600 };
}

function iniciarTrazo(e) {
  dibujando = true;
  trazoActual = [{...coordsLienzo(e), grosor:grosorPincel, color:colorPincel}];
}

function continuarTrazo(e) {
  if (!dibujando) return;
  trazoActual.push({...coordsLienzo(e), grosor:grosorPincel, color:colorPincel});
  redibujarLienzo();
}

function finalizarTrazo() {
  if (dibujando && trazoActual.length > 1) trazos.push([...trazoActual]);
  dibujando = false; trazoActual = [];
}

function redibujarLienzo() {
  const ctx = camaraSigCtx;
  ctx.clearRect(0,0,600,600);
  const dibujarTrazo = (t) => {
    if (t.length < 2) return;
    ctx.beginPath();
    ctx.moveTo(t[0].x, t[0].y);
    for (let i=1;i<t.length;i++) ctx.lineTo(t[i].x, t[i].y);
    ctx.strokeStyle = t[0].color;
    ctx.lineWidth = t[0].grosor;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.shadowColor = t[0].color; ctx.shadowBlur = 8;
    ctx.stroke();
    ctx.shadowBlur = 0;
  };
  trazos.forEach(dibujarTrazo);
  if (trazoActual.length > 1) dibujarTrazo(trazoActual);
}

function deshacerTrazo() { trazos.pop(); redibujarLienzo(); }
function limpiarLienzo() { trazos = []; redibujarLienzo(); }

function setGrosor(g, btn) {
  grosorPincel = g;
  document.querySelectorAll('.grosor-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function setPincelColor(c) { colorPincel = c; }

function generarSigilo() {
  const texto = document.getElementById('sigilo-intencion').value.trim();
  if (!texto) return;
  const original  = texto.toUpperCase();
  const sinEspacios = original.replace(/\s+/g,'');
  const VOCALES = 'AEIOU\u00C1\u00C9\u00CD\u00D3\u00DA\u00DC';
  const sinVocales = [...sinEspacios].filter(c => !VOCALES.includes(c) && /[A-Z\u00D1]/.test(c)).join('');
  const esenciales = [];
  for (const c of sinVocales) if (!esenciales.includes(c)) esenciales.push(c);
  const proc = document.getElementById('sigilo-proceso');
  const tachar = (str, mantener) => [...str].map(c => mantener.includes(c) ? c : '<span class="tachada">' + c + '</span>').join('');
  proc.innerHTML = [
    '<div class="proceso-paso"><span class="proceso-label">intenci\u00F3n</span><span class="proceso-valor">' + original + '</span></div>',
    '<div class="proceso-paso"><span class="proceso-label">sin vocales</span><span class="proceso-valor">' + tachar(sinEspacios, sinVocales) + '</span></div>',
    '<div class="proceso-paso"><span class="proceso-label">sin repetir</span><span class="proceso-valor">' + esenciales.join(' ') + '</span></div>',
    '<div class="proceso-esencia">' + esenciales.join('') + '</div>',
  ].join('');
  document.getElementById('sigilo-proceso-wrap').style.display = 'block';
  dibujarRueda(esenciales);
}

function dibujarRueda(letras) {
  const ctx = camaraRuedaCtx;
  ctx.clearRect(0,0,600,600);
  if (!letras.length) return;
  const cx=300, cy=300, R=210;
  const n = letras.length;
  const puntos = letras.map((L,i) => {
    const ang = (i/n)*Math.PI*2 - Math.PI/2;
    return { x: cx+Math.cos(ang)*R, y: cy+Math.sin(ang)*R, L };
  });
  ctx.font = '22px Cinzel, serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillStyle = 'rgba(122,112,96,0.5)';
  puntos.forEach(p => {
    const ang = Math.atan2(p.y-cy, p.x-cx);
    const lx = cx+Math.cos(ang)*(R+28), ly = cy+Math.sin(ang)*(R+28);
    ctx.fillText(p.L, lx, ly);
  });
  ctx.beginPath();
  ctx.moveTo(puntos[0].x, puntos[0].y);
  for (let i=1;i<puntos.length;i++) ctx.lineTo(puntos[i].x, puntos[i].y);
  ctx.strokeStyle = 'rgba(196,169,106,0.35)';
  ctx.lineWidth = 1.5; ctx.lineCap='round'; ctx.lineJoin='round';
  ctx.stroke();
  puntos.forEach((p,i) => {
    ctx.beginPath();
    ctx.arc(p.x,p.y, i===0?6:4, 0,Math.PI*2);
    ctx.fillStyle = i===0 ? 'rgba(196,169,106,0.7)' : 'rgba(196,169,106,0.4)';
    ctx.fill();
  });
}

function verSigiloDeidad() {
  const svg = SIGILOS_DEIDAD[selectedDeidad];
  if (!svg) return;
  const ctx = camaraRuedaCtx;
  ctx.clearRect(0,0,600,600);
  const img = new Image();
  const blob = new Blob([svg.replace('viewBox="0 0 200 200"','viewBox="0 0 200 200" width="600" height="600"')], {type:'image/svg+xml'});
  const url = URL.createObjectURL(blob);
  img.onload = () => { ctx.globalAlpha=0.5; ctx.drawImage(img,0,0,600,600); ctx.globalAlpha=1; URL.revokeObjectURL(url); };
  img.src = url;
  mostrarMensajeDeidad('Este es mi sigilo. T\u00F3malo como base o deja que te inspire.');
}

async function pedirIntencionDeidad() {
  mostrarMensajeDeidad('La deidad medita tu intenci\u00F3n...');
  try {
    const res = await fetchAPI('/api/sigilo/regalo/' + selectedDeidad, {method:'POST'});
    const data = await res.json();
    if (data.intencion) {
      document.getElementById('sigilo-intencion').value = data.intencion;
      mostrarMensajeDeidad('"' + data.intencion + '" \u2014 deja que esta intenci\u00F3n se vuelva forma.');
      generarSigilo();
    }
  } catch(e) { mostrarMensajeDeidad('El humo se dispersa. Intenta de nuevo.'); }
}

async function cocrearDeidad() {
  const intencion = document.getElementById('sigilo-intencion').value.trim();
  if (!intencion) { mostrarMensajeDeidad('Escribe primero tu intenci\u00F3n.'); return; }
  mostrarMensajeDeidad('La deidad contempla tu intenci\u00F3n...');
  try {
    const prompt = 'Estoy creando un sigilo con esta intenci\u00F3n: "' + intencion + '". Gu\u00EDame en una o dos frases sobre qu\u00E9 formas o trazos deber\u00EDa dibujar desde tu naturaleza. S\u00E9 concreto y breve.';
    const res = await fetchAPI('/api/consultar', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ mensaje: prompt, entidad: selectedDeidad }),
    });
    const data = await res.json();
    mostrarMensajeDeidad(data.respuesta);
  } catch(e) { mostrarMensajeDeidad('El humo se dispersa. Intenta de nuevo.'); }
}

function mostrarMensajeDeidad(txt) {
  const el = document.getElementById('lienzo-mensaje-deidad');
  el.style.color = DEIDADES_META[selectedDeidad].color;
  el.textContent = txt;
}

function componerSigiloPNG() {
  const out = document.createElement('canvas');
  out.width = 600; out.height = 600;
  const octx = out.getContext('2d');
  octx.fillStyle = '#0d0b09';
  octx.fillRect(0,0,600,600);
  octx.drawImage(document.getElementById('sigilo-rueda'), 0,0);
  octx.drawImage(document.getElementById('sigilo-lienzo'),0,0);
  return out.toDataURL('image/png');
}

async function guardarSigilo() {
  const intencion = document.getElementById('sigilo-intencion').value.trim() || 'sin intenci\u00F3n';
  const imagen    = componerSigiloPNG();
  try {
    await fetchAPI('/api/sigilo', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ intencion, imagen, entidad:selectedDeidad, origen:'practicante' }),
    });
    mostrarMensajeDeidad('\u2716 Sellado en el grimorio.');
    cargarGaleria();
    limpiarLienzo();
  } catch(e) { mostrarMensajeDeidad('No se pudo sellar. Intenta de nuevo.'); }
}

async function cargarGaleria() {
  try {
    const res = await fetchAPI('/api/sigilos');
    const sigilos = await res.json();
    const grid = document.getElementById('galeria-sigilos');
    if (!sigilos.length) { grid.innerHTML = '<div class="galeria-vacia">A\u00FAn no hay sigilos sellados.</div>'; return; }
    grid.innerHTML = sigilos.map(s => {
      const tit = s.intencion.replace(/"/g,'&quot;');
      return '<div class="galeria-item ' + (s.cargado?'cargado':'') + '" title="' + tit + '">' +
        '<img src="' + s.imagen + '" alt="sigilo"/>' +
        '<div class="galeria-item-acciones">' +
        (s.cargado ? '' : '<button class="gal-btn cargar" onclick="ritualCargar(' + s.id + ')">\u2726 Cargar</button>') +
        '<button class="gal-btn quemar" onclick="ritualQuemar(' + s.id + ')">\uD83D\uDD02 Quemar</button>' +
        '</div></div>';
    }).join('');
  } catch(e) {}
}

async function ritualCargar(id) {
  if (sonidoOn) campanilla();
  try {
    await fetchAPI('/api/sigilo/cargar/' + id, {method:'POST'});
    mostrarMensajeDeidad('El sigilo arde en tu mente y se disuelve. Ahora olv\u00EDdalo \u2014 el inconsciente trabajar\u00E1.');
    cargarGaleria();
  } catch(e) {}
}

async function ritualQuemar(id) {
  try {
    await fetchAPI('/api/sigilo/quemar/' + id, {method:'POST'});
    cargarGaleria();
  } catch(e) {}
}
