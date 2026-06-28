"""Tests for Mini Rogue game logic."""

import unittest
import random

from mini_rogue import Game, DIRS, WALLS, SIZE, EXIT_POS, TREASURE_POSITIONS, render


class TestMovement(unittest.TestCase):
    """Tests for player movement bounds and wall blocking."""

    def test_move_within_bounds(self):
        game = Game()
        # Player starts at (0,0). Move right should succeed.
        self.assertTrue(game.move_player('d'))
        self.assertEqual(game.player, [0, 1])

    def test_blocked_by_left_wall(self):
        game = Game()
        # Player at (0,0) — moving left goes out of bounds.
        self.assertFalse(game.move_player('a'))
        self.assertEqual(game.player, [0, 0])

    def test_blocked_by_top_wall(self):
        game = Game()
        self.assertFalse(game.move_player('w'))
        self.assertEqual(game.player, [0, 0])

    def test_blocked_by_bottom_wall(self):
        game = Game()
        game.player = [SIZE - 1, 0]
        self.assertFalse(game.move_player('s'))
        self.assertEqual(game.player, [SIZE - 1, 0])

    def test_blocked_by_right_wall(self):
        game = Game()
        game.player = [0, SIZE - 1]
        self.assertFalse(game.move_player('d'))
        self.assertEqual(game.player, [0, SIZE - 1])

    def test_blocked_by_interior_wall(self):
        game = Game()
        # (1,1) is a wall. Move player adjacent and try to walk into it.
        game.player = [1, 0]
        self.assertFalse(game.move_player('d'))
        self.assertEqual(game.player, [1, 0])

    def test_cannot_move_when_game_over(self):
        game = Game()
        game.game_over = True
        self.assertFalse(game.move_player('d'))

    def test_player_cannot_walk_through_monster(self):
        game = Game()
        # Place player adjacent to monster, try to walk into it.
        game.player = [5, 4]
        game.monster = [5, 5]
        self.assertFalse(game.move_player('d'))
        self.assertEqual(game.player, [5, 4])


class TestTreasure(unittest.TestCase):
    """Tests for treasure collection."""

    def test_collect_treasure(self):
        game = Game()
        # Treasure at (2,3). Walk onto it.
        game.player = [2, 2]
        self.assertTrue(game.move_player('d'))
        self.assertEqual(game.collected, 1)
        self.assertNotIn((2, 3), game.treasures)

    def test_no_double_collect(self):
        game = Game()
        game.player = [2, 2]
        game.move_player('d')          # collect
        self.assertEqual(game.collected, 1)
        game.move_player('a')          # step off
        game.move_player('d')          # step back on
        self.assertEqual(game.collected, 1)  # still 1


class TestWinCondition(unittest.TestCase):
    """Tests for winning the game."""

    def test_win_at_exit_with_all_treasures(self):
        game = Game()
        game.collected = len(TREASURE_POSITIONS)
        game.player = [EXIT_POS[0], EXIT_POS[1]]
        game.check_win()
        self.assertTrue(game.game_over)
        self.assertTrue(game.won)

    def test_no_win_at_exit_without_treasures(self):
        game = Game()
        game.player = [EXIT_POS[0], EXIT_POS[1]]
        game.check_win()
        self.assertFalse(game.game_over)

    def test_no_win_with_treasures_but_not_at_exit(self):
        game = Game()
        game.collected = len(TREASURE_POSITIONS)
        game.check_win()
        self.assertFalse(game.game_over)


class TestLoseCondition(unittest.TestCase):
    """Tests for losing to the monster."""

    def test_collision_loses(self):
        game = Game()
        game.player = [3, 3]
        game.monster = [3, 3]
        game.check_collision()
        self.assertTrue(game.game_over)
        self.assertFalse(game.won)

    def test_no_collision_when_apart(self):
        game = Game()
        game.player = [0, 0]
        game.monster = [9, 9]
        game.check_collision()
        self.assertFalse(game.game_over)


class TestMonsterMovement(unittest.TestCase):
    """Tests for monster behaviour."""

    def test_monster_moves(self):
        game = Game()
        game.player = [9, 9]          # far away from monster
        game.monster = [0, 0]
        game.move_monster()
        self.assertNotEqual(game.monster, [0, 0])
        mr, mc = game.monster
        self.assertTrue(game.in_bounds(mr, mc))
        self.assertFalse(game.is_wall(mr, mc))

    def test_monster_avoids_walls(self):
        game = Game()
        game.player = [9, 9]
        # Surround monster with walls on 3 sides, only one escape.
        # (1,1),(1,2),(1,3) are walls. Place monster at (0,2)
        # valid moves: (0,1), (0,3), (1,2-wall). Only (0,1) and (0,3).
        game.monster = [0, 2]
        for _ in range(10):
            game.move_monster()
            self.assertNotIn(tuple(game.monster), WALLS)

    def test_monster_does_not_move_when_game_over(self):
        game = Game()
        game.game_over = True
        game.monster = [0, 0]
        game.move_monster()
        self.assertEqual(game.monster, [0, 0])


class TestRender(unittest.TestCase):
    """Tests for the render function."""

    def test_player_rendered(self):
        game = Game()
        lines = render(game)
        # Player starts at (0,0). First row, first column should be '@'.
        row0 = lines[0].split()
        self.assertEqual(row0[0], '@')

    def test_monster_rendered(self):
        game = Game()
        lines = render(game)
        # Monster starts at (5,5). Row 5, column 5 should be 'M'.
        row5 = lines[5].split()
        self.assertEqual(row5[5], 'M')

    def test_wall_rendered(self):
        game = Game()
        lines = render(game)
        # (1,1) is a wall.
        row1 = lines[1].split()
        self.assertEqual(row1[1], '#')

    def test_win_status_line(self):
        game = Game()
        game.collected = len(TREASURE_POSITIONS)
        game.player = [EXIT_POS[0], EXIT_POS[1]]
        game.check_win()
        lines = render(game)
        self.assertIn('*** YOU ESCAPED THE DUNGEON! ***', lines)


if __name__ == '__main__':
    unittest.main()
