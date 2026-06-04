import urllib.request, json, sys

BASE = "http://localhost:5000"

def post(path, data, headers=None, timeout=10):
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode(),
        headers=hdrs
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except Exception:
            body = {"error": "parse error"}
        return e.code, body
    except Exception as e:
        return 0, {"error": str(e)}

# Test 1: proyecto/nuevo rate limit (5/hr)
print("=== Test 1: proyecto/nuevo (5/hr) ===")
for i in range(8):
    status, data = post("/api/proyecto/nuevo", {"nombre": "spam"}, timeout=5)
    if status == 429:
        print(f"[429] req {i+1}: retry_after={data.get('retry_after')}")
        break
    print(f"[{status}] req {i+1}: ok" if status == 200 else f"[{status}] req {i+1}: {data}")

# Test 2: validar que consultar con mensaje vacio da 400
print("\n=== Test 2: consultar sin mensaje ===")
status, data = post("/api/consultar", {}, timeout=5)
print(f"[{status}] {data}")

# Test 3: validar mensaje demasiado largo
print("\n=== Test 3: mensaje demasiado largo ===")
status, data = post("/api/consultar", {"mensaje": "x" * 5000}, timeout=5)
print(f"[{status}] {data}")

# Test 4: validar JSON invalido
print("\n=== Test 4: JSON invalido en consultar ===")
import http.client
conn = http.client.HTTPConnection("localhost", 5000, timeout=5)
conn.request("POST", "/api/consultar", body="not json", headers={"Content-Type": "application/json"})
resp = conn.getresponse()
body = json.loads(resp.read().decode())
print(f"[{resp.status}] {body}")
conn.close()

# Test 5: 404 handler
print("\n=== Test 5: ruta inexistente ===")
status, data = post("/api/noexiste", {})
print(f"[{status}] {data}")

print("\n=== PASO: Todos los tests de seguridad completados ===")
