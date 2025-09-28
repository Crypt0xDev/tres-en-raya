// Tres en Raya - Cliente JavaScript con IA (Versión estática para GitHub Pages)
let currentPlayer = "X";
let gameActive = true;
let gameState = ["", "", "", "", "", "", "", "", ""];
let gameMode = "pvp"; // "pvp" o "ai"
let aiDifficulty = "easy"; // "easy", "medium", "hard"
let isAiThinking = false;

const winningConditions = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8], // Rows
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8], // Columns
  [0, 4, 8],
  [2, 4, 6], // Diagonals
];

document.addEventListener("DOMContentLoaded", () => {
  initializeGame();
});

function initializeGame() {
  const cells = document.querySelectorAll(".cell");
  const resetButton = document.getElementById("reset-btn");
  const toggleInfoButton = document.getElementById("toggle-info");
  
  // Mode selection buttons
  const pvpModeBtn = document.getElementById("pvp-mode");
  const aiModeBtn = document.getElementById("ai-mode");
  
  // Difficulty buttons
  const easyBtn = document.getElementById("easy-btn");
  const mediumBtn = document.getElementById("medium-btn");
  const hardBtn = document.getElementById("hard-btn");

  // Add event listeners to cells
  cells.forEach((cell, index) => {
    cell.addEventListener("click", () => makeMove(index));
  });

  // Add event listener to reset button
  if (resetButton) {
    resetButton.addEventListener("click", resetGame);
  }

  // Add event listener to toggle info button
  if (toggleInfoButton) {
    toggleInfoButton.addEventListener("click", toggleInfo);
  }

  // Mode selection event listeners
  if (pvpModeBtn) {
    pvpModeBtn.addEventListener("click", () => setGameMode("pvp"));
  }
  
  if (aiModeBtn) {
    aiModeBtn.addEventListener("click", () => setGameMode("ai"));
  }

  // Difficulty selection event listeners
  if (easyBtn) {
    easyBtn.addEventListener("click", () => setAiDifficulty("easy"));
  }
  
  if (mediumBtn) {
    mediumBtn.addEventListener("click", () => setAiDifficulty("medium"));
  }
  
  if (hardBtn) {
    hardBtn.addEventListener("click", () => setAiDifficulty("hard"));
  }

  // Initialize game state
  gameActive = true;
  updateDisplay();
}

function makeMove(position) {
  if (!gameActive || gameState[position] !== "" || isAiThinking) {
    return;
  }

  // Make move locally
  gameState[position] = currentPlayer;
  updateCell(position, currentPlayer);

  const winner = checkWinner();
  if (winner) {
    endGame(winner);
    return;
  } else if (isBoardFull()) {
    endGame("draw");
    return;
  }

  switchPlayer();

  // If it's AI mode and now it's O's turn (AI), make AI move
  if (gameMode === "ai" && currentPlayer === "O" && gameActive) {
    isAiThinking = true;
    updateDisplay();
    
    // Add delay for better UX
    setTimeout(() => {
      makeAiMove();
      isAiThinking = false;
    }, 800);
  }
}

function checkWinner() {
  for (let condition of winningConditions) {
    const [a, b, c] = condition;
    if (
      gameState[a] &&
      gameState[a] === gameState[b] &&
      gameState[a] === gameState[c]
    ) {
      return gameState[a];
    }
  }
  return null;
}

function isBoardFull() {
  return gameState.every((cell) => cell !== "");
}

function updateCell(index, value) {
  const cell = document.querySelector(`[data-index="${index}"]`);
  if (cell) {
    cell.textContent = value;
    cell.classList.add("filled");

    // Add animation effect
    cell.style.transform = "scale(0.95)";
    setTimeout(() => {
      cell.style.transform = "scale(1)";
    }, 150);
  }
}

function switchPlayer() {
  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateDisplay();
}

function updateDisplay() {
  const playerDisplay = document.getElementById("current-player");
  const statusDisplay = document.getElementById("game-status");
  const modeDisplay = document.getElementById("game-mode-display");

  if (modeDisplay) {
    if (gameMode === "pvp") {
      modeDisplay.textContent = "Modo: Jugador vs Jugador";
    } else {
      const difficultyText = {
        easy: "Fácil",
        medium: "Medio", 
        hard: "Difícil"
      };
      modeDisplay.textContent = `Modo: Jugador vs IA (${difficultyText[aiDifficulty]})`;
    }
  }

  if (playerDisplay) {
    if (gameMode === "ai") {
      if (currentPlayer === "X") {
        playerDisplay.textContent = isAiThinking ? "IA está pensando..." : "Tu turno (X)";
      } else {
        playerDisplay.textContent = isAiThinking ? "IA está pensando..." : "Turno de la IA (O)";
      }
    } else {
      playerDisplay.textContent = `Turno de: Jugador ${currentPlayer}`;
    }
  }

  if (statusDisplay && !gameActive) {
    statusDisplay.style.display = "block";
  } else if (statusDisplay) {
    statusDisplay.style.display = "none";
  }
}

