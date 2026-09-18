# Guía de Contribución

## Estructura del Proyecto

| Carpeta/Archivo | Propósito |
|-----------------|-----------|
| `data/raw/` | Datos originales (CSV, TSV) descargados del servicio externo |
| `sql/oltp/` | Esquema y consultas de la base transaccional (SQLite3) |
| `sql/olap/` | Modelo dimensional y vistas analíticas (DuckDB) |
| `src/data/` | Código de extracción, transformación y carga de datos |
| `src/oltp/` | Capa transaccional — conexiones y consultas SQLite3 |
| `src/olap/` | Capa analítica — conexiones y consultas DuckDB |
| `informe/` | Aplicación Streamlit para informes estadísticos |
| `dashboard/` | Reportes PowerBI (.pbip) y artefactos generados |
| `scripts/` | Utilidades de configuración y ejecución |

## Flujo de Datos

```
Servicio Externo → CSV → SQLite3 (OLTP) → DuckDB (OLAP) → Streamlit/PowerBI
```

1. **Extracción**: Los archivos CSV/TSV se descargan del servicio externo
2. **Ingesta**: Se carga la información a SQLite3 (base transaccional)
3. **Transformación**: Se procesa, limpia y normaliza la información
4. **Carga analítica**: Se materializa en DuckDB para consultas rápidas
5. **Visualización**: Streamlit y PowerBI consumen de DuckDB

## Desarrollo Local

### Configuración inicial
```bash
# Clonar repositorio
git clone <url-repositorio>
cd hotel-analisis

# Crear entorno virtual
python -m venv venv
# Automáticamente VS Code lo activa, si no
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Verificar que el código corre
```bash
python main.py  # o el archivo principal
```

**Regla de oro:** Si no corre localmente, no commitees.

### Configurar bases de datos
```bash
# Inicializar SQLite3 (OLTP)
python scripts/setup_db.py

# Poblar DuckDB (OLAP)
python src/olap/materialize.py
```

### Ejecutar dashboard
```bash
cd dashboard
streamlit run app.py
```

## Flujo de Trabajo (GitHub Flow)

**Regla de oro:** Nunca trabajar directamente sobre `main`. La rama `main` es sagrada y solo contiene código revisado que funciona.

### 1. Convención de ramas

Usa el formato: `nombre-corto-descriptivo`

**Ejemplos:**
- `dashboard-streamlit` → Página de análisis estadístico
- `calculo-metricas` → Implementar métricas descriptivas
- `limpieza-datos-hoteles` → Preparar datos de hoteles
- `agregar-filtro-fecha` → Nueva funcionalidad de filtrado
- `analisis-reviews` → Análisis de reseñas de usuarios

### 2. Crear rama y trabajar
```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear tu rama
git checkout -b nombre-corto-descriptivo

# 3. Trabajar y commitear
git add .
git commit -m "feat: agregar filtro de fechas al dashboard"

