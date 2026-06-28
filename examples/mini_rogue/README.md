# Mini Rogue

A tiny 10×10 dungeon terminal game written in pure Python (stdlib only).

## How to Play

```
python3 mini_rogue.py
```

You are `@` — the adventurer.  
Collect all 3 treasures (`$`) then reach the exit (`E`) at the bottom-right corner.  
Avoid the monster (`M`) that roams randomly each turn.

### Controls

| Key | Action |
|-----|--------|
| `w` | Move up |
| `a` | Move left |
| `s` | Move down |
| `d` | Move right |
| `q` | Quit |

### Symbols

| Symbol | Meaning |
|--------|---------|
| `@` | Player |
| `M` | Monster |
| `#` | Wall |
| `$` | Treasure (uncollected) |
| `E` | Exit |
| `.` | Empty floor |

### Win / Lose

- **Win**: Reach the exit (`E`) after collecting all 3 treasures.
- **Lose**: The monster steps onto your cell.

## Running Tests

```bash
# With unittest (stdlib, no deps needed):
python3 -m unittest test_mini_rogue -v

# Or with pytest if you have it:
python3 -m pytest test_mini_rogue.py -v
```

Tests cover movement bounds, wall blocking, treasure collection,
win condition, lose condition, and monster movement.
