// Tres en Raya - Cliente JavaScript (Versión estática para GitHub Pages)
let currentPlayer = "X";
let gameActive = true;
let gameState = ["", "", "", "", "", "", "", "", ""];

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

  // Initialize game state
  gameActive = true;
  updateDisplay();
}

function makeMove(position) {
  if (!gameActive || gameState[position] !== "") {
    return;
  }

  // Make move locally
  gameState[position] = currentPlayer;
  updateCell(position, currentPlayer);

  const winner = checkWinner();
  if (winner) {
    endGame(winner);
  } else if (isBoardFull()) {
    endGame("draw");
  } else {
    switchPlayer();
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

  if (playerDisplay) {
    playerDisplay.textContent = `Turno de: Jugador ${currentPlayer}`;
  }

  if (statusDisplay && !gameActive) {
    statusDisplay.style.display = "block";
  } else if (statusDisplay) {
    statusDisplay.style.display = "none";
  }
}

function endGame(winner) {
  gameActive = false;
  const statusDisplay = document.getElementById("game-status");

  if (statusDisplay) {
    if (winner === "draw") {
      statusDisplay.textContent = "¡Es un empate!";
      statusDisplay.style.color = "#f39c12";
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
