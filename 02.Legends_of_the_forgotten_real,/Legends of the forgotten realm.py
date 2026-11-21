import json
import os
import random
import sys
import time
from collections import Counter


# ============================================================================
# GAME DATA: items, classes, skills, enemies, bosses, regions
# ============================================================================
MAX_LEVEL = 100
BUFF_TURNS = 3
HEAL_SPELL_COST = 20          # mana cost of the "Heal" action in battle
HEAL_SPELL_PERCENT = 0.30     # fraction of max HP restored by "Heal"
DEFENSE_FACTOR = 0.5          # how much of the player's defense blocks enemy damage
BOSS_HP_MULT = 3.0
BOSS_ATK_MULT = 1.15
BOSS_DEF_MULT = 1.1

# ----------------------------------------------------------------------------
# Rarity system
# ----------------------------------------------------------------------------
RARITY_ORDER = ["Common", "Uncommon", "Rare",
                "Super Rare", "Epic", "Mythical", "Legendary"]

RARITIES = {
    "Common":     {"colour": "white",  "mult": 1.0, "crit": 0,  "drop": 50.0},
    "Uncommon":   {"colour": "green",  "mult": 1.1, "crit": 2,  "drop": 25.0},
    "Rare":       {"colour": "blue",   "mult": 1.3, "crit": 5,  "drop": 15.0},
    "Super Rare": {"colour": "purple", "mult": 1.5, "crit": 8,  "drop": 6.0},
    "Epic":       {"colour": "orange", "mult": 1.8, "crit": 12, "drop": 3.0},
    "Mythical":   {"colour": "red",    "mult": 2.2, "crit": 18, "drop": 0.9},
    "Legendary":  {"colour": "gold",   "mult": 2.8, "crit": 25, "drop": 0.1},
}

# ----------------------------------------------------------------------------
# Weapons: (name, rank, base damage, price, required level)
# Final damage = base damage x rarity multiplier.
# ----------------------------------------------------------------------------
_WEAPON_ROWS = [
    ("Wooden Sword", "Common", 5, 50, 1),
    ("Rusty Axe", "Common", 6, 60, 1),
    ("Training Bow", "Common", 5, 50, 1),
    ("Apprentice Staff", "Common", 5, 50, 1),
    ("Training Dagger", "Common", 5, 50, 1),
    ("Bronze Sword", "Uncommon", 8, 120, 3),
    ("Hunter Bow", "Uncommon", 8, 120, 3),
    ("Oak Staff", "Uncommon", 8, 120, 3),
    ("Iron Sword", "Rare", 12, 300, 8),
    ("Steel Axe", "Rare", 14, 350, 10),
    ("Long Bow", "Rare", 13, 320, 9),
    ("Crystal Blade", "Super Rare", 20, 800, 18),
    ("Shadow Dagger", "Super Rare", 22, 900, 20),
    ("Lightning Bow", "Super Rare", 21, 850, 19),
    ("Flame Sword", "Epic", 32, 2000, 30),
    ("Ice Spear", "Epic", 34, 2200, 32),
    ("Thunder Hammer", "Epic", 36, 2400, 35),
    ("Phoenix Blade", "Mythical", 50, 6000, 50),
    ("Demon Slayer", "Mythical", 54, 6800, 55),
    ("Celestial Staff", "Mythical", 52, 6400, 52),
    ("Dragon King's Sword", "Legendary", 80, 20000, 75),
    ("Blade of Eternity", "Legendary", 85, 24000, 80),
    ("Bow of the Gods", "Legendary", 90, 28000, 85),
]

WEAPONS = [
    {"name": n, "rank": r, "damage": int(d * RARITIES[r]["mult"]),
     "crit": RARITIES[r]["crit"], "price": p, "level": lv}
    for n, r, d, p, lv in _WEAPON_ROWS
]
WEAPON_BY_NAME = {w["name"]: w for w in WEAPONS}

# ----------------------------------------------------------------------------
# Armor: (name, rank, defense, hp, mana, crit resistance, price, required level)
# ----------------------------------------------------------------------------
_ARMOR_ROWS = [
    ("Cloth Tunic", "Common", 2, 10, 0, 0, 40, 1),
    ("Leather Armor", "Common", 4, 20, 0, 1, 80, 1),
    ("Studded Leather", "Uncommon", 6, 35, 5, 1, 160, 4),
    ("Chainmail", "Rare", 10, 60, 10, 2, 400, 8),
    ("Mage Robe", "Rare", 6, 40, 40, 2, 380, 8),
    ("Crystal Mail", "Super Rare", 16, 100, 20, 4, 1000, 18),
    ("Shadow Cloak", "Super Rare", 12, 80, 30, 5, 1100, 20),
    ("Flame Plate", "Epic", 25, 180, 30, 6, 2500, 30),
    ("Frost Armor", "Epic", 27, 200, 40, 7, 2800, 33),
    ("Phoenix Armor", "Mythical", 40, 320, 60, 10, 7000, 50),
    ("Celestial Robe", "Mythical", 32, 280, 120, 10, 7200, 52),
    ("Dragon Scale Armor", "Legendary", 65, 600, 100, 15, 25000, 75),
    ("Eternal Aegis", "Legendary", 70, 700, 150, 18, 30000, 82),
]

ARMORS = [
    {"name": n, "rank": r, "defense": d, "hp": h, "mana": m,
     "crit_res": c, "price": p, "level": lv}
    for n, r, d, h, m, c, p, lv in _ARMOR_ROWS
]
ARMOR_BY_NAME = {a["name"]: a for a in ARMORS}

# ----------------------------------------------------------------------------
# Potions. amount / hp / mana of None means "restore fully".
# Buff potions: value is a fraction for attack/defense, flat % points for crit.
# ----------------------------------------------------------------------------
POTIONS = {
    "Small Health Potion":    {"kind": "hp", "amount": 50,   "price": 20,  "tier": 1},
    "Medium Health Potion":   {"kind": "hp", "amount": 100,  "price": 45,  "tier": 2},
    "Large Health Potion":    {"kind": "hp", "amount": 250,  "price": 110, "tier": 3},
    "Giant Health Potion":    {"kind": "hp", "amount": 500,  "price": 230, "tier": 4},
    "Ultimate Health Potion": {"kind": "hp", "amount": None, "price": 600, "tier": 5},
    "Small Mana Potion":      {"kind": "mana", "amount": 30,   "price": 25,  "tier": 1},
    "Medium Mana Potion":     {"kind": "mana", "amount": 75,   "price": 55,  "tier": 2},
    "Large Mana Potion":      {"kind": "mana", "amount": 150,  "price": 130, "tier": 3},
    "Giant Mana Potion":      {"kind": "mana", "amount": 300,  "price": 260, "tier": 4},
    "Ultimate Mana Potion":   {"kind": "mana", "amount": None, "price": 650, "tier": 5},
    "Minor Elixir": {"kind": "mixed", "hp": 100,  "mana": 50,   "price": 90,  "tier": 2},
    "Elixir":       {"kind": "mixed", "hp": 250,  "mana": 150,  "price": 250, "tier": 3},
    "Grand Elixir": {"kind": "mixed", "hp": None, "mana": None, "price": 900, "tier": 5},
    "Strength Potion":  {"kind": "buff", "stat": "attack",  "value": 0.30, "price": 60, "tier": 2},
    "Iron Skin Potion": {"kind": "buff", "stat": "defense", "value": 0.30, "price": 60, "tier": 2},
    "Focus Potion":     {"kind": "buff", "stat": "crit",    "value": 15,   "price": 70, "tier": 2},
}

# Crafting materials: name -> sell price
MATERIALS = {
    "Slime Gel": 4, "Wolf Pelt": 6, "Bone Fragment": 5, "Iron Ore": 12,
    "Spider Silk": 18, "Magic Crystal": 35, "Dragon Scale": 90, "Demon Horn": 160,
}
MATERIAL_LIST = list(MATERIALS)

