# 🎮 Tres en Raya - Tic Tac Toe Game

<div align="center">

![Tres en Raya Logo](https://img.shields.io/badge/🎮-Tres%20en%20Raya-blue?style=for-the-badge)

[![Live Demo](https://img.shields.io/badge/🌐-Live%20Demo-success?style=for-the-badge)](https://crypt0xdev.github.io/tres-en-raya/)
[![GitHub Pages](https://img.shields.io/github/deployments/Crypt0xDev/tres-en-raya/github-pages?label=GitHub%20Pages&style=flat-square)](https://github.com/Crypt0xDev/tres-en-raya/deployments)
[![Tests](https://img.shields.io/github/actions/workflow/status/Crypt0xDev/tres-en-raya/test.yml?branch=main&label=Tests&style=flat-square)](https://github.com/Crypt0xDev/tres-en-raya/actions)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?style=flat-square&logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)

**Un juego clásico de Tres en Raya con IA inteligente, múltiples modos de juego y interfaz moderna**

[🎯 **Jugar Ahora**](https://crypt0xdev.github.io/tres-en-raya/) • [📖 **Documentación**](#-instalación) • [🐛 **Reportar Bug**](https://github.com/Crypt0xDev/tres-en-raya/issues/new?template=bug_report.yml) • [💡 **Solicitar Feature**](https://github.com/Crypt0xDev/tres-en-raya/issues/new?template=feature_request.yml)

</div>

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

# 4. ¡Listo! Elige tu modo de juego favorito
```

## 🎮 Formas de Jugar

### 🌐 **Modo Web (Recomendado)**
```bash
# Servidor simple (más rápido)
python -m http.server 8000
# Luego ve a: http://localhost:8000

# O servidor Flask completo (más características)
python -m src.web.app
# Luego ve a: http://localhost:5000
```

### 💻 **Modo Terminal/Consola**
```bash
python -m src.local.main
```
¡Perfecto para programadores que aman la línea de comandos!

### 🚀 **Modo Multijugador (Experimental)**
```bash
# Servidor multijugador
python -m src.multiplayer.server

# Cliente (en otra terminal)
python -m src.multiplayer.client
```

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
🎮 tres-en-raya/
├── 📄 index.html              # 🌐 Página principal (GitHub Pages)
├── 🎮 game.js                 # 🧠 Lógica del juego con IA
├── 🎨 style.css               # ✨ Estilos modernos
├── 
├── 📁 .github/                # 🤖 Configuración de GitHub
│   ├── workflows/             # ⚙️ GitHub Actions (CI/CD)
│   └── ISSUE_TEMPLATE/        # 📝 Templates para issues
├── 
├── 📁 src/                    # 💻 Código fuente principal
│   ├── core/                  # 🎯 Lógica principal del juego
│   │   ├── board.py          # 📋 Gestión del tablero
│   │   ├── game_engine.py    # ⚡ Motor del juego
│   │   └── player.py         # 👤 Gestión de jugadores
│   ├── 
│   ├── local/                 # 💻 Versión terminal/consola
│   │   ├── main.py           # 🚀 Punto de entrada
│   │   ├── game_logic.py     # 🧠 Lógica del juego
│   │   └── ui/
│   │       └── console_ui.py # 💬 Interfaz de consola
│   ├── 
│   ├── web/                   # 🌐 Aplicación Flask
│   │   ├── app.py            # 🖥️ Servidor Flask
│   │   ├── static/           # 📦 Archivos estáticos
│   │   ├── templates/        # 📄 Templates HTML
│   │   └── routes/           # 🔗 Rutas del API
│   ├── 
│   ├── multiplayer/           # 🌍 Multijugador online
│   │   ├── server.py         # 🖥️ Servidor WebSocket
│   │   ├── client.py         # 👤 Cliente
│   │   └── socket_handlers.py # 🔌 Manejadores
│   └── 
│   └── utils/                 # 🔧 Utilidades
│       └── helpers.py        # 🛠️ Funciones auxiliares
├── 
├── 📁 tests/                  # 🧪 Pruebas unitarias
│   ├── test_game_logic.py    # 🎯 Tests de lógica
│   └── test_multiplayer.py   # 🌐 Tests multijugador
├── 
├── 📁 config/                 # ⚙️ Configuraciones
└── 📁 data/                   # 📊 Datos del juego
```

</details>

## 🛠️ Tecnologías Utilizadas

<div align="center">

| Frontend | Backend | AI/Logic | Tools | Testing |
|:---:|:---:|:---:|:---:|:---:|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | ![Algorithm](https://img.shields.io/badge/Minimax-Algorithm-blue?style=flat-square) | ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | ![JavaScript](https://img.shields.io/badge/Game_Logic-JavaScript-yellow?style=flat-square) | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white) | ![Coverage](https://img.shields.io/badge/Coverage-Testing-green?style=flat-square) |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | ![Socket.IO](https://img.shields.io/badge/Socket.IO-010101?style=flat-square&logo=socket.io&logoColor=white) | ![AI](https://img.shields.io/badge/AI-Strategy-purple?style=flat-square) | ![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-222222?style=flat-square&logo=github-pages&logoColor=white) |  |

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

- 🎵 Añadir efectos de sonido
- 🌙 Modo oscuro/claro
- 🏆 Sistema de puntuaciones
- 📊 Estadísticas de partidas
- 🎨 Más themes visuales
- 📱 Mejorar versión móvil
- 🌐 Traducir a otros idiomas
- 🤖 Mejorar algoritmos de IA
- 🔊 Accesibilidad para personas con discapacidades
- 📈 Analytics de uso

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
- 🌐 Desplegado con GitHub Pages
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