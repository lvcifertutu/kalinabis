"""Bibliotecario — revisor de formato para los libros de la Biblioteca.

Reglas de formato grimorio:
  1. Primera línea no vacía es un título '#'
  2. El título está en MAYÚSCULAS
  3. Tiene al menos una sección '##'
  4. Tiene sección '## FUENTES' al final
  5. Tiene al menos un separador '---'
"""

from pathlib import Path
from dataclasses import dataclass, field


BIBLIOTECA_PATH = Path(__file__).parent.parent / "biblioteca"

REGLAS = [
    "titulo_presente",
    "titulo_mayusculas",
    "secciones_presentes",
    "fuentes_presentes",
    "separadores_presentes",
]

NOMBRES_REGLAS = {
    "titulo_presente":     "Tiene título '#'",
    "titulo_mayusculas":   "Título en MAYÚSCULAS",
    "secciones_presentes": "Tiene secciones '##'",
    "fuentes_presentes":   "Tiene sección FUENTES",
    "separadores_presentes": "Tiene separadores '---'",
}


@dataclass
class ResultadoArchivo:
    ruta: Path
    checks: dict[str, bool] = field(default_factory=dict)

    @property
    def nombre(self) -> str:
        return self.ruta.name

    @property
    def ok(self) -> bool:
        return all(self.checks.values())

    @property
    def faltantes(self) -> list[str]:
        return [r for r, v in self.checks.items() if not v]


def revisar_archivo(ruta: Path) -> ResultadoArchivo:
    resultado = ResultadoArchivo(ruta=ruta)
    try:
        texto = ruta.read_text(encoding="utf-8")
    except Exception:
        for r in REGLAS:
            resultado.checks[r] = False
        return resultado

    lineas = texto.splitlines()
    lineas_no_vacias = [l for l in lineas if l.strip()]

    # Regla 1: primera línea no vacía es título '#'
    primera = lineas_no_vacias[0] if lineas_no_vacias else ""
    tiene_titulo = primera.startswith("# ")
    resultado.checks["titulo_presente"] = tiene_titulo

    # Regla 2: título en mayúsculas
    if tiene_titulo:
        texto_titulo = primera[2:].strip()
        resultado.checks["titulo_mayusculas"] = texto_titulo == texto_titulo.upper()
    else:
        resultado.checks["titulo_mayusculas"] = False

    # Regla 3: al menos una sección '##'
    resultado.checks["secciones_presentes"] = any(
        l.startswith("## ") for l in lineas
    )

    # Regla 4: sección '## FUENTES'
    resultado.checks["fuentes_presentes"] = any(
        l.strip().upper().startswith("## FUENTES") for l in lineas
    )

    # Regla 5: al menos un separador '---'
    resultado.checks["separadores_presentes"] = any(
        l.strip() == "---" for l in lineas
    )

    return resultado


def revisar_biblioteca(base: Path = BIBLIOTECA_PATH) -> list[ResultadoArchivo]:
    archivos = sorted(base.rglob("*.md"))
    return [revisar_archivo(a) for a in archivos if a.name != "README.md"]


def reporte_texto(resultados: list[ResultadoArchivo]) -> str:
    lineas = []
    ok = sum(1 for r in resultados if r.ok)
    total = len(resultados)

    lineas.append(f"BIBLIOTECA — {ok}/{total} libros en formato correcto\n")
    lineas.append("─" * 50)

    for res in resultados:
        estado = "✓" if res.ok else "✗"
        lineas.append(f"\n{estado} {res.nombre}")
        for regla, pasó in res.checks.items():
            icono = "  ✓" if pasó else "  ✗"
            lineas.append(f"{icono}  {NOMBRES_REGLAS[regla]}")

    lineas.append("\n" + "─" * 50)
    if ok == total:
        lineas.append("Todo en orden.")
    else:
        pendientes = total - ok
        lineas.append(f"{pendientes} libro(s) necesitan trabajo.")

    return "\n".join(lineas)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    resultados = revisar_biblioteca()
    print(reporte_texto(resultados))