# 4. Push de tu rama
git push origin nombre-corto-descriptivo
```

### 3. Commits atómicos — Un commit = Un cambio lógico

No hagas "todo lo que hice hoy" en un solo commit. Cada commit debe representar **un único cambio funcional**. Si algo falla, es fácil revertir solo ese paso.

> Esto es un estándar que se usa, no es obligatorio pero ayuda a entender lo que están haciendo en cada commit sin tener que leer la descripción

**Formato:** `[tipo]: Descripción en imperativo`

**Tipos permitidos:**
| Tipo | Cuándo usar |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de error |
| `data` | Cambios en datos o fuente |
| `refactor` | Reestructurar código sin cambiar comportamiento |
| `chore` | Configuración, dependencias, cosas rutinarias |
| `docs` | Documentación o README |
| `sql` | Cambios en esquemas o consultas |
| `limpieza` | Procesamiento y transformación de datos |
| `informe` | Cambios en la aplicación Streamlit |
| `dashboard` | Cambios en el dashboard de PowerBI |

✅ **Ejemplos de excelentes commits:**
- `feat: crear tabla DDL inicial para dim_tiempo`
- `fix: corregir cálculo de media en métricas`
- `chore: actualice .gitignore para ignorar los archivos del entorno local`
- `limpieza: imputar valores nulos en cuestionario de hábitos`
- `informe: integrar gráfico de distribución de frecuencias en Streamlit`
- `docs: actualizar diccionario de variables en el README`

❌ **Prohibidos (serán rechazados en el PR):**
- `subiendo avances`
- `terminé la tabla`
- `cambios varios en el eda`
- `fix`

> Por favor pongan un título y una descripción acorde

### 4. Dividir tareas en múltiples commits

No hagas todo en un solo commit gigante. Ejemplo: si te asignan crear una tabla del modelo dimensional, divide tu trabajo en commits lógicos:

1. **Commit 1:** `sql: crear tabla DDL inicial para dim_estudiante`
2. **Commit 2:** `sql: añadir primary keys y constraints a dim_estudiante`
3. **Commit 3:** `sql: crear script INSERT para poblar dim_estudiante`
4. **Commit 4:** `limpieza: estandarizar variables cualitativas del dataset`
5. **Commit 5:** `docs: comentar decisiones de limpieza en el código`

Cada commit es un paso que puede revisarse por separado y revertirse sin romper todo.

### 5. Abrir Pull Request

Un Pull Request (PR) es la forma de proponer tus cambios para que sean revisados y añadidos a `main`.

**Desde GitHub Desktop:**
1. Commit y push de tus cambios en la rama
2. Haz clic en **"Publish branch"** o **"Push origin"** si la rama ya existe
3. Haz clic en **"Create Pull Request"** → se abre GitHub en el navegador
4. Completa título, descripción y crea el PR

**Desde VSCode:**
- **Opción A — Panel Source Control:** `Ctrl+Shift+G` → Commit → Publish Branch → clic en nombre de rama → "Create Pull Request"
- **Opción B — Command Palette:** `Ctrl+Shift+P` → "GitHub: Create Pull Request"
- **Opción C — Extensión GitHub Pull Requests:** instalar extensión → panel lateral → "+" → "Create Pull Request"

**Desde la interfaz web de GitHub:**
1. Después de hacer push, ve al repositorio en GitHub
2. Aparecerá un banner amarillo: **"Compare & pull request"** → haz clic
3. Completa el formulario:

| Campo | Qué poner |
|-------|-----------|
| **Title** | `tipo: descripción corta` (ej: `feat: agregar filtro de fechas`) |
| **Description** | Qué hiciste, por qué, cómo probarlo |
| **Reviewers** | Selecciona al menos 1 revisor |
| **Assignees** | Tu nombre |

4. Haz clic en **"Create pull request"**

**Draft PR:** Si el trabajo está en progreso, marca **"Create draft pull request"** para que se sepa que aún no está listo para revisión.

### 6. Qué poner en título y descripción

**Título — formato del proyecto:**
```
tipo: descripción del cambio
```

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

### 7. Checklist antes de pedir revisión

- [ ] Código SQL es idempotente (usa `DROP TABLE IF EXISTS`)
- [ ] No se suben archivos de datos reales a Git (`.gitignore` respetado)
- [ ] Código de Streamlit corre localmente sin errores en el entorno virtual
- [ ] Commits son atómicos y tienen mensajes descriptivos
- [ ] Rama está actualizada con `main` (`git pull --rebase origin main`)

### 8. Después de crear el PR

1. **Espera la revisión** — el Senior revisará tu código
2. **Si piden cambios** → edita en tu rama, haz push y el PR se actualiza solo
3. **Cuando se apruebe** → se hace **Squash and Merge** (queda un solo commit limpio en `main`)
4. **Elimina la rama** después del merge

### 9. Revisión y Merge

- **1 aprobación mínima** para merge
- Usar **Squash and Merge** para mantener historial limpio
- El Senior revisará la lógica y calidad del código

## Estructura del Código

### Funciones de datos (`src/data/`)
```python
def extract_csv(path):
    """Extraer datos desde archivo CSV."""
    pass

