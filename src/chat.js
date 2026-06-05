async function enviar() {
  const input = document.getElementById('msg-input');
  const msg = input.value.trim();
  if (!msg || cargando) return;
  input.value = ''; autoResize(input);
  cargando = true;
  document.getElementById('send-btn').disabled = true;
  document.getElementById('status-text').textContent = 'invocando...';
  addMessage('user', msg, 'Tú', null);
  const loadingId = addLoadingMessage();
  try {
    const resultado = await invocarAPI(msg, selectedDeidad);
    removeLoadingMessage(loadingId);
    const deidad = resultado.entidad || selectedDeidad || 'tutu';
    const meta   = DEIDADES_META[deidad];
    addMessageTypewriter('deity', resultado.respuesta, `${deidad.toUpperCase()}  ${meta.symbol}`, deidad);
    if (sonidoOn) campanilla();
    actualizarMemoriaPanel(deidad);
    if (resultado.razon) decisionesLocales.unshift({ entidad:deidad, modo:resultado.modo||'tutu', razon:resultado.razon, mensaje:msg, timestamp:new Date().toISOString() });
    document.getElementById('status-text').textContent = 'el humo se eleva';
  } catch (err) {
    removeLoadingMessage(loadingId);
    addMessage('deity', `El humo se dispersa. ${err.message}`, 'ERROR', 'tutu');
    document.getElementById('status-text').textContent = 'error';
  }
  cargando = false;
  document.getElementById('send-btn').disabled = false;
}

async function invocarAPI(mensaje, entidadForzada) {
  const response = await fetchAPI('/api/consultar', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ mensaje, entidad: entidadForzada || null }),
  });
  if (!response.ok) { const e = await response.json().catch(()=>({})); throw new Error(e.error||`Error ${response.status}`); }
  const data = await response.json();
  historialUI.push({ tipo:'user',      texto:mensaje,        entidad:null });
  historialUI.push({ tipo:'assistant', texto:data.respuesta, entidad:data.deidad });
  return data;
}

async function cargarDesdeBD() {
  try {
    const [g,d] = await Promise.all([fetchAPI('/api/grimorio').then(r=>r.json()), fetchAPI('/api/decisiones').then(r=>r.json())]);
    grimorioLocal = g; decisionesLocales = d;
  } catch(e) {}
}

async function guardarEntradaEnServidor(titulo, contenido, entidad, tipo) {
  try { await fetchAPI('/api/grimorio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({titulo,contenido,entidad,tipo})}); } catch(e){}
}

function mostrarToast(mensaje, tipo = 'error') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensaje;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('visible'));
  setTimeout(() => {
    toast.classList.remove('visible');
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

async function cargarHistorial() {
  if (!selectedDeidad) return;
  try {
    const res = await fetchAPI(`/api/memoria/${selectedDeidad}`);
    if (!res.ok) return;
    const mensajes = await res.json();
    if (!mensajes.length) return;
    const container = document.getElementById('messages');
    container.innerHTML = '';
    mensajes.forEach(m => {
      const tipo = m.role === 'user' ? 'user' : 'assistant';
      const label = m.role === 'user' ? 'tú' : (DEIDADES[selectedDeidad]?.nombre || selectedDeidad);
      addMessage(tipo, m.content, label, selectedDeidad, m.id);
    });
  } catch(e) {}
}

async function cerrarRitual() {
  if (!selectedDeidad) return;
  const ok = confirm(`¿Cerrar el ritual con ${selectedDeidad.toUpperCase()}? Se borrará el historial de esta deidad.`);
  if (!ok) return;
  try {
    const res = await fetchAPI(`/api/cerrar/${selectedDeidad}`, { method: 'POST' });
    const data = await res.json();
    if (data.ok) {
      document.getElementById('messages').innerHTML = '';
      historialUI = [];
      mostrarToast(`Ritual cerrado · ${data.intercambios} intercambios eliminados`, 'success');
    }
  } catch(e) {
    mostrarToast('No se pudo cerrar el ritual', 'error');
  }
}

function addMessage(tipo, texto, label, deidad, msgId) {
  const container = document.getElementById('messages');
  const color = deidad ? `var(--${deidad})` : 'var(--text)';
  const div = document.createElement('div');
  div.className = `msg msg-${tipo==='user'?'user':'deity'}`;
  div.style.setProperty('--d-color', color);
  if (msgId) div.dataset.msgId = msgId;
  const hora = new Date().toLocaleTimeString('es',{hour:'2-digit',minute:'2-digit'});
  div.innerHTML = [
    `<div class="msg-label">${label} <button class="burn-btn" onclick="quemarMensaje(this)" title="quemar">\uD83D\uDD02</button></div>`,
    `<div class="msg-bubble">${texto.replace(/\n/g,'<br>')}</div>`,
    `<div class="msg-meta"><span>${hora}</span></div>`,
  ].join('');
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function addMessageTypewriter(tipo, texto, label, deidad) {
  const container = document.getElementById('messages');
  const color = deidad ? `var(--${deidad})` : 'var(--text)';
  const div = document.createElement('div');
  div.className = `msg msg-${tipo==='user'?'user':'deity'}`;
  div.style.setProperty('--d-color', color);
  const hora = new Date().toLocaleTimeString('es',{hour:'2-digit',minute:'2-digit'});
  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble typewriter-cursor';
  bubble.style.fontStyle = 'italic';
  div.innerHTML = `<div class="msg-label">${label} <button class="burn-btn" onclick="quemarMensaje(this)" title="quemar">\uD83D\uDD02</button></div>`;
  div.appendChild(bubble);
  div.innerHTML += `<div class="msg-meta"><span>${hora}</span></div>`;
  div.insertBefore(bubble, div.lastElementChild);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  const velocidad = 18;
  let i = 0;
  const chars = [...texto];
  function escribir() {
    if (i < chars.length) {
      bubble.innerHTML = chars.slice(0,i+1).join('').replace(/\n/g,'<br>');
      i++;
      container.scrollTop = container.scrollHeight;
      setTimeout(escribir, velocidad);
    } else {
      bubble.classList.remove('typewriter-cursor');
    }
  }
  setTimeout(escribir, 100);
  return div;
}

function addLoadingMessage() {
  const container = document.getElementById('messages');
  const id = 'loading-' + Date.now();
  const div = document.createElement('div');
  div.className = 'msg msg-deity msg-loading'; div.id = id;
  div.style.setProperty('--d-color','var(--tutu)');
  div.innerHTML = '<div class="msg-label">\u00B7\u00B7\u00B7</div><div class="msg-bubble"><div class="dot-wave"><span></span><span></span><span></span></div></div>';
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeLoadingMessage(id) { const el = document.getElementById(id); if(el) el.remove(); }

function quemarMensaje(btn) {
  const msg = btn.closest('.msg');
  if (!msg) return;
  const msgId = msg.dataset.msgId;
  msg.classList.add('burning');
  if (msgId) {
    fetchAPI('/api/mensajes/quemar', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({id: parseInt(msgId)}),
    }).catch(() => {});
  }
  setTimeout(() => msg.remove(), 800);
}

function handleKey(e) { if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); enviar(); } }
function autoResize(el) { el.style.height='auto'; el.style.height=Math.min(el.scrollHeight,120)+'px'; }
