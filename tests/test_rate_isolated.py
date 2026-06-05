import time, threading
from collections import defaultdict

lock = threading.Lock()
data = defaultdict(list)

def check(key, ventana, max_req):
    ahora = time.time()
    with lock:
        ts = data[key]
        cutoff = ahora - ventana
        data[key] = [t for t in ts if t > cutoff]
        if len(data[key]) >= max_req:
            return False, int(ventana - (ahora - data[key][0])) + 1
        data[key].append(ahora)
        return True, 0

for i in range(8):
    ok, retry = check('test:proyecto', 3600, 5)
    dlen = len(data['test:proyecto'])
    print(f'{i}: ok={ok} retry={retry} len={dlen}')
    if not ok:
        break
print('OK - rate limiter works in isolation')