def transform(df):
    """Aplicar transformaciones a los datos."""
    pass

def load_to_sqlite(df, table) -> None:
    """Cargar datos a SQLite3."""
    pass
```

### Conexiones a bases (`src/oltp/`, `src/olap/`)
```python
import sqlite3
import duckdb

def get_sqlite_connection(db_path: str) -> sqlite3.Connection:
    """Obtener conexión a SQLite3."""
    return sqlite3.connect(db_path)

def get_duckdb_connection(db_path: str) -> duckdb.DuckDBPyConnection:
    """Obtener conexión a DuckDB."""
    return duckdb.connect(db_path)
```

### Dashboard Streamlit (`dashboard/`)
```python
# dashboard/app.py
import streamlit as st
from utils.data_loader import load_analytics_data

st.title("Informe Estadístico de Investigación")

df = load_analytics_data()
st.dataframe(df)
```

## Convenciones de Código

### Python
- Seguir **PEP 8**
- Usar **type hints**
- Máximo 88 caracteres por línea (Black)

### SQL
- Keywords en MAYÚSCULAS: `SELECT`, `FROM`, `WHERE`
- Tablas en snake_case: `hoteles_resena`
- Columnas en snake_case: `fecha_registro`

### Nomenclatura
```python
# Funciones
def calcular_media():    # snake_case

# Clases
class ProcesadorDatos:   # PascalCase

# Constantes
MAXIMO_REGISTROS = 1000  # UPPER_SNAKE_CASE

# Archivos
mi_modulo.py             # snake_case
```

## Resolución de Conflictos

### Prevención
1. Sincronizar con `main` antes de empezar a trabajar
2. Commits pequeños y atómicos
3. Coordinar cambios en archivos compartidos

### Si ocurre un conflicto
```bash
# 1. Actualizar
git fetch origin
git rebase origin/main

# 2. Resolver conflictos en el editor

# 3. Continuar
git add .
git rebase --continue

# 4. Push
git push --force-with-lease
```

## Errores Comunes

### Python

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError` | Falta instalar paquete | `pip install <paquete>` |
| `IndentationError` | Espacios mezclados con tabs | Usar solo 4 espacios |
| `TypeError: argument` | Argumentos incorrectos | Revisar función |
| `KeyError` | Key que no existe | Usar `.get()` o verificar |
| `ValueError: truth value` | Comparar Series pandas | Usar `.any()` o `.all()` |
| `SettingWithCopyWarning` | Modificar vista vs copia | Usar `.loc[]` |
| `MemoryError` | Dataset muy grande | Procesar por chunks |
| `UnicodeDecodeError` | Encoding incorrecto | `encoding='utf-8'` |
| `AttributeError` | Método no existe | Verificar documentación |
| `FileNotFoundError` | Archivo no encontrado | Verificar ruta |

```python
# ❌ MAL
valores = [1, 2, 3]
print(valores[5])  # IndexError

# ✅ BIEN
if len(valores) > 5:
    print(valores[5])
```

### SQL

| Error | Causa | Solución |
|-------|-------|----------|
| `no such table` | Tabla no existe | Verificar nombre y conexión |
| `column mismatch` | Columnas incorrectas | Verificar INSERT |
| `FOREIGN KEY constraint` | Violación de integridad | Verificar datos referenciados |
| `near "WHERE": syntax error` | Falta WHERE | Siempre incluir WHERE |
| `unrecognized token` | Comillas incorrectas | Usar comillas simples |

```sql
-- ❌ MAL: Borra TODO
DELETE FROM ventas;

-- ✅ BIEN: Borra solo lo que necesitas
DELETE FROM ventas WHERE id = 123;
```

### Git

| Error | Causa | Solución |
|-------|-------|----------|
| `fatal: not a git repository` | No inicializado | `git init` |
| `rejected (non-fast-forward)` | Commits pendientes | `git pull --rebase` |
| `merge conflict` | Cambios en misma línea | Resolver y `git add .` |
| `fatal: refusing to merge` | Historial no relacionado | `git pull --allow-unrelated-histories` |
| `error: pathspec 'X'` | Rama no existe | Verificar nombre |
| `dirty working tree` | Cambios sin commit | `git stash` o `git commit` |

