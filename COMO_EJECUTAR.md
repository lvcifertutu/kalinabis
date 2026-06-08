# KALINABIS FASE 1 — CÓMO EJECUTAR

## ✅ OPCIÓN 1: Batch File (RECOMENDADO para Windows)

Simplemente **doble-click en `run-dev.bat`**

```
C:\grimorio\run-dev.bat
```

Esto:
1. Mata procesos previos en puertos 5000 y 3000-3001
2. Abre 2 ventanas CMD nuevas:
   - Una con Flask Backend (puerto 5000)
   - Una con Next.js Frontend (puerto 3001+)

**URL para acceder:** http://localhost:3001 (o 3002, 3003 si están ocupados)

---

## ✅ OPCIÓN 2: Manual en CMD (2 ventanas)

### Ventana 1 - Backend:
```cmd
cd C:\grimorio
python servidor.py
```

### Ventana 2 - Frontend:
```cmd
cd C:\grimorio
npm run dev
```

Espera a que diga "Ready in X.Xs" en la ventana de Frontend.

**URL:** http://localhost:3001+

---

## ✅ OPCIÓN 3: PowerShell (si quieres solucionar restricciones)

Si quieres usar PowerShell sin restricciones:

```powershell
# Una sola vez (ejecutar como Admin):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego:
.\run-dev.ps1
```

---

## 🔍 VERIFICACIÓN

Cuando todo esté listo, deberías ver:

**Backend (puerto 5000):**
```
Serving Flask app 'servidor'
Running on http://127.0.0.1:5000
```

**Frontend (puerto 3001+):**
```
▲ Next.js 14.2.3
- Local: http://localhost:3001
✓ Ready in X.Xs
```

---

## 🌐 ACCEDER

1. Abre navegador: **http://localhost:3001**
2. Verás **splash screen** (3.5 segundos)
3. Luego: **ALTAR cyberpunk** con:
   - Chat (izquierda)
   - Terminal (derecha)
   - Selector de deidades en header

---

## ❌ PROBLEMAS COMUNES

### "Puerto ya en uso"
```cmd
REM Mata procesos en puerto 5000:
netstat -ano | find ":5000"
taskkill /pid <PID> /f

REM O simplemente ejecuta run-dev.bat (lo hace automático)
```

### "npm: comando no encontido"
- Instala Node.js desde https://nodejs.org/
- Reinicia CMD
- Corre `npm install` en C:\grimorio

### "Python no encontrado"
- Instala Python desde https://python.org/
- **Marca "Add Python to PATH"**
- Reinicia CMD

### PowerShell "cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Luego: .\run-dev.ps1
```

---

## 📝 NOTAS

- **Los logs aparecen en las ventanas CMD** — no cierres hasta que termines
- Para **detener todo**: cierra ambas ventanas CMD
- **Puerto 3000 ocupado?** Next.js intenta 3001, 3002, 3003... (automático)
- **Primera ejecución lenta**: npm install + next build toma tiempo

---

**¿Problemas?** Usa **OPCIÓN 1 (run-dev.bat)** — es la más confiable en Windows.
