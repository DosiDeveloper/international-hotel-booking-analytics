# Guía para empezar - Errores comunes en desarrollo

---

## 1. Antes de empezar (Configuración)

### 1.1 Crear entorno virtual SIEMPRE

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 1.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 1.3 Verificar que el código corre

```bash
python .\src\setup.py
```

**Regla de oro:** Si no corre localmente, no commitees.

---

## 2. Errores Comunes en Python

| Error                     | Causa                       | Solución                  |
| ------------------------- | --------------------------- | ------------------------- |
| `ModuleNotFoundError`     | Falta instalar paquete      | `pip install <paquete>`   |
| `IndentationError`        | Espacios mezclados con tabs | Usar solo 4 espacios      |
| `TypeError: argument`     | Argumentos incorrectos      | Revisar función           |
| `KeyError`                | Key que no existe           | Usar `.get()` o verificar |
| `ValueError: truth value` | Comparar Series pandas      | Usar `.any()` o `.all()`  |
| `SettingWithCopyWarning`  | Modificar vista vs copia    | Usar `.loc[]`             |
| `MemoryError`             | Dataset muy grande          | Procesar por chunks       |
| `UnicodeDecodeError`      | Encoding incorrecto         | `encoding='utf-8'`        |
| `AttributeError`          | Método no existe            | Verificar documentación   |
| `FileNotFoundError`       | Archivo no encontrado       | Verificar ruta            |

**Ejemplo de error común:**

```python
# ❌ MAL
valores = [1, 2, 3]
print(valores[5])  # IndexError

# ✅ BIEN
if len(valores) > 5:
    print(valores[5])
```

---

## 3. Errores Comunes en SQL

| Error                        | Causa                   | Solución                      |
| ---------------------------- | ----------------------- | ----------------------------- |
| `no such table`              | Tabla no existe         | Verificar nombre y conexión   |
| `column mismatch`            | Columnas incorrectas    | Verificar INSERT              |
| `FOREIGN KEY constraint`     | Violación de integridad | Verificar datos referenciados |
| `near "WHERE": syntax error` | Falta WHERE             | Siempre incluir WHERE         |
| `unrecognized token`         | Comillas incorrectas    | Usar comillas simples         |

**Ejemplo peligroso:**

```sql
-- ❌ MAL: Borra TODO
DELETE FROM ventas;

-- ✅ BIEN: Borra solo lo que necesitas
DELETE FROM ventas WHERE id = 123;
```

---

## 4. Errores Comunes en Git

| Error                         | Causa                    | Solución                               |
| ----------------------------- | ------------------------ | -------------------------------------- |
| `fatal: not a git repository` | No inicializado          | `git init`                             |
| `rejected (non-fast-forward)` | Commits pendientes       | `git pull --rebase`                    |
| `merge conflict`              | Cambios en misma línea   | Resolver y `git add .`                 |
| `fatal: refusing to merge`    | Historial no relacionado | `git pull --allow-unrelated-histories` |
| `error: pathspec 'X'`         | Rama no existe           | Verificar nombre                       |
| `dirty working tree`          | Cambios sin commit       | `git stash` o `git commit`             |

**Reglas de oro:**

1. Nunca hacer `git push --force` a `main`
2. Siempre sincronizar antes de trabajar: `git pull --rebase origin main`
3. Commits pequeños y descriptivos

---

## 5. Errores Comunes en Streamlit

| Error                   | Causa                   | Solución                           |
| ----------------------- | ----------------------- | ---------------------------------- |
| Página se recarga       | Session state mal usado | Usar `st.session_state`            |
| Widget no retiene valor | No inicializar estado   | `if 'key' not in st.session_state` |
| Gráfico no aparece      | Falta `st.pyplot()`     | Agregar después de figura          |
| Imports circulares      | Dependencias cruzadas   | Reorganizar imports                |

**Ejemplo de session_state:**

```python
import streamlit as st

# ✅ BIEN: Inicializar una vez
if 'contador' not in st.session_state:
    st.session_state.contador = 0

if st.button("Sumar"):
    st.session_state.contador += 1

st.write(f"Contador: {st.session_state.contador}")
```

---

## 6. Errores Comunes en PowerBI (.pbip)

