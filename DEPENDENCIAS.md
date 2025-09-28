# 📦 GUÍA DE DEPENDENCIAS - PROYECTO TRES EN RAYA

## 📁 **Estructura de Archivos de Dependencias**

### 🎯 **Archivos Principales**

| Archivo | Propósito | Cuándo Usar |
|---------|-----------|-------------|
| `requirements.txt` | **Desarrollo completo** | Desarrollo local completo |
| `requirements-prod.txt` | **Solo producción** | Deploy en servidor |
| `requirements-dev.txt` | **Desarrollo + herramientas** | Setup desarrollo profesional |
| `requirements-ci.txt` | **CI/CD pipelines** | GitHub Actions workflows |

---

## 🚀 **Instalación Según Entorno**

### 🔧 **Desarrollo Local**
```bash
# Instalación completa para desarrollo
pip install -r requirements.txt

# O para desarrollo avanzado con herramientas
pip install -r requirements-dev.txt
```

### 🌐 **Producción/Deploy**
```bash
# Solo dependencias esenciales
pip install -r requirements-prod.txt
```

### ⚙️ **CI/CD (GitHub Actions)**
```bash
# Para workflows automáticos
pip install -r requirements-ci.txt
```

---

## 📋 **Contenido de Cada Archivo**

### 🎯 `requirements.txt` (Desarrollo)
```
✅ Dependencias de producción
✅ Herramientas de testing
📦 Flask, SocketIO, pytest, etc.
```

### 🏭 `requirements-prod.txt` (Producción)
```
✅ Solo Flask y dependencias core
✅ SocketIO para multiplayer
✅ Validación JSON
❌ Sin herramientas de desarrollo
```

### 🛠️ `requirements-dev.txt` (Desarrollo Avanzado)
```
✅ Todo de requirements-prod.txt
✅ Testing: pytest, pytest-cov
✅ Quality: flake8, black
✅ Security: pip-audit, safety, bandit
```

### 🔄 `requirements-ci.txt` (CI/CD)
```
✅ Solo testing y security tools
✅ Dependencias mínimas para importar
✅ Optimizado para GitHub Actions
```

---

## 🎯 **Casos de Uso Específicos**

### 👨‍💻 **Desarrollador Nuevo**
```bash
git clone <repo>
cd tres-en-raya
pip install -r requirements.txt
```

### 🚀 **Deploy a Producción**
```bash
# Heroku, AWS, etc.
pip install -r requirements-prod.txt
```

### 🔧 **Setup Desarrollo Profesional**
```bash
pip install -r requirements-dev.txt
# Incluye linting, formatting, security scanning
```

### 🤖 **GitHub Actions (Automático)**
```yaml
# Ya configurado en workflows
pip install -r requirements-ci.txt
```

---

## 🔒 **Versiones de Seguridad**

### ✅ **Versiones Seguras Garantizadas**
- **Flask:** ≥2.3.0 (Sin vulnerabilidades críticas)
- **Werkzeug:** ≥3.0.6 (10 CVEs corregidos)
- **urllib3:** ≥2.5.0 (Vulnerabilidades GHSA resueltas)
- **idna:** ≥3.7 (PYSEC-2024-60 corregido)

### 🛡️ **Herramientas de Seguridad Incluidas**
- **pip-audit:** Scanner de vulnerabilidades
- **safety:** Base de datos de seguridad Python
- **bandit:** Análisis de código estático

---

## ⚡ **Comandos Útiles**

### 🔍 **Verificar Instalación**
```bash
pip list | grep -E "(Flask|pytest)"
```

### 🔄 **Actualizar Dependencias**
```bash
pip install --upgrade -r requirements.txt
```

### 🛡️ **Verificar Seguridad**
```bash
pip-audit
safety check
```

---

## ❓ **Preguntas Frecuentes**

### **P: ¿Qué archivo uso para desarrollo?**
**R:** `requirements.txt` para desarrollo básico, `requirements-dev.txt` para desarrollo profesional.

### **P: ¿Cómo deploy en producción?**
**R:** Usa `requirements-prod.txt` - es más ligero y seguro.

### **P: ¿Los workflows CI/CD están configurados?**
**R:** Sí, usan `requirements-ci.txt` automáticamente.

### **P: ¿Cómo actualizar dependencias?**
**R:** Modifica el archivo correspondiente y ejecuta `pip install --upgrade -r <archivo>`

---

*✅ Estructura optimizada para desarrollo, producción y CI/CD*  
*🔒 Todas las versiones verificadas sin vulnerabilidades*