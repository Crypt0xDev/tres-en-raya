# 📁 Estructura del Proyecto - Tres en Raya

## 🏗️ Nueva Arquitectura Organizada

### 📋 Estructura de Carpetas

```
tres-en-raya/
├── 📁 docs/                           # 📚 Documentación del proyecto
│   ├── CHANGELOG.md                   # Historial de cambios
│   ├── CODE_OF_CONDUCT.md            # Código de conducta
│   ├── CONTRIBUTING.md               # Guía de contribución
│   └── DEPENDENCIAS.md               # Información de dependencias
│
├── 📁 config/                         # ⚙️ Configuraciones
│   ├── .env.example                  # Variables de entorno de ejemplo
│   ├── development.py                # Configuración de desarrollo
│   └── production.py                 # Configuración de producción
│
├── 📁 requirements/                   # 📦 Dependencias organizadas
│   ├── base.txt                      # Dependencias básicas
│   ├── development.txt               # Dependencias de desarrollo
│   ├── production.txt                # Dependencias de producción
│   └── ci.txt                        # Dependencias para CI/CD
│
├── 📁 src/                           # 💾 Código fuente principal
│   ├── 📁 core/                      # 🎯 Lógica central del juego
│   │   ├── __init__.py
│   │   ├── board.py                  # Gestión del tablero
│   │   ├── game_engine.py            # Motor del juego
│   │   └── player.py                 # Gestión de jugadores
│   │
│   ├── 📁 interfaces/                # 🖥️ Interfaces de usuario
│   │   ├── __init__.py
│   │   ├── 📁 cli/                   # 💻 Interfaz línea de comandos
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # Punto de entrada CLI
│   │   │   ├── game_logic.py         # Lógica específica CLI
│   │   │   └── ui/                   # Componentes UI consola
│   │   │
│   │   └── 📁 web/                   # 🌐 Interfaz web (Flask)
│   │       ├── __init__.py
│   │       ├── app.py                # Aplicación Flask principal
│   │       ├── 📁 routes/            # Rutas de la aplicación
│   │       │   ├── __init__.py
│   │       │   ├── api_routes.py     # API endpoints
│   │       │   └── game_routes.py    # Rutas del juego
│   │       ├── 📁 static/            # Archivos estáticos
│   │       │   ├── 📁 css/
│   │       │   │   └── style.css     # Estilos CSS
│   │       │   └── 📁 js/
│   │       │       └── game.js       # Lógica JavaScript
│   │       └── 📁 templates/         # Plantillas HTML
│   │           ├── base.html
│   │           ├── game.html
│   │           └── index.html
│   │
│   ├── 📁 multiplayer/              # 🔗 Funcionalidad multijugador
│   │   ├── __init__.py
│   │   ├── server.py                 # Servidor WebSocket
│   │   ├── client.py                 # Cliente multijugador
│   │   └── socket_handlers.py        # Manejadores de sockets
│   │
│   └── 📁 utils/                     # 🛠️ Utilidades generales
│       ├── __init__.py
│       └── helpers.py                # Funciones auxiliares
│
├── 📁 tests/                         # 🧪 Pruebas del sistema
│   ├── __init__.py
│   ├── test_game_logic.py            # Tests lógica del juego
│   ├── test_helpers.py               # Tests utilidades
│   └── test_multiplayer.py           # Tests multijugador
│
├── 📁 data/                          # 💾 Datos de configuración
│   ├── config.json                   # Configuración general
│   └── scores.json                   # Almacenamiento puntuaciones
│
├── 📄 README.md                      # 📖 Documentación principal
├── 📄 SECURITY.md                    # 🔒 Política de seguridad
├── 📄 LICENSE.md                     # ⚖️ Licencia del proyecto
├── 📄 setup.py                       # 📦 Configuración del paquete
├── 📄 setup.cfg                      # ⚙️ Configuración de herramientas
└── 📄 pytest.ini                     # 🧪 Configuración de pytest
```

## 🔄 Cambios Realizados

### ✅ **Reorganización Completada:**

1. **Archivos web movidos**: `game.js`, `style.css`, `index.html` → `src/interfaces/web/static/`
2. **Documentación centralizada**: Todos los `.md` → `docs/`
3. **Configuración organizada**: Variables de entorno → `config/`
4. **Dependencias estructuradas**: Requirements → `requirements/`
5. **Interfaces separadas**: CLI y Web en carpetas específicas

### 🎯 **Beneficios de la Nueva Estructura:**

- **📁 Mejor organización**: Cada tipo de archivo tiene su lugar
- **🔍 Fácil navegación**: Estructura lógica y predecible  
- **🛠️ Mantenimiento simple**: Separación clara de responsabilidades
- **📈 Escalabilidad**: Fácil agregar nuevas funcionalidades
- **👥 Colaboración mejorada**: Estructura estándar de proyecto Python

### 🚀 **Comandos de Ejecución Actualizados:**

```bash
# Interfaz CLI (línea de comandos)
python -m src.interfaces.cli.main

# Interfaz Web (Flask)  
python -m src.interfaces.web.app

# Servidor Multijugador
python -m src.multiplayer.server

# O usando los comandos instalados:
tres-en-raya-cli
tres-en-raya-web  
tres-en-raya-multiplayer
```

### 📋 **Archivos Actualizados:**

- ✅ `setup.py`: Entry points actualizados
- ✅ `src/interfaces/web/app.py`: Imports simplificados
- ✅ `src/interfaces/web/templates/index.html`: Rutas Flask actualizadas
- ✅ Estructura de carpetas reorganizada completamente

## 🔧 **Próximos Pasos Recomendados:**

1. **Verificar funcionamiento** de todas las interfaces
2. **Actualizar tests** para nueva estructura
3. **Documentar APIs** en carpeta docs/
4. **Optimizar imports** si es necesario

---

**Esta nueva estructura sigue las mejores prácticas de desarrollo Python y facilita enormemente el mantenimiento y escalabilidad del proyecto.** 🎉