# ----------------------------------------------------------------------------
# Classes and skills
# skill types: damage, multi, stun, poison, buff_attack, dodge, ignore_def, instakill
# ----------------------------------------------------------------------------
CLASSES = {
    "Warrior": {
        "hp": 150, "mana": 40, "attack": 16, "defense": 10, "crit": 5,
        "gain": {"hp": 22, "mana": 4, "attack": 4, "defense": 2},
        "weapon": "Wooden Sword",
        "desc": "Tough front-liner: high HP, attack and defense.",
        "skills": [
            {"name": "Slash", "mana": 5, "level": 1, "type": "damage", "mult": 1.4,
             "desc": "A strong sword strike (x1.4 damage)."},
            {"name": "Shield Bash", "mana": 10, "level": 5, "type": "stun", "mult": 1.2, "chance": 0.5,
             "desc": "Hit and 50% chance to stun the enemy."},
            {"name": "Rage", "mana": 15, "level": 10, "type": "buff_attack", "value": 0.5,
             "desc": "+50% Attack for 3 turns."},
            {"name": "Earthquake", "mana": 30, "level": 20, "type": "damage", "mult": 2.6,
             "desc": "Shake the ground (x2.6 damage)."},
        ],
    },
    "Mage": {
        "hp": 100, "mana": 120, "attack": 18, "defense": 4, "crit": 10,
        "gain": {"hp": 12, "mana": 10, "attack": 4, "defense": 1},
        "weapon": "Apprentice Staff",
        "desc": "Glass cannon: huge mana pool and powerful magic.",
        "skills": [
            {"name": "Fireball", "mana": 8, "level": 1, "type": "damage", "mult": 1.7,
             "desc": "Hurl a fireball (x1.7 damage)."},
            {"name": "Ice Blast", "mana": 14, "level": 5, "type": "stun", "mult": 1.5, "chance": 0.4,
             "desc": "Hit and 40% chance to freeze (stun)."},
            {"name": "Thunder Strike", "mana": 24, "level": 10, "type": "damage", "mult": 2.3,
             "desc": "Call down lightning (x2.3 damage)."},
            {"name": "Meteor", "mana": 40, "level": 20, "type": "damage", "mult": 3.6,
             "desc": "Rain fire from the sky (x3.6 damage)."},
        ],
    },
    "Archer": {
        "hp": 110, "mana": 70, "attack": 13, "defense": 7, "crit": 20,
        "gain": {"hp": 15, "mana": 6, "attack": 3, "defense": 1},
        "weapon": "Training Bow",
        "desc": "Balanced ranged fighter with a high critical chance.",
        "skills": [
            {"name": "Multi Shot", "mana": 8, "level": 1, "type": "multi", "mult": 0.6, "hits": 3,
             "desc": "Fire 3 arrows (x0.6 damage each)."},
            {"name": "Poison Arrow", "mana": 12, "level": 5, "type": "poison", "mult": 1.0,
             "desc": "Hit and poison the enemy for 3 turns."},
            {"name": "Explosive Arrow", "mana": 24, "level": 10, "type": "damage", "mult": 2.3,
             "desc": "An arrow that explodes (x2.3 damage)."},
            {"name": "Sniper Shot", "mana": 32, "level": 20, "type": "ignore_def", "mult": 3.0,
             "desc": "x3.0 damage that ignores enemy defense."},
        ],
    },
    "Assassin": {
        "hp": 90, "mana": 60, "attack": 16, "defense": 5, "crit": 35,
        "gain": {"hp": 12, "mana": 5, "attack": 4, "defense": 1},
        "weapon": "Training Dagger",
        "desc": "Fragile but deadly: very high critical chance.",
        "skills": [
            {"name": "Backstab", "mana": 6, "level": 1, "type": "damage", "mult": 1.6, "crit_bonus": 30,
             "desc": "x1.6 damage with +30% crit chance."},
            {"name": "Smoke Bomb", "mana": 12, "level": 5, "type": "dodge",
             "desc": "Dodge the enemy's next attack."},
            {"name": "Shadow Strike", "mana": 24, "level": 10, "type": "damage", "mult": 2.4, "crit_bonus": 20,
             "desc": "x2.4 damage with +20% crit chance."},
            {"name": "Instant Kill", "mana": 40, "level": 20, "type": "instakill", "mult": 1.2, "chance": 0.05,
             "desc": "5% chance to slay a foe outright (not bosses)."},
        ],
    },
}

# ----------------------------------------------------------------------------
# World: 10 regions, each with its own enemy family.
# Enemy tuple: (name, hp multiplier, attack multiplier, defense multiplier, skill name)
# Region i covers levels 10*i+1 .. 10*i+10 and unlocks after boss i-1 falls.
# ----------------------------------------------------------------------------
REGIONS = [
    {"name": "Village", "enemies": [
        ("Goblin", 1.0, 1.0, 1.0, "Rusty Stab"), ("Wolf",
                                                  0.9, 1.15, 0.8, "Savage Bite"),
        ("Slime", 1.2, 0.8, 0.7, "Acid Splash"), ("Zombie",
                                                  1.3, 0.9, 0.9, "Rotting Claw"),
        ("Skeleton", 0.9, 1.1, 1.1, "Bone Strike")]},
    {"name": "Forest", "enemies": [
        ("Orc", 1.2, 1.1, 1.1, "Axe Cleave"), ("Bandit",
                                               1.0, 1.15, 0.9, "Dirty Trick"),
        ("Troll", 1.5, 1.0, 1.0, "Club Smash"), ("Dark Archer",
                                                 0.8, 1.3, 0.7, "Shadow Arrow"),
        ("Giant Spider", 1.0, 1.1, 0.9, "Venom Fang")]},
    {"name": "Cave", "enemies": [
        ("Vampire", 1.1, 1.2, 1.0, "Blood Drain"), ("Werewolf",
                                                    1.3, 1.2, 0.9, "Lunar Claw"),
        ("Necromancer", 0.9, 1.3, 0.8,
         "Death Bolt"), ("Ice Golem", 1.6, 0.9, 1.4, "Frost Slam"),
        ("Fire Demon", 1.2, 1.3, 1.0, "Hellfire")]},
    {"name": "Desert", "enemies": [
        ("Sand Scorpion", 1.0, 1.2, 1.0,
         "Tail Sting"), ("Mummy", 1.4, 1.0, 1.1, "Curse Wrap"),
        ("Dust Wraith", 0.9, 1.3, 0.7, "Sandstorm"), ("Desert Bandit", 1.1, 1.2, 0.9, "Scimitar Slash")]},
    {"name": "Ruins", "enemies": [
        ("Stone Gargoyle", 1.5, 1.0, 1.4,
         "Stone Fist"), ("Cursed Knight", 1.2, 1.2, 1.2, "Cursed Blade"),
        ("Ruin Lich", 0.9, 1.4, 0.8, "Soul Burn"), ("Spectral Priest", 1.0, 1.2, 0.9, "Dark Prayer")]},
    {"name": "Castle", "enemies": [
        ("Dark Knight", 1.3, 1.3, 1.3, "Dark Cleave"), ("Castle Guard",
                                                        1.2, 1.1, 1.3, "Spear Thrust"),
        ("Shadow Mage", 0.9, 1.5, 0.8, "Shadow Bolt"), ("Gargoyle Lord", 1.6, 1.1, 1.4, "Wing Crush")]},
    {"name": "Volcano", "enemies": [
        ("Lava Golem", 1.7, 1.1, 1.4, "Magma Slam"), ("Magma Drake",
                                                      1.3, 1.4, 1.1, "Flame Breath"),
        ("Fire Imp", 0.8, 1.4, 0.8, "Ember Dart"), ("Ash Wraith", 1.0, 1.3, 0.9, "Ash Cloud")]},
    {"name": "Frozen Mountain", "enemies": [
        ("Frost Wolf", 1.0, 1.4, 0.9, "Icy Fangs"), ("Ice Wraith",
                                                     0.9, 1.4, 0.8, "Chill Touch"),
        ("Yeti", 1.7, 1.2, 1.2, "Avalanche Smash"), ("Frozen Revenant", 1.3, 1.3, 1.2, "Frostbite Blade")]},
    {"name": "Sky Temple", "enemies": [
        ("Storm Harpy", 0.9, 1.5, 0.8, "Gale Talons"), ("Thunder Sentinel",
                                                        1.5, 1.3, 1.3, "Lightning Lance"),
        ("Cloud Serpent", 1.2, 1.4, 1.0, "Constrict"), ("Sky Guardian", 1.5, 1.2, 1.4, "Heaven's Hammer")]},
    {"name": "Demon Realm", "enemies": [
        ("Imp Legion", 0.9, 1.5, 0.9, "Swarm Strike"), ("Hellhound",
                                                        1.2, 1.5, 1.0, "Infernal Bite"),
        ("Demon Knight", 1.5, 1.4, 1.4, "Abyssal Slash"), ("Abyss Lord", 1.7, 1.5, 1.3, "Void Crush")]},
]

