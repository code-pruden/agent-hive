#!/usr/bin/env python3
"""Star Trader - a tiny terminal trading game.

You are a space trader flying between four planets. Buy low, sell high,
and reach 1000 credits before you run out of fuel.
"""

# -- planetary system --------------------------------------------------------

PLANETS = {
    "Earth": {
        "desc": "a temperate, well-supplied homeworld",
        "food": (5, 15),       # (buy_price, sell_price)
        "ore": (20, 35),
        "medicine": (30, 50),
    },
    "Mars": {
        "desc": "a dusty mining colony",
        "food": (15, 25),
        "ore": (10, 18),
        "medicine": (25, 45),
    },
    "Europa": {
        "desc": "an icy research outpost",
        "food": (20, 30),
        "ore": (15, 28),
        "medicine": (10, 20),
    },
    "Titan": {
        "desc": "a remote methane-processing hub",
        "food": (25, 40),
        "ore": (8, 14),
        "medicine": (20, 35),
    },
}

# distance in AU between each pair of planets
DISTANCES = {
    ("Earth", "Mars"): 4,
    ("Earth", "Europa"): 6,
    ("Earth", "Titan"): 10,
    ("Mars", "Europa"): 3,
    ("Mars", "Titan"): 7,
    ("Europa", "Titan"): 5,
}

GOODS = ("food", "ore", "medicine")

FUEL_PRICE = 2  # credits per unit of fuel
WIN_CREDITS = 1000
START_CREDITS = 100
START_FUEL = 50
MAX_CARGO = 10


def _distance(a, b):
    """Return the distance between two planets, canonicalising order."""
    key = (a, b) if (a, b) in DISTANCES else (b, a)
    if key not in DISTANCES:
        raise ValueError(f"No distance defined between {a} and {b}")
    return DISTANCES[key]


# -- game state --------------------------------------------------------------

class Game:
    """Holds all mutable state for a Star Trader session."""

    def __init__(self):
        self.credits = START_CREDITS
        self.fuel = START_FUEL
        self.cargo = {g: 0 for g in GOODS}
        self.location = "Earth"
        self.turn = 0

    # -- properties --

    @property
    def cargo_used(self):
        return sum(self.cargo.values())

    @property
    def cargo_free(self):
        return MAX_CARGO - self.cargo_used

    @property
    def won(self):
        return self.credits >= WIN_CREDITS

    @property
    def lost(self):
        return self.fuel <= 0

    @property
    def over(self):
        return self.won or self.lost

    # -- helpers --

    def buy_price(self, good):
        """Price the *player* pays to buy one unit of *good* here."""
        return PLANETS[self.location][good][0]

    def sell_price(self, good):
        """Price the *player* receives for one unit of *good* here."""
        return PLANETS[self.location][good][1]

    # -- actions --

    def travel(self, destination):
        """Fly to *destination*.  Returns an (ok, message) tuple."""
        if destination not in PLANETS:
            return False, f"No such planet: {destination}"
        if destination == self.location:
            return False, f"You are already at {self.location}."

        cost = _distance(self.location, destination)
        if self.fuel < cost:
            return False, (
                f"Not enough fuel.  Need {cost}, have {self.fuel}."
            )

        self.fuel -= cost
        self.location = destination
        self.turn += 1
        return True, (
            f"You fly to {destination} "
            f"({PLANETS[destination]['desc']}).  "
            f"Fuel used: {cost}."
        )

    def buy(self, good, amount):
        """Buy *amount* of *good* at the current planet."""
        if good not in GOODS:
            return False, f"No such good: {good}"
        if amount < 1:
            return False, "Amount must be at least 1."
        if self.cargo_free < amount:
            return False, (
                f"Not enough cargo space.  "
                f"Free: {self.cargo_free}, wanted: {amount}."
            )

        price = self.buy_price(good) * amount
        if self.credits < price:
            return False, (
                f"Not enough credits.  "
                f"Need {price}, have {self.credits}."
            )

        self.credits -= price
        self.cargo[good] += amount
        self.turn += 1
        return True, f"Bought {amount} {good} for {price} credits."

    def sell(self, good, amount):
        """Sell *amount* of *good* at the current planet."""
        if good not in GOODS:
            return False, f"No such good: {good}"
        if amount < 1:
            return False, "Amount must be at least 1."
        if self.cargo[good] < amount:
            return False, (
                f"Not enough {good} in cargo.  "
                f"Have {self.cargo[good]}, wanted {amount}."
            )

        income = self.sell_price(good) * amount
        self.credits += income
        self.cargo[good] -= amount
        self.turn += 1
        return True, f"Sold {amount} {good} for {income} credits."

    def refuel(self, amount):
        """Buy *amount* fuel units at the current planet."""
        if amount < 1:
            return False, "Amount must be at least 1."

        cost = amount * FUEL_PRICE
        if self.credits < cost:
            return False, (
                f"Not enough credits.  "
                f"Need {cost}, have {self.credits}."
            )

        self.credits -= cost
        self.fuel += amount
        self.turn += 1
        return True, f"Bought {amount} fuel for {cost} credits."

    # -- display --

    def status(self):
        """Return a multi-line status string."""
        lines = [
            "-" * 40,
            f"Location: {self.location}  ({PLANETS[self.location]['desc']})",
            f"Credits:  {self.credits}",
            f"Fuel:     {self.fuel}",
            f"Turn:     {self.turn}",
            "",
            "Market prices (buy / sell):",
        ]
        for g in GOODS:
            bp = self.buy_price(g)
            sp = self.sell_price(g)
            lines.append(f"  {g:<9} buy {bp:>3}  sell {sp:>3}")
        lines.append("")
        lines.append(
            f"Cargo ({self.cargo_used}/{MAX_CARGO}):  "
            + " | ".join(f"{g}={self.cargo[g]}" for g in GOODS)
        )
        lines.append("-" * 40)
        return "\n".join(lines)

    def planet_list(self):
        """Return a listing of known planets with distances."""
        lines = ["Known planets:"]
        for name, info in PLANETS.items():
            if name == self.location:
                marker = "  <- you are here"
            else:
                d = _distance(self.location, name)
                marker = f"  ({d} AU away)"
            lines.append(f"  {name:<8} {info['desc']}{marker}")
        return "\n".join(lines)


