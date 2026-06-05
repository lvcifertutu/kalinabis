const cursorEl = document.getElementById('cursor');
document.addEventListener('mousemove', e => {
  cursorEl.style.left = e.clientX + 'px';
  cursorEl.style.top  = e.clientY + 'px';
});
document.addEventListener('mousedown', () => cursorEl.classList.add('clicking'));
document.addEventListener('mouseup',   () => cursorEl.classList.remove('clicking'));

let ritualOn = false;
function toggleRitual() {
  ritualOn = !ritualOn;
  document.body.classList.toggle('ritual', ritualOn);
}

function setDeidad(nombre) {
  selectedDeidad = nombre;
  const btn = document.querySelector(`.deity-btn[data-deity="${nombre}"]`);
  document.querySelectorAll('.deity-btn').forEach(b => b.classList.remove('active','invocando'));
  if (btn) { btn.classList.add('active','invocando'); setTimeout(() => btn.classList.remove('invocando'), 700); }
  const velo = document.getElementById('velo');
  velo.classList.add('oscuro');
  setTimeout(() => velo.classList.remove('oscuro'), 1200);
  const meta = DEIDADES_META[nombre];
  document.getElementById('active-name').textContent   = nombre.toUpperCase();
  document.getElementById('active-name').style.color   = meta.color;
  document.getElementById('active-symbol').textContent = meta.symbol;
  document.getElementById('active-attrs').textContent  = meta.attrs;
  cursorEl.textContent = CURSOR_SYMBOLS[nombre];
  cursorEl.style.color = meta.hex;
  smokeTargetRGB = meta.smokeRGB;
  cambiarAtmosfera(nombre);
  manifestarTrono(nombre);
  cambiarParticulasDominio(nombre);
  actualizarBrujula(nombre, meta);
  document.querySelectorAll('.deity-memory').forEach(m => m.classList.remove('visible'));
  const mem = document.getElementById(`mem-${nombre}`);
  if (mem) mem.classList.add('visible');
  actualizarMemoriaPanel(nombre);
  if (sonidoOn && audioCtx) iniciarAmbient(nombre);
  cargarHistorial();
}

function actualizarBrujula(nombre, meta) {
  const svg = document.getElementById('active-compass');
  const hex = meta.hex;
  const dir = meta.dir;
  if (dir) {
    const angles = { N:270, E:0, S:90, O:180 };
    const a  = (angles[dir] * Math.PI) / 180;
    const nx = 18 + Math.cos(a)*13, ny = 18 + Math.sin(a)*13;
    const p1x = 18 + Math.cos(a+Math.PI/2)*3, p1y = 18 + Math.sin(a+Math.PI/2)*3;
    const p2x = 18 + Math.cos(a-Math.PI/2)*3, p2y = 18 + Math.sin(a-Math.PI/2)*3;
    const bx  = 18 + Math.cos(a+Math.PI)*10,  by  = 18 + Math.sin(a+Math.PI)*10;
    svg.innerHTML = [
      `<circle cx="18" cy="18" r="16" fill="none" stroke="${hex}44" stroke-width="1"/>`,
      `<circle cx="18" cy="18" r="2" fill="${hex}"/>`,
      `<polygon points="${nx},${ny} ${p1x},${p1y} ${bx},${by} ${p2x},${p2y}" fill="${hex}" opacity="0.95"/>`,
      `<text x="${18+Math.cos(a)*13.5}" y="${18+Math.sin(a)*13.5+1.5}" text-anchor="middle" font-size="4.5" fill="${hex}" font-family="serif">${dir}</text>`,
    ].join('');
  } else {
    svg.innerHTML = `<circle cx="18" cy="18" r="16" fill="none" stroke="${hex}44" stroke-width="1"/><circle cx="18" cy="18" r="4" fill="${hex}" opacity="0.5"/>`;
  }
}

async function actualizarMemoriaPanel(nombre) {
  const el = document.getElementById(`mem-${nombre}`);
  if (!el) return;
  try {
    const res  = await fetchAPI(`/api/memoria/${nombre}`);
    const msgs = await res.json();
    if (!msgs.length) { el.innerHTML = '<span style="color:var(--dim);font-style:italic">sin memoria aún</span>'; return; }
    el.innerHTML = msgs.slice(-6).map(m =>
      `<div class="memory-msg ${m.role}">${m.content.slice(0,65)}${m.content.length>65?'…':''}</div>`
    ).join('');
    el.scrollTop = el.scrollHeight;
  } catch(e) { el.innerHTML = '<span style="color:var(--dim)">—</span>'; }
}

const SALUDO = {
  isis:     'Preséntate ante el practicante en una sola frase desde tu esencia. Sin saludos formales.',
  afrodita: 'Preséntate ante el practicante en una sola frase desde tu claridad. Sin saludos formales.',
  lilith:   'Preséntate ante el practicante en una sola frase desde tu tormenta. Sin saludos formales.',
  artemisa: 'Preséntate ante el practicante en una sola frase desde tu raíz colectiva. Sin saludos formales.',
};

async function enviarMensajeDeidad(nombre) {
  try {
    const res  = await fetchAPI('/api/consultar', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ mensaje: SALUDO[nombre], entidad: nombre }),
    });
    const data = await res.json();
    const meta = DEIDADES_META[nombre];
    addMessageTypewriter('deity', data.respuesta, `${nombre.toUpperCase()}  ${meta.symbol}`, nombre);
    actualizarMemoriaPanel(nombre);
    if (sonidoOn) campanilla();
  } catch(e) { console.warn(nombre, e.message); }
}
