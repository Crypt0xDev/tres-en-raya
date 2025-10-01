// 🎮 Tres en Raya - Sistema Completo con Centro de Usuario
class UserManager {
  constructor() {
    this.currentUser = null;
    this.isGuest = true;
  }

  // Autenticación y registro
  register(username, email, password) {
    const users = this.getUsers();

    if (users.find((u) => u.username === username)) {
      throw new Error("El nombre de usuario ya existe");
    }

    if (users.find((u) => u.email === email)) {
      throw new Error("El email ya está registrado");
    }

    const newUser = {
      id: Date.now(),
      username,
      email,
      password: btoa(password), // Codificación básica (no segura para producción)
      avatar: "👤",
      stats: {
        gamesPlayed: 0,
        wins: 0,
        losses: 0,
        draws: 0,
        points: 0,
        winStreak: 0,
        bestStreak: 0,
        level: 1,
      },
      createdAt: new Date().toISOString(),
    };

    users.push(newUser);
    this.saveUsers(users);
    this.login(username, password);
    return newUser;
  }

  login(username, password) {
    const users = this.getUsers();
    const user = users.find(
      (u) => u.username === username && u.password === btoa(password)
    );

    if (!user) {
      throw new Error("Credenciales incorrectas");
    }

    this.currentUser = user;
    this.isGuest = false;
    localStorage.setItem("currentUser", JSON.stringify(user));
    return user;
  }

  loginAsGuest() {
    this.currentUser = {
      id: "guest",
      username: "Invitado",
      avatar: "👤",
      stats: {
        gamesPlayed: 0,
        wins: 0,
        losses: 0,
        draws: 0,
        points: 0,
        winStreak: 0,
        bestStreak: 0,
        level: 1,
      },
    };
    this.isGuest = true;
    localStorage.setItem("currentUser", JSON.stringify(this.currentUser));
  }

  logout() {
    this.currentUser = null;
    this.isGuest = true;
    localStorage.removeItem("currentUser");
  }

  // Gestión de usuarios
  getUsers() {
    return JSON.parse(localStorage.getItem("gameUsers") || "[]");
  }

  saveUsers(users) {
    localStorage.setItem("gameUsers", JSON.stringify(users));
  }

  updateUserStats(gameResult) {
    if (!this.currentUser || this.isGuest) return;

    const users = this.getUsers();
    const userIndex = users.findIndex((u) => u.id === this.currentUser.id);

    if (userIndex === -1) return;

    const user = users[userIndex];
    user.stats.gamesPlayed++;

    switch (gameResult) {
      case "win":
        user.stats.wins++;
        user.stats.winStreak++;
        user.stats.points += 10;
        if (user.stats.winStreak > user.stats.bestStreak) {
          user.stats.bestStreak = user.stats.winStreak;
        }
        break;
      case "loss":
        user.stats.losses++;
        user.stats.winStreak = 0;
        user.stats.points = Math.max(0, user.stats.points - 3);
        break;
      case "draw":
        user.stats.draws++;
        user.stats.points += 3;
        break;
    }

    // Calcular nivel basado en puntos
    user.stats.level = Math.floor(user.stats.points / 50) + 1;

    users[userIndex] = user;
    this.currentUser = user;
    this.saveUsers(users);
    localStorage.setItem("currentUser", JSON.stringify(user));
  }

  updateAvatar(avatar) {
    if (!this.currentUser) return;

    this.currentUser.avatar = avatar;

    if (!this.isGuest) {
      const users = this.getUsers();
      const userIndex = users.findIndex((u) => u.id === this.currentUser.id);
      if (userIndex !== -1) {
        users[userIndex].avatar = avatar;
        this.saveUsers(users);
      }
    }

    localStorage.setItem("currentUser", JSON.stringify(this.currentUser));
  }

  // Leaderboard
  getLeaderboard(sortBy = "points") {
    const users = this.getUsers().filter((u) => u.stats.gamesPlayed > 0);

    users.sort((a, b) => {
      switch (sortBy) {
        case "wins":
          return b.stats.wins - a.stats.wins;
        case "winrate":
          const aWinRate =
            a.stats.gamesPlayed > 0 ? a.stats.wins / a.stats.gamesPlayed : 0;
          const bWinRate =
            b.stats.gamesPlayed > 0 ? b.stats.wins / b.stats.gamesPlayed : 0;
          return bWinRate - aWinRate;
        default:
          return b.stats.points - a.stats.points;
      }
    });

    return users.slice(0, 10);
  }

  getUserRank(sortBy = "points") {
    const users = this.getUsers().filter((u) => u.stats.gamesPlayed > 0);
    users.sort((a, b) => b.stats[sortBy] - a.stats[sortBy]);

    if (!this.currentUser || this.isGuest) return -1;

    return users.findIndex((u) => u.id === this.currentUser.id) + 1;
  }

  // Inicialización
  loadCurrentUser() {
    const savedUser = localStorage.getItem("currentUser");
    if (savedUser) {
      this.currentUser = JSON.parse(savedUser);
      this.isGuest = this.currentUser.id === "guest";
    }

    // Agregar usuarios demo si es la primera vez
    this.initializeDemoUsers();
  }

