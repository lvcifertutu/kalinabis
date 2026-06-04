from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    logs = []
    page.on('console', lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.on('pageerror', lambda exc: logs.append(f"[ERR] {exc}"))

    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Test 1: verificar project code visible
    code = page.locator('#project-code-display').text_content()
    print(f'[TEST 1] Project code visible: "{code}"')
    assert '...' not in code, "FAIL: project code is placeholder"

    # Test 2: enviar mensaje
    page.locator('#msg-input').fill('Que es el silencio para ti?')
    page.locator('#send-btn').click()
    page.wait_for_timeout(8000)

    msgs = page.locator('.msg').count()
    print(f'[TEST 2] Mensajes totales: {msgs}')

    # Test 3: verificar respuesta de Tutu
    last = page.locator('.msg').last
    last_txt = last.text_content() if last.count() else ''
    print(f'[TEST 3] Ultima respuesta: {last_txt[:200]}')
    assert 'ERROR' not in last_txt, f"FAIL: error en respuesta: {last_txt}"

    # Test 4: refrescar y verificar historial
    page.reload()
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)
    msgs_after = page.locator('.msg').count()
    print(f'[TEST 4] Mensajes despues de refresh: {msgs_after}')
    assert msgs_after > 0, "FAIL: no se cargo historial"

    # Test 5: grimorio modal
    page.evaluate("() => { openModal(); }")
    page.wait_for_timeout(1000)
    modal = page.locator('#modal.open')
    print(f'[TEST 5] Modal grimorio abierto: {modal.count() > 0}')

    # Test 6: tabs
    tabs = page.locator('.grimorio-tab').count()
    print(f'[TEST 6] Tabs en grimorio: {tabs}')

    print('\n--- LOGS ---')
    for log in logs:
        print(log)

    page.screenshot(path='C:\\grimorio\\final_test.png', full_page=True)
    print('\n[OK] Screenshot: final_test.png')
    browser.close()
