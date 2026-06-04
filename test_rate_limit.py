import urllib.request, json

BASE = "http://localhost:5000"

def post(path, data, headers=None):
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode(),
        headers=hdrs
    )
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except Exception:
            body = {"error": "parse error"}
        return e.code, body

# Probar rate limit en proyecto/nuevo (5/hr)
for i in range(8):
    status, data = post("/api/proyecto/nuevo", {"nombre": "spam"})
    if status == 429:
        print(f"[429] request {i+1}: {data}")
        break
    print(f"[{status}] request {i+1}: {data.get('codigo','')[:20] if status==200 else data}")

# Probar rate limit en consultar sin proyecto real (deberia devolver 401)
print("---")
for i in range(15):
    status, data = post("/api/consultar", {"mensaje": "ping"}, {"X-Project-Code": "fakefake"})
    if status == 429:
        print(f"[429] consultar {i+1}: {data}")
        break
    if i == 14:
        print(f"[{status}] consultar {i+1}: {data} (rate limit DID NOT fire!)")
    elif i > 8:
        print(f"[{status}] consultar {i+1}: {data}")
