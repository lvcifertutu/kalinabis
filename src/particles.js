(function initCanvas() {
  const canvas = document.getElementById('smoke-canvas');
  const ctx = canvas.getContext('2d');
  let W, H;
  const particles = [];
  const sparks = [];

  function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
  resize();
  window.addEventListener('resize', resize);

  function lerpRGB(cur, target, t) {
    return cur.map((c,i) => c + (target[i] - c) * t);
  }

  class Smoke {
    constructor(init) { this.reset(init); }
    reset(init) {
      this.x  = Math.random() * W;
      this.y  = init ? Math.random() * H : H + 30;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = -(0.2 + Math.random() * 0.5);
      this.r  = 50 + Math.random() * 120;
      this.alpha = 0;
      this.maxAlpha = 0.10 + Math.random() * 0.14;
      this.life = 0;
      this.maxLife = 250 + Math.random() * 280;
      this.wobble = Math.random() * Math.PI * 2;
    }
    update() {
      this.life++;
      this.wobble += 0.018;
      this.x += this.vx + Math.sin(this.wobble) * 0.5;
      this.y += this.vy;
      this.r += 0.18;
      const p = this.life / this.maxLife;
      this.alpha = p < 0.2 ? (p/0.2)*this.maxAlpha : p < 0.65 ? this.maxAlpha : ((1-p)/0.35)*this.maxAlpha;
      if (this.life >= this.maxLife || this.y < -this.r) this.reset(false);
    }
    draw() {
      const [r,g,b] = smokeCurRGB;
      const gr = ctx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r);
      gr.addColorStop(0, `rgba(${r},${g},${b},${this.alpha})`);
      gr.addColorStop(0.5, `rgba(${r},${g},${b},${this.alpha*0.4})`);
      gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
      ctx.fillStyle = gr;
      ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.fill();
    }
  }

  class Spark {
    constructor() { this.reset(); }
    reset() {
      this.x  = Math.random() * W;
      this.y  = H * 0.5 + Math.random() * H * 0.5;
      this.vx = (Math.random() - 0.5) * 1.2;
      this.vy = -(0.8 + Math.random() * 2.5);
      this.r  = 1 + Math.random() * 2;
      this.alpha = 0.8 + Math.random() * 0.2;
      this.life = 0;
      this.maxLife = 60 + Math.random() * 80;
    }
    update() {
      this.life++;
      this.x += this.vx;
      this.y += this.vy;
      this.vy += 0.03;
      this.alpha -= 0.012;
      if (this.life >= this.maxLife || this.alpha <= 0) this.reset();
    }
    draw() {
      const [r,g,b] = smokeCurRGB;
      ctx.beginPath();
      ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
      ctx.fillStyle = `rgba(${Math.min(r+60,255)},${Math.min(g+40,255)},${Math.min(b+20,255)},${this.alpha})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < 70; i++) particles.push(new Smoke(true));
  for (let i = 0; i < 30; i++) sparks.push(new Spark());

  function loop() {
    ctx.clearRect(0,0,W,H);
    smokeCurRGB = lerpRGB(smokeCurRGB, smokeTargetRGB, 0.01);
    particles.forEach(p => { p.update(); p.draw(); });
    sparks.forEach(s => { s.update(); s.draw(); });
    requestAnimationFrame(loop);
  }
  loop();
})();