| Error                           | Causa                 | Solución                  |
| ------------------------------- | --------------------- | ------------------------- |
| Archivo no abre                 | Edición externa       | Editar en PowerBI Desktop |
| `localSettings.json` conflictos | No está en .gitignore | Agregar a .gitignore      |
| Encoding incorrecto             | BOM en archivos       | Guardar UTF-8 sin BOM     |
| No se actualiza                 | No guardar            | Guardar antes de commit   |

**Estructura .pbip:**

```
powerbi/
├── MiReporte.Report/
│   └── definition.pbir
├── MiReporte.SemanticModel/
│   ├── definition.pbism
│   └── .pbi/
│       ├── localSettings.json  ← AGREGAR A .gitignore
│       └── cache.abf           ← AGREGAR A .gitignore
└── MiReporte.pbip
```

> En caso de que no este en el .gitignore

**.gitignore para PowerBI:**

```
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

---

## 7. Buenas Prácticas Generales

- **LEER EL ERROR** antes de preguntar - el 90% dice qué está mal
- **Google/Stack Overflow** primero - casi todo está documentado
- **Uso de IA** usar con cuidado
- **No copiar código** sin entenderlo
- **Commits pequeños** - 1 cambio lógico por commit (ver sección 9.4)
- **Nombres descriptivos** - `calcular_media` no `funcion1`

### Commits Atómicos — Un commit = Un cambio lógico

No hagas "todo lo que hice hoy" en un solo commit. Cada commit debe representar **un único cambio funcional**. Si algo falla, es fácil revertir solo ese paso.

**Formato:** `[tipo]: Descripción en imperativo`

✅ **Ejemplos de excelentes commits:**

- `feat: crear tabla DDL inicial para dim_tiempo`
- `fix: corregir cálculo de media en métricas`
- `limpieza: imputar valores nulos en cuestionario de hábitos`
- `app: integrar gráfico de distribución de frecuencias en Streamlit`
- `docs: actualizar diccionario de variables en el README`

❌ **Prohibidos (serán rechazados en el PR):**

- `subiendo avances`
- `terminé la tabla`
- `cambios varios en el eda`
- `fix`

**Ejemplo:**

```python
# ❌ MAL: Hardcodeado
precio = 100 * 1.16

# ✅ BIEN: Con variable
TASA_IMPUESTO = 0.16
precio = 100 * (1 + TASA_IMPUESTO)
```

---

## 8. Cómo Pedir Ayuda (Template)

```markdown
## Contexto

¿Qué estabas intentando hacer?

## Error
```

pegar mensaje de error completo

````

## Lo que intenté
- Opción 1
- Opción 2

## Código relevante
```python
# pegar solo el código que falla
````

## Pregunta específica

¿Qué estoy haciendo mal?

````

---

## 9. Guía Rápida de Git - GitHub Flow

**Regla de oro:** Nunca trabajar directamente sobre `main`. La rama `main` es sagrada y solo contiene código revisado que funciona.

### Flujo paso a paso
1. Actualiza tu rama local: `git pull origin main`
2. Crea una rama nueva para tu tarea
3. Trabaja y haz commits atómicos
4. Sube tu rama: `git push origin nombre-rama`
5. Abre un Pull Request para revisión

### Convención de nombres de rama

Usa el formato: `tipo/nombre-descriptivo`

| Tipo | Cuándo usar |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de error |
| `sql` | Cambios en esquemas o consultas |
| `limpieza` | Procesamiento y transformación de datos |
| `app` | Cambios en la aplicación Streamlit |
| `docs` | Documentación |

**Ejemplos:**
- `feat/agregar-filtro-fecha`
- `sql/crear-dim-tiempo`
- `limpieza/imputar-nulos-cuestionario`
- `app/sidebar-streamlit-filtros`
- `fix/bug-nulos-distribucion`

### 9.1 Por Consola

| Comando | Qué hace |
|---------|----------|
| `git branch` | Ver ramas existentes |
| `git branch -a` | Ver todas las ramas |
| `git checkout nombre-rama` | Cambiar a rama |
| `git checkout -b nombre-rama` | Crear y cambiar a rama nueva |
| `git switch nombre-rama` | Cambiar de rama (moderno) |
| `git switch -c nombre-rama` | Crear y cambiar (moderno) |