# One boss every 10 levels.
BOSSES = [
    {"level": 10,  "name": "Goblin King",        "skills": ["Royal Smash", "War Cry"],
     "trophy": "Goblin King's Crown"},
    {"level": 20,  "name": "Forest Guardian",    "skills": ["Thorn Lash", "Nature's Wrath"],
     "trophy": "Guardian's Heartwood"},
    {"level": 30,  "name": "Ancient Golem",      "skills": ["Boulder Toss", "Quake Stomp"],
     "trophy": "Ancient Golem Core"},
    {"level": 40,  "name": "Vampire Lord",       "skills": ["Crimson Feast", "Bat Swarm"],
     "trophy": "Vampire Lord's Fang"},
    {"level": 50,  "name": "Dragon Rider",       "skills": ["Dragon Dive", "Lance Charge"],
     "trophy": "Dragon Rider's Lance"},
    {"level": 60,  "name": "Demon General",      "skills": ["Hellfire Barrage", "Warlord's Command"],
     "trophy": "Demon General's Banner"},
    {"level": 70,  "name": "Ice Titan",          "skills": ["Glacier Crush", "Blizzard"],
     "trophy": "Ice Titan's Shard"},
    {"level": 80,  "name": "Shadow Emperor",     "skills": ["Umbral Slash", "Void Grasp"],
     "trophy": "Shadow Emperor's Mask"},
    {"level": 90,  "name": "Celestial Dragon",   "skills": ["Star Breath", "Comet Tail"],
     "trophy": "Celestial Dragon Pearl"},
    {"level": 100, "name": "Ancient Demon King", "skills": ["Doom Blade", "Soul Devour"],
     "trophy": "Demon King's Horn"},
]


# ============================================================================
# CONSOLE HELPERS: input validation, colours, bars
# ============================================================================
class GameExit(Exception):
    """Raised when the player quits or input ends, so the game can stop cleanly."""


USE_COLOUR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
if USE_COLOUR and os.name == "nt":
    os.system("")  # enables ANSI escape codes on Windows 10+ terminals

ANSI = {
    "white": "\033[97m", "green": "\033[92m", "blue": "\033[94m",
    "purple": "\033[95m", "orange": "\033[38;5;208m", "red": "\033[91m",
    "gold": "\033[93m", "cyan": "\033[96m", "bold": "\033[1m", "reset": "\033[0m",
}


def paint(text, colour):
    """Wrap text in an ANSI colour (does nothing when colours are unavailable)."""
    if not USE_COLOUR or colour not in ANSI:
        return str(text)
    return f"{ANSI[colour]}{text}{ANSI['reset']}"


def line(char="=", width=40):
    print(char * width)


def title(text, char="="):
    line(char)
    print(text.center(40).rstrip())
    line(char)


