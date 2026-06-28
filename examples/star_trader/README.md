# Star Trader

A tiny terminal trading game written in Python (stdlib only).

## How to Play

You are a space trader with **100 credits**, **50 fuel**, and **10 cargo
capacity**.  Four planets offer different buy/sell prices for three goods:
food, ore, and medicine.

**Goal:** reach **1000 credits** before you run out of fuel.

### Commands

| Command          | Description                              |
| ---------------- | ---------------------------------------- |
| `go <planet>`    | Travel to another planet (costs fuel)    |
| `buy <n> <good>` | Buy *n* units of a good                  |
| `sell <n> <good>`| Sell *n* units of a good                 |
| `fuel <n>`       | Buy *n* units of fuel (2 credits each)   |
| `status`         | Show credits, fuel, cargo, market prices |
| `planets`        | List known planets and distances         |
| `help`           | Show command help                        |
| `quit`           | Exit the game                            |

Run the game:

```
python3 star_trader.py
```

## Running Tests

```
python3 -m unittest test_star_trader.py
```

Or with verbose output:

```
python3 -m unittest test_star_trader.py -v
```
