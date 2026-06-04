from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

results = []

def test(name, viewport=None, reduced_motion=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        opts = {'viewport': viewport or {'width': 1280, 'height': 800}}
        if reduced_motion:
            opts['reduced_motion'] = 'reduce'
        context = browser.new_context(**opts)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        page.goto('http://localhost:5000')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)

        # Verificaciones
        has_skip = page.locator('.skip-link').count() > 0
        has_focus_visible = True
        msg_input_aria = page.locator('#msg-input').get_attribute('aria-label')
        send_btn_aria = page.locator('#send-btn').get_attribute('aria-label')
        ritual_aria = page.locator('.ritual-exit').get_attribute('aria-label')
        deity_aria = page.locator('[data-deity="tutu"]').first.get_attribute('aria-label')
        messages_role = page.locator('#messages').get_attribute('role')
        modal_aria = page.locator('#modal').get_attribute('role')

        # Test: focus visible con Tab
        page.keyboard.press('Tab')
        active = page.evaluate('document.activeElement.className')

        result = {
            'name': name,
            'viewport': viewport,
            'reduced_motion': reduced_motion,
            'errors': errors,
            'skip_link': has_skip,
            'aria_msg_input': msg_input_aria,
            'aria_send_btn': send_btn_aria,
            'aria_ritual': ritual_aria,
            'aria_deity': deity_aria,
            'messages_role': messages_role,
            'modal_role': modal_aria,
            'first_tab_focus': active,
        }
        results.append(result)
        browser.close()

# Test 1: Desktop
test('desktop-1280', {'width': 1280, 'height': 800})

# Test 2: Mobile
test('mobile-375', {'width': 375, 'height': 667})

# Test 3: Tablet
test('tablet-768', {'width': 768, 'height': 1024})

# Test 4: Reduced motion
test('reduced-motion', {'width': 1280, 'height': 800}, reduced_motion=True)

print('=' * 60)
for r in results:
    print(f"\n=== {r['name']} ===")
    print(f"  Viewport: {r['viewport']}")
    print(f"  Errors JS: {len(r['errors'])}")
    for e in r['errors']:
        print(f"    - {e}")
    print(f"  Skip link: {r['skip_link']}")
    print(f"  ARIA msg-input: '{r['aria_msg_input']}'")
    print(f"  ARIA send-btn: '{r['aria_send_btn']}'")
    print(f"  ARIA ritual: '{r['aria_ritual']}'")
    print(f"  ARIA deity: '{r['aria_deity']}'")
    print(f"  Messages role: '{r['messages_role']}'")
    print(f"  Modal role: '{r['modal_role']}'")
    print(f"  First Tab focus: '{r['first_tab_focus']}'")