**Flujo típico:**
```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear tu rama con el formato tipo/nombre
git checkout -b feat/agregar-filtro-fecha

# 3. Trabajar y commitear
git add .
git commit -m "feat: agregar filtro de fechas al dashboard"

# 4. Push de tu rama
git push origin feat/agregar-filtro-fecha
````

### 9.2 En VSCode

| Acción          | Cómo                                            |
| --------------- | ----------------------------------------------- |
| Ver rama actual | Barra de estado abajo a la izquierda            |
| Cambiar de rama | Click en nombre de rama → seleccionar otra      |
| Crear rama      | Click en nombre → "Create new branch"           |
| Fetch/Pull      | Command Palette (`Ctrl+Shift+P`) → "Git: Fetch" |

**Atajos útiles:**

- `Ctrl+Shift+P` → Command Palette
- `Ctrl+Shift+G` → Panel Source Control
- `Ctrl+Enter` → Commit

### 9.3 Errores Comunes al Cambiar de Ramas

| Error                                                | Solución                             |
| ---------------------------------------------------- | ------------------------------------ |
| `Your local changes would be overwritten`            | `git stash` antes de cambiar         |
| `The following untracked files would be overwritten` | `git clean -fd` o mover archivo      |
| `fatal: Invalid reference`                           | Verificar nombre con `git branch -a` |

**Flujo seguro:**

```bash
git status              # Verificar cambios
git stash               # Guardar cambios (opcional)
git checkout main       # Cambiar
# ... trabajar ...
git checkout mi-rama    # Volver
git stash pop           # Recuperar cambios
```

### 9.4 Cómo Dividir una Tarea en Múltiples Commits

No hagas todo en un solo commit gigante. Ejemplo: si te asignan crear una tabla del modelo dimensional, divide tu trabajo en commits lógicos:

1. **Commit 1:** `sql: crear tabla DDL inicial para dim_estudiante`
2. **Commit 2:** `sql: añadir primary keys y constraints a dim_estudiante`
3. **Commit 3:** `sql: crear script INSERT para poblar dim_estudiante`
4. **Commit 4:** `limpieza: estandarizar variables cualitativas del dataset`
5. **Commit 5:** `docs: comentar decisiones de limpieza en el código`

Cada commit es un paso que puede revisarse por separado y revertirse sin romper todo.

---

## 10. Funciones y Módulos para Principiantes

### 10.1 ¿Qué es una Función?

Una función es como una **receta de cocina**: tiene un nombre, ingredientes (parámetros) y te da un resultado.

```python
def saludar(nombre):
    return f"Hola, {nombre}!"

mensaje = saludar("Ana")
print(mensaje)  # → "Hola, Ana!"
```

**Partes de una función:**

```
def  saludar  (nombre):
│    │        │       │
│    │        │       └── cuerpo (indentado)
│    │        └── parámetros (inputs)
│    └── nombre
└── "def" (define)
```

### 10.2 Tipos de Parámetros

```python
# Obligatorios
def sumar(a, b):
    return a + b
sumar(3, 5)  # → 8

# Con valor por defecto
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}!"
saludar("Ana")           # → "Hola, Ana!"
saludar("Ana", "Buenos días")  # → "Buenos días, Ana!"

# Con nombre
crear_usuario(nombre="Ana", edad=25, email="a@b.com")

# *args (valores variables)
def sumar_todos(*numeros):
    return sum(numeros)
sumar_todos(1, 2, 3, 4)  # → 10

# **kwargs (valores con nombre variables)
def crear_perfil(**datos):
    return datos
crear_perfil(nombre="Ana", edad=25)  # → {"nombre": "Ana", "edad": 25}
```

### 10.3 ¿Qué es un Módulo?

Un módulo es una **caja de herramientas** que agrupa funciones relacionadas.

**Crear módulo (`utils.py`):**

```python
def calcular_media(lista):
    return sum(lista) / len(lista)