  initializeDemoUsers() {
    const users = this.getUsers();
    if (users.length === 0) {
      const demoUsers = [
        {
          id: 1,
          username: "ProGamer2024",
          email: "pro@demo.com",
          password: btoa("demo"),
          avatar: "🏆",
          stats: {
            gamesPlayed: 50,
            wins: 42,
            losses: 6,
            draws: 2,
            points: 420,
            winStreak: 5,
            bestStreak: 15,
            level: 9,
          },
        },
        {
          id: 2,
          username: "TacToe_Master",
          email: "master@demo.com",
          password: btoa("demo"),
          avatar: "🦸‍♂️",
          stats: {
            gamesPlayed: 45,
            wins: 35,
            losses: 8,
            draws: 2,
            points: 356,
            winStreak: 3,
            bestStreak: 12,
            level: 8,
          },
        },
        {
          id: 3,
          username: "IA_Hunter",
          email: "hunter@demo.com",
          password: btoa("demo"),
          avatar: "🤖",
          stats: {
            gamesPlayed: 38,
            wins: 28,
            losses: 7,
            draws: 3,
            points: 289,
            winStreak: 2,
            bestStreak: 8,
            level: 6,
          },
        },
        {
          id: 4,
          username: "UniversityChamp",
          email: "champ@demo.com",
          password: btoa("demo"),
          avatar: "🧑‍🎓",
          stats: {
            gamesPlayed: 32,
            wins: 22,
            losses: 8,
            draws: 2,
            points: 226,
            winStreak: 1,
            bestStreak: 6,
            level: 5,
          },
        },
        {
          id: 5,
          username: "CodeWarrior",
          email: "warrior@demo.com",
          password: btoa("demo"),
          avatar: "👨‍💻",
          stats: {
            gamesPlayed: 28,
            wins: 18,
            losses: 8,
            draws: 2,
            points: 186,
            winStreak: 0,
            bestStreak: 5,
            level: 4,
          },
        },
        {
          id: 6,
          username: "XO_Legend",
          email: "legend@demo.com",
          password: btoa("demo"),
          avatar: "⭐",
          stats: {
            gamesPlayed: 25,
            wins: 15,
            losses: 8,
            draws: 2,
            points: 156,
            winStreak: 2,
            bestStreak: 4,
            level: 4,
          },
        },
        {
          id: 7,
          username: "GameMaster",
          email: "gamemaster@demo.com",
          password: btoa("demo"),
          avatar: "🎮",
          stats: {
            gamesPlayed: 22,
            wins: 12,
            losses: 8,
            draws: 2,
            points: 126,
            winStreak: 1,
            bestStreak: 3,
            level: 3,
          },
        },
        {
          id: 8,
          username: "StrategicMind",
          email: "strategic@demo.com",
          password: btoa("demo"),
          avatar: "🧠",
          stats: {
            gamesPlayed: 20,
            wins: 10,
            losses: 8,
            draws: 2,
            points: 106,
            winStreak: 0,
            bestStreak: 3,
            level: 3,
          },
        },
        {
          id: 9,
          username: "QuickPlayer",
          email: "quick@demo.com",
          password: btoa("demo"),
          avatar: "⚡",
          stats: {
            gamesPlayed: 18,
            wins: 8,
            losses: 8,
            draws: 2,
            points: 86,
            winStreak: 1,
            bestStreak: 2,
            level: 2,
          },
        },
        {
          id: 10,
          username: "Rookie2024",
          email: "rookie@demo.com",
          password: btoa("demo"),
          avatar: "👤",
          stats: {
            gamesPlayed: 15,
            wins: 6,
            losses: 7,
            draws: 2,
            points: 66,
            winStreak: 0,
            bestStreak: 2,
            level: 2,
          },
        },
      ];

      this.saveUsers(demoUsers);
    }
  }
}

