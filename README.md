# 🎮 Tres en Raya - Aplicación Web con IA y Torneos

<div align="center">

![Tres en Raya Logo](https://img.shields.io/badge/🎮-Tres%20en%20Raya-blue?style=for-the-badge)
![Screaming Architecture](https://img.shields.io/badge/🏗️-Screaming%20Architecture-brightgreen?style=for-the-badge)
![Web App├── 🌐 interfaces/            # 🚚 ENTREGA - Interfaces(https://img.shields.io/badge/🌐-Aplicaci%C3%B3n%20Web-success?style=for-the-badge)

[![Tests](https://img.shields.io/github/actions/workflow/status/Crypt0xDev/tres-en-raya/test.yml?branch=main&label=Tests&style=flat-square)](https://github.com/Crypt0xDev/tres-en-raya/actions)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?style=flat-square&logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)

**Aplicación web de Tres en Raya con IA, torneos y funcionalidad online**

*Implementación completa con Screaming Architecture 100%*

[🎯 **Jugar Ahora**](https://crypt0xdev.github.io/tres-en-raya/) • [🤖 **IA Avanzada**](#-inteligencia-artificial) • [🏆 **Torneos**](#-torneos-y-rankings) • [🌐 **Multijugador Online**](#-funcionalidad-online) • [🏗️ **Ver Arquitectura**](#-screaming-architecture)

</div>

## ✨ Características Principales

- 🤖 **Inteligencia Artificial** - IA con múltiples niveles de dificultad
- 🏆 **Sistema de Torneos** - Compite en torneos y sube en los rankings  
- 🌐 **Multijugador Online** - Juega contra otros jugadores en tiempo real
- 📊 **Estadísticas Detalladas** - Seguimiento completo de rendimiento
- 🎨 **Interfaz Moderna** - Diseño responsivo y atractivo
- ⚡ **Tiempo Real** - Actualizaciones instantáneas con WebSockets

## 🏗️ Screaming Architecture

Este proyecto es un **ejemplo completo de Screaming Architecture**, donde la estructura del código **'grita' sobre el dominio del negocio** (Tres en Raya) en lugar de sobre las tecnologías utilizadas.

### 🎯 ¿Por qué "Screaming"?

Cuando miras la estructura del proyecto, **inmediatamente sabes que es un juego de Tres en Raya**:

```
📁 tres-en-raya/
├── 🎮 game/                           # ← ¡GRITA "JUEGO"!
│   ├── entities/                     # ← ¡GRITA "ENTIDADES DEL JUEGO"!
│   ├── use_cases/                   # ← ¡GRITA "CASOS DE USO DEL JUEGO"!
│   ├── services/                    # ← ¡GRITA "SERVICIOS DEL JUEGO"!
│   └── rules/                       # ← ¡GRITA "REGLAS DEL JUEGO"!
├── 🎪 application/                   # Orquestación de la aplicación web
│   └── entry_points/                # Punto de entrada web único
├── 🌐 interfaces/                  # Adaptador web (Flask)
│   └── web_ui/                     # Interfaz web moderna
├── 💾 persistence/                  # Persistencia de datos  
├── 🏗️ infrastructure/              # Configuración e infraestructura
│   ├── configuration/              # Configuraciones del sistema
│   └── development/                # Herramientas de desarrollo
└── 🧪 tests/                       # Tests estructurados por dominio
```

**NO** encuentras carpetas como:
- ❌ `controllers/` (tecnología web)
- ❌ `models/` (patrón MVC)  
- ❌ `views/` (interfaz específica)
- ❌ `database/` (detalle de implementación)

### 🚀 Principios Aplicados

✅ **El dominio es el protagonista**: `game/` es el centro de todo  
✅ **Casos de uso explícitos**: `StartNewGame`, `MakeMove`, `CheckWinner`  
✅ **Independencia tecnológica**: El juego funciona sin Flask, CLI o cualquier framework  
✅ **Inversión de dependencias**: Las tecnologías dependen del dominio, no al revés  
✅ **Tests arquitectónicos**: Los tests reflejan la estructura del dominio  

### 📖 Uncle Bob's Vision

> *"Your architecture should tell readers about the system, not about the frameworks you used in your system."*  
> — Robert C. Martin (Uncle Bob)

Este proyecto demuestra cómo estructurar código para que **la arquitectura comunique la intención de negocio**.</div>

## ✨ Características del Juego

## ✨ Características

🎮 **Múltiples Modos de Juego:**
- 👥 **Jugador vs Jugador** - Clásico modo para dos personas
- 🤖 **Jugador vs IA** - Desafía a la inteligencia artificial
- 💻 **Terminal/Consola** - Versión de línea de comandos
- 🌐 **Multijugador Online** - Juega con amigos en tiempo real

🧠 **IA Inteligente con 3 Niveles:**
- 😊 **Fácil** - Movimientos aleatorios, perfecto para principiantes
- 😐 **Medio** - Estrategia mixta (70% inteligente, 30% aleatorio)
- 😈 **Difícil** - IA perfecta usando algoritmo Minimax (¡casi imposible de ganar!)

🎨 **Interfaz Moderna:**
- ✨ Animaciones fluidas y efectos visuales
- 📱 Diseño totalmente responsive
- 🌈 Interfaz intuitiva y atractiva
- 🔄 Transiciones suaves entre estados

## 🚀 Demo en Vivo

**¡Juega directamente en tu navegador!**

[![Tres en Raya Demo](https://img.shields.io/badge/🎮-Jugar%20Ahora-success?style=for-the-badge&logo=github)](https://crypt0xdev.github.io/tres-en-raya/)

> 🌐 **Sitio Web:** https://crypt0xdev.github.io/tres-en-raya/

## 📸 Capturas de Pantalla

<div align="center">

| Selector de Modo | Jugando vs IA | Victoria |
|:---:|:---:|:---:|
| ![Modo](https://via.placeholder.com/250x200/667eea/ffffff?text=Selector+de+Modo) | ![Jugando](https://via.placeholder.com/250x200/764ba2/ffffff?text=Jugando+vs+IA) | ![Victoria](https://via.placeholder.com/250x200/27ae60/ffffff?text=Victoria!) |

</div>

## 🏛️ Arquitectura del Proyecto

### 📁 Estructura "Que Grita"

```
tres-en-raya/                    # 🎯 ESTRUCTURA LIMPIA - SCREAMING ARCHITECTURE
├── 🎮 game/                     # DOMINIO DEL JUEGO (lo más importante)
│   ├── entities/               # Entidades del negocio
│   │   ├── board.py           # Tablero de 3x3
│   │   ├── player.py          # Jugador (Humano/AI)
│   │   └── game_session.py    # Sesión de partida
│   ├── use_cases/             # Casos de uso del juego
│   │   ├── start_new_game.py  # ▶️ Iniciar partida
│   │   ├── make_move.py       # 🎯 Realizar movimiento  
│   │   ├── check_winner.py    # 🏆 Verificar ganador
│   │   └── manage_players.py  # 👥 Gestionar jugadores
│   ├── services/              # Servicios del dominio
│   │   ├── ai_opponent.py     # 🤖 Inteligencia Artificial
│   │   ├── score_calculator.py # 📊 Calculadora de puntos
│   │   └── statistics_tracker.py # 📈 Estadísticas
│   └── rules/                 # Reglas del juego
│       ├── game_rules.py      # ⚖️ Reglas principales
│       ├── victory_conditions.py # 🏆 Condiciones de victoria  
│       └── ai_strategy.py     # 🧠 Estrategias de AI
│
├── 🚀 application/             # ORQUESTACIÓN DE LA APP
│   └── entry_points/          # Puntos de entrada
│       ├── cli_app.py        # 💻 Aplicación CLI
│       ├── web_app.py        # 🌐 Aplicación Web
│       └── multiplayer_server.py # 🌍 Servidor Multijugador
│
├── 🔌 interfaces/             # ADAPTADORES DE INTERFAZ
│   ├── web_ui/               # Interfaz web
│   │   └── flask_adapter.py  # Adaptador Flask
│   └── console_ui/           # Interfaz consola
│       └── cli_adapter.py    # Adaptador CLI
│
├── 💾 persistence/            # PERSISTENCIA DE DATOS
│   ├── repositories/         # Repositorios abstractos
│   └── data_sources/        # Implementaciones concretas
│
├── ⚙️ infrastructure/         # INFRAESTRUCTURA TÉCNICA
│   ├── configuration/        # Configuración del juego
│   │   ├── game_config.py   # Configuración del juego
│   │   ├── development.py   # Config desarrollo
│   │   ├── production.py    # Config producción
│   │   └── config.json      # Datos de configuración
│   ├── development/          # Herramientas de desarrollo
│   │   ├── requirements*.txt # Dependencias
│   │   ├── pytest.ini       # Config de tests
│   │   ├── mypy.ini         # Config de tipos
│   │   └── pyproject.toml   # Config del proyecto
│   └── external_services/    # Servicios externos
│
└── 🧪 tests/                  # TESTS ARQUITECTÓNICOS
    ├── unit/game/            # Tests del dominio
    ├── unit/interfaces/         # Tests de adaptadores
    ├── integration/          # Tests de integración
    └── e2e/                 # Tests end-to-end
```

### 🎯 Lo que hace único a este proyecto

1. **🎮 Domain-First**: El directorio `game/` contiene TODA la lógica del negocio
2. **🌐 Web-Focused**: Aplicación web completa con IA, torneos y funcionalidad online
3. **🧪 Tests que hablan**: Los tests están organizados por dominio, no por tecnología
4. **📖 Casos de uso explícitos**: Cada funcionalidad del juego es un caso de uso claro
5. **🚫 Sin dependencias técnicas**: El dominio es independiente de la tecnología web

## ⚡ Inicio Rápido

### 🌐 Opción 1: Jugar Online (Más Fácil)
Simplemente ve a **[crypt0xdev.github.io/tres-en-raya](https://crypt0xdev.github.io/tres-en-raya/)** y ¡empieza a jugar!

### 💻 Opción 2: Ejecutar Localmente

#### Prerrequisitos
- Python 3.9 o superior
- Git (opcional)

#### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/Crypt0xDev/tres-en-raya.git
cd tres-en-raya

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. ¡Iniciar la aplicación web!
python run_web_server.py
# 🌐 Ve a: http://localhost:5000
```

## 🎮 Formas de Jugar (Screaming Architecture)

### 🌐 **Servidor Web (Flask)**
```bash
python run_web_server.py
# 🌐 Ve a: http://localhost:5000
```

### 🌐 **Servidor Web con IA y Torneos**
```bash
python run_web_server.py
# 🌐 Ve a: http://localhost:5000
# ¡Disfruta de IA avanzada, torneos y multijugador online!
```

### 🧪 **Ejecutar Tests Arquitectónicos**
```bash
python run_tests.py --all
```

### 🛠️ **Herramientas de Desarrollo**
```bash
python dev.py --architecture   # Ver estructura
python dev.py --lint          # Análisis de código
python dev.py --docs          # Generar documentación
python dev.py --clean         # Limpiar archivos temporales
```

### 🏆 **Funcionalidades Web Avanzadas**
- 🤖 **IA Inteligente:** Múltiples niveles de dificultad con algoritmo Minimax
- 🏆 **Sistema de Torneos:** Compite con otros jugadores online
- 🌐 **Multijugador Online:** Partidas en tiempo real con otros usuarios
- 📊 **Estadísticas:** Seguimiento completo de tu progreso

## 🎯 Cómo Jugar

### 🎮 **Reglas Básicas**
1. El tablero es una cuadrícula de 3×3
2. Los jugadores se turnan colocando X y O
3. **¡El primero en conseguir 3 en línea gana!** (horizontal, vertical o diagonal)
4. Si el tablero se llena sin ganador, es empate

### 🤖 **Jugando contra la IA**
- **😊 Fácil:** La IA hace movimientos aleatorios - perfecto para aprender
- **😐 Medio:** Mezcla estrategia inteligente con algo de aleatoriedad - buen desafío
- **😈 Difícil:** ¡Algoritmo Minimax! La IA juega perfectamente - ¿puedes ganarle?

> 💡 **Tip:** Empieza en modo Fácil y ve subiendo la dificultad conforme mejores

## 🏗️ Arquitectura del Proyecto

<details>
<summary><b>📁 Estructura de Carpetas</b></summary>

```
🎮 tres-en-raya/ (Screaming Architecture)
├── � run_web_server.py       # � Punto de entrada principal
├── 🧪 run_tests.py            # 🔍 Ejecutor de tests
├── 🛠️ dev.py                  # 🔧 Herramientas de desarrollo
├── 
├── 🎮 game/                   # 🏛️ DOMINIO - Lógica de negocio
│   ├── entities/             # 👥 Entidades del dominio
│   │   ├── board.py         # � Tablero del juego
│   │   ├── game_session.py  # 🎯 Sesión de juego
│   │   └── player.py        # � Jugador
│   ├── rules/               # 📏 Reglas del juego
│   │   ├── ai_strategy.py   # 🤖 Estrategias de IA
│   │   ├── game_rules.py    # ⚖️ Reglas fundamentales
│   │   └── victory_conditions.py # 🏆 Condiciones de victoria
│   ├── services/            # � Servicios del dominio
│   │   ├── ai_opponent.py   # 🤖 Oponente IA
│   │   ├── score_calculator.py # � Calculador de puntuación
│   │   └── statistics_tracker.py # 📈 Seguimiento estadísticas
│   └── use_cases/           # 📝 Casos de uso
│       ├── check_winner.py  # 🏆 Verificar ganador
│       ├── make_move.py     # ✋ Realizar movimiento
│       ├── manage_players.py # 👥 Gestión jugadores
│       └── start_new_game.py # 🆕 Iniciar juego
├── 
├── 📱 application/            # � APLICACIÓN - Coordinadores
│   └── entry_points/         # � Puntos de entrada
│       └── web_main.py       # 🌐 Aplicación web principal
├── 
├── 🌐 delivery_mechanisms/    # � ENTREGA - Interfaces
│   └── web_ui/              # � Interfaz web (Flask)
│       ├── flask_adapter.py  # 🔌 Adaptador Flask
│       ├── controllers/      # 🎛️ Controladores web
│       ├── templates/        # � Plantillas HTML
│       └── static/          # � CSS, JS, imágenes
├── 
├── 🏗️ infrastructure/        # 🔧 INFRAESTRUCTURA
│   ├── configuration/       # ⚙️ Configuraciones
│   └── development/         # 🛠️ Herramientas desarrollo
├── 
├── � persistence/           # 🗃️ PERSISTENCIA - Datos
│   ├── data_sources/        # 📊 Fuentes de datos
│   └── repositories/        # � Repositorios
├── 
└── 🧪 tests/                 # ✅ Pruebas y validación
    ├── unit/                # 🔬 Tests unitarios
    ├── integration/         # 🔗 Tests integración
    └── e2e/                 # 🌍 Tests end-to-end
```

</details>

## 🛠️ Tecnologías Utilizadas

<div align="center">

| Frontend | Backend | AI/Logic | Architecture | Testing |
|:---:|:---:|:---:|:---:|:---:|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) | ![Python](https://img.shields.io/badge/Python_3.13-3776AB?style=flat-square&logo=python&logoColor=white) | ![Minimax](https://img.shields.io/badge/Minimax-Algorithm-blue?style=flat-square) | ![Clean](https://img.shields.io/badge/Screaming-Architecture-green?style=flat-square) | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | ![AI](https://img.shields.io/badge/Tournament-System-purple?style=flat-square) | ![Domain](https://img.shields.io/badge/Domain-Driven-orange?style=flat-square) | ![Coverage](https://img.shields.io/badge/100%25-Coverage-brightgreen?style=flat-square) |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | ![WebSocket](https://img.shields.io/badge/WebSocket-Real_Time-red?style=flat-square) | ![Online](https://img.shields.io/badge/Online-Multiplayer-gold?style=flat-square) | ![Hexagonal](https://img.shields.io/badge/Hexagonal-Pattern-lightblue?style=flat-square) | ![Validation](https://img.shields.io/badge/Architecture-Validated-success?style=flat-square) |

</div>

## 🤝 Contribuir

¡Las contribuciones son muy bienvenidas! Este proyecto es perfecto para:

- 🆕 **Principiantes** - Issues etiquetados como `good-first-issue`
- 🎓 **Estudiantes** - Excelente para aprender algoritmos de juegos
- 👨‍💻 **Desarrolladores** - Mejoras de UI/UX, nuevas funcionalidades
- 🤖 **Expertos en IA** - Optimizaciones del algoritmo Minimax

### 📋 **Cómo Contribuir**

1. 🍴 **Fork** el repositorio
2. 🌿 **Crea** una rama: `git checkout -b feature/mi-nueva-funcionalidad`
3. 💻 **Programa** tu cambio
4. ✅ **Prueba** que todo funcione
5. 📝 **Commit**: `git commit -m 'Add: nueva funcionalidad increíble'`
6. 🚀 **Push**: `git push origin feature/mi-nueva-funcionalidad`  
7. 🔄 **Crea** un Pull Request

### 🏷️ **Tipos de Contribuciones**

- 🐛 **Bug fixes** - Corrige errores
- ✨ **Features** - Nuevas funcionalidades
- 📚 **Documentación** - Mejora la documentación
- 🎨 **UI/UX** - Mejoras visuales
- ⚡ **Performance** - Optimizaciones
- 🧪 **Tests** - Más cobertura de pruebas

<details>
<summary><b>💡 Ideas de Contribución</b></summary>

- 🤖 **IA Avanzada:** Nuevos algoritmos y dificultades
- � **Torneos:** Brackets, clasificaciones, premios
- � **Multijugador:** Chat, salas privadas, matchmaking
- 🎵 **Multimedia:** Efectos de sonido y animaciones
- 🎨 **UI/UX:** Themes visuales y modo oscuro/claro
- 📊 **Analytics:** Estadísticas avanzadas y dashboards
- 📱 **Responsive:** Optimización para móviles y tablets
- 🌍 **i18n:** Soporte multiidioma
- 🔊 **Accesibilidad:** Soporte para discapacidades
- ⚡ **Performance:** Optimizaciones de velocidad
- 🧪 **Testing:** Más cobertura y tests E2E
- 📈 **Monitoring:** Métricas de uso y rendimiento

</details>

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

```
MIT License - Libre para usar, modificar y distribuir ❤️
```

## 🙏 Agradecimientos

- 🎮 Inspirado en el clásico juego Tic-Tac-Toe
- 🤖 Algoritmo Minimax para IA perfecta
- 🎨 Diseño moderno inspirado en Material Design
- 👥 Gracias a todos los [contribuidores](https://github.com/Crypt0xDev/tres-en-raya/graphs/contributors)

## 📞 Contacto y Soporte

<div align="center">

[![GitHub Profile](https://img.shields.io/badge/GitHub-Crypt0xDev-181717?style=for-the-badge&logo=github)](https://github.com/Crypt0xDev)
[![Issues](https://img.shields.io/badge/Issues-Reportar%20Bug-red?style=for-the-badge&logo=github)](https://github.com/Crypt0xDev/tres-en-raya/issues/new?template=bug_report.yml)
[![Discussions](https://img.shields.io/badge/Discussions-Hacer%20Pregunta-blue?style=for-the-badge&logo=github)](https://github.com/Crypt0xDev/tres-en-raya/discussions)

**🔗 Link del Proyecto:** [https://github.com/Crypt0xDev/tres-en-raya](https://github.com/Crypt0xDev/tres-en-raya)

</div>

---

<div align="center">

**¡Dale una ⭐ si te gustó el proyecto!**

*Desarrollado con ❤️ por [Crypt0xDev](https://github.com/Crypt0xDev)*

</div>

## 📂 Estructura de Carpetas Detallada

```
│                                     # 🎮 EL GRITO: "SOY UN JUEGO DE TRES EN RAYA"
├── 📁 game/                          # 🎯 DOMINIO PRINCIPAL DEL NEGOCIO
│   ├── 📁 entities/                  # 🏛️ Entidades del dominio
│   │   ├── board.py                  # 📋 Tablero del juego
│   │   ├── player.py                 # 👤 Jugador
│   │   ├── game_session.py           # 🎮 Sesión de juego
│   │   └── move.py                   # 🎯 Movimiento
│   │
│   ├── 📁 use_cases/                 # 🎪 Casos de uso del negocio
│   │   ├── start_game.py             # 🚀 Iniciar partida
│   │   ├── make_move.py              # 🎯 Realizar movimiento
│   │   ├── check_winner.py           # 🏆 Verificar ganador
│   │   ├── manage_players.py         # 👥 Gestionar jugadores
│   │   └── calculate_statistics.py   # 📊 Calcular estadísticas
│   │
│   ├── 📁 rules/                     # 📜 Reglas del dominio
│   │   ├── game_rules.py             # 🎮 Reglas básicas del juego
│   │   ├── victory_conditions.py     # 🏆 Condiciones de victoria
│   │   ├── ai_strategy.py            # 🤖 Estrategias de IA
│   │   └── validation_rules.py       # ✅ Reglas de validación
│   │
│   └── 📁 services/                  # 🛠️ Servicios del dominio
│       ├── game_engine.py            # ⚡ Motor principal del juego
│       ├── ai_opponent.py            # 🤖 Oponente IA
│       ├── score_calculator.py       # 🏅 Calculador de puntuaciones
│       └── statistics_tracker.py     # 📈 Rastreador estadísticas
│
├── 📁 interfaces/                   # 🚚 INTERFACES DE ENTREGA
│   ├── 📁 web_ui/                   # 🌐 Interfaz Web
│   │   ├── flask_app.py             # 🔗 Adaptador Flask
│   │   ├── 📁 controllers/          # 🎛️ Controladores web
│   │   ├── 📁 static/               # 📦 Recursos estáticos
│   │   └── 📁 templates/            # 📝 Plantillas HTML
│   │
│   ├── 📁 console_ui/               # 💻 Interfaz Consola
│   │   ├── cli_adapter.py           # 🔗 Adaptador CLI
│   │   ├── console_display.py       # 🖥️ Visualización consola
│   │   └── input_handler.py         # ⌨️ Manejo de entrada
│   │
│   └── 📁 api/                      # 🔌 API REST
│       ├── rest_endpoints.py        # 🌐 Endpoints REST
│       └── websocket_handler.py     # 🔌 Manejador WebSocket
│
├── 📁 persistence/                   # 💾 PERSISTENCIA DE DATOS
│   ├── 📁 repositories/             # 🏪 Repositorios
│   │   ├── game_repository.py       # 🎮 Repo de juegos
│   │   ├── player_repository.py     # 👤 Repo de jugadores
│   │   └── statistics_repository.py # 📊 Repo de estadísticas
│   │
│   └── 📁 data_sources/             # 💽 Fuentes de datos
│       ├── json_storage.py          # 📄 Almacén JSON
│       ├── memory_storage.py        # 🧠 Almacén en memoria
│       └── file_storage.py          # 📁 Almacén en archivos
│
├── 📁 infrastructure/               # 🏗️ INFRAESTRUCTURA TÉCNICA
│   ├── 📁 configuration/            # ⚙️ Configuración
│   ├── 📁 logging/                  # 📋 Logging
│   ├── 📁 monitoring/               # 📊 Monitoreo
│   └── 📁 external_services/        # 🌐 Servicios externos
│
└── 📁 application/                  # 🎪 ORQUESTACIÓN DE LA APLICACIÓN
    ├── 📁 coordinators/             # 🎭 Coordinadores de casos de uso
    ├── 📁 workflows/                # 🔄 Flujos de trabajo
    └── 📁 entry_points/             # 🚪 Puntos de entrada
        ├── run_web.py               # 🌐 Entrada web
        ├── run_console.py           # 💻 Entrada consola
        └── run_api.py               # 🔌 Entrada API
```