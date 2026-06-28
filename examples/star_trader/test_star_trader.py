"""Tests for Star Trader game logic."""

import unittest

# Import the game module (star_trader.py must be in the same directory)
import star_trader as st


class TestBuying(unittest.TestCase):
    """Tests for the buy action."""

    def setUp(self):
        self.g = st.Game()

    def test_buy_food(self):
        ok, msg = self.g.buy("food", 2)
        self.assertTrue(ok)
        self.assertEqual(self.g.cargo["food"], 2)
        # Earth food buy price is 5, so 2 * 5 = 10 credits spent
        self.assertEqual(self.g.credits, st.START_CREDITS - 10)

    def test_buy_no_credits(self):
        self.g.credits = 0
        ok, msg = self.g.buy("food", 1)
        self.assertFalse(ok)
        self.assertIn("Not enough credits", msg)

    def test_buy_no_cargo_space(self):
        # Fill cargo completely
        self.g.cargo = {"food": 5, "ore": 3, "medicine": 2}
        ok, msg = self.g.buy("food", 1)
        self.assertFalse(ok)
        self.assertIn("Not enough cargo space", msg)

    def test_buy_invalid_good(self):
        ok, msg = self.g.buy("weapons", 1)
        self.assertFalse(ok)
        self.assertIn("No such good", msg)

    def test_buy_zero_amount(self):
        ok, msg = self.g.buy("food", 0)
        self.assertFalse(ok)
        self.assertIn("Amount must be at least 1", msg)


class TestSelling(unittest.TestCase):
    """Tests for the sell action."""

    def setUp(self):
        self.g = st.Game()
        # Give player some goods to sell
        self.g.cargo["food"] = 3

    def test_sell_food(self):
        ok, msg = self.g.sell("food", 2)
        self.assertTrue(ok)
        self.assertEqual(self.g.cargo["food"], 1)
        # Earth food sell price is 15, so 2 * 15 = 30 credits gained
        self.assertEqual(self.g.credits, st.START_CREDITS + 30)

    def test_sell_what_you_dont_have(self):
        ok, msg = self.g.sell("food", 10)
        self.assertFalse(ok)
        self.assertIn("Not enough food", msg)

    def test_sell_invalid_good(self):
        ok, msg = self.g.sell("weapons", 1)
        self.assertFalse(ok)
        self.assertIn("No such good", msg)

    def test_sell_zero_amount(self):
        ok, msg = self.g.sell("food", 0)
        self.assertFalse(ok)
        self.assertIn("Amount must be at least 1", msg)


class TestTravel(unittest.TestCase):
    """Tests for the travel action."""

    def setUp(self):
        self.g = st.Game()

    def test_travel_to_mars(self):
        ok, msg = self.g.travel("Mars")
        self.assertTrue(ok)
        self.assertEqual(self.g.location, "Mars")
        # Earth-Mars distance is 4
        self.assertEqual(self.g.fuel, st.START_FUEL - 4)

    def test_travel_no_fuel(self):
        self.g.fuel = 0
        ok, msg = self.g.travel("Mars")
        self.assertFalse(ok)
        self.assertIn("Not enough fuel", msg)

    def test_travel_to_current_planet(self):
        ok, msg = self.g.travel("Earth")
        self.assertFalse(ok)
        self.assertIn("already at", msg)

    def test_travel_invalid_planet(self):
        ok, msg = self.g.travel("Pluto")
        self.assertFalse(ok)
        self.assertIn("No such planet", msg)

    def test_travel_fuel_cost_varies(self):
        # Earth->Titan uses more fuel than Earth->Mars
        g2 = st.Game()
        g2.travel("Titan")
        self.assertEqual(g2.fuel, st.START_FUEL - 10)  # distance = 10

        g3 = st.Game()
        g3.travel("Mars")
        self.assertEqual(g3.fuel, st.START_FUEL - 4)  # distance = 4

    def test_travel_exhausts_fuel(self):
        self.g.fuel = 4  # exactly Earth->Mars distance
        ok, msg = self.g.travel("Mars")
        self.assertTrue(ok)
        self.assertEqual(self.g.fuel, 0)
        self.assertTrue(self.g.lost)


class TestRefueling(unittest.TestCase):
    """Tests for the refuel action."""

    def setUp(self):
        self.g = st.Game()

    def test_refuel(self):
        self.g.fuel = 10
        ok, msg = self.g.refuel(5)
        self.assertTrue(ok)
        self.assertEqual(self.g.fuel, 15)
        # 5 * FUEL_PRICE(2) = 10 credits
        self.assertEqual(self.g.credits, st.START_CREDITS - 10)

    def test_refuel_no_credits(self):
        self.g.credits = 0
        ok, msg = self.g.refuel(5)
        self.assertFalse(ok)
        self.assertIn("Not enough credits", msg)

    def test_refuel_zero_amount(self):
        ok, msg = self.g.refuel(0)
        self.assertFalse(ok)
        self.assertIn("Amount must be at least 1", msg)


class TestCargoLimits(unittest.TestCase):
    """Tests for cargo capacity constraints."""

    def setUp(self):
        self.g = st.Game()

    def test_cargo_full(self):
        self.g.cargo = {"food": 4, "ore": 3, "medicine": 3}  # total = 10
        self.assertEqual(self.g.cargo_used, 10)
        self.assertEqual(self.g.cargo_free, 0)
        ok, msg = self.g.buy("food", 1)
        self.assertFalse(ok)

    def test_cargo_empty(self):
        self.assertEqual(self.g.cargo_used, 0)
        self.assertEqual(self.g.cargo_free, st.MAX_CARGO)


class TestWinLoss(unittest.TestCase):
    """Tests for win and loss conditions."""

    def test_not_won_at_start(self):
        g = st.Game()
        self.assertFalse(g.won)
        self.assertFalse(g.lost)
        self.assertFalse(g.over)

    def test_win_at_1000_credits(self):
        g = st.Game()
        g.credits = 1000
        self.assertTrue(g.won)
        self.assertTrue(g.over)

    def test_lose_at_zero_fuel(self):
        g = st.Game()
        g.fuel = 0
        self.assertTrue(g.lost)
        self.assertTrue(g.over)

    def test_lose_at_negative_fuel(self):
        g = st.Game()
        g.fuel = -5
        self.assertTrue(g.lost)
        self.assertTrue(g.over)


if __name__ == "__main__":
    unittest.main()
