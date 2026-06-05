window.addEventListener('DOMContentLoaded', async () => {
  initDomainCanvas();
  setDeidad('tutu');
  await initProyecto();
  await cargarHistorial();
  cargarDesdeBD();
  cargarLuna();
});
