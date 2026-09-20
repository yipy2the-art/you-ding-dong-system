"""NES-style Tetris clone using pygame.

Install and run on Windows:
    py -m pip install pygame mote
    py tetris.py

Controls: Left/Right move, Down soft drop, Up rotate, Space hard drop,
P pause, Esc quit. Wii Remote support works on Windows via the mote library.
"""
import random
import sys

try:
    from mote import Mote
except ImportError:
    Mote = None

import pygame

COLS, ROWS = 10, 20
CELL = 28
BOARD_X, BOARD_Y = 24, 20
PANEL_X = BOARD_X + COLS * CELL + 32
WIDTH, HEIGHT = PANEL_X + 185, BOARD_Y + ROWS * CELL + 20
BLACK = (8, 8, 16)
GRID = (40, 40, 55)
WHITE = (240, 240, 240)
DIM = (155, 155, 170)
COLORS = {
    "I": (39, 190, 205), "J": (45, 75, 190), "L": (210, 125, 35),
    "O": (220, 190, 35), "S": (45, 160, 75), "T": (145, 55, 170),
    "Z": (190, 45, 50),
}
SHAPES = {
    "I": ("....", "IIII", "....", "...."),
    "J": ("J..", "JJJ", "..."), "L": ("..L", "LLL", "..."),
    "O": ("OO", "OO"), "S": (".SS", "SS.", "..."),
    "T": (".T.", "TTT", "..."), "Z": ("ZZ.", ".ZZ", "..."),
}
KINDS = tuple(SHAPES)


class WiimoteController:
    def __init__(self):
        self.device = None
        self.connected = False
        self.last_pressed = set()

    def connect(self):
        if Mote is None:
            return False
        try:
            self.device = Mote()
            print("Press buttons 1 and 2 on the Wii Remote...")
            if self.device.connect():
                self.connected = True
                print("Wii Remote connected.")
                return True
        except Exception as exc:  # pragma: no cover - depends on hardware
            print(f"Wiimote connection failed: {exc}")
        self.connected = False
        self.device = None
        return False

    def get_events(self):
        if not self.connected or self.device is None:
            return []
        try:
            buttons = self.device.get_buttons()
        except Exception:  # pragma: no cover - depends on hardware
            return []
        current = {name for name, pressed in buttons.items() if pressed}
        events = sorted(current - self.last_pressed)
        self.last_pressed = current
        return events


def rotate(shape):
    return tuple("".join(row[x] for row in shape[::-1])
                 for x in range(len(shape[0])))


class Piece:
    def __init__(self, kind, x=3, y=0):
        self.kind, self.x, self.y, self.rotation = kind, x, y, 0

    def cells(self):
        shape = SHAPES[self.kind]
        for _ in range(self.rotation):
            shape = rotate(shape)
        return [(self.x + x, self.y + y)
                for y, row in enumerate(shape)
                for x, value in enumerate(row) if value != "."]


def new_piece():
    return Piece(random.choice(KINDS))


def blocked(board, piece):
    for x, y in piece.cells():
        if x < 0 or x >= COLS or y >= ROWS:
            return True
        if y >= 0 and board[y][x] is not None:
            return True
    return False


def move(board, piece, dx, dy):
    piece.x += dx
    piece.y += dy
    if blocked(board, piece):
        piece.x -= dx
        piece.y -= dy
        return False
    return True


def rotate_piece(board, piece):
    old = piece.rotation
    piece.rotation = (piece.rotation + 1) % 4
    for kick in (0, -1, 1, -2, 2):
        piece.x += kick
        if not blocked(board, piece):
            return
        piece.x -= kick
    piece.rotation = old


def lock(board, piece):
    for x, y in piece.cells():
        if 0 <= y < ROWS:
            board[y][x] = piece.kind


def clear_lines(board):
    kept = [row for row in board if any(cell is None for cell in row)]
    count = ROWS - len(kept)
    return [[None] * COLS for _ in range(count)] + kept, count


def block(screen, x, y, color, size=CELL):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect)
    dark = tuple(max(0, c - 55) for c in color)
    light = tuple(min(255, c + 35) for c in color)
    pygame.draw.rect(screen, dark, rect, 2)
    pygame.draw.line(screen, light, rect.topleft, (rect.right - 2, rect.top + 1), 2)


def preview(screen, piece, x, y):
    for px, py in Piece(piece.kind, 0, 0).cells():
        block(screen, x + px * 20, y + py * 20, COLORS[piece.kind], 20)


def text(screen, font, value, x, y, color=WHITE):
    screen.blit(font.render(value, True, color), (x, y))


