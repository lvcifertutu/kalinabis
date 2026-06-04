function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const len = audioCtx.sampleRate * 3.5;
  const buf = audioCtx.createBuffer(2, len, audioCtx.sampleRate);
  for (let ch = 0; ch < 2; ch++) {
    const d = buf.getChannelData(ch);
    for (let i = 0; i < len; i++)
      d[i] = (Math.random()*2 - 1) * Math.pow(1 - i/len, 2.2);
  }
  reverbNode = audioCtx.createConvolver();
  reverbNode.buffer = buf;
  const reverbGain = audioCtx.createGain();
  reverbGain.gain.value = 0.35;
  reverbNode.connect(reverbGain);
  reverbGain.connect(audioCtx.destination);
}

let reverbNode  = null;
let ambientNodes = [];
let bowlInterval = null;

const BOWL_CFG = {
  tutu:     { root:396, drone:99,  decay:8, interval:9000,  glide:6,  vol:0.18 },
  isis:     { root:528, drone:132, decay:7, interval:8000,  glide:8,  vol:0.16 },
  afrodita: { root:432, drone:108, decay:9, interval:10000, glide:5,  vol:0.15 },
  lilith:   { root:174, drone:87,  decay:6, interval:7000,  glide:10, vol:0.20 },
  artemisa: { root:285, drone:95,  decay:8, interval:9500,  glide:7,  vol:0.17 },
};

const ARMONICOS      = [1, 2.756, 5.404, 8.933, 13.344];
const ARMONICO_GAINS = [1, 0.38,  0.20,  0.11,  0.06];

function golpearCuenco(cfg) {
  if (!audioCtx || !reverbNode) return;
  const now = audioCtx.currentTime;
  ARMONICOS.forEach((ratio, i) => {
    const freq = cfg.root * ratio;
    const osc  = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    const filt = audioCtx.createBiquadFilter();
    filt.type = 'bandpass';
    filt.frequency.value = freq;
    filt.Q.value = 10;
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq + cfg.glide / (i + 1), now);
    osc.frequency.exponentialRampToValueAtTime(freq, now + 0.3);
    const peak = cfg.vol * ARMONICO_GAINS[i];
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(peak, now + 0.008);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + cfg.decay);
    osc.connect(filt); filt.connect(gain);
    gain.connect(audioCtx.destination);
    gain.connect(reverbNode);
    osc.start(now);
    osc.stop(now + cfg.decay + 0.2);
    ambientNodes.push({ osc, gain });
  });
}

function iniciarDrone(cfg) {
  if (!audioCtx) return;
  const osc  = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const filt = audioCtx.createBiquadFilter();
  osc.type = 'sine';
  osc.frequency.value = cfg.drone;
  filt.type = 'lowpass'; filt.frequency.value = 280;
  const lfo     = audioCtx.createOscillator();
  const lfoGain = audioCtx.createGain();
  lfo.frequency.value = 0.07;
  lfoGain.gain.value  = 0.3;
  lfo.connect(lfoGain); lfoGain.connect(osc.frequency);
  lfo.start();
  gain.gain.setValueAtTime(0, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(cfg.vol * 0.10, audioCtx.currentTime + 4);
  osc.connect(filt); filt.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  ambientNodes.push({ osc, gain, lfo });
}

function iniciarAmbient(deidad) {
  if (!sonidoOn || !audioCtx) return;
  detenerAmbient();
  const cfg = BOWL_CFG[deidad] || BOWL_CFG.tutu;
  iniciarDrone(cfg);
  setTimeout(() => { if (sonidoOn) golpearCuenco(cfg); }, 1000);
  bowlInterval = setInterval(() => {
    if (sonidoOn) golpearCuenco(cfg);
  }, cfg.interval + Math.random() * 3000);
}

function detenerAmbient() {
  if (bowlInterval) { clearInterval(bowlInterval); bowlInterval = null; }
  ambientNodes.forEach(n => {
    try {
      n.gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 2);
      setTimeout(() => { try { n.osc.stop(); if(n.lfo) n.lfo.stop(); } catch(e){} }, 2100);
    } catch(e) {}
  });
  ambientNodes = [];
}

function campanilla() {
  if (!sonidoOn || !audioCtx) return;
  const base = BOWL_CFG[selectedDeidad] || BOWL_CFG.tutu;
  golpearCuenco({ ...base, root: base.root * 2, decay: 3, glide: base.glide * 0.4, vol: base.vol * 0.65 });
}

function toggleSonido() {
  sonidoOn = !sonidoOn;
  const btn = document.getElementById('btn-sonido');
  if (sonidoOn) {
    initAudio();
    btn.classList.add('on');
    btn.textContent = '♪ SONIDO';
    iniciarAmbient(selectedDeidad);
  } else {
    btn.classList.remove('on');
    detenerAmbient();
  }
}