def ask(prompt):
    """input() wrapper that turns Ctrl+C / end-of-input into a clean exit."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise GameExit()


def ask_int(prompt, low, high):
    """Keep asking until the player enters a whole number in [low, high]."""
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(
                f"Invalid input. Please enter a number from {low} to {high}.")
            continue
        if low <= value <= high:
            return value
        print(f"Out of range. Please enter a number from {low} to {high}.")


def ask_yes_no(prompt):
    while True:
        raw = ask(prompt).lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer y or n.")


def ask_name(prompt, max_len=20):
    while True:
        name = ask(prompt)
        if not name:
            print("Name cannot be empty.")
        elif len(name) > max_len:
            print(f"Name must be at most {max_len} characters.")
        else:
            return name


def pause():
    ask("\nPress Enter to continue...")


def bar(current, maximum, width=15):
    filled = int(width * max(0, current) / maximum) if maximum > 0 else 0
    filled = min(width, filled)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def format_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


# ============================================================================
# PLAYER: stats, levelling, equipment, save data
# ============================================================================
def _to_int(value, low, high=None):
    """Convert to int and range-check (raises ValueError / TypeError if bad)."""
    number = int(value)
    if number < low or (high is not None and number > high):
        raise ValueError("value out of range")
    return number


class Player:
    def __init__(self, name, class_name):
        base = CLASSES[class_name]
        self.name = name
        self.class_name = class_name
        self.level = 1
        self.exp = 0
        self.base_max_hp = base["hp"]
        self.base_max_mana = base["mana"]
        self.base_attack = base["attack"]
        self.base_defense = base["defense"]
        self.base_crit = base["crit"]
        self.crit_damage = 1.5
        self.gold = 100
        self.weapon = base["weapon"]          # equipped weapon name (or None)
        self.armor = "Cloth Tunic"            # equipped armor name (or None)
        self.weapons = []                     # weapons in the bag (names)
        self.armors = []                      # armors in the bag (names)
        self.potions = {"Small Health Potion": 3, "Small Mana Potion": 1}
        self.materials = {}
        self.quest_items = []
        self.bosses_defeated = 0
        self.enemies_defeated = 0
        self.region = 0
        self.play_time = 0.0
        self._session_start = time.time()
        self.weapons_collected = {self.weapon}
        self.rare_items = set()
        # battle-only state (never saved)
        self.buffs = {}
        self.defending = False
        self.dodge_next = False
        self.hp = self.max_hp
        self.mana = self.max_mana

    # ---- derived stats -------------------------------------------------
    @property
    def weapon_data(self):
        return WEAPON_BY_NAME.get(self.weapon)

    @property
    def armor_data(self):
        return ARMOR_BY_NAME.get(self.armor)

    @property
    def max_hp(self):
        armor = self.armor_data
        return self.base_max_hp + (armor["hp"] if armor else 0)

    @property
    def max_mana(self):
        armor = self.armor_data
        return self.base_max_mana + (armor["mana"] if armor else 0)

    @property
    def attack(self):
        """Attack + weapon damage (the formula from the specification)."""
        weapon = self.weapon_data
        total = self.base_attack + (weapon["damage"] if weapon else 0)
        return int(total * (1 + self.buffs.get("attack", {}).get("value", 0)))

    @property
    def defense(self):
        armor = self.armor_data
        total = self.base_defense + (armor["defense"] if armor else 0)
        return int(total * (1 + self.buffs.get("defense", {}).get("value", 0)))

    @property
    def crit_chance(self):
        weapon = self.weapon_data
        total = self.base_crit + (weapon["crit"] if weapon else 0)
        total += self.buffs.get("crit", {}).get("value", 0)
        return min(80, total)

    @property
    def crit_resist(self):
        armor = self.armor_data
        return armor["crit_res"] if armor else 0

    def is_alive(self):
        return self.hp > 0

    def total_play_time(self):
        return self.play_time + (time.time() - self._session_start)

    def clamp_vitals(self):
        self.hp = max(0, min(self.hp, self.max_hp))
        self.mana = max(0, min(self.mana, self.max_mana))

    # ---- levelling ----------------------------------------------------
    def exp_to_next(self):
        return int(30 * self.level ** 1.2)

    def level_cap(self):
        """Highest level reachable until the next boss is defeated."""
        return min(MAX_LEVEL, (self.bosses_defeated + 1) * 10)

    def unlocked_skills(self):
        return [s for s in CLASSES[self.class_name]["skills"] if s["level"] <= self.level]

    def add_exp(self, amount):
        """Add EXP, level up as needed, and return messages to display."""
        if self.level >= self.level_cap():
            return ["You are at the level cap. Defeat the region boss to grow stronger!"]
        messages = []
        self.exp += amount
        while self.level < self.level_cap() and self.exp >= self.exp_to_next():
            self.exp -= self.exp_to_next()
            messages.extend(self.level_up())
        if self.level >= self.level_cap():
            self.exp = 0
            messages.append("Level cap reached - defeat the boss to continue!")
        return messages

    def level_up(self):
        gain = CLASSES[self.class_name]["gain"]
        self.level += 1
        self.base_max_hp += gain["hp"]
        self.base_max_mana += gain["mana"]
        self.base_attack += gain["attack"]
        self.base_defense += gain["defense"]
        messages = [f"LEVEL UP! You are now level {self.level}!",
                    f"  HP +{gain['hp']}  Mana +{gain['mana']}  "
                    f"Attack +{gain['attack']}  Defense +{gain['defense']}"]
        if self.level % 5 == 0:   # passive bonus every 5 levels
            self.base_attack += 5
            self.base_defense += 3
            self.base_crit += 2
            self.crit_damage = round(self.crit_damage + 0.05, 2)
            messages.append("  Passive unlocked: Battle Mastery "
                            "(+5 Attack, +3 Defense, +2% Crit, +0.05 Crit Damage)")
        for skill in CLASSES[self.class_name]["skills"]:
            if skill["level"] == self.level:
                messages.append(f"  New skill unlocked: {skill['name']}!")
        self.hp = self.max_hp
        self.mana = self.max_mana
        return messages

    # ---- items --------------------------------------------------------
    def add_item(self, kind, name, qty=1):
        if kind == "weapon":
            self.weapons.extend([name] * qty)
            self.weapons_collected.add(name)
            self._track_rare(WEAPON_BY_NAME[name]["rank"], name)
        elif kind == "armor":
            self.armors.extend([name] * qty)
            self._track_rare(ARMOR_BY_NAME[name]["rank"], name)
        elif kind == "potion":
            self.potions[name] = self.potions.get(name, 0) + qty
        elif kind == "material":
            self.materials[name] = self.materials.get(name, 0) + qty
        elif kind == "quest":
            self.quest_items.append(name)

    def _track_rare(self, rank, name):
        if RARITY_ORDER.index(rank) >= RARITY_ORDER.index("Rare"):
            self.rare_items.add(name)

    def remove_item(self, kind, name, qty=1):
        """Remove items from the bag. Returns True on success."""
        if kind in ("weapon", "armor"):
            bag = self.weapons if kind == "weapon" else self.armors
            if bag.count(name) < qty:
                return False
            for _ in range(qty):
                bag.remove(name)
            return True
        stock = self.potions if kind == "potion" else self.materials if kind == "material" else None
        if stock is None or stock.get(name, 0) < qty:
            return False
        stock[name] -= qty
        if stock[name] <= 0:
            del stock[name]
        return True

    def tick_buffs(self):
        """Count buffs down by one turn; returns the names of expired buffs."""
        expired = []
        for stat in list(self.buffs):
            self.buffs[stat]["turns"] -= 1
            if self.buffs[stat]["turns"] <= 0:
                del self.buffs[stat]
                expired.append(stat)
        return expired

    # ---- display ------------------------------------------------------
    def stat_sheet(self):
        weapon, armor = self.weapon_data, self.armor_data
        potion_count = sum(self.potions.values())
        return "\n".join([
            f"Name: {self.name}    Class: {self.class_name}",
            f"Level: {self.level}/{MAX_LEVEL} (cap {self.level_cap()})    "
            f"EXP: {self.exp}/{self.exp_to_next()}",
            f"HP: {self.hp}/{self.max_hp}    Mana: {self.mana}/{self.max_mana}",
            f"Attack: {self.attack}    Defense: {self.defense}",
            f"Crit Chance: {self.crit_chance:.0f}%    Crit Damage: x{self.crit_damage:.2f}    "
            f"Crit Resist: {self.crit_resist}%",
            f"Weapon: {weapon['name'] if weapon else 'None'}",
            f"Armor: {armor['name'] if armor else 'None'}",
            f"Gold: {self.gold}    Potions: {potion_count}",
            f"Bosses Defeated: {self.bosses_defeated}    Enemies Defeated: {self.enemies_defeated}",
        ])

    # ---- save / load --------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name, "class_name": self.class_name, "level": self.level,
            "exp": self.exp, "base_max_hp": self.base_max_hp,
            "base_max_mana": self.base_max_mana, "hp": self.hp, "mana": self.mana,
            "base_attack": self.base_attack, "base_defense": self.base_defense,
            "base_crit": self.base_crit, "crit_damage": self.crit_damage,
            "gold": self.gold, "weapon": self.weapon, "armor": self.armor,
            "weapons": list(self.weapons), "armors": list(self.armors),
            "potions": dict(self.potions), "materials": dict(self.materials),
            "quest_items": list(self.quest_items),
            "bosses_defeated": self.bosses_defeated,
            "enemies_defeated": self.enemies_defeated, "region": self.region,
            "play_time": self.total_play_time(),
            "weapons_collected": sorted(self.weapons_collected),
            "rare_items": sorted(self.rare_items),
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a player from saved data. Raises ValueError/KeyError/TypeError if invalid."""
        if not isinstance(data, dict):
            raise ValueError("save data is not a dictionary")
        class_name = data["class_name"]
        if class_name not in CLASSES:
            raise ValueError("unknown class")
        name = str(data["name"]).strip()[:20] or "Hero"
        p = cls(name, class_name)
        p.level = _to_int(data["level"], 1, MAX_LEVEL)
        p.exp = _to_int(data["exp"], 0)
        p.base_max_hp = _to_int(data["base_max_hp"], 1)
        p.base_max_mana = _to_int(data["base_max_mana"], 0)
        p.base_attack = _to_int(data["base_attack"], 0)
        p.base_defense = _to_int(data["base_defense"], 0)
        p.base_crit = _to_int(data["base_crit"], 0)
        p.crit_damage = float(data["crit_damage"])
        if not 1.0 <= p.crit_damage <= 5.0:
            raise ValueError("bad crit damage")
        p.gold = _to_int(data["gold"], 0)
        p.bosses_defeated = _to_int(data["bosses_defeated"], 0, len(BOSSES))
        p.enemies_defeated = _to_int(data["enemies_defeated"], 0)
        p.region = _to_int(data["region"], 0, len(REGIONS) - 1)
        p.play_time = max(0.0, float(data["play_time"]))
        p.weapon = data["weapon"]
        p.armor = data["armor"]
        if p.weapon is not None and p.weapon not in WEAPON_BY_NAME:
            raise ValueError("unknown weapon")
        if p.armor is not None and p.armor not in ARMOR_BY_NAME:
            raise ValueError("unknown armor")
        p.weapons = [str(n) for n in data["weapons"]]
        p.armors = [str(n) for n in data["armors"]]
        if any(n not in WEAPON_BY_NAME for n in p.weapons) or \
           any(n not in ARMOR_BY_NAME for n in p.armors):
            raise ValueError("unknown item in bag")
        p.potions = {}
        for pname, qty in data["potions"].items():
            if pname not in POTIONS:
                raise ValueError("unknown potion")
            qty = _to_int(qty, 0)
            if qty:
                p.potions[pname] = qty
        p.materials = {}
        for mname, qty in data["materials"].items():
            if mname not in MATERIALS:
                raise ValueError("unknown material")
            qty = _to_int(qty, 0)
            if qty:
                p.materials[mname] = qty
        p.quest_items = [str(n) for n in data["quest_items"]]
        p.weapons_collected = {
            n for n in data["weapons_collected"] if n in WEAPON_BY_NAME}
        p.rare_items = {str(n) for n in data["rare_items"]}
        p.hp = _to_int(data["hp"], 0)
        p.mana = _to_int(data["mana"], 0)
        p.clamp_vitals()
        if p.hp == 0:
            p.hp = p.max_hp
        return p


# ============================================================================
# SAVE / LOAD (JSON)
# ============================================================================
SAVE_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "savegame.json")


def save_game(player, quiet=False):
    """Write the save file safely (temp file + rename). Returns True on success."""
    temp_path = SAVE_FILE + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as handle:
            json.dump(player.to_dict(), handle, indent=2)
        os.replace(temp_path, SAVE_FILE)
    except OSError as error:
        print(f"Could not save the game: {error}")
        return False
    if not quiet:
        print("Game saved!")
    return True


def load_game():
    """Return a Player loaded from disk, or None (with a message) if that fails."""
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        player = Player.from_dict(data)
    except (OSError, json.JSONDecodeError):
        print("The save file could not be read (it may be damaged).")
        return None
    except (KeyError, ValueError, TypeError, AttributeError):
        print("The save file is corrupted or incompatible.")
        return None
    print(f"Welcome back, {player.name}!")
    return player


