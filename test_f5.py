import urllib.request, json, http.client, sys

BASE = "http://localhost:5000"

def post(path, data, headers=None, timeout=5):
    hdrs = {"Content-Type": "application/json"}
    if headers: hdrs.update(headers)
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(), headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except:
            return e.code, {}
    except Exception as e:
        print(f"  [EXCEPTION] {path}: {e}")
        return 0, {}

ok = 0
fail = 0

def check(name, got, expected, extra=""):
    global ok, fail
    if got == expected:
        ok += 1
        print(f"  [OK] {name}")
    else:
        fail += 1
        print(f"  [FAIL] {name}: esperado={expected} recibido={got} {extra}")

# 1. Create project
s, d = post("/api/proyecto/nuevo", {"nombre": "test"})
codigo = d.get("codigo", "")
check("crear proyecto", s, 200)
if s != 200:
    sys.exit(1)
print(f"  codigo={codigo[:20]}...")

H = {"X-Project-Code": codigo, "Content-Type": "application/json"}

# 2. Validaciones basicas
check(*post("/api/consultar", {}, H), 400, "(sin mensaje)")
check(*post("/api/consultar", {"mensaje": "x" * 5000}, H), 400, "(mensaje largo)")

# 3. 404
req = urllib.request.Request(BASE + "/api/noexiste")
try:
    r = urllib.request.urlopen(req, timeout=5)
    check("ruta 404", r.status, 404)
except urllib.error.HTTPError as e:
    check("ruta 404", e.code, 404)

# 4. POST a GET-only
req2 = urllib.request.Request(BASE + "/api/esferas", data=json.dumps({}).encode(), headers=H, method="POST")
try:
    r = urllib.request.urlopen(req2, timeout=5)
    check("POST GET-only", r.status, 405)
except urllib.error.HTTPError as e:
    check("POST GET-only", e.code, 405)

# 5. JSON invalido en body (Flask 400)
conn = http.client.HTTPConnection("localhost", 5000, timeout=5)
conn.request("POST", "/api/consultar", body="no-json", headers=H)
r = conn.getresponse()
r.read()
conn.close()
check("JSON no valido", r.status, 400)

# 6. Grimorio validacion
check(*post("/api/grimorio", {"titulo": "x" * 500, "contenido": "test"}, H), 400)
check(*post("/api/grimorio", {"titulo": "ok", "contenido": "x" * 20000}, H), 400)

# 7. Sigilo validacion
check(*post("/api/sigilo", {"intencion": "x" * 500, "imagen": "test"}, H), 400)

print(f"\n=== {ok}/{ok+fail} tests OK ===")