def calcular_mediana(lista):
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)
    if n % 2 == 0:
        return (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2
    return lista_ordenada[n//2]
```

**Usar el módulo (`main.py`):**

```python
import utils
media = utils.calcular_media([1, 2, 3, 4, 5])

# O importar funciones específicas
from utils import calcular_media, calcular_mediana
```

### 10.4 ¿Qué es `__init__.py`?

El archivo `__init__.py` le dice a Python que una carpeta es un **paquete** (un módulo que contiene otros módulos).

**Sin `__init__.py`:**

```
src/
├── data/
│   └── utils.py    ← Python no reconoce "data" como paquete
```

```python
from src.data import utils  # ❌ Error: No module named 'src'
```

**Con `__init__.py`:**

```
src/
├── __init__.py     ← Hace que "src" sea un paquete
├── data/
│   ├── __init__.py ← Hace que "data" sea un paquete
│   └── utils.py
```

```python
from src.data import utils  # ✅ Funciona
from src.data.utils import calcular_media  # ✅ Funciona
```

**Qué poner en `__init__.py`:**

```python
# Opción 1: Archivo vacío (solo marca la carpeta como paquete)

# Opción 2: Exportar funciones principales
from .utils import calcular_media, calcular_mediana

# Ahora puedes importar así:
# from src.data import calcular_media
```

**Ejemplo completo:**

```
hotel-analisis/
├── src/
│   ├── __init__.py          # Vacío o con imports
│   ├── data/
│   │   ├── __init__.py      # from .utils import *
│   │   └── utils.py
│   └── oltp/
│       ├── __init__.py
│       └── connection.py
└── main.py
```

```python
# main.py
from src.data import calcular_media  # Funciona gracias a __init__.py
from src.oltp.connection import get_sqlite_connection
```

### 10.5 Estructura de Módulos en un Proyecto

```
hotel-analisis/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   ├── oltp/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── queries.py
│   └── olap/
│       ├── __init__.py
│       ├── connection.py
│       └── queries.py
└── main.py
```

**Uso en `main.py`:**

```python
from src.data.extract import extract_csv
from src.data.transform import clean_data
from src.oltp.connection import get_sqlite_connection

df = extract_csv("data/raw/hotels.csv")
df_limpio = clean_data(df)
conn = get_sqlite_connection("db/hotel.db")
```

### 10.6 Errores Comunes

| Error                                | Causa                            | Solución                   |
| ------------------------------------ | -------------------------------- | -------------------------- |
| `ModuleNotFoundError`                | Falta `__init__.py` o import mal | Verificar estructura       |
| `ImportError: cannot import name`    | Nombre incorrecto                | Verificar nombre en módulo |
| `NameError: name 'X' is not defined` | No se importó                    | Agregar import             |
| `TypeError: takes N arguments`       | Número incorrecto de args        | Revisar función            |

### 10.7 Ejemplo Práctico

**`src/data/utils.py`:**

```python
import pandas as pd

def cargar_csv(ruta, separador=","):
    return pd.read_csv(ruta, sep=separador)

def limpiar_nulos(df, estrategia="eliminar"):
    if estrategia == "eliminar":
        return df.dropna()
    return df.fillna(0)

def obtener_estadisticas(df, columna):
    return {
        "media": df[columna].mean(),
        "mediana": df[columna].median(),
        "minimo": df[columna].min(),
        "maximo": df[columna].max()
    }
```

**`src/data/__init__.py`:**

```python
from .utils import cargar_csv, limpiar_nulos, obtener_estadisticas
```

**`main.py`:**

```python
from src.data import cargar_csv, limpiar_nulos, obtener_estadisticas

df = cargar_csv("data/hotels.csv")
df_limpio = limpiar_nulos(df)
stats = obtener_estadisticas(df_limpio, "precio")
print(stats)
```

---

## 11. Cómo Hacer un Pull Request en GitHub

Un Pull Request (PR) es la forma de proponer tus cambios para que sean revisados y añadidos a `main`.

### 11.1 Desde GitHub Desktop

1. Commit y push de tus cambios en la rama
2. Haz clic en **"Publish branch"** o **"Push origin"** si la rama ya existe
3. Haz clic en **"Create Pull Request"** → se abre GitHub en el navegador
4. Completa título, descripción y crea el PR

```
GitHub Desktop
├── Pestaña "Changes" → Commit
├── Botón "Push origin"
└── Botón "Create Pull Request" → abre el navegador
```

### 11.2 Desde VSCode

**Opción A — Panel Source Control:**

1. Abre el panel Source Control (`Ctrl+Shift+G`)
2. Escribe tu mensaje de commit y haz clic en **"Commit"**
3. Haz clic en **"Publish Branch"** o sincroniza con el botón de sync
4. En la barra de estado inferior, haz clic en el nombre de la rama → **"Create Pull Request"**

**Opción B — Command Palette:**

1. `Ctrl+Shift+P` → escribe **"GitHub: Create Pull Request"**
2. Completa título y descripción

**Opción C — Extensión GitHub Pull Requests:**

1. Instala la extensión **GitHub Pull Requests** desde el marketplace
2. En el panel lateral verás la sección "Pull Requests"
3. Haz clic en **"+"** → **"Create Pull Request"**

### 11.3 Desde la interfaz web de GitHub

1. Después de hacer push, ve al repositorio en GitHub
2. Aparecerá un banner amarillo: **"Compare & pull request"** → haz clic
3. Completa el formulario:

| Campo           | Qué poner                                                        |
| --------------- | ---------------------------------------------------------------- |
| **Title**       | `tipo: descripción corta` (ej: `feat: agregar filtro de fechas`) |
| **Description** | Qué hiciste, por qué, cómo probarlo                              |
| **Reviewers**   | Selecciona al menos 1 revisor                                    |
| **Assignees**   | Tu nombre                                                        |

4. Haz clic en **"Create pull request"**

**Draft PR:** Si el trabajo está en progreso, marca **"Create draft pull request"** para que se sepa que aún no está listo para revisión.

### 11.4 Qué poner en título y descripción

**Título — formato del proyecto:**

```
> Esto es una formalidad o metodologia estandar que se usa si desean usarlo bienvenido sea pero por favor hagan una buena descripcion de lo que hicieron
tipo: descripción del cambio
```

| Tipo       | Cuándo usar                 |
| ---------- | --------------------------- |
| `feat`     | Nueva funcionalidad         |
| `fix`      | Corrección de error         |
| `data`     | Cambios en datos o fuente   |
| `refactor` | Reestructurar código        |
| `chore`    | Configuración, dependencias |

**Descripción — template:**

```markdown
## Qué se hizo

Descripción breve del cambio

## Por qué

Motivo del cambio

## Cómo probarlo

1. Paso 1
2. Paso 2

## Screenshots (si aplica)

pegar imagen
```

### 11.5 Después de crear el PR

1. **Espera la revisión** — el Senior revisará tu código
2. **Si piden cambios** → edita en tu rama, haz push y el PR se actualiza solo
3. **Cuando se apruebe** → se hace **Squash and Merge** (queda un solo commit limpio en `main`)
4. **Elimina la rama** después del merge

### 11.6 Checklist antes de pedir revisión

- [ ] Código SQL es idempotente (usa `DROP TABLE IF EXISTS`)
- [ ] No se suben archivos de datos reales a Git (`.gitignore` respetado)
- [ ] Código de Streamlit corre localmente sin errores en el entorno virtual
- [ ] Commits son atómicos y tienen mensajes descriptivos
- [ ] Rama está actualizada con `main` (`git pull --rebase origin main`)

### 11.7 Errores comunes

| Error               | Causa                         | Solución                                        |
| ------------------- | ----------------------------- | ----------------------------------------------- |
| Rama desactualizada | `main` tiene cambios nuevos   | `git pull --rebase origin main` y vuelve a push |
| Conflictos de merge | Otro cambió lo mismo          | Resolver en el editor, `git add .`, push        |
| No puede hacer push | Rama protegida o sin permisos | Verificar que estás en tu rama                  |

**Rama desactualizada — paso a paso:**

```bash
git checkout mi-rama
git pull --rebase origin main
# Resolver conflictos si aparecen
git push origin mi-rama
```

---

## Resumen Rápido

| Sección      | Punto Clave                                                                     |
| ------------ | ------------------------------------------------------------------------------- |
| Python       | Leer error, buscar solución, no hardcodear                                      |
| SQL          | Siempre WHERE en UPDATE/DELETE                                                  |
| Git          | GitHub Flow, rama `tipo/nombre`, commits atómicos                               |
| Streamlit    | Usar session_state para estado                                                  |
| PowerBI      | Guardar como .pbip, .gitignore para cache                                       |
| Funciones    | Una función = una tarea                                                         |
| Módulos      | `__init__.py` = carpeta es paquete                                              |
| Pull Request | Checklist: idempotente, .gitignore, Streamlit corre, 1 aprobación, squash merge |
