# Chapter 3 Practice Quiz 3 — Recycling audit

This quiz is **practice for the timed Chapter 3 assessment**. It isn't graded. Try to finish it in about **30 minutes**.

Write your code in `src/recycling_audit.py`. The data is already there.

## Running the tests

```
python -m unittest discover test -v
```

The test classes are named after the grade bands: `TestTierB`, `TestTierBPlus`, `TestTierAMinus`, `TestTierA` and `TestTierAPlus`. Run the suite and the classes that pass show which band you have reached. To run a single tier, for example:

```
python -m unittest discover test -k TestTierAMinus -v
```

You can also run the file itself to see everything it prints:

```
python src/recycling_audit.py
```

## Bands

| Completed                     | Band |
|-------------------------------|------|
| 1 of the two Tier B functions | C+   |
| both Tier B functions         | B    |
| + `net_weights`               | B+   |
| + `from_building`             | A-   |
| + `material_total`            | A    |
| + `building_report`           | A+   |

## Data

```python
bins = [
    {"location": "Cafeteria West", "material": "PAPER",   "weight": "1,250 g", "flagged": "no"},
    {"location": "Cafeteria East", "material": "plastic", "weight": "480 g",   "flagged": "yes"},
    {"location": "Library",        "material": "Paper",   "weight": "2,015 g", "flagged": "no"},
    {"location": "Gym Lobby",      "material": "GLASS",   "weight": "935 g",   "flagged": "yes"},
    {"location": "Library Annex",  "material": "paper",   "weight": "60 g",    "flagged": "no"},
]
```

A `flagged` value of `"yes"` means the bin was contaminated and 50 g of its contents had to be discarded.

- A flagged bin loses 50 g. When a decision sits inside arithmetic, use parentheses to make sure Python is choosing between the two things you meant.
- "In this building" means the location *contains* the word, not that it equals it.
- Weights arrive as text, and not all of them are punctuated the same way.

---

## Tier B: map, a lambda, chained string methods

**Constraint:** You must use `map()` and a lambda. The body is a single `return` statement. No loops and no list comprehensions.

### 1. `bin_weights(bins: list) -> list`

Each bin's weight as a plain integer number of grams.

```python
bin_weights(bins)
[1250, 480, 2015, 935, 60]
```

### 2. `bin_rows(bins: list) -> list`

A new dict per bin with `"location"` (unchanged) and `"grams"` (the weight as an integer, as in function 1).

```python
bin_rows(bins)
[{'location': 'Cafeteria West', 'grams': 1250},
 {'location': 'Cafeteria East', 'grams': 480},
 {'location': 'Library', 'grams': 2015},
 {'location': 'Gym Lobby', 'grams': 935},
 {'location': 'Library Annex', 'grams': 60}]
```

---

## Tier B+: a conditional expression inside arithmetic

**Constraint:** Same as Tier B.

### 3. `net_weights(bins: list) -> list`

Each bin's weight in grams, **minus 50 if the bin was flagged**. A plain list of integers.

```python
net_weights(bins)
[1250, 430, 2015, 885, 60]
```

---

## Tier A-: filter and map combined

**Constraint from here on:** No loops. Bodies may be more than one line, and you choose the structure. You must use both `map()` and `filter()`.

### 4. `from_building(bins: list, word: str) -> list`

Every bin whose location **contains** the given word, as a dict with `"location"` and `"grams"`.

```python
from_building(bins, "Library")    # [{'location': 'Library', 'grams': 2015},
                                  #  {'location': 'Library Annex', 'grams': 60}]
from_building(bins, "Cafeteria")  # [{'location': 'Cafeteria West', 'grams': 1250},
                                  #  {'location': 'Cafeteria East', 'grams': 480}]
from_building(bins, "Gym Lobby")  # [{'location': 'Gym Lobby', 'grams': 935}]
from_building(bins, "Pool")       # []
```

---

## Tier A: filter and a combine step

### 5. `material_total(bins: list, material: str) -> int`

The total grams collected for one material. The material arrives lowercase; the data's capitalization is inconsistent.

```python
material_total(bins, "paper")    # 3325
material_total(bins, "plastic")  # 480
material_total(bins, "glass")    # 935
material_total(bins, "metal")    # 0
```

---

## Tier A+: pull it together

### 6. `building_report(bins: list, word: str) -> dict`

A single dictionary summarizing one building, with the keys `"bins"` (how many bins are there), `"grams"` (their total weight), and `"flagged"` (how many of them were flagged).

```python
building_report(bins, "Cafeteria")  # {'bins': 2, 'grams': 1730, 'flagged': 1}
building_report(bins, "Library")    # {'bins': 2, 'grams': 2075, 'flagged': 0}
building_report(bins, "Gym Lobby")  # {'bins': 1, 'grams': 935, 'flagged': 1}
building_report(bins, "Pool")       # {'bins': 0, 'grams': 0, 'flagged': 0}
building_report([], "Library")      # {'bins': 0, 'grams': 0, 'flagged': 0}
```
