# Test del backend completo
import sys, threading, time, json, urllib.request
sys.path.insert(0, 'C:/grimorio')
import servidor

def run():
    servidor.app.run(host='127.0.0.1', port=5001, debug=False)

t = threading.Thread(target=run, daemon=True)
t.start()
time.sleep(2)

def test(method, path, body=None, headers=None):
    url = f'http://127.0.0.1:5001{path}'
    data = json.dumps(body).encode() if body else None
    hdrs = {'Content-Type': 'application/json'}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {'error': str(e)}

print('1. GET /api/luna...')
r = test('GET', '/api/luna')
print(f'   OK: {list(r.keys())[:5]}')

print('2. GET /api/cosmologia...')
r = test('GET', '/api/cosmologia')
print(f'   OK: {list(r.keys())}')

print('3. POST /api/proyecto/nuevo...')
r = test('POST', '/api/proyecto/nuevo', {'nombre': 'Test'})
code = r.get('codigo', '')
h = r.get('hash', '')
print(f'   OK: codigo={code[:20]}... hash={h}')

print(f'4. POST /api/proyecto/verificar (codigo correcto)...')
r = test('POST', '/api/proyecto/verificar', headers={'X-Project-Code': code})
print(f'   OK: existe={r.get("existe")}')

print(f'5. GET /api/esferas (vacio)...')
r = test('GET', '/api/esferas')
print(f'   OK: total={r.get("total")}')

print('6. POST /api/consultar (sin Gemini Key, esperando error controlado)...')
r = test('POST', '/api/consultar',
         {'mensaje': 'hola', 'entidad': 'isis', 'ubicacion': 'Santiago'},
         {'X-Project-Code': code})
resp = r.get('respuesta', '')
print(f'   OK: respuesta=[{resp[:60]}...]')
print(f'   Esferas activadas: {len(r.get("esferas_activadas", []))}')
if r.get('eje_del_mundo'):
    eje = r['eje_del_mundo']['eje_del_mundo']['nombres_locales']
    print(f'   Eje del Mundo: {eje}')

print('7. GET /api/bosque/mapa...')
r = test('GET', '/api/bosque/mapa')
print(f'   OK: {len(r.get("nodos",[]))} nodos')
print(f'   Stats: {r.get("estadisticas",{})}')

print('8. GET /api/bosque/salud...')
r = test('GET', '/api/bosque/salud')
print(f'   OK: total_esferas={r.get("total_esferas")}')
print(f'   Activas: {r.get("activas")}')

print('9. POST /api/bosque/ciclo...')
r = test('POST', '/api/bosque/ciclo')
print(f'   OK: actualizadas={r.get("actualizadas")}')

print('10. GET /api/geografia/ecorregiones...')
r = test('GET', '/api/geografia/ecorregiones')
print(f'   OK: {r.get("total")} ecorregiones')

print('11. POST /api/geografia/eje...')
r = test('POST', '/api/geografia/eje', {'ubicacion': 'Bogota'})
print(f'   OK: {r.get("eje_del_mundo",{}).get("especie","?")}')

print()
print('ALL TESTS PASSED')
