bins = [
    {"location": "Cafeteria West", "material": "PAPER",   "weight": "1,250 g", "flagged": "no"},
    {"location": "Cafeteria East", "material": "plastic", "weight": "480 g",   "flagged": "yes"},
    {"location": "Library",        "material": "Paper",   "weight": "2,015 g", "flagged": "no"},
    {"location": "Gym Lobby",      "material": "GLASS",   "weight": "935 g",   "flagged": "yes"},
    {"location": "Library Annex",  "material": "paper",   "weight": "60 g",    "flagged": "no"},
]


# === TIER B ===
# Must use map() and a lambda. Body is a single return statement.
# No loops, no list comprehensions.

def bin_weights(bins: list) -> list:
    """Return each bin's weight as a plain integer number of grams."""
    pass


def bin_rows(bins: list) -> list:
    """Return a new dict per bin with keys "location" (unchanged) and
    "grams" (the weight as an integer, as in bin_weights)."""
    pass


# === TIER B+ ===
# Same constraint as Tier B.

def net_weights(bins: list) -> list:
    """Return each bin's weight in grams, minus 50 if the bin was flagged."""
    pass


# === TIER A-, A and A+ ===
# No loops. Bodies may be more than one line. map() and filter() must both
# be used.

def from_building(bins: list, word: str) -> list:
    """Return every bin whose location contains `word`, as a dict with keys
    "location" and "grams"."""
    pass


def material_total(bins: list, material: str) -> int:
    """Return the total grams collected for one material. `material` arrives
    lowercase."""
    pass


def building_report(bins: list, word: str) -> dict:
    """Return a dict summarizing one building, with keys "bins" (how many
    bins are there), "grams" (their total weight) and "flagged" (how many of
    them were flagged)."""
    pass


def main():
    print("bin_weights:", bin_weights(bins))
    print("bin_rows:   ", bin_rows(bins))
    print("net_weights:", net_weights(bins))
    print()
    print('from_building(bins, "Library"):  ', from_building(bins, "Library"))
    print('from_building(bins, "Cafeteria"):', from_building(bins, "Cafeteria"))
    print('from_building(bins, "Gym Lobby"):', from_building(bins, "Gym Lobby"))
    print('from_building(bins, "Pool"):     ', from_building(bins, "Pool"))
    print()
    print('material_total(bins, "paper"):  ', material_total(bins, "paper"))
    print('material_total(bins, "plastic"):', material_total(bins, "plastic"))
    print('material_total(bins, "glass"):  ', material_total(bins, "glass"))
    print('material_total(bins, "metal"):  ', material_total(bins, "metal"))
    print()
    print('building_report(bins, "Cafeteria"):', building_report(bins, "Cafeteria"))
    print('building_report(bins, "Library"):  ', building_report(bins, "Library"))
    print('building_report(bins, "Gym Lobby"):', building_report(bins, "Gym Lobby"))
    print('building_report(bins, "Pool"):     ', building_report(bins, "Pool"))
    print('building_report([], "Library"):    ', building_report([], "Library"))


if __name__ == "__main__":
    main()
