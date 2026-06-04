from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    errors = []
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.on('console', lambda msg: errors.append(f'[{msg.type}] {msg.text}') if msg.type == 'error' else None)

    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)

    # Verificar botón BOSQUE existe
    bosque_btn = page.locator('button:has-text("BOSQUE")')
    print(f'[1] Boton BOSQUE en header: {bosque_btn.count() > 0}')

    # Abrir panel
    bosque_btn.click()
    page.wait_for_timeout(2000)

    panel = page.locator('#panel-bosque.open')
    print(f'[2] Panel abierto: {panel.count() > 0}')

    # Verificar datos de salud
    total = page.locator('#bosque-total').text_content()
    activas = page.locator('#bosque-activas').text_content()
    print(f'[3] Total esferas: {total}, Activas: {activas}')

    # Verificar amplitud
    amp_valor = page.locator('#bosque-amp-valor').text_content()
    print(f'[4] Amplitud promedio: {amp_valor}')

    # Verificar distribución
    dist_items = page.locator('.bosque-distribucion-item').count()
    print(f'[5] Items de distribucion: {dist_items}')

    # Verificar esferas fuertes
    fuertes = page.locator('.bosque-fuerte-item').count()
    print(f'[6] Esferas fuertes mostradas: {fuertes}')

    # Verificar SVG
    svg_nodos = page.locator('#bosque-mapa-svg circle').count()
    print(f'[7] Nodos SVG renderizados: {svg_nodos}')

    # Verificar leyenda
    leyenda = page.locator('.bosque-leyenda-item').count()
    print(f'[8] Items en leyenda: {leyenda}')

    # Cerrar con Esc
    page.keyboard.press('Escape')
    page.wait_for_timeout(500)
    panel_closed = page.locator('#panel-bosque.open').count()
    print(f'[9] Panel cerrado con Esc: {panel_closed == 0}')

    print(f'\n--- Errores ({len(errors)}) ---')
    for e in errors:
        print(f'  {e}')

    # Screenshot
    page.locator('button:has-text("BOSQUE")').click()
    page.wait_for_timeout(1500)
    page.screenshot(path='C:\\grimorio\\bosque_panel.png', full_page=True)
    print('\n[OK] Screenshot: bosque_panel.png')

    browser.close()
