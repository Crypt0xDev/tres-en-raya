// Tres en Raya - Cliente JavaScript
let gameId = null;
let currentPlayer = "X";
let gameActive = false;
let gameState = ["", "", "", "", "", "", "", "", ""];
let playerName = "Player 1";

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

  // Add event listeners to cells
  cells.forEach((cell, index) => {
    cell.addEventListener("click", () => makeMove(index));
  });

  // Add event listener to reset button
  if (resetButton) {
    resetButton.addEventListener("click", resetGame);
  }

  // Start a new game if in web mode
  if (typeof gameMode !== "undefined" && gameMode === "multiplayer") {
    startNewGame();
  } else {
    gameActive = true;
    updateDisplay();
  }
}

async function startNewGame() {
  try {
    const response = await fetch("/game/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        player1: "Player 1",
        player2: "Player 2",
      }),
    });

    const data = await response.json();
    if (data.game_id) {
      gameId = data.game_id;
      gameActive = true;
      resetLocalState();
      updateDisplay();
    }
  } catch (error) {
    console.error("Error starting game:", error);
    // Fallback to local mode
    gameActive = true;
    updateDisplay();
  }
}

async function makeMove(position) {
  if (!gameActive || gameState[position] !== "") {
    return;
  }

  if (gameId) {
    // Online mode
    await makeMoveOnline(position);
  } else {
    // Local mode
    makeMoveLocal(position);
  }
}

async function makeMoveOnline(position) {
  try {
    const response = await fetch("/game/move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        game_id: gameId,
        player: playerName,
        position: position,
      }),
    });

    const result = await response.json();
    if (result.success) {
      gameState[position] = currentPlayer;
      updateCell(position, currentPlayer);

      if (result.winner) {
        endGame(result.winner);
      } else {
        switchPlayer();
      }
    } else {
      console.error("Move failed:", result.error);
    }
  } catch (error) {
    console.error("Error making move:", error);
  }
}

function makeMoveLocal(position) {
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
    statusDisplay.textContent = "Juego terminado";
  }
}

function endGame(winner) {
  gameActive = false;
  const statusDisplay = document.getElementById("game-status");

  if (statusDisplay) {
    if (winner === "draw") {
      statusDisplay.textContent = "¡Es un empate!";
    } else {
      statusDisplay.textContent = `¡Jugador ${winner} ha ganado!`;
    }
  }
}

function resetGame() {
  if (gameId) {
    startNewGame();
  } else {
    resetLocalState();
    gameActive = true;
    updateDisplay();
  }
}

function resetLocalState() {
  gameState = ["", "", "", "", "", "", "", "", ""];
  currentPlayer = "X";

  const cells = document.querySelectorAll(".cell");
  cells.forEach((cell) => {
    cell.textContent = "";
    cell.classList.remove("filled");
  });

  const statusDisplay = document.getElementById("game-status");
  if (statusDisplay) {
    statusDisplay.textContent = "";
  }
}