class TicTacToeGame {
  constructor() {
    this.currentPlayer = "X";
    this.gameActive = false;
    this.gameState = ["", "", "", "", "", "", "", "", ""];
    this.gameMode = null; // "local", "ai", "online"
    this.aiDifficulty = "easy";
    this.isAiThinking = false;
    this.playerNames = { X: "Jugador 1", O: "Jugador 2" };
    this.audioDuration = 5000; // Duración por defecto para efectos de celebración
    this.defeatAudioDuration = 4000; // Duración por defecto para efectos de derrota

    this.winningConditions = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8], // Rows
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8], // Columns
      [0, 4, 8],
      [2, 4, 6], // Diagonals
    ];

    this.screens = {
      home: document.getElementById("home-screen"),
      auth: document.getElementById("auth-screen"),
      profile: document.getElementById("profile-screen"),
      leaderboard: document.getElementById("leaderboard-screen"),
      aiConfig: document.getElementById("ai-config-screen"),
      game: document.getElementById("game-screen"),
    };

    this.userManager = new UserManager();
    this.init();
  }

  init() {
    this.userManager.loadCurrentUser();
    this.setupEventListeners();

    if (this.userManager.currentUser) {
      this.showScreen("home");
      this.updateUserInterface();
    } else {
      this.showScreen("auth");
    }
  }

  updateUserInterface() {
    const user = this.userManager.currentUser;
    if (!user) return;

    // Actualizar navegación superior
    const navAvatar = document.getElementById("nav-avatar");
    const navUsername = document.getElementById("nav-username");
    const headerAvatar = document.getElementById("header-avatar");
    const headerPoints = document.getElementById("header-points");

    if (navAvatar) navAvatar.textContent = user.avatar;
    if (navUsername) navUsername.textContent = user.username;
    if (headerAvatar) headerAvatar.textContent = user.avatar;
    if (headerPoints) headerPoints.textContent = user.stats.points;

    // Actualizar perfil si está visible
    this.updateProfileDisplay();
  }

  updateProfileDisplay() {
    const user = this.userManager.currentUser;
    if (!user) return;

    // Avatar y nombre
    const userAvatar = document.getElementById("user-avatar");
    const userDisplayName = document.getElementById("user-display-name");

    if (userAvatar) userAvatar.textContent = user.avatar;
    if (userDisplayName) userDisplayName.textContent = user.username;

    // Stats preview
    document.getElementById("user-level").textContent = user.stats.level;
    document.getElementById("user-points").textContent = user.stats.points;
    document.getElementById("user-rank").textContent =
      this.userManager.getUserRank() || "-";

    // Stats detalladas
    document.getElementById("total-games").textContent = user.stats.gamesPlayed;
    document.getElementById("total-wins").textContent = user.stats.wins;
    document.getElementById("total-losses").textContent = user.stats.losses;
    document.getElementById("total-draws").textContent = user.stats.draws;
    document.getElementById("win-streak").textContent = user.stats.winStreak;
    document.getElementById("best-streak").textContent = user.stats.bestStreak;

    // Win rate
    const winRate =
      user.stats.gamesPlayed > 0
        ? Math.round((user.stats.wins / user.stats.gamesPlayed) * 100)
        : 0;
    document.getElementById("win-rate-fill").style.width = winRate + "%";
    document.getElementById("win-rate-text").textContent = winRate + "%";
  }

  updateLeaderboard() {
    const activeFilter =
      document.querySelector(".filter-btn.active")?.dataset.filter || "points";
    const leaderboard = this.userManager.getLeaderboard(activeFilter);
    const leaderboardList = document.getElementById("leaderboard-list");

    if (!leaderboardList) return;

    // Actualizar estadísticas generales
    this.updateLeaderboardStats();

    leaderboardList.innerHTML = "";

    leaderboard.forEach((user, index) => {
      const playerRow = document.createElement("div");
      playerRow.className = `player-row ${index < 3 ? `top-${index + 1}` : ""}`;

      let statValue;
      switch (activeFilter) {
        case "wins":
          statValue = `${user.stats.wins} victorias`;
          break;
        case "winrate":
          const winRate =
            user.stats.gamesPlayed > 0
              ? Math.round((user.stats.wins / user.stats.gamesPlayed) * 100)
              : 0;
          statValue = `${winRate}% win rate`;
          break;
        default:
          statValue = `${user.stats.points} pts`;
      }

      playerRow.innerHTML = `
                <div class="player-rank">#${index + 1}</div>
                <div class="player-avatar">${user.avatar}</div>
                <div class="player-info">
                    <span class="player-name">${user.username}</span>
                    <span class="player-stats">Nivel ${user.stats.level} • ${
        user.stats.gamesPlayed
      } partidas</span>
                </div>
                <div class="player-points">${statValue}</div>
            `;

      leaderboardList.appendChild(playerRow);
    });

    // Actualizar posición del usuario
    const userPosition = document.getElementById("user-position");
    if (
      userPosition &&
      this.userManager.currentUser &&
      !this.userManager.isGuest
    ) {
      const rank = this.userManager.getUserRank(activeFilter);
      const rankElement = userPosition.querySelector(".position-rank");
      const nameElement = userPosition.querySelector(".position-name");
      const pointsElement = userPosition.querySelector(".position-points");

      if (rankElement) rankElement.textContent = rank > 0 ? `#${rank}` : "#-";
      if (nameElement)
        nameElement.textContent = this.userManager.currentUser.username;
      if (pointsElement)
        pointsElement.textContent = `${this.userManager.currentUser.stats.points} puntos`;
    }
  }

  setupEventListeners() {
    // Navigation
    document.getElementById("user-btn")?.addEventListener("click", () => {
      if (this.userManager.currentUser) {
        this.showScreen("profile");
        this.updateProfileDisplay();
      } else {
        this.showScreen("auth");
      }
    });

    // Leaderboard button - múltiples selectores para asegurar detección
    const leaderboardBtn =
      document.getElementById("leaderboard-btn") ||
      document.querySelector(".leaderboard-btn") ||
      document.querySelector("button[title*='Clasificación']");

    if (leaderboardBtn) {
      // Log de información de resolución para debug
      console.log(`✅ Botón leaderboard encontrado:`, leaderboardBtn);
      console.log(`📱 Resolución: ${window.innerWidth}x${window.innerHeight}`);
      console.log(`🖥️ Tipo de dispositivo: ${this.detectDeviceType()}`);
      console.log(`👁️ Estilos del botón:`, {
        display: getComputedStyle(leaderboardBtn).display,
        visibility: getComputedStyle(leaderboardBtn).visibility,
        opacity: getComputedStyle(leaderboardBtn).opacity,
      });

      leaderboardBtn.addEventListener("click", (e) => {
        console.log("🎯 Botón leaderboard clickeado");
        this.showScreen("leaderboard");
        this.updateLeaderboard();
      });
    } else {
      console.error("❌ Botón leaderboard NO encontrado");
      console.log(
        "🔍 Elementos disponibles con 'leaderboard':",
        document.querySelectorAll(
          "*[class*='leaderboard'], *[id*='leaderboard']"
        )
      );
    }

    // Auth tabs
    document.querySelectorAll(".auth-tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        this.switchAuthTab(tab.dataset.tab);
      });
    });

    // Auth buttons
    document.getElementById("login-btn")?.addEventListener("click", () => {
      this.handleLogin();
    });

    document.getElementById("register-btn")?.addEventListener("click", () => {
      this.handleRegister();
    });

    document.getElementById("guest-btn")?.addEventListener("click", () => {
      this.handleGuestLogin();
    });

    // Profile
    document.getElementById("logout-btn")?.addEventListener("click", () => {
      this.handleLogout();
    });

    document.getElementById("change-avatar")?.addEventListener("click", () => {
      this.toggleAvatarPicker();
    });

    document.querySelectorAll(".avatar-option").forEach((option) => {
      option.addEventListener("click", () => {
        this.selectAvatar(option.dataset.avatar);
      });
    });

    document
      .getElementById("header-profile-btn")
      ?.addEventListener("click", () => {
        this.showScreen("profile");
        this.updateProfileDisplay();
      });

    // Leaderboard
    document.querySelectorAll(".filter-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.setLeaderboardFilter(btn.dataset.filter);
      });
    });

    document
      .getElementById("refresh-leaderboard")
      ?.addEventListener("click", () => {
        this.updateLeaderboard();
      });

    // Mode selection
    document.querySelectorAll(".mode-card").forEach((card) => {
      card.addEventListener("click", () => {
        const mode = card.dataset.mode;
        this.selectGameMode(mode);
      });
    });

    // Difficulty selection
    document.querySelectorAll(".difficulty-card").forEach((card) => {
      card.addEventListener("click", () => {
        const difficulty = card.dataset.difficulty;
        this.selectDifficulty(difficulty);
      });
    });

    // Back buttons
    document.getElementById("back-from-ai")?.addEventListener("click", () => {
      this.showScreen("home");
    });

    document
      .getElementById("back-from-profile")
      ?.addEventListener("click", () => {
        this.showScreen("home");
      });

    document
      .getElementById("back-from-leaderboard")
      ?.addEventListener("click", () => {
        this.showScreen("home");
      });

    document.getElementById("back-to-menu")?.addEventListener("click", () => {
      this.showScreen("home");
      this.resetGame();
    });

    // Game controls
    document.getElementById("restart-game")?.addEventListener("click", () => {
      this.resetGame();
    });

    document.getElementById("new-game")?.addEventListener("click", () => {
      this.showScreen("home");
      this.resetGame();
    });

    // Game board
    document.querySelectorAll(".cell").forEach((cell, index) => {
      cell.addEventListener("click", () => this.makeMove(index));
    });
  }

  // Auth methods
  switchAuthTab(tab) {
    document
      .querySelectorAll(".auth-tab")
      .forEach((t) => t.classList.remove("active"));
    document
      .querySelectorAll(".auth-form")
      .forEach((f) => f.classList.remove("active"));

    document.querySelector(`[data-tab="${tab}"]`).classList.add("active");
    document.getElementById(`${tab}-form`).classList.add("active");
  }

  handleLogin() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;

    if (!username || !password) {
      alert("Por favor completa todos los campos");
      return;
    }

    try {
      this.userManager.login(username, password);
      this.showScreen("home");
      this.updateUserInterface();
      this.showNotification("¡Bienvenido de vuelta!", "success");
    } catch (error) {
      alert(error.message);
    }
  }

  handleRegister() {
    const username = document.getElementById("register-username").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;

    if (!username || !email || !password) {
      alert("Por favor completa todos los campos");
      return;
    }

    if (password.length < 4) {
      alert("La contraseña debe tener al menos 4 caracteres");
      return;
    }

    try {
      this.userManager.register(username, email, password);
      this.showScreen("home");
      this.updateUserInterface();
      this.showNotification("¡Cuenta creada exitosamente!", "success");
    } catch (error) {
      alert(error.message);
    }
  }

  handleGuestLogin() {
    this.userManager.loginAsGuest();
    this.showScreen("home");
    this.updateUserInterface();
    this.showNotification("¡Jugando como invitado!", "info");
  }

  handleLogout() {
    this.userManager.logout();
    this.showScreen("auth");
    this.showNotification("Sesión cerrada", "info");
  }

  // Avatar methods
  toggleAvatarPicker() {
    const picker = document.getElementById("avatar-picker");
    if (picker) {
      picker.classList.toggle("hidden");
    }
  }

  selectAvatar(avatar) {
    this.userManager.updateAvatar(avatar);
    this.updateUserInterface();
    this.toggleAvatarPicker();

    // Update avatar selection
    document.querySelectorAll(".avatar-option").forEach((option) => {
      option.classList.remove("selected");
    });
    document
      .querySelector(`[data-avatar="${avatar}"]`)
      ?.classList.add("selected");
  }

  // Leaderboard methods
  setLeaderboardFilter(filter) {
    document.querySelectorAll(".filter-btn").forEach((btn) => {
      btn.classList.remove("active");
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add("active");
    this.updateLeaderboard();
  }

  // Notification system
  showNotification(message, type = "info") {
    // Simple notification - could be enhanced with a proper notification system
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${
              type === "success"
                ? "#27ae60"
                : type === "error"
                ? "#e74c3c"
                : "#3498db"
            };
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }

  selectGameMode(mode) {
    // Check if mode is disabled
    const modeCard = document.querySelector(`[data-mode="${mode}"]`);
    if (modeCard && modeCard.classList.contains("disabled")) {
      this.showNotification(
        "🚧 Este modo está en desarrollo. ¡Próximamente disponible!",
        "info"
      );
      return;
    }

    // Remove previous selections
    document.querySelectorAll(".mode-card:not(.disabled)").forEach((card) => {
      card.classList.remove("selected");
    });

    // Select current mode
    if (modeCard && !modeCard.classList.contains("disabled")) {
      modeCard.classList.add("selected");
    }

    this.gameMode = mode;

    if (mode === "local") {
      this.playerNames = {
        X: this.userManager.currentUser
          ? this.userManager.currentUser.username
          : "JUGADOR 1",
        O: "JUGADOR 2",
      };
      this.startGame();
    } else if (mode === "ai") {
      this.showScreen("aiConfig");
    }
  }

  selectDifficulty(difficulty) {
    // Remove previous selections
    document.querySelectorAll(".difficulty-card").forEach((card) => {
      card.classList.remove("selected");
    });

    // Select current difficulty
    document
      .querySelector(`[data-difficulty="${difficulty}"]`)
      .classList.add("selected");

    this.aiDifficulty = difficulty;

    // Set player names based on difficulty
    const usernameName = this.userManager.currentUser
      ? this.userManager.currentUser.username
      : "JUGADOR";
    const difficultyNames = {
      easy: "IA FÁCIL",
      medium: "IA MEDIO",
      hard: "IA DIFÍCIL",
    };

    this.playerNames = {
      X: usernameName,
      O: difficultyNames[difficulty] || "IA",
    };

    // Show confirmation message
    this.showNotification(
      `Dificultad ${difficulty.toUpperCase()} seleccionada`,
      "success"
    );

    setTimeout(() => {
      this.startGame();
    }, 800);
  }

  startGame() {
    // Validar que tenemos un modo de juego válido
    if (
      !this.gameMode ||
      (this.gameMode !== "local" && this.gameMode !== "ai")
    ) {
      this.showNotification("Error: Modo de juego no válido", "error");
      this.showScreen("home");
      return;
    }

    // Validar configuración de IA si es necesario
    if (this.gameMode === "ai" && !this.aiDifficulty) {
      this.showNotification("Error: Selecciona una dificultad de IA", "error");
      this.showScreen("aiConfig");
      return;
    }

    this.showScreen("game");
    this.gameActive = true;
    this.currentPlayer = "X";
    this.gameState = ["", "", "", "", "", "", "", "", ""];
    this.isAiThinking = false;

    this.clearBoard();
    this.updateGameDisplay();

    // Mostrar mensaje de inicio
    const modeText =
      this.gameMode === "ai"
        ? `VS IA (${this.aiDifficulty.toUpperCase()})`
        : "LOCAL (2 Jugadores)";
    this.showNotification(`Juego iniciado: ${modeText}`, "success");
  }

  showScreen(screenName) {
    Object.values(this.screens).forEach((screen) => {
      if (screen) screen.classList.remove("active");
    });

    if (this.screens[screenName]) {
      this.screens[screenName].classList.add("active");
    }
  }

  makeMove(position) {
    if (
      !this.gameActive ||
      this.gameState[position] !== "" ||
      this.isAiThinking
    ) {
      return;
    }

    this.gameState[position] = this.currentPlayer;
    this.updateCell(position, this.currentPlayer);

    const winner = this.checkWinner();
    if (winner) {
      this.endGame(winner);
      return;
    } else if (this.isBoardFull()) {
      this.endGame("draw");
      return;
    }

    this.switchPlayer();

    // AI move if in AI mode
    if (this.gameMode === "ai" && this.currentPlayer === "O") {
      this.makeAiMove();
    }
  }

  makeAiMove() {
    if (!this.gameActive || this.gameMode !== "ai") return;

    this.isAiThinking = true;
    this.updateGameDisplay("🤖 IA pensando...");

    // Tiempo de pensamiento variable según dificultad
    const thinkTime = {
      easy: 500,
      medium: 800,
      hard: 1200,
    };

    setTimeout(() => {
      if (!this.gameActive) return; // Verificar que el juego siga activo

      const move = this.getAiMove();
      if (move !== -1 && this.gameState[move] === "") {
        this.gameState[move] = this.currentPlayer;
        this.updateCell(move, this.currentPlayer);

        const winner = this.checkWinner();
        if (winner) {
          this.endGame(winner);
        } else if (this.isBoardFull()) {
          this.endGame("draw");
        } else {
          this.switchPlayer();
        }
      }

      this.isAiThinking = false;
    }, thinkTime[this.aiDifficulty] || 800);
  }

  getAiMove() {
    const emptyCells = this.gameState
      .map((cell, index) => (cell === "" ? index : null))
      .filter((val) => val !== null);

    if (emptyCells.length === 0) return -1;

    switch (this.aiDifficulty) {
      case "easy":
        // Movimientos completamente aleatorios
        return emptyCells[Math.floor(Math.random() * emptyCells.length)];

      case "medium":
        // 70% estratégico, 30% aleatorio
        if (Math.random() < 0.7) {
          const smartMove = this.getBestMove();
          return smartMove !== -1
            ? smartMove
            : emptyCells[Math.floor(Math.random() * emptyCells.length)];
        } else {
          return emptyCells[Math.floor(Math.random() * emptyCells.length)];
        }

      case "hard":
        // Siempre el mejor movimiento posible
        const bestMove = this.getBestMove();
        return bestMove !== -1 ? bestMove : emptyCells[0];

      default:
        return emptyCells[0];
    }
  }

  getBestMove() {
    // Primero verificar si puede ganar
    for (let i = 0; i < 9; i++) {
      if (this.gameState[i] === "") {
        this.gameState[i] = "O";
        if (this.checkWinner() === "O") {
          this.gameState[i] = "";
          return i;
        }
        this.gameState[i] = "";
      }
    }

    // Luego verificar si debe bloquear al jugador
    for (let i = 0; i < 9; i++) {
      if (this.gameState[i] === "") {
        this.gameState[i] = "X";
        if (this.checkWinner() === "X") {
          this.gameState[i] = "";
          return i;
        }
        this.gameState[i] = "";
      }
    }

    // Si no hay movimientos críticos, usar minimax
    let bestScore = -Infinity;
    let bestMove = -1;

    for (let i = 0; i < 9; i++) {
      if (this.gameState[i] === "") {
        this.gameState[i] = "O";
        let score = this.minimax(this.gameState, 0, false);
        this.gameState[i] = "";

        if (score > bestScore) {
          bestScore = score;
          bestMove = i;
        }
      }
    }

    return bestMove;
  }

  minimax(board, depth, isMaximizing) {
    const winner = this.checkWinnerForBoard(board);

    if (winner === "O") return 10 - depth;
    if (winner === "X") return depth - 10;
    if (this.isBoardFullForBoard(board)) return 0;

    if (isMaximizing) {
      let bestScore = -Infinity;
      for (let i = 0; i < 9; i++) {
        if (board[i] === "") {
          board[i] = "O";
          let score = this.minimax(board, depth + 1, false);
          board[i] = "";
          bestScore = Math.max(score, bestScore);
        }
      }
      return bestScore;
    } else {
      let bestScore = Infinity;
      for (let i = 0; i < 9; i++) {
        if (board[i] === "") {
          board[i] = "X";
          let score = this.minimax(board, depth + 1, true);
          board[i] = "";
          bestScore = Math.min(score, bestScore);
        }
      }
      return bestScore;
    }
  }

  checkWinner() {
    return this.checkWinnerForBoard(this.gameState);
  }

  checkWinnerForBoard(board) {
    for (let condition of this.winningConditions) {
      const [a, b, c] = condition;
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return board[a];
      }
    }
    return null;
  }

  isBoardFull() {
    return this.isBoardFullForBoard(this.gameState);
  }

  isBoardFullForBoard(board) {
    return board.every((cell) => cell !== "");
  }

  updateCell(index, value) {
    const cell = document.querySelector(`[data-index="${index}"]`);
    if (cell) {
      cell.textContent = value;
      cell.classList.add("filled");
      cell.classList.add(value.toLowerCase());

      // Animation effect
      cell.style.transform = "scale(0.8)";
      setTimeout(() => {
        cell.style.transform = "scale(1)";
      }, 200);
    }
  }

  switchPlayer() {
    this.currentPlayer = this.currentPlayer === "X" ? "O" : "X";
    this.updateGameDisplay();
  }

  updateGameDisplay(customMessage = null) {
    const playerBadge = document.getElementById("current-player-badge");
    const turnText = document.getElementById("turn-text");

    if (playerBadge && turnText) {
      if (customMessage) {
        turnText.textContent = customMessage;
        return;
      }

      const currentPlayerName = this.playerNames[this.currentPlayer];
      playerBadge.textContent = currentPlayerName;

      if (this.gameMode === "ai") {
        if (this.currentPlayer === "X") {
          turnText.textContent = `Tu turno (${this.currentPlayer})`;
        } else {
          turnText.textContent = "Turno de la IA";
        }
      } else if (this.gameMode === "local") {
        turnText.textContent = `Turno de ${currentPlayerName} (${this.currentPlayer})`;
      } else {
        turnText.textContent = `Turno del Jugador ${this.currentPlayer}`;
      }
    }
  }

  endGame(winner) {
    this.gameActive = false;
    this.isAiThinking = false;

    // Update user statistics
    let gameResult = null;
    if (winner === "draw") {
      this.updateGameDisplay("¡Es un empate! 🤝");
      gameResult = "draw";
    } else if (this.gameMode === "ai") {
      if (winner === "X") {
        this.updateGameDisplay("¡Has ganado! 🎉");
        gameResult = "win";
      } else {
        this.updateGameDisplay("La IA ha ganado 🤖");
        gameResult = "loss";
      }
    } else if (this.gameMode === "local") {
      this.updateGameDisplay(`¡${this.playerNames[winner]} ha ganado! 🎉`);
      // En modo local, solo registramos si el usuario principal (X) gana
      if (this.userManager.currentUser && !this.userManager.isGuest) {
        gameResult = winner === "X" ? "win" : "loss";
      }
    }

    // Actualizar estadísticas del usuario
    if (gameResult) {
      this.userManager.updateUserStats(gameResult);
      this.updateUserInterface();
    }

    // Highlight winning cells
    if (winner !== "draw") {
      this.highlightWinningCells(winner);
    }

    // Show celebration effect
    this.showCelebration(winner);

    // Show points earned notification
    if (
      gameResult &&
      this.userManager.currentUser &&
      !this.userManager.isGuest
    ) {
      const pointsEarned =
        gameResult === "win" ? 10 : gameResult === "draw" ? 3 : -3;
      if (pointsEarned > 0) {
        this.showNotification(`+${pointsEarned} puntos ganados!`, "success");
      }
    }
  }

  highlightWinningCells(winner) {
    for (let condition of this.winningConditions) {
      const [a, b, c] = condition;
      if (
        this.gameState[a] === winner &&
        this.gameState[b] === winner &&
        this.gameState[c] === winner
      ) {
        [a, b, c].forEach((index) => {
          const cell = document.querySelector(`[data-index="${index}"]`);
          if (cell) {
            cell.style.background = "rgba(255, 215, 0, 0.3)";
            cell.style.borderColor = "#ffd700";
            cell.style.boxShadow = "0 0 20px rgba(255, 215, 0, 0.5)";
          }
        });
        break;
      }
    }
  }

  showCelebration(winner) {
    if (winner !== "draw") {
      // Determinar si es victoria o derrota
      const isVictory = this.isPlayerVictory(winner);

      if (isVictory) {
        // 🎵 Reproducir audio de victoria
        this.playVictorySound();

        // 🎉 Mostrar mensaje de victoria
        this.showVictoryMessage(winner);

        // 🎊 Crear confeti y efectos
        this.createConfettiEffect();

        // 🎆 Fuegos artificiales
        this.createFireworksEffect();
      } else {
        // 💀 Reproducir audio de derrota
        this.playDefeatSound();

        // 😢 Mostrar mensaje de derrota
        this.showDefeatMessage(winner);

        // 💀 Crear efectos de derrota
        this.createDefeatEffect();

        // 🌧️ Lluvia roja
        this.createRedRainEffect();
      }

      // ✨ Animar tablero
      const gameBoard = document.querySelector(".game-board");
      if (gameBoard) {
        const animation = isVictory
          ? "pulse 0.5s ease-in-out"
          : "shake 0.6s ease-in-out";
        gameBoard.style.animation = animation;
        setTimeout(
          () => {
            gameBoard.style.animation = "";
          },
          isVictory ? 500 : 600
        );
      }
    }
  }

  isPlayerVictory(winner) {
    if (this.gameMode === "ai") {
      return winner === "X"; // El jugador siempre es X
    } else if (this.gameMode === "local") {
      // En modo local, consideramos victoria si el usuario actual gana
      if (this.userManager.currentUser && !this.userManager.isGuest) {
        return winner === "X"; // Asumimos que el usuario principal es X
      } else {
        return true; // En modo invitado, cualquier victoria es celebración
      }
    }
    return true;
  }

  playVictorySound() {
    try {
      const audio = new Audio("static/music/efectos/ganstes.mp3");
      audio.volume = 0.7;
      audio
        .play()
        .catch((e) => console.log("No se pudo reproducir el audio:", e));

      // Obtener duración del audio para sincronizar efectos
      audio.addEventListener("loadedmetadata", () => {
        this.audioDuration = audio.duration * 1000; // Convertir a milisegundos
      });
    } catch (error) {
      console.log("Error al cargar el audio de victoria:", error);
      this.audioDuration = 5000; // Duración por defecto de 5 segundos
    }
  }

  playDefeatSound() {
    try {
      const audio = new Audio("static/music/efectos/perdiste.mp3");
      audio.volume = 0.7;
      audio
        .play()
        .catch((e) =>
          console.log("No se pudo reproducir el audio de derrota:", e)
        );

      // Obtener duración del audio para sincronizar efectos
      audio.addEventListener("loadedmetadata", () => {
        this.defeatAudioDuration = audio.duration * 1000; // Convertir a milisegundos
      });
    } catch (error) {
      console.log("Error al cargar el audio de derrota:", error);
      this.defeatAudioDuration = 4000; // Duración por defecto de 4 segundos
    }
  }

  showVictoryMessage(winner) {
    const message = document.createElement("div");
    message.className = "victory-message";

    let messageText = "";
    if (this.gameMode === "ai") {
      messageText =
        winner === "X" ? "¡Felicitaciones! 🏆" : "La IA ha ganado 🤖";
    } else {
      messageText = `¡${this.playerNames[winner]} ha ganado! 🏆`;
    }

    message.innerHTML = `
      <h1>🎉 ${messageText} 🎉</h1>
      <p>¡Excelente partida!</p>
    `;

    document.body.appendChild(message);

    // Remover mensaje después de la duración del audio
    setTimeout(() => {
      if (message.parentNode) {
        message.style.animation = "fadeOut 0.5s ease-out forwards";
        setTimeout(() => message.remove(), 500);
      }
    }, this.audioDuration || 5000);
  }

  createConfettiEffect() {
    const overlay = document.createElement("div");
    overlay.className = "celebration-overlay";
    document.body.appendChild(overlay);

    const confettiTypes = [
      { class: "confetti-square", content: "" },
      { class: "confetti-circle", content: "" },
      { class: "confetti-triangle", content: "" },
      { class: "confetti-star", content: "" },
      { class: "confetti-trophy", content: "🏆" },
      { class: "confetti-trophy", content: "🥇" },
      { class: "confetti-heart", content: "💎" },
      { class: "confetti-heart", content: "⭐" },
      { class: "confetti-heart", content: "🎊" },
      { class: "confetti-heart", content: "🎉" },
    ];

    const particleCount = 150;
    const duration = this.audioDuration || 5000;

    for (let i = 0; i < particleCount; i++) {
      setTimeout(() => {
        const particle = document.createElement("div");
        const type =
          confettiTypes[Math.floor(Math.random() * confettiTypes.length)];

        particle.className = `confetti-particle ${type.class}`;
        particle.textContent = type.content;

        // Posición inicial aleatoria en la parte superior
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDuration = 2 + Math.random() * 3 + "s";
        particle.style.animationDelay = Math.random() * 2 + "s";

        overlay.appendChild(particle);

        // Remover partícula después de la animación
        setTimeout(() => {
          if (particle.parentNode) {
            particle.remove();
          }
        }, 6000);
      }, Math.random() * (duration * 0.8));
    }

    // Remover overlay después de la duración del audio
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.remove();
      }
    }, duration + 2000);
  }

  createFireworksEffect() {
    const colors = ["#1db954", "#1ed760", "#ffd700", "#ff6b6b", "#ee5a24"];
    const fireworkCount = 8;

    for (let i = 0; i < fireworkCount; i++) {
      setTimeout(() => {
        const firework = document.createElement("div");
        firework.className = "firework";
        firework.style.background =
          colors[Math.floor(Math.random() * colors.length)];
        firework.style.left = 20 + Math.random() * 60 + "%";
        firework.style.top = 20 + Math.random() * 60 + "%";

        document.body.appendChild(firework);

        setTimeout(() => {
          if (firework.parentNode) {
            firework.remove();
          }
        }, 1200);
      }, i * 300);
    }
  }

  showDefeatMessage(winner) {
    const message = document.createElement("div");
    message.className = "defeat-message";

    let messageText = "";
    if (this.gameMode === "ai") {
      messageText = "¡Has perdido! 💀";
    } else {
      messageText = `¡${this.playerNames[winner]} ha ganado! 😔`;
    }

    message.innerHTML = `
      <h1>💀 ${messageText} 💀</h1>
      <p>¡La próxima vez será!</p>
    `;

    document.body.appendChild(message);

    // Remover mensaje después de la duración del audio
    setTimeout(() => {
      if (message.parentNode) {
        message.style.animation = "fadeOut 0.5s ease-out forwards";
        setTimeout(() => message.remove(), 500);
      }
    }, this.defeatAudioDuration || 4000);
  }

  createDefeatEffect() {
    const overlay = document.createElement("div");
    overlay.className = "defeat-overlay";
    document.body.appendChild(overlay);

    const defeatSymbols = [
      { class: "defeat-skull", content: "💀" },
      { class: "defeat-skull", content: "☠️" },
      { class: "defeat-broken-heart", content: "💔" },
      { class: "defeat-broken-heart", content: "😵" },
      { class: "defeat-cross", content: "✖️" },
      { class: "defeat-cross", content: "❌" },
      { class: "defeat-sad", content: "😭" },
      { class: "defeat-sad", content: "😢" },
      { class: "defeat-sad", content: "😰" },
      { class: "defeat-cross", content: "⚰️" },
    ];

    const particleCount = 100;
    const duration = this.defeatAudioDuration || 4000;

    for (let i = 0; i < particleCount; i++) {
      setTimeout(() => {
        const particle = document.createElement("div");
        const symbol =
          defeatSymbols[Math.floor(Math.random() * defeatSymbols.length)];

        particle.className = `defeat-particle ${symbol.class}`;
        particle.textContent = symbol.content;

        // Posición inicial aleatoria en la parte superior
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDuration = 3 + Math.random() * 2 + "s";
        particle.style.animationDelay = Math.random() * 1 + "s";

        overlay.appendChild(particle);

        // Remover partícula después de la animación
        setTimeout(() => {
          if (particle.parentNode) {
            particle.remove();
          }
        }, 7000);
      }, Math.random() * (duration * 0.8));
    }

    // Remover overlay después de la duración del audio
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.remove();
      }
    }, duration + 2000);
  }

  createRedRainEffect() {
    const rainCount = 40;
    const duration = this.defeatAudioDuration || 4000;

    for (let i = 0; i < rainCount; i++) {
      setTimeout(() => {
        const rainDrop = document.createElement("div");
        rainDrop.className = "red-rain";

        // Posición inicial aleatoria en la parte superior
        rainDrop.style.left = Math.random() * 100 + "%";
        rainDrop.style.animationDuration = 1 + Math.random() * 2 + "s";
        rainDrop.style.animationDelay = Math.random() * 0.5 + "s";

        document.body.appendChild(rainDrop);

        // Remover gota después de la animación
        setTimeout(() => {
          if (rainDrop.parentNode) {
            rainDrop.remove();
          }
        }, 4000);
      }, Math.random() * (duration * 0.9));
    }
  }

  resetGame() {
    this.gameState = ["", "", "", "", "", "", "", "", ""];
    this.currentPlayer = "X";
    this.gameActive = true;
    this.isAiThinking = false;
    this.clearBoard();
    this.updateGameDisplay();
  }

  clearBoard() {
    const cells = document.querySelectorAll(".cell");
    cells.forEach((cell) => {
      cell.textContent = "";
      cell.classList.remove("filled", "x", "o");
      cell.style.background = "";
      cell.style.borderColor = "";
      cell.style.boxShadow = "";
      cell.style.transform = "";
    });
  }

  // Actualizar estadísticas generales del leaderboard
  updateLeaderboardStats() {
    const users = this.userManager
      .getUsers()
      .filter((u) => u.stats.gamesPlayed > 0);

    // Total de jugadores activos
    const totalPlayers = users.length;
    const totalPlayersEl = document.getElementById("total-players");
    if (totalPlayersEl) totalPlayersEl.textContent = totalPlayers;

    // Total de partidas jugadas
    const totalGames = users.reduce(
      (sum, user) => sum + user.stats.gamesPlayed,
      0
    );
    const totalGamesEl = document.getElementById("total-games-played");
    if (totalGamesEl) totalGamesEl.textContent = totalGames.toLocaleString();

    // Puntuación máxima
    const highestScore =
      users.length > 0 ? Math.max(...users.map((u) => u.stats.points)) : 0;
    const highestScoreEl = document.getElementById("highest-score");
    if (highestScoreEl)
      highestScoreEl.textContent = highestScore.toLocaleString();
  }

  // Método para detectar el tipo de dispositivo
  detectDeviceType() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    if (width <= 480) {
      return "Móvil (Portrait)";
    } else if (width <= 768) {
      return "Móvil/Tablet";
    } else if (width <= 1024) {
      return "Tablet/Laptop pequeña";
    } else if (width <= 1440) {
      return "Laptop/Desktop";
    } else {
      return "TV/Monitor grande";
    }
  }
}

