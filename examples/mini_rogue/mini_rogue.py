#!/usr/bin/env python3
"""Mini Rogue — a tiny 10x10 dungeon terminal game.

Collect all 3 treasures then reach the exit at (9,9).
Avoid the randomly-roaming monster.

Controls: w=up  a=left  s=down  d=right  q=quit
"""

import random
import sys
import os

# --- Constants ---
SIZE = 10
PLAYER_START = (0, 0)
EXIT_POS = (9, 9)
MONSTER_START = (5, 5)
TREASURE_POSITIONS = [(2, 3), (4, 6), (7, 2)]

WALLS = {
    (1, 1), (1, 2), (1, 3),
    (3, 5), (3, 6), (3, 7),
    (5, 1), (6, 1), (7, 1),
    (7, 3), (7, 4), (7, 5),
    (2, 8), (3, 8), (4, 8),
}

DIRS = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}


class Game:
    """Holds all mutable game state for testability."""

    def __init__(self):
        self.player = list(PLAYER_START)
        self.monster = list(MONSTER_START)
        self.treasures = set(TREASURE_POSITIONS)
        self.collected = 0
        self.game_over = False
        self.won = False

    def in_bounds(self, r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def is_wall(self, r, c):
        return (r, c) in WALLS

    def can_move_to(self, r, c):
        return self.in_bounds(r, c) and not self.is_wall(r, c) and (r, c) != tuple(self.monster)

    def move_player(self, direction):
        """Attempt to move player. Returns True if the move succeeded."""
        if self.game_over:
            return False
        if direction not in DIRS:
            return False
        dr, dc = DIRS[direction]
        nr, nc = self.player[0] + dr, self.player[1] + dc
        if not self.can_move_to(nr, nc):
            return False
        self.player[0], self.player[1] = nr, nc
        self._collect()
        self.check_win()
        return True

    def _collect(self):
        pos = tuple(self.player)
        if pos in self.treasures:
            self.treasures.discard(pos)
            self.collected += 1

    def check_win(self):
        """Public for testability. Checks win condition."""
        if tuple(self.player) == EXIT_POS and self.collected == len(TREASURE_POSITIONS):
            self.game_over = True
            self.won = True

    def move_monster(self):
        """Move monster one step randomly, then check collision."""
        if self.game_over:
            return
        candidates = []
        mr, mc = self.monster
        for dr, dc in DIRS.values():
            nr, nc = mr + dr, mc + dc
            if self.in_bounds(nr, nc) and not self.is_wall(nr, nc):
                candidates.append((nr, nc))
        if candidates:
            self.monster[0], self.monster[1] = random.choice(candidates)
        self.check_collision()

    def check_collision(self):
        """Public for testability. Sets game_over if monster caught player."""
        if tuple(self.monster) == tuple(self.player):
            self.game_over = True
            self.won = False


def clear_screen():
    print('\033[2J\033[H', end='')


def render(game):
    """Return a list of strings representing the grid."""
    lines = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            pos = (r, c)
            if pos == tuple(game.player):
                row.append('@')
            elif pos == tuple(game.monster):
                row.append('M')
            elif pos in WALLS:
                row.append('#')
            elif pos in game.treasures:
                row.append('$')
            elif pos == EXIT_POS:
                row.append('E')
            else:
                row.append('.')
        lines.append(' '.join(row))
    lines.append('')
    lines.append('Treasures: {}/{}  [w/a/s/d move, q quit]'.format(
        game.collected, len(TREASURE_POSITIONS)))
    if game.game_over:
        if game.won:
            lines.append('*** YOU ESCAPED THE DUNGEON! ***')
        else:
            lines.append('*** THE MONSTER GOT YOU! ***')
    return lines


def _getch():
    """Read a single character from stdin without waiting for Enter."""
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode('utf-8', errors='replace')
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch


def main():
    game = Game()
    while not game.game_over:
        clear_screen()
        for line in render(game):
            print(line)
        key = _getch().lower()
        if key == 'q':
            print('Quit.')
            return
        if key in DIRS:
            game.move_player(key)
            game.move_monster()
    clear_screen()
    for line in render(game):
        print(line)


if __name__ == '__main__':
    main()