function endGame(winner) {
  gameActive = false;
  isAiThinking = false;
  const statusDisplay = document.getElementById("game-status");

  if (statusDisplay) {
    if (winner === "draw") {
      statusDisplay.textContent = "¡Es un empate!";
      statusDisplay.style.color = "#f39c12";
    } else if (gameMode === "ai") {
      if (winner === "X") {
        statusDisplay.textContent = "¡Has ganado! 🎉";
        statusDisplay.style.color = "#27ae60";
      } else {
        statusDisplay.textContent = "La IA ha ganado 🤖";
        statusDisplay.style.color = "#e74c3c";
      }
    } else {
      statusDisplay.textContent = `¡Jugador ${winner} ha ganado!`;
      statusDisplay.style.color = "#27ae60";
    }
    statusDisplay.style.display = "block";
  }

  // Highlight winning cells if there's a winner
  if (winner !== "draw") {
    highlightWinningCells(winner);
  }
}

function highlightWinningCells(winner) {
  for (let condition of winningConditions) {
    const [a, b, c] = condition;
    if (
      gameState[a] === winner &&
      gameState[b] === winner &&
      gameState[c] === winner
    ) {
      const cells = [a, b, c];
      cells.forEach((index) => {
        const cell = document.querySelector(`[data-index="${index}"]`);
        if (cell) {
          cell.style.background = "rgba(39, 174, 96, 0.4)";
          cell.style.borderColor = "#27ae60";
        }
      });
      break;
    }
  }
}

function resetGame() {
  gameState = ["", "", "", "", "", "", "", "", ""];
  currentPlayer = "X";
  gameActive = true;
  isAiThinking = false;

  const cells = document.querySelectorAll(".cell");
  cells.forEach((cell) => {
    cell.textContent = "";
    cell.classList.remove("filled");
    cell.style.background = "";
    cell.style.borderColor = "";
  });

  const statusDisplay = document.getElementById("game-status");
  if (statusDisplay) {
    statusDisplay.textContent = "";
    statusDisplay.style.display = "none";
  }

  updateDisplay();
}

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

// =============== FUNCIONES DE MODO DE JUEGO ===============

function setGameMode(mode) {
  gameMode = mode;
  
  // Update button states
  const pvpBtn = document.getElementById("pvp-mode");
  const aiBtn = document.getElementById("ai-mode");
  const difficultySelector = document.getElementById("ai-difficulty");
  
  if (mode === "pvp") {
    pvpBtn.classList.add("active");
    aiBtn.classList.remove("active");
    difficultySelector.classList.add("hidden");
  } else {
    aiBtn.classList.add("active");
    pvpBtn.classList.remove("active");
    difficultySelector.classList.remove("hidden");
  }
  
  resetGame();
}

function setAiDifficulty(difficulty) {
  aiDifficulty = difficulty;
  
  // Update difficulty button states
  document.querySelectorAll(".difficulty-btn").forEach(btn => {
    btn.classList.remove("active");
  });
  
  document.getElementById(`${difficulty}-btn`).classList.add("active");
  
  if (gameMode === "ai") {
    updateDisplay();
  }
}

// =============== FUNCIONES DE IA ===============

function makeAiMove() {
  if (!gameActive || currentPlayer !== "O") {
    return;
  }

  let position;
  
  switch (aiDifficulty) {
    case "easy":
      position = getEasyMove();
      break;
    case "medium":
      position = getMediumMove();
      break;
    case "hard":
      position = getHardMove();
      break;
    default:
      position = getEasyMove();
  }

  if (position !== -1) {
    gameState[position] = "O";
    updateCell(position, "O");

    const winner = checkWinner();
    if (winner) {
      endGame(winner);
    } else if (isBoardFull()) {
      endGame("draw");
    } else {
      switchPlayer();
    }
  }
}

function getEasyMove() {
  // Easy: Random move
  const availableMoves = gameState
    .map((cell, index) => cell === "" ? index : null)
    .filter(val => val !== null);
    
  if (availableMoves.length === 0) return -1;
  
  return availableMoves[Math.floor(Math.random() * availableMoves.length)];
}

function getMediumMove() {
  // Medium: 70% chance strategic, 30% random
  if (Math.random() < 0.7) {
    return getHardMove();
  } else {
    return getEasyMove();
  }
}

function getHardMove() {
  // Hard: Use minimax algorithm
  const bestMove = minimax(gameState, 0, true);
  return bestMove.index;
}

function minimax(board, depth, isMaximizing) {
  const winner = checkWinnerForBoard(board);
  
  if (winner === "O") return { score: 10 - depth };
  if (winner === "X") return { score: depth - 10 };
  if (board.every(cell => cell !== "")) return { score: 0 };

  if (isMaximizing) {
    let bestScore = -Infinity;
    let bestMove = { index: -1, score: bestScore };
    
    for (let i = 0; i < 9; i++) {
      if (board[i] === "") {
        board[i] = "O";
        const score = minimax(board, depth + 1, false);
        board[i] = "";
        
        if (score.score > bestScore) {
          bestScore = score.score;
          bestMove = { index: i, score: bestScore };
        }
      }
    }
    return bestMove;
  } else {
    let bestScore = Infinity;
    let bestMove = { index: -1, score: bestScore };
    
    for (let i = 0; i < 9; i++) {
      if (board[i] === "") {
        board[i] = "X";
        const score = minimax(board, depth + 1, true);
        board[i] = "";
        
        if (score.score < bestScore) {
          bestScore = score.score;
          bestMove = { index: i, score: bestScore };
        }
      }
    }
    return bestMove;
  }
}

function checkWinnerForBoard(board) {
  for (let condition of winningConditions) {
    const [a, b, c] = condition;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a];
    }
  }
  return null;
}
