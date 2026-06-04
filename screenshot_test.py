from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Mobile
    context = browser.new_context(viewport={'width': 375, 'height': 667})
    page = context.new_page()
    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.screenshot(path='C:\\grimorio\\mobile.png', full_page=True)
    print('Mobile screenshot saved')
    context.close()

    # Desktop
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()
    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.screenshot(path='C:\\grimorio\\desktop.png', full_page=True)
    print('Desktop screenshot saved')
    context.close()

    # Open modal on mobile
    context = browser.new_context(viewport={'width': 375, 'height': 667})
    page = context.new_page()
    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.evaluate('() => openModal()')
    page.wait_for_timeout(1000)
    page.screenshot(path='C:\\grimorio\\mobile_modal.png', full_page=True)
    print('Mobile modal screenshot saved')

    browser.close()