def main():
    pygame.init()
    pygame.display.set_caption("NES-style Tetris")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    title_font = pygame.font.Font(None, 38)
    board = [[None] * COLS for _ in range(ROWS)]
    current, upcoming = new_piece(), new_piece()
    score = lines = level = 0
    fall_time = 0
    paused = game_over = False
    running = True
    wiimote = WiimoteController()
    wiimote.connected = wiimote.connect()

    def spawn_next():
        nonlocal current, upcoming, game_over
        current, upcoming = upcoming, new_piece()
        if blocked(board, current):
            game_over = True

    while running:
        dt = clock.tick(60)
        fall_time += dt

        wiimote_events = wiimote.get_events() if wiimote.connected else []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and not game_over:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    return main()
                elif not paused and not game_over:
                    if event.key == pygame.K_LEFT:
                        move(board, current, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        move(board, current, 1, 0)
                    elif event.key == pygame.K_DOWN:
                        if move(board, current, 0, 1):
                            score += 1
                    elif event.key == pygame.K_UP:
                        rotate_piece(board, current)
                    elif event.key == pygame.K_SPACE:
                        distance = 0
                        while move(board, current, 0, 1):
                            distance += 1
                        score += distance * 2
                        lock(board, current)
                        board, count = clear_lines(board)
                        if count:
                            score += (0, 40, 100, 300, 1200)[count] * (level + 1)
                            lines += count
                            level = lines // 10
                        spawn_next()

        if wiimote.connected and not paused and not game_over:
            for key in wiimote_events:
                if key == "LEFT":
                    move(board, current, -1, 0)
                elif key == "RIGHT":
                    move(board, current, 1, 0)
                elif key == "DOWN":
                    if move(board, current, 0, 1):
                        score += 1
                elif key == "UP":
                    rotate_piece(board, current)
                elif key == "A":
                    distance = 0
                    while move(board, current, 0, 1):
                        distance += 1
                    score += distance * 2
                    lock(board, current)
                    board, count = clear_lines(board)
                    if count:
                        score += (0, 40, 100, 300, 1200)[count] * (level + 1)
                        lines += count
                        level = lines // 10
                    spawn_next()
                elif key == "B":
                    rotate_piece(board, current)
                elif key == "PLUS":
                    paused = not paused
                elif key == "HOME":
                    running = False

        if not paused and not game_over:
            interval = max(70, 800 - level * 60)
            if fall_time >= interval:
                fall_time = 0
                if not move(board, current, 0, 1):
                    lock(board, current)
                    board, count = clear_lines(board)
                    if count:
                        score += (0, 40, 100, 300, 1200)[count] * (level + 1)
                        lines += count
                        level = lines // 10
                    spawn_next()

        screen.fill(BLACK)
        pygame.draw.rect(screen, (18, 18, 28),
                         (BOARD_X, BOARD_Y, COLS * CELL, ROWS * CELL))
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(BOARD_X + x * CELL, BOARD_Y + y * CELL,
                                   CELL, CELL)
                pygame.draw.rect(screen, GRID, rect, 1)
                if board[y][x]:
                    block(screen, rect.x + 1, rect.y + 1,
                          COLORS[board[y][x]], CELL - 2)
        if not game_over:
            for x, y in current.cells():
                if y >= 0:
                    block(screen, BOARD_X + x * CELL + 1,
                          BOARD_Y + y * CELL + 1, COLORS[current.kind], CELL - 2)

        text(screen, title_font, "TETRIS", PANEL_X, 25)
        text(screen, font, f"SCORE {score}", PANEL_X, 85)
        text(screen, font, f"LINES {lines}", PANEL_X, 115)
        text(screen, font, f"LEVEL {level}", PANEL_X, 145)
        text(screen, font, "NEXT", PANEL_X, 205, DIM)
        preview(screen, upcoming, PANEL_X, 235)
        text(screen, font, "ARROWS  MOVE", PANEL_X, 350, DIM)
        text(screen, font, "UP      ROTATE", PANEL_X, 378, DIM)
        text(screen, font, "SPACE   DROP", PANEL_X, 406, DIM)
        text(screen, font, "P       PAUSE", PANEL_X, 434, DIM)
        if wiimote.connected:
            text(screen, font, "WII REMOTE OK", PANEL_X, 465, (100, 220, 120))
        if paused:
            text(screen, title_font, "PAUSED", BOARD_X + 70, BOARD_Y + 260)
        elif game_over:
            text(screen, title_font, "GAME OVER", BOARD_X + 35, BOARD_Y + 240)
            text(screen, font, "R TO RESTART", BOARD_X + 75, BOARD_Y + 285, DIM)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
