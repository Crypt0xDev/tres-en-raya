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

    document
      .getElementById("leaderboard-btn")
      ?.addEventListener("click", () => {
        this.showScreen("leaderboard");
        this.updateLeaderboard();
      });

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
      // Add some celebration particles or animation
      const gameBoard = document.querySelector(".game-board");
      if (gameBoard) {
        gameBoard.style.animation = "pulse 0.5s ease-in-out";
        setTimeout(() => {
          gameBoard.style.animation = "";
        }, 500);
      }
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
}

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", () => {
  new TicTacToeGame();
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
