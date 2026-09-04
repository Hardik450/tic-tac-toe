const EMPTY = null;

const pickerEl = document.getElementById("picker");
const gameEl = document.getElementById("game");
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const againBtn = document.getElementById("againBtn");
const pickXBtn = document.getElementById("pickX");
const pickOBtn = document.getElementById("pickO");

let board = emptyBoard();
let user = null;
let gameOver = false;
let winner = null;
let currentPlayer = "X";
let busy = false; // true while waiting on a server round trip

function emptyBoard() {
  return [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
  ];
}

function buildBoard() {
  boardEl.innerHTML = "";
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = i;
      cell.dataset.col = j;
      cell.addEventListener("click", () => onCellClick(i, j));
      boardEl.appendChild(cell);
    }
  }
}

function markCell(i, j, mark) {
  const cell = boardEl.querySelector(`[data-row="${i}"][data-col="${j}"]`);
  cell.classList.add("filled", mark === "X" ? "mark-x" : "mark-o");
  cell.innerHTML =
    mark === "X"
      ? '<svg viewBox="0 0 100 100"><path d="M20 20 L80 80" /><path d="M80 20 L20 80" /></svg>'
      : '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="34" /></svg>';
}

function renderBoard() {
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (board[i][j]) markCell(i, j, board[i][j]);
    }
  }
}

function renderStatus() {
  if (gameOver) {
    statusEl.textContent = winner ? `Game over — ${winner} wins!` : "Game over — a tie.";
    boardEl.classList.add("no-click");
    againBtn.classList.remove("hidden");
  } else if (busy) {
    statusEl.textContent = "Computer is thinking…";
  } else if (currentPlayer === user) {
    statusEl.textContent = `Your move, ${user}`;
  } else {
    statusEl.textContent = "Computer is thinking…";
  }
}

function applyStatus(data) {
  board = data.board;
  gameOver = data.game_over;
  winner = data.winner;
  currentPlayer = data.current_player;
  renderBoard();
  renderStatus();
}

async function onCellClick(i, j) {
  if (busy || gameOver || board[i][j] !== EMPTY || currentPlayer !== user) return;

  busy = true;
  renderStatus();
  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board, action: [i, j] }),
    });
    if (!res.ok) throw new Error((await res.json()).error || "Move failed");
    const data = await res.json();
    applyStatus(data);

    if (!data.game_over && data.current_player !== user) {
      await requestAiMove();
    }
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Something went wrong — try again.";
  } finally {
    busy = false;
    if (!gameOver) renderStatus();
  }
}

async function requestAiMove() {
  busy = true;
  renderStatus();
  // Small pause so the AI's move doesn't feel instantaneous.
  await new Promise((r) => setTimeout(r, 450));
  try {
    const res = await fetch("/api/ai_move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board }),
    });
    if (!res.ok) throw new Error((await res.json()).error || "AI move failed");
    const data = await res.json();
    applyStatus(data);
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Something went wrong — try again.";
  } finally {
    busy = false;
    if (!gameOver) renderStatus();
  }
}

function startGame(chosenUser) {
  user = chosenUser;
  board = emptyBoard();
  gameOver = false;
  winner = null;
  currentPlayer = "X";
  busy = false;

  pickerEl.classList.add("hidden");
  gameEl.classList.remove("hidden");
  againBtn.classList.add("hidden");
  boardEl.classList.remove("no-click");

  buildBoard();
  renderStatus();

  if (currentPlayer !== user) {
    requestAiMove();
  }
}

pickXBtn.addEventListener("click", () => startGame("X"));
pickOBtn.addEventListener("click", () => startGame("O"));
againBtn.addEventListener("click", () => {
  gameEl.classList.add("hidden");
  pickerEl.classList.remove("hidden");
  user = null;
});