# ============================================================================
# ITEMS: loot, potions, inventory, shop
# ============================================================================
BAG_KINDS = ("weapon", "armor", "potion", "material", "quest")


# ---------------------------------------------------------------- descriptions
def potion_effect(name):
    p = POTIONS[name]
    kind = p["kind"]
    if kind == "hp":
        return "Restores " + ("all" if p["amount"] is None else str(p["amount"])) + " HP"
    if kind == "mana":
        return "Restores " + ("all" if p["amount"] is None else str(p["amount"])) + " Mana"
    if kind == "mixed":
        hp = "all" if p["hp"] is None else str(p["hp"])
        mana = "all" if p["mana"] is None else str(p["mana"])
        return f"Restores {hp} HP and {mana} Mana"
    if p["stat"] == "crit":
        return f"+{p['value']}% Crit Chance for {BUFF_TURNS} turns"
    return f"+{int(p['value'] * 100)}% {p['stat'].title()} for {BUFF_TURNS} turns"


def describe(kind, name):
    """One-line description of any item."""
    if kind == "weapon":
        w = WEAPON_BY_NAME[name]
        coloured = paint(name, RARITIES[w["rank"]]["colour"])
        return (f"{coloured} [{w['rank']}] DMG {w['damage']} "
                f"CRIT +{w['crit']}% (Lv {w['level']})")
    if kind == "armor":
        a = ARMOR_BY_NAME[name]
        coloured = paint(name, RARITIES[a["rank"]]["colour"])
        return (f"{coloured} [{a['rank']}] DEF +{a['defense']} HP +{a['hp']} "
                f"MP +{a['mana']} CritRes {a['crit_res']}% (Lv {a['level']})")
    if kind == "potion":
        return f"{name} - {potion_effect(name)}"
    if kind == "material":
        return f"{name} (material, sells for {MATERIALS[name]}g)"
    return f"{name} (quest item)"


def sell_value(kind, name):
    if kind == "weapon":
        return WEAPON_BY_NAME[name]["price"] // 2
    if kind == "armor":
        return ARMOR_BY_NAME[name]["price"] // 2
    if kind == "potion":
        return POTIONS[name]["price"] // 2
    if kind == "material":
        return MATERIALS[name]
    return 0


# ----------------------------------------------------------------------- loot
def roll_rarity(min_rank="Common"):
    names = RARITY_ORDER[RARITY_ORDER.index(min_rank):]
    return random.choices(names, weights=[RARITIES[n]["drop"] for n in names])[0]


def random_equipment(catalog, level, min_rank="Common"):
    """Pick a random weapon/armor; rarer ones are less likely (see drop table)."""
    floor = RARITY_ORDER.index(min_rank)
    index = RARITY_ORDER.index(roll_rarity(min_rank))
    while index >= floor:
        pool = [i for i in catalog
                if i["rank"] == RARITY_ORDER[index] and i["level"] <= level + 15]
        if pool:
            return random.choice(pool)
        index -= 1
    candidates = [i for i in catalog if RARITY_ORDER.index(i["rank"]) >= floor]
    return min(candidates, key=lambda i: i["level"]) if candidates else None


def pick_potion(level):
    limit = level // 20 + 1
    names = [n for n, p in POTIONS.items() if p["tier"] <= limit]
    return random.choices(names, weights=[1 / POTIONS[n]["tier"] for n in names])[0]