// Función para forzar la visibilidad del botón leaderboard
function forceLeaderboardButtonVisibility() {
  setTimeout(() => {
    const buttons = [
      document.getElementById("leaderboard-btn"),
      document.querySelector(".leaderboard-btn"),
      document.querySelector("button[title*='Clasificación']"),
    ].filter(Boolean);

    buttons.forEach((btn) => {
      if (btn) {
        btn.style.display = "flex";
        btn.style.visibility = "visible";
        btn.style.opacity = "1";
        btn.style.zIndex = "9999";
        btn.style.position = "relative";
        console.log("🔧 Forzada visibilidad del botón:", btn);
      }
    });
  }, 100);
}

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", () => {
  new TicTacToeGame();
  initializeMusicBubble();

  // Forzar visibilidad del botón después de cargar
  forceLeaderboardButtonVisibility();

  // También verificar cada segundo por si hay cambios dinámicos
  setInterval(forceLeaderboardButtonVisibility, 1000);
});

// Función auxiliar para información (opcional)
function toggleInfo() {
  const infoContent = document.getElementById("info-content");
  const toggleButton = document.getElementById("toggle-info");

  if (infoContent && toggleButton) {
    infoContent.classList.toggle("hidden");

    if (infoContent.classList.contains("hidden")) {
      toggleButton.textContent = "ℹ️ Información del Proyecto";
    } else {
      toggleButton.textContent = "❌ Ocultar Información";
    }
  }
}