# -- REPL --------------------------------------------------------------------

HELP_TEXT = """Commands:
  go <planet>     Travel to another planet
  buy <n> <good>  Buy *n* units of a good
  sell <n> <good> Sell *n* units of a good
  fuel <n>        Buy *n* units of fuel (2 cr each)
  status          Show your current status
  planets         List known planets and distances
  help            Show this help
  quit            Exit the game"""


def _parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def repl(game=None):
    """Run the interactive main loop.  Returns final Game state."""
    if game is None:
        game = Game()

    print("+==============================+")
    print("|       STAR  TRADER           |")
    print("+==============================+")
    print()
    print("You are a trader plying the space lanes.")
    print(f"Start with {START_CREDITS} credits and {START_FUEL} fuel.")
    print(f"Reach {WIN_CREDITS} credits to win!")
    print()
    print(game.status())

    while not game.over:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        if cmd == "quit":
            print("Goodbye.")
            break

        if cmd == "help":
            print(HELP_TEXT)
            continue

        if cmd == "status":
            print(game.status())
            continue

        if cmd == "planets":
            print(game.planet_list())
            continue

        if cmd == "go" and len(parts) >= 2:
            dest = " ".join(parts[1:]).title()
            ok, msg = game.travel(dest)
            print(msg)
            if ok:
                print(game.status())
            continue

        if cmd == "buy" and len(parts) >= 3:
            n = _parse_int(parts[1])
            good = parts[2].lower()
            if n is None:
                print("Invalid amount.")
                continue
            ok, msg = game.buy(good, n)
            print(msg)
            continue

        if cmd == "sell" and len(parts) >= 3:
            n = _parse_int(parts[1])
            good = parts[2].lower()
            if n is None:
                print("Invalid amount.")
                continue
            ok, msg = game.sell(good, n)
            print(msg)
            continue

        if cmd == "fuel" and len(parts) >= 2:
            n = _parse_int(parts[1])
            if n is None:
                print("Invalid amount.")
                continue
            ok, msg = game.refuel(n)
            print(msg)
            continue

        print(f"Unknown command: {raw!r}.  Type 'help' for commands.")

    if game.over:
        if game.won:
            print(f"\n*** Congratulations!  You reached {WIN_CREDITS} credits in "
                  f"{game.turn} turns! ***")
        elif game.lost:
            print("\n*** You ran out of fuel.  Game over. ***")

    return game


# -- main --------------------------------------------------------------------

if __name__ == "__main__":
    repl()
