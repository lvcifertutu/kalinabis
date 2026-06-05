import urllib.request, json, http.client, sys

BASE = "http://localhost:5000"

def post(path, data, headers=None, timeout=8):
    hdrs = {"Content-Type": "application/json"}
    if headers: hdrs.update(headers)
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(), headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        body = json.loads(resp.read().decode())
        print(f"POST {path} -> {resp.status}", flush=True)
        return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except:
            body = {}
        print(f"POST {path} -> {e.code} ERR", flush=True)
        return e.code, body
    except Exception as e:
        print(f"POST {path} -> EXCEPTION: {e}", flush=True)
        return 0, {}

print("step1: crear proyecto", flush=True)
s, d = post("/api/proyecto/nuevo", {"nombre": "test"})
codigo = d.get("codigo", "")
if not codigo:
    print("NO PROJECT CODE", flush=True)
    sys.exit(1)
print(f"codigo={codigo[:20]}", flush=True)

H = {"X-Project-Code": codigo, "Content-Type": "application/json"}

print("step2: tests rapidos", flush=True)
post("/api/consultar", {}, H)
post("/api/consultar", {"mensaje": "x" * 5000}, H)

import urllib.request as ureq
u2 = ureq.Request(BASE + "/api/noexiste")
try:
    r = ureq.urlopen(u2, timeout=5)
    print(f"GET /api/noexiste -> {r.status}", flush=True)
except urllib.error.HTTPError as e:
    print(f"GET /api/noexiste -> {e.code}", flush=True)

post("/api/grimorio", {"titulo": "x" * 500, "contenido": "test"}, H)
post("/api/grimorio", {"titulo": "ok", "contenido": "x" * 20000}, H)
post("/api/sigilo", {"intencion": "x" * 500, "imagen": "test"}, H)

print("step3: rate limit proyecto", flush=True)
for i in range(6):
    s, d = post("/api/proyecto/nuevo", {"nombre": "spam"}, H)
    if s == 429:
        print(f"RATE LIMITED en intento {i+2} (429)", flush=True)
        break
else:
    print("NUNCA RATE LIMITED", flush=True)

print("END", flush=True)