// 🎵 Sistema de Música Estilo Spotify
function initializeMusicBubble() {
  const musicBubble = document.getElementById("music-bubble");
  const musicPanel = document.getElementById("music-panel");
  const panelClose = document.getElementById("panel-close");
  const musicToggle = document.getElementById("music-toggle");
  const musicPrev = document.getElementById("music-prev");
  const musicNext = document.getElementById("music-next");
  const musicShuffle = document.getElementById("music-shuffle");
  const musicRepeat = document.getElementById("music-repeat");
  const volumeControl = document.getElementById("volume-control");
  const volumePercentage = document.getElementById("volume-percentage");
  const volumeBtn = document.getElementById("volume-btn");
  const progressFill = document.getElementById("progress-fill");
  const progressHandle = document.getElementById("progress-handle");
  const backgroundMusic = document.getElementById("background-music");

  let isPlaying = true;
  let isPanelOpen = false;
  let isShuffled = false;
  let repeatMode = 0; // 0: off, 1: all, 2: one
  let currentTime = 0;
  let duration = 204; // 3:24 en segundos

  // Función para abrir/cerrar el panel
  function togglePanel() {
    isPanelOpen = !isPanelOpen;
    musicPanel.classList.toggle("active", isPanelOpen);
  }

  // Función para cerrar el panel
  function closePanel() {
    isPanelOpen = false;
    musicPanel.classList.remove("active");
  }

  // Función para toggle play/pause
  function toggleMusic() {
    if (isPlaying) {
      backgroundMusic.pause();
      document.querySelector(".play-icon").style.display = "block";
      document.querySelector(".pause-icon").style.display = "none";
      isPlaying = false;
    } else {
      backgroundMusic
        .play()
        .catch((e) => console.log("Error al reproducir:", e));
      document.querySelector(".play-icon").style.display = "none";
      document.querySelector(".pause-icon").style.display = "block";
      isPlaying = true;
    }
  }

  // Función para retroceder
  function previousTrack() {
    backgroundMusic.currentTime = 0;
    currentTime = 0;
    updateProgress();
    showNotification("⏮️ Pista anterior", "info");
  }

  // Función para siguiente pista
  function nextTrack() {
    backgroundMusic.currentTime = 0;
    currentTime = 0;
    updateProgress();
    showNotification("⏭️ Siguiente pista", "info");
  }

  // Función para toggle shuffle
  function toggleShuffle() {
    isShuffled = !isShuffled;
    musicShuffle.classList.toggle("active", isShuffled);
    showNotification(
      isShuffled ? "🔀 Aleatorio activado" : "🔀 Aleatorio desactivado",
      "info"
    );
  }

  // Función para toggle repeat
  function toggleRepeat() {
    repeatMode = (repeatMode + 1) % 3;
    musicRepeat.classList.toggle("active", repeatMode > 0);

    const messages = [
      "🔁 Repetir desactivado",
      "🔁 Repetir todas",
      "🔂 Repetir una",
    ];
    showNotification(messages[repeatMode], "info");
  }

  // Función para cambiar volumen
  function changeVolume() {
    const volume = parseFloat(volumeControl.value);
    backgroundMusic.volume = volume;
    volumePercentage.textContent = Math.round(volume * 100);

    // Actualizar gradiente del slider
    const percentage = volume * 100;
    volumeControl.style.background = `linear-gradient(to right, #1db954 0%, #1db954 ${percentage}%, #4f4f4f ${percentage}%, #4f4f4f 100%)`;
  }

  // Función para actualizar progreso
  function updateProgress() {
    if (backgroundMusic && !isNaN(backgroundMusic.duration)) {
      currentTime = backgroundMusic.currentTime;
      duration = backgroundMusic.duration;

      const percentage = (currentTime / duration) * 100;
      progressFill.style.width = percentage + "%";
      progressHandle.style.left = percentage + "%";

      // Actualizar tiempos
      document.querySelector(".time-current").textContent =
        formatTime(currentTime);
      document.querySelector(".time-total").textContent = formatTime(duration);
    }
  }

  // Función para formatear tiempo
  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  }

  // Función para mostrar notificaciones
  function showNotification(message, type = "info") {
    // Crear elemento de notificación
    const notification = document.createElement("div");
    notification.className = `music-notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      bottom: 100px;
      right: 30px;
      background: rgba(0, 0, 0, 0.9);
      color: white;
      padding: 10px 15px;
      border-radius: 10px;
      font-size: 0.9rem;
      z-index: 1001;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
    `;

    document.body.appendChild(notification);

    // Mostrar notificación
    setTimeout(() => {
      notification.style.opacity = "1";
      notification.style.transform = "translateY(0)";
    }, 100);

    // Ocultar y eliminar después de 2 segundos
    setTimeout(() => {
      notification.style.opacity = "0";
      notification.style.transform = "translateY(-20px)";
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 2000);
  }

  // Event listeners
  if (musicBubble) {
    musicBubble.addEventListener("click", (e) => {
      if (e.target === musicBubble || e.target.closest(".bubble-icon")) {
        togglePanel();
      }
    });
  }

  if (panelClose) {
    panelClose.addEventListener("click", closePanel);
  }

  if (musicToggle) {
    musicToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleMusic();
    });
  }

  if (musicPrev) {
    musicPrev.addEventListener("click", (e) => {
      e.stopPropagation();
      previousTrack();
    });
  }

  if (musicNext) {
    musicNext.addEventListener("click", (e) => {
      e.stopPropagation();
      nextTrack();
    });
  }

  if (musicShuffle) {
    musicShuffle.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleShuffle();
    });
  }

  if (musicRepeat) {
    musicRepeat.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleRepeat();
    });
  }

  if (volumeControl) {
    volumeControl.addEventListener("input", changeVolume);
    // Inicializar volumen
    changeVolume();
  }

  // Progreso de la canción
  if (backgroundMusic) {
    backgroundMusic.addEventListener("timeupdate", updateProgress);
    backgroundMusic.addEventListener("loadedmetadata", updateProgress);
  }

  // Barra de progreso clickeable
  if (progressFill && progressFill.parentElement) {
    progressFill.parentElement.addEventListener("click", (e) => {
      if (backgroundMusic && !isNaN(backgroundMusic.duration)) {
        const rect = e.currentTarget.getBoundingClientRect();
        const percentage = (e.clientX - rect.left) / rect.width;
        const newTime = percentage * backgroundMusic.duration;
        backgroundMusic.currentTime = newTime;
        updateProgress();
      }
    });
  }

  // Cerrar panel al hacer clic fuera
  document.addEventListener("click", (e) => {
    if (isPanelOpen && !musicBubble.contains(e.target)) {
      closePanel();
    }
  });

  // Manejar eventos de la música
  if (backgroundMusic) {
    backgroundMusic.addEventListener("ended", () => {
      if (repeatMode === 2) {
        // Repetir una
        backgroundMusic.currentTime = 0;
        backgroundMusic
          .play()
          .catch((e) => console.log("Error al reproducir:", e));
      } else {
        // Pasar a siguiente (simular)
        nextTrack();
      }
    });

    backgroundMusic.addEventListener("pause", () => {
      document.querySelector(".play-icon").style.display = "block";
      document.querySelector(".pause-icon").style.display = "none";
      isPlaying = false;
    });

    backgroundMusic.addEventListener("play", () => {
      document.querySelector(".play-icon").style.display = "none";
      document.querySelector(".pause-icon").style.display = "block";
      isPlaying = true;
    });

    backgroundMusic.addEventListener("loadstart", () => {
      updateProgress();
    });
  }

  // Inicialización del estado
  setTimeout(() => {
    updateProgress();
    if (isPlaying) {
      document.querySelector(".pause-icon").style.display = "block";
      document.querySelector(".play-icon").style.display = "none";
    }
  }, 500);

  // Inicializar estado
  showNotification("🎵 Player Spotify listo", "success");
}