**Reglas de oro:**
1. Nunca hacer `git push --force` a `main`
2. Siempre sincronizar antes de trabajar: `git pull --rebase origin main`
3. Commits pequeños y descriptivos

### Streamlit

| Error | Causa | Solución |
|-------|-------|----------|
| Página se recarga | Session state mal usado | Usar `st.session_state` |
| Widget no retiene valor | No inicializar estado | `if 'key' not in st.session_state` |
| Gráfico no aparece | Falta `st.pyplot()` | Agregar después de figura |
| Imports circulares | Dependencias cruzadas | Reorganizar imports |

```python
import streamlit as st

# ✅ BIEN: Inicializar una vez
if 'contador' not in st.session_state:
    st.session_state.contador = 0

if st.button("Sumar"):
    st.session_state.contador += 1

st.write(f"Contador: {st.session_state.contador}")
```

### PowerBI (.pbip)

| Error | Causa | Solución |
|-------|-------|----------|
| Archivo no abre | Edición externa | Editar en PowerBI Desktop |
| `localSettings.json` conflictos | No está en .gitignore | Agregar a .gitignore |
| Encoding incorrecto | BOM en archivos | Guardar UTF-8 sin BOM |
| No se actualiza | No guardar | Guardar antes de commit |

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

**.gitignore para PowerBI:**
```
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

## Errores Comunes al Cambiar de Ramas

| Error | Solución |
|-------|----------|
| `Your local changes would be overwritten` | `git stash` antes de cambiar |
| `The following untracked files would be overwritten` | `git clean -fd` o mover archivo |
| `fatal: Invalid reference` | Verificar nombre con `git branch -a` |

**Flujo seguro:**
```bash
git status              # Verificar cambios
git stash               # Guardar cambios (opcional)
git checkout main       # Cambiar
# ... trabajar ...
git checkout mi-rama    # Volver
git stash pop           # Recuperar cambios
```

## Errores Comunes en Pull Requests

| Error | Causa | Solución |
|-------|-------|----------|
| Rama desactualizada | `main` tiene cambios nuevos | `git pull --rebase origin main` y vuelve a push |
| Conflictos de merge | Otro cambió lo mismo | Resolver en el editor, `git add .`, push |
| No puede hacer push | Rama protegida o sin permisos | Verificar que estás en tu rama |

**Rama desactualizada — paso a paso:**
```bash
git checkout mi-rama
git pull --rebase origin main
# Resolver conflictos si aparecen
git push origin mi-rama
```

## Buenas Prácticas Generales

- **LEER EL ERROR** antes de preguntar - el 90% dice qué está mal
- **Google/Stack Overflow** primero - casi todo está documentado
- **Uso de IA** usar con cuidado y no **COPIAR Y PEGAR SIN LEER O VER**
- **No copiar código** sin entenderlo
- **Commits pequeños** - 1 cambio lógico por commit
- **Nombres descriptivos** - `calcular_media` no `funcion1`

```python
# ❌ MAL: Hardcodeado
precio = 100 * 1.16

# ✅ BIEN: Con variable
TASA_IMPUESTO = 0.16
precio = 100 * (1 + TASA_IMPUESTO)
```

## Cómo Pedir Ayuda (Template)

```markdown
## Contexto
¿Qué estabas intentando hacer?

## Error
```
pegar mensaje de error completo
```

## Lo que intenté
- Opción 1
- Opción 2

## Código relevante
```python
# pegar solo el código que falla
```

## Pregunta específica
¿Qué estoy haciendo mal?
```

## Comandos Útiles

```bash
# Ver estado
git status

# Ver historial
git log --oneline -10

# Sincronizar
git fetch origin && git rebase origin/main
```

## Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `requirements.txt` | Dependencias Python |
| `config/settings.yaml` | Configuración del proyecto |