def pick_material(level):
    return random.choice(MATERIAL_LIST[: level // 15 + 3])


def generate_loot(level, boss=False):
    """Return a list of (kind, name, quantity) drops (gold is handled separately)."""
    loot = []
    if boss:   # guaranteed rare-or-better gear plus supplies
        weapon = random_equipment(WEAPONS, level, "Rare")
        armor = random_equipment(ARMORS, level, "Rare")
        if weapon:
            loot.append(("weapon", weapon["name"], 1))
        if armor:
            loot.append(("armor", armor["name"], 1))
        loot.append(("potion", pick_potion(level), 2))
        loot.append(("material", pick_material(level), 2))
        return loot
    if random.random() < 0.30:
        loot.append(("potion", pick_potion(level), 1))
    if random.random() < 0.25:
        loot.append(("material", pick_material(level), 1))
    if random.random() < 0.12:
        weapon = random_equipment(WEAPONS, level)
        if weapon:
            loot.append(("weapon", weapon["name"], 1))
    if random.random() < 0.10:
        armor = random_equipment(ARMORS, level)
        if armor:
            loot.append(("armor", armor["name"], 1))
    return loot


# -------------------------------------------------------------------- potions
def use_potion(player, name, in_battle=False):
    """Apply a potion. Returns (used, message); the caller removes it from the bag."""
    p = POTIONS[name]
    kind = p["kind"]
    if kind == "buff":
        if not in_battle:
            return False, "Buff potions can only be used during battle."
        # +1 because the turn in which you drink also counts down once
        player.buffs[p["stat"]] = {
            "value": p["value"], "turns": BUFF_TURNS + 1}
        return True, f"You drink the {name}. {potion_effect(name)}!"
    if kind == "hp":
        hp_gain, mana_gain = p["amount"], 0
    elif kind == "mana":
        hp_gain, mana_gain = 0, p["amount"]
    else:
        hp_gain, mana_gain = p["hp"], p["mana"]
    hp_room = player.max_hp - player.hp
    mana_room = player.max_mana - player.mana
    healed = hp_room if hp_gain is None else min(hp_gain, hp_room)
    restored = mana_room if mana_gain is None else min(mana_gain, mana_room)
    if healed <= 0 and restored <= 0:
        return False, "That would have no effect right now."
    player.hp += healed
    player.mana += restored
    parts = []
    if healed > 0:
        parts.append(f"{healed} HP")
    if restored > 0:
        parts.append(f"{restored} Mana")
    return True, f"You drink the {name} and restore " + " and ".join(parts) + "."


# ------------------------------------------------------------------ inventory
def bag_entries(player, kinds):
    """List of (kind, name, quantity) for everything in the bag of the given kinds."""
    entries = []
    if "weapon" in kinds:
        entries += [("weapon", n, q)
                    for n, q in sorted(Counter(player.weapons).items())]
    if "armor" in kinds:
        entries += [("armor", n, q)
                    for n, q in sorted(Counter(player.armors).items())]
    if "potion" in kinds:
        entries += [("potion", n, q)
                    for n, q in sorted(player.potions.items())]
    if "material" in kinds:
        entries += [("material", n, q)
                    for n, q in sorted(player.materials.items())]
    if "quest" in kinds:
        entries += [("quest", n, q)
                    for n, q in sorted(Counter(player.quest_items).items())]
    return entries


def show_inventory(player):
    title("INVENTORY")
    print("Equipped:")
    print("  Weapon:", describe("weapon", player.weapon)
          if player.weapon else "None")
    print("  Armor: ", describe("armor", player.armor)
          if player.armor else "None")
    entries = bag_entries(player, BAG_KINDS)
    print("\nBag:" if entries else "\nYour bag is empty.")
    for kind, name, qty in entries:
        print(f"  - {describe(kind, name)}  x{qty}")
    print(f"\nGold: {player.gold}")


def pick_entry(player, kinds, heading):
    """Show a numbered list and return the chosen (kind, name, qty), or None."""
    entries = bag_entries(player, kinds)
    if not entries:
        print("You have nothing suitable.")
        return None
    print(f"\n{heading}")
    for number, (kind, name, qty) in enumerate(entries, 1):
        print(f" {number}. {describe(kind, name)}  x{qty}")
    print(" 0. Cancel")
    choice = ask_int("> ", 0, len(entries))
    return entries[choice - 1] if choice else None


def equip(player, kind):
    entry = pick_entry(player, (kind,), f"Choose {kind} to equip:")
    if not entry:
        return
    name = entry[1]
    item = WEAPON_BY_NAME[name] if kind == "weapon" else ARMOR_BY_NAME[name]
    if item["level"] > player.level:
        print(f"You need level {item['level']} to equip {name}.")
        return
    player.remove_item(kind, name)
    old = player.weapon if kind == "weapon" else player.armor
    if old:
        player.add_item(kind, old)
    if kind == "weapon":
        player.weapon = name
    else:
        player.armor = name
    player.clamp_vitals()
    print(f"You equip {name}.")


def unequip(player, kind):
    current = player.weapon if kind == "weapon" else player.armor
    if not current:
        print(f"No {kind} equipped.")
        return
    player.add_item(kind, current)
    if kind == "weapon":
        player.weapon = None
    else:
        player.armor = None
    player.clamp_vitals()
    print(f"You unequip {current}.")


def use_potion_menu(player, in_battle=False):
    """Pick and drink a potion. Returns True if one was consumed."""
    entry = pick_entry(player, ("potion",), "Choose a potion:")
    if not entry:
        return False
    used, message = use_potion(player, entry[1], in_battle)
    print(message)
    if used:
        player.remove_item("potion", entry[1])
    return used


def ask_quantity(maximum):
    return ask_int(f"How many? (1-{maximum}): ", 1, maximum) if maximum > 1 else 1


def drop_item(player):
    entry = pick_entry(player, ("weapon", "armor", "potion",
                       "material"), "Choose item to drop:")
    if not entry:
        return
    kind, name, qty = entry
    amount = ask_quantity(qty)
    if ask_yes_no(f"Really drop {amount}x {name}? (y/n): "):
        player.remove_item(kind, name, amount)
        print(f"You dropped {amount}x {name}.")


def sell_items(player):
    while True:
        print(f"\nGold: {player.gold}")
        entry = pick_entry(player, ("weapon", "armor", "potion", "material"),
                           "Choose item to sell (half price for gear/potions):")
        if not entry:
            return
        kind, name, qty = entry
        amount = ask_quantity(qty)
        earned = sell_value(kind, name) * amount
        if player.remove_item(kind, name, amount):
            player.gold += earned
            print(f"Sold {amount}x {name} for {earned} gold.")


def inventory_menu(player, in_battle=False, can_sell=False):
    if in_battle:      # view only during combat
        show_inventory(player)
        pause()
        return
    while True:
        show_inventory(player)
        print("\n1 Equip Weapon   2 Equip Armor\n3 Unequip Weapon 4 Unequip Armor\n"
              "5 Use Potion     6 Drop Item\n7 Sell Item       0 Back")
        choice = ask_int("> ", 0, 7)
        if choice == 0:
            return
        if choice == 1:
            equip(player, "weapon")
        elif choice == 2:
            equip(player, "armor")
        elif choice == 3:
            unequip(player, "weapon")
        elif choice == 4:
            unequip(player, "armor")
        elif choice == 5:
            use_potion_menu(player)
        elif choice == 6:
            drop_item(player)
        elif choice == 7:
            if can_sell:
                sell_items(player)
            else:
                print("You can only sell items at the village shop.")


# ----------------------------------------------------------------------- shop
def buy_equipment(player, kind):
    catalog = WEAPONS if kind == "weapon" else ARMORS
    stock = sorted((i for i in catalog if i["level"] <= player.level + 5),
                   key=lambda i: i["price"])
    while True:
        print(f"\nGold: {player.gold}")
        for number, item in enumerate(stock, 1):
            print(
                f" {number}. {describe(kind, item['name'])} - {item['price']}g")
        print(" 0. Back")
        choice = ask_int("> ", 0, len(stock))
        if choice == 0:
            return
        item = stock[choice - 1]
        if player.gold < item["price"]:
            print("Not enough gold!")
            continue
        player.gold -= item["price"]
        player.add_item(kind, item["name"])
        print(f"You bought {item['name']}.")


def buy_potions(player):
    names = sorted(POTIONS, key=lambda n: POTIONS[n]["price"])
    while True:
        print(f"\nGold: {player.gold}")
        for number, name in enumerate(names, 1):
            print(
                f" {number}. {describe('potion', name)} - {POTIONS[name]['price']}g")
        print(" 0. Back")
        choice = ask_int("> ", 0, len(names))
        if choice == 0:
            return
        name = names[choice - 1]
        amount = ask_int("How many? (1-99): ", 1, 99)
        cost = POTIONS[name]["price"] * amount
        if player.gold < cost:
            print(f"Not enough gold! You need {cost}.")
            continue
        player.gold -= cost
        player.add_item("potion", name, amount)
        print(f"You bought {amount}x {name} for {cost} gold.")


def shop_menu(player):
    while True:
        title("VILLAGE SHOP")
        print(f"Gold: {player.gold}")
        print("1 Buy Weapons\n2 Buy Armor\n3 Buy Potions\n4 Sell Items\n5 Exit")
        choice = ask_int("> ", 1, 5)
        if choice == 1:
            buy_equipment(player, "weapon")
        elif choice == 2:
            buy_equipment(player, "armor")
        elif choice == 3:
            buy_potions(player)
        elif choice == 4:
            sell_items(player)
        else:
            return


# ============================================================================
# BATTLE SYSTEM: enemies, bosses, combat loop
# ============================================================================
class Enemy:
    def __init__(self, name, level, hp, attack, defense, xp, gold, skills,
                 boss=False, crit_chance=5, heals=1, trophy=None):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.xp = xp
        self.gold = gold
        self.skills = skills
        self.boss = boss
        self.crit_chance = crit_chance
        self.heals_left = heals
        self.trophy = trophy
        self.turn_count = 0
        self.stunned = False
        self.poison_turns = 0
        self.poison_damage = 0


def scaled_stats(level):
    """Base HP / attack / defense of an enemy for a given level."""
    return 30 + 22 * level, 8 + 3.2 * level, 1 + 1.2 * level


def make_enemy(level, region_index):
    name, hp_mult, atk_mult, def_mult, skill = random.choice(
        REGIONS[region_index]["enemies"])
    hp0, atk0, def0 = scaled_stats(level)
    variation = random.uniform(0.9, 1.1)
    return Enemy(
        name, level,
        hp=max(10, int(hp0 * hp_mult * variation)),
        attack=max(1, int(atk0 * atk_mult * variation)),
        defense=int(def0 * def_mult),
        xp=int((15 + 10 * level) * (hp_mult + atk_mult) / 2),
        gold=int((6 + 4 * level) * random.uniform(0.7, 1.3)),
        skills=[skill])


def make_boss(index):
    data = BOSSES[index]
    level = data["level"]
    hp0, atk0, def0 = scaled_stats(level)
    return Enemy(
        data["name"], level,
        hp=int(hp0 * BOSS_HP_MULT), attack=int(atk0 * BOSS_ATK_MULT),
        defense=int(def0 * BOSS_DEF_MULT), xp=(15 + 10 * level) * 5,
        gold=(6 + 4 * level) * 6, skills=list(data["skills"]),
        boss=True, crit_chance=15, heals=3, trophy=data["trophy"])


# ------------------------------------------------------------------ display
def show_status(player, enemy):
    tag = "BOSS" if enemy.boss else "Enemy"
    print(f"\n{tag}: {enemy.name} (Lv {enemy.level})  "
          f"HP {enemy.hp}/{enemy.max_hp} {bar(enemy.hp, enemy.max_hp)}")
    effects = []
    if enemy.stunned:
        effects.append("Stunned")
    if enemy.poison_turns > 0:
        effects.append(f"Poisoned ({enemy.poison_turns})")
    if effects:
        print("  Status:", ", ".join(effects))
    print(f"You:   {player.name} (Lv {player.level})  HP {player.hp}/{player.max_hp} "
          f"{bar(player.hp, player.max_hp)}  Mana {player.mana}/{player.max_mana}")
    if player.buffs:
        text = ", ".join(f"{stat.title()} buff ({b['turns'] - 1} turns left)"
                         for stat, b in player.buffs.items())
        print("  Buffs:", text)
    if player.defending:
        print("  You are defending.")


def report_hit(damage, crit):
    if crit:
        print("CRITICAL HIT!")
    print(f"You dealt {damage} Damage!")


# ------------------------------------------------------------ player actions
def player_hit(player, enemy, mult=1.0, crit_bonus=0, ignore_def=False):
    """Damage = Attack + Weapon - Enemy Defense; crits multiply the result."""
    defense = 0 if ignore_def else enemy.defense
    damage = max(1, int(player.attack * mult) - defense)
    damage = max(1, int(damage * random.uniform(0.9, 1.1)))
    crit = random.random() * 100 < min(95, player.crit_chance + crit_bonus)
    if crit:
        damage = int(damage * player.crit_damage)
    enemy.hp = max(0, enemy.hp - damage)
    return damage, crit


def attack_action(player, enemy):
    print(f"\nYou attack {enemy.name}!")
    report_hit(*player_hit(player, enemy))
    return True


def skill_action(player, enemy):
    skills = player.unlocked_skills()
    print("\nSkills:")
    for number, skill in enumerate(skills, 1):
        print(
            f" {number}. {skill['name']} (Mana {skill['mana']}) - {skill['desc']}")
    print(" 0. Back")
    choice = ask_int("Choose skill: ", 0, len(skills))
    if choice == 0:
        return False
    skill = skills[choice - 1]
    if player.mana < skill["mana"]:
        print("Not enough mana!")
        return False
    player.mana -= skill["mana"]
    print(f"\nYou use {skill['name']}!")
    kind = skill["type"]
    if kind in ("damage", "ignore_def"):
        report_hit(*player_hit(player, enemy, skill["mult"], skill.get("crit_bonus", 0),
                               ignore_def=(kind == "ignore_def")))
    elif kind == "multi":
        for shot in range(1, skill["hits"] + 1):
            print(f"Shot {shot}:")
            report_hit(*player_hit(player, enemy, skill["mult"]))
            if enemy.hp <= 0:
                break
    elif kind == "stun":
        report_hit(*player_hit(player, enemy, skill["mult"]))
        chance = skill["chance"] * \
            (0.3 if enemy.boss else 1.0)   # bosses resist
        if enemy.hp > 0 and random.random() < chance:
            enemy.stunned = True
            print(f"{enemy.name} is stunned!")
        elif enemy.hp > 0 and enemy.boss:
            print(f"{enemy.name} resists the effect!")
    elif kind == "poison":
        report_hit(*player_hit(player, enemy, skill["mult"]))
        if enemy.hp > 0:
            enemy.poison_turns = 3
            enemy.poison_damage = max(1, int(player.attack * 0.35))
            print(f"{enemy.name} is poisoned!")
    elif kind == "buff_attack":
        player.buffs["attack"] = {"value": skill["value"], "turns": 4}
        print("Your Attack surges for 3 turns!")
    elif kind == "dodge":
        player.dodge_next = True
        print("You vanish in smoke - the next attack will miss!")
    elif kind == "instakill":
        if not enemy.boss and random.random() < skill["chance"]:
            enemy.hp = 0
            print("INSTANT KILL! The enemy collapses!")
        else:
            if enemy.boss:
                print("The boss is immune to instant death!")
            report_hit(*player_hit(player, enemy, skill["mult"]))
    return True


def heal_action(player):
    if player.hp >= player.max_hp:
        print("Your HP is already full.")
        return False
    if player.mana < HEAL_SPELL_COST:
        print(f"Not enough mana! Heal costs {HEAL_SPELL_COST}.")
        return False
    player.mana -= HEAL_SPELL_COST
    healed = min(int(player.max_hp * HEAL_SPELL_PERCENT),
                 player.max_hp - player.hp)
    player.hp += healed
    print(f"\nYou cast Heal and recover {healed} HP!")
    return True


def player_turn(player, enemy):
    """Run the player's turn. Returns "ran" if the player escaped, otherwise None."""
    while True:
        show_status(player, enemy)
        print()
        title("YOUR TURN")
        print("1 Attack\n2 Skills\n3 Heal\n4 Use Potion\n5 Defend\n6 Inventory\n7 View Stats\n8 Run")
        choice = ask_int("Choose action: ", 1, 8)
        if choice == 1:
            attack_action(player, enemy)
            return None
        if choice == 2:
            if skill_action(player, enemy):
                return None
        elif choice == 3:
            if heal_action(player):
                return None
        elif choice == 4:
            if use_potion_menu(player, in_battle=True):
                return None
        elif choice == 5:
            player.defending = True
            print("\nYou raise your guard! Incoming damage is halved.")
            return None
        elif choice == 6:
            inventory_menu(player, in_battle=True)
        elif choice == 7:
            print()
            print(player.stat_sheet())
            pause()
        elif choice == 8:
            if enemy.boss:
                print("You cannot run from a boss!")
            elif random.random() < 0.5:
                print("You escaped safely!")
                return "ran"
            else:
                print("You failed to escape!")
                return None


# ------------------------------------------------------------- enemy actions
def enemy_attack(player, enemy, mult):
    if player.dodge_next:
        player.dodge_next = False
        print("The attack misses you completely!")
        return
    raw = enemy.attack * mult - player.defense * DEFENSE_FACTOR
    damage = max(1, int(raw * random.uniform(0.9, 1.1)))
    crit_chance = max(0, enemy.crit_chance - player.crit_resist)
    if random.random() * 100 < crit_chance:
        damage = int(damage * 1.5)
        print(f"{enemy.name} lands a CRITICAL HIT!")
    if player.defending:
        damage = max(1, damage // 2)
        print("Your guard absorbs half the damage!")
    player.hp = max(0, player.hp - damage)
    print(f"{enemy.name} deals {damage} damage to you!")


def enemy_turn(player, enemy):
    enemy.turn_count += 1
    print()
    if enemy.stunned:
        enemy.stunned = False
        print(f"{enemy.name} is stunned and cannot move!")
        return
    if enemy.boss and enemy.turn_count % 3 == 0:
        print(f"{enemy.name} unleashes its SPECIAL ATTACK!")
        enemy_attack(player, enemy, 2.0)
        return
    low_hp = enemy.hp < enemy.max_hp * (0.5 if enemy.boss else 0.35)
    if low_hp and enemy.heals_left > 0 and random.random() < 0.3:
        enemy.heals_left -= 1
        amount = int(enemy.max_hp * (0.12 if enemy.boss else 0.15))
        enemy.hp = min(enemy.max_hp, enemy.hp + amount)
        print(f"{enemy.name} heals itself for {amount} HP!")
        return
    if random.random() < 0.25:
        skill = random.choice(enemy.skills)
        print(f"{enemy.name} uses {skill}!")
        enemy_attack(player, enemy, 1.4)
        return
    print(f"{enemy.name} attacks!")
    enemy_attack(player, enemy, 1.0)


# ------------------------------------------------------------------- rewards
def victory_rewards(player, enemy):
    print()
    title("VICTORY!")
    print(f"You defeated {enemy.name}!")
    if enemy.boss:
        player.bosses_defeated += 1     # raises the level cap before EXP is added
    player.enemies_defeated += 1
    player.gold += enemy.gold
    print(f"Gold +{enemy.gold}   EXP +{enemy.xp}")
    for message in player.add_exp(enemy.xp):
        print(message)
    loot = generate_loot(enemy.level, enemy.boss)
    if enemy.trophy:
        player.add_item("quest", enemy.trophy)
        print(f"Quest item obtained: {enemy.trophy}")
    for kind, name, qty in loot:
        player.add_item(kind, name, qty)
        print(f"Loot: {name}" + (f" x{qty}" if qty > 1 else ""))
    if enemy.boss and player.bosses_defeated < len(REGIONS):
        print(
            f"\nA new region is now open: {REGIONS[player.bosses_defeated]['name']}!")


# ---------------------------------------------------------------------- loop
def battle(player, enemy):
    """Fight until someone falls or the player escapes. Returns "win", "lose" or "ran"."""
    player.buffs.clear()
    player.defending = False
    player.dodge_next = False
    print()
    title(f"BATTLE: {enemy.name} (Lv {enemy.level})")
    result = None
    while result is None:
        if player_turn(player, enemy) == "ran":
            result = "ran"
            break
        if enemy.hp > 0 and enemy.poison_turns > 0:
            enemy.hp = max(0, enemy.hp - enemy.poison_damage)
            enemy.poison_turns -= 1
            print(
                f"\nPoison deals {enemy.poison_damage} damage to {enemy.name}!")
        if enemy.hp <= 0:
            result = "win"
            break
        enemy_turn(player, enemy)
        if player.hp <= 0:
            result = "lose"
            break
        # end of round: mana regeneration, buff countdown, guard drops
        player.mana = min(player.max_mana, player.mana +
                          max(2, int(player.max_mana * 0.05)))
        for stat in player.tick_buffs():
            print(f"Your {stat} buff wore off.")
        player.defending = False
    player.buffs.clear()
    player.defending = False
    player.dodge_next = False
    if result == "win":
        victory_rewards(player, enemy)
    elif result == "lose":
        print(f"\nYou were defeated by {enemy.name}...")
    return result


# ============================================================================
# GAME FLOW: menus, hub, game over, victory
# ============================================================================
INSTRUCTIONS = """
HOW TO PLAY
- Create a hero and fight monsters to earn EXP, gold and loot.
- Every 10 levels a boss blocks your path. You cannot level past the cap
  until you defeat it. Beating a boss unlocks the next region.
- Reach level 100 and defeat the Ancient Demon King to win!
- In battle: Attack, use class Skills (cost mana), Heal (20 mana),
  drink Potions, Defend (halves the next hit) or Run (not from bosses).
- Buy gear and potions at the Village shop; equip gear from your Inventory.
- The game auto-saves after every victory. You can also save manually.
- Tips: stock up on potions before a boss, and keep your gear up to date!
"""


# ----------------------------------------------------------------- new game
def new_game():
    name = ask_name("Enter Player Name: ")
    print("\nChoose Your Class")
    class_names = list(CLASSES)
    for number, cname in enumerate(class_names, 1):
        c = CLASSES[cname]
        print(f" {number}. {cname:<9} HP {c['hp']:<4} Mana {c['mana']:<4} ATK {c['attack']:<3} "
              f"DEF {c['defense']:<3} Crit {c['crit']}%")
        print(f"    {c['desc']}")
    choice = ask_int("> ", 1, len(class_names))
    player = Player(name, class_names[choice - 1])
    print(f"\n{player.name} the {player.class_name} sets out to save Eldoria!")
    return player


# --------------------------------------------------------------- hub helpers
def boss_available(player):
    return (player.bosses_defeated < len(BOSSES)
            and player.level >= BOSSES[player.bosses_defeated]["level"])


def show_location(player):
    print()
    line("-")
    print(f"Location: {REGIONS[player.region]['name']}    Gold: {player.gold}")
    print(f"{player.name} the {player.class_name}  Lv {player.level}/{player.level_cap()}  "
          f"EXP {player.exp}/{player.exp_to_next()}")
    print(f"HP {player.hp}/{player.max_hp} {bar(player.hp, player.max_hp)}  "
          f"Mana {player.mana}/{player.max_mana}")
    line("-")


def travel(player):
    print("\nWORLD MAP")
    for index, region in enumerate(REGIONS):
        unlocked = player.bosses_defeated >= index
        here = "  <- you are here" if index == player.region else ""
        status = "" if unlocked else f"  [LOCKED - defeat {BOSSES[index - 1]['name']}]"
        print(f" {index + 1}. {region['name']}{status}{here}")
    print(" 0. Back")
    choice = ask_int("Travel to: ", 0, len(REGIONS))
    if choice == 0:
        return
    if player.bosses_defeated < choice - 1:
        print("That region is still locked!")
        return
    player.region = choice - 1
    print(f"You travel to the {REGIONS[player.region]['name']}.")


def rest_at_inn(player):
    cost = 10 + 5 * player.level
    print(f"\nA night at the inn costs {cost} gold (full HP and Mana).")
    if player.hp >= player.max_hp and player.mana >= player.max_mana:
        print("You are already fully rested.")
    elif player.gold < cost:
        print("You cannot afford it.")
    elif ask_yes_no("Rest? (y/n): "):
        player.gold -= cost
        player.hp, player.mana = player.max_hp, player.max_mana
        print("You wake up refreshed!")


def fight_boss(player):
    boss = make_boss(player.bosses_defeated)
    print()
    title(f"BOSS: {boss.name}")
    print(
        f"Level {boss.level}   HP {boss.max_hp}   Attack {boss.attack}   Defense {boss.defense}")
    print("It heals, strikes critically and unleashes a special attack every 3 turns.")
    print("You cannot run from a boss. Be prepared!")
    if not ask_yes_no("Face the boss? (y/n): "):
        return None
    return battle(player, boss)


# ------------------------------------------------------------ game states
def game_over(player):
    """Show the Game Over menu. Returns the (possibly reloaded) player."""
    while True:
        print()
        title("GAME OVER")
        print("1 Retry\n2 Load Save\n3 Exit")
        choice = ask_int("> ", 1, 3)
        if choice == 1:
            lost = player.gold // 10
            player.gold -= lost
            player.region = 0
            player.hp, player.mana = player.max_hp, player.max_mana
            print(f"You wake up in the village, having lost {lost} gold.")
            return player
        if choice == 2:
            loaded = load_game()
            if loaded:
                return loaded
        else:
            raise GameExit()


def final_score(player):
    return (player.level * 100 + player.gold + player.bosses_defeated * 1000
            + player.enemies_defeated * 5 + len(player.rare_items) * 50)


def victory_screen(player):
    print()
    title("VICTORY - ELDORIA IS SAVED!")
    print("The Ancient Demon King falls. Peace returns to the realm!\n")
    print(f"Player Name:       {player.name} the {player.class_name}")
    print(f"Final Level:       {player.level}")
    print(f"Total Gold:        {player.gold}")
    print(f"Bosses Defeated:   {player.bosses_defeated}")
    print(f"Enemies Defeated:  {player.enemies_defeated}")
    print(f"Weapons Collected: {len(player.weapons_collected)}")
    print(f"Rare Items Found:  {len(player.rare_items)}")
    print(f"Total Play Time:   {format_time(player.total_play_time())}")
    print(f"Final Score:       {final_score(player)}")
    line()
    pause()


# --------------------------------------------------------------- main loop
def play(player):
    """Hub loop. Returns when the player quits or wins."""
    while True:
        show_location(player)
        options = [("Hunt Monsters", "hunt")]
        if boss_available(player):
            options.append(
                (f"Challenge Boss: {BOSSES[player.bosses_defeated]['name']}", "boss"))
        options.append(("Travel (World Map)", "travel"))
        if player.region == 0:
            options += [("Visit Shop", "shop"), ("Rest at Inn", "inn")]
        options += [("Inventory", "inventory"), ("View Stats", "stats"),
                    ("Save Game", "save"), ("Quit to Main Menu", "quit")]
        for number, (label, _) in enumerate(options, 1):
            print(f"{number}. {label}")
        action = options[ask_int("> ", 1, len(options)) - 1][1]

        result = None
        if action == "hunt":
            result = battle(player, make_enemy(player.level, player.region))
        elif action == "boss":
            result = fight_boss(player)
        elif action == "travel":
            travel(player)
        elif action == "shop":
            shop_menu(player)
        elif action == "inn":
            rest_at_inn(player)
        elif action == "inventory":
            inventory_menu(player, can_sell=(player.region == 0))
        elif action == "stats":
            print()
            print(player.stat_sheet())
            pause()
        elif action == "save":
            save_game(player)
        elif action == "quit":
            if ask_yes_no("Quit to main menu? Unsaved progress is lost (y/n): "):
                return

        if result == "win":
            if player.bosses_defeated >= len(BOSSES):
                save_game(player, quiet=True)
                victory_screen(player)
                return
            save_game(player, quiet=True)      # auto-save
            pause()
        elif result == "lose":
            player = game_over(player)


def main_menu():
    while True:
        print()
        title("LEGENDS OF THE FORGOTTEN REALM")
        print("1. New Game\n2. Continue\n3. Instructions\n4. Exit")
        choice = ask_int("> ", 1, 4)
        if choice == 1:
            play(new_game())
        elif choice == 2:
            player = load_game()
            if player:
                play(player)
        elif choice == 3:
            print(INSTRUCTIONS)
            pause()
        else:
            print("Farewell, hero!")
            return


# ============================================================================
# ENTRY POINT
# ============================================================================
def main():
    try:
        main_menu()
    except (GameExit, KeyboardInterrupt):
        print("\nFarewell, hero. Eldoria awaits your return!")


if __name__ == "__main__":
    main()
