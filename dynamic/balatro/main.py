from drafter import *
from dataclasses import dataclass, field
from bakery import assert_equal as bakery_assert_equal
import random


HAND_SIZE = 8
MAX_SELECT = 5
HANDS_PER_BLIND = 4
DISCARDS_PER_BLIND = 3
JOKER_PRICE = 4
MAX_JOKERS = 2

BLIND_TARGETS = {
    1: 300,
    2: 600,
    3: 1000,
}

HAND_ORDER = [
    "Straight Flush",
    "Four of a Kind",
    "Full House",
    "Flush",
    "Straight",
    "Three of a Kind",
    "Two Pair",
    "Pair",
    "High Card",
]

BASE_CHIPS_TABLE = {
    "High Card": 5,
    "Pair": 10,
    "Two Pair": 20,
    "Three of a Kind": 30,
    "Straight": 30,
    "Flush": 35,
    "Full House": 40,
    "Four of a Kind": 60,
    "Straight Flush": 100,
}

BASE_MULTIPLIER_TABLE = {
    "High Card": 1,
    "Pair": 2,
    "Two Pair": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Flush": 4,
    "Full House": 4,
    "Four of a Kind": 7,
    "Straight Flush": 8,
}

JOKER_DESCRIPTIONS = {
    "Chip Booster": "Add 25 chips to every played hand.",
    "Mult Booster": "Add 4 to the multiplier of every played hand.",
    "Pair Pal": "Add 5 multiplier for Pair, Two Pair, Full House, or Four of a Kind.",
    "Flush Fan": "Add 6 multiplier for Flush or Straight Flush.",
    "Frugal Joker": "Add 10 chips for every discard remaining when played.",
    "Odd Todd": "Add 5 chips for each scoring Ace, 3, 5, 7, or 9.",
}

SHOP_BY_BLIND = {
    1: ["Chip Booster", "Pair Pal", "Flush Fan"],
    2: ["Mult Booster", "Frugal Joker", "Odd Todd"],
}


set_website_title("Mini-Balatro")

add_website_css("body", """
    margin: 0;
    font-family: Trebuchet MS, Verdana, sans-serif;
    background: radial-gradient(circle at 20% 20%, #23414a 0%, #102329 55%, #08161b 100%);
    color: #fff8ea;
""")

add_website_css(".screen", """
    max-width: 1100px;
    margin: 0 auto;
    padding: 28px 22px 40px;
""")

add_website_css(".hero", """
    background: linear-gradient(125deg, #1f5a62, #438a6a 55%, #d3a44a);
    color: #fff7e6;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.3);
    margin-bottom: 16px;
""")

add_website_css(".panel", """
    background: rgba(8, 16, 22, 0.72);
    border: 1px solid rgba(232, 214, 174, 0.22);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    color: #fff3d8;
""")

add_website_css(".hud-grid", """
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 10px;
""")

add_website_css(".stat", """
    background: rgba(249, 237, 203, 0.09);
    border-radius: 12px;
    padding: 9px;
""")

add_website_css(".stat-label", """
    display: block;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #f7e8bd;
    font-weight: 700;
""")

add_website_css(".stat-value", """
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff4d3;
""")

add_website_css(".message", """
    background: rgba(91, 141, 126, 0.2);
    border: 1px solid rgba(165, 211, 166, 0.35);
    color: #f2ffe8;
    border-radius: 10px;
    padding: 10px;
""")

add_website_css(".message.bad", """
    background: rgba(127, 39, 39, 0.25);
    border-color: rgba(255, 159, 159, 0.45);
    color: #ffd9d9;
""")

add_website_css(".card-grid", """
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
    gap: 10px;
""")

add_website_css(".playing-card", """
    background: linear-gradient(160deg, #fffaf0, #f4ead8);
    border: 2px solid #d8bf90;
    border-radius: 14px;
    min-height: 168px;
    color: #202020;
    padding: 10px;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
""")

add_website_css(".playing-card.empty", """
    background: linear-gradient(160deg, #2f3e47, #25323a);
    border-color: #6f7f88;
    color: #eef5fa;
""")

add_website_css(".card-red", """
    color: #b11f2a;
""")

add_website_css(".card-black", """
    color: #1f1f1f;
""")

add_website_css(".card-main", """
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
""")

add_website_css(".card-name", """
    display: block;
    margin: 7px 0 14px;
    font-size: 0.87rem;
    color: inherit;
""")

add_website_css(".card-select", """
    display: flex;
    align-items: center;
    gap: 7px;
    margin-top: auto;
""")

add_website_css(".actions", """
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
""")

add_website_css("button", """
    border: none;
    border-radius: 999px;
    padding: 10px 16px;
    background: linear-gradient(120deg, #f2bb4a, #e59036);
    color: #2f1e07;
    font-weight: 700;
    cursor: pointer;
""")

add_website_css("table", """
    width: 100%;
    border-collapse: collapse;
    background: rgba(10, 18, 24, 0.88);
    color: #fff1d2;
""")

add_website_css("td, th", """
    padding: 8px;
    border-bottom: 1px solid rgba(240, 219, 169, 0.2);
    text-align: left;
    font-size: 0.95rem;
""")

add_website_css("th", """
    color: #ffe6a8;
    font-weight: 700;
""")

add_website_css(".shop-buttons", """
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
""")


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str


@dataclass
class ScoreResult:
    category: str = ""
    base_chips: int = 0
    card_chips: int = 0
    joker_chips: int = 0
    base_multiplier: int = 0
    joker_multiplier: int = 0
    total: int = 0


@dataclass
class State:
    deck: list[Card] = field(default_factory=list)
    hand: list[Card] = field(default_factory=list)
    blind: int = 1
    target: int = BLIND_TARGETS[1]
    blind_score: int = 0
    hands_remaining: int = HANDS_PER_BLIND
    discards_remaining: int = DISCARDS_PER_BLIND
    money: int = 0
    jokers: list[str] = field(default_factory=list)
    phase: str = "welcome"
    message: str = ""
    last_result: ScoreResult | None = None
    purchased_this_shop: bool = False


def assert_equal(expected, actual) -> bool:
    return bakery_assert_equal(actual, expected)


# -------------------------
# Deck and card helpers
# -------------------------

def make_deck() -> list[Card]:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(rank, suit))
    return deck


def shuffled_deck() -> list[Card]:
    deck = make_deck()
    random.shuffle(deck)
    return deck


def draw_until_full(deck: list[Card], hand: list[Card], desired_size: int) -> None:
    while len(hand) < desired_size and deck:
        hand.append(deck.pop())


def card_chip_value(card: Card) -> int:
    if card.rank == "Ace":
        return 11
    if card.rank in ["King", "Queen", "Jack", "10"]:
        return 10
    return int(card.rank)


def card_name(card: Card) -> str:
    return f"{card.rank} of {card.suit}"


def suit_symbol(suit: str) -> str:
    if suit == "Clubs":
        return "♣"
    if suit == "Diamonds":
        return "♦"
    if suit == "Hearts":
        return "♥"
    return "♠"


def short_rank(rank: str) -> str:
    if rank == "Jack":
        return "J"
    if rank == "Queen":
        return "Q"
    if rank == "King":
        return "K"
    if rank == "Ace":
        return "A"
    return rank


def card_face(card: Card) -> str:
    return f"{short_rank(card.rank)}{suit_symbol(card.suit)}"


def card_color_class(card: Card) -> str:
    if card.suit in ["Hearts", "Diamonds"]:
        return "card-red"
    return "card-black"


def rank_number(card: Card) -> int:
    if card.rank == "Ace":
        return 14
    if card.rank == "King":
        return 13
    if card.rank == "Queen":
        return 12
    if card.rank == "Jack":
        return 11
    return int(card.rank)


def rank_counts(cards: list[Card]) -> list[int]:
    counts_by_rank = {}
    for card in cards:
        if card.rank in counts_by_rank:
            counts_by_rank[card.rank] += 1
        else:
            counts_by_rank[card.rank] = 1
    counts = []
    for rank in counts_by_rank:
        counts.append(counts_by_rank[rank])
    counts.sort(reverse=True)
    return counts


def count_by_rank(cards: list[Card]) -> dict[str, int]:
    counts = {}
    for card in cards:
        if card.rank in counts:
            counts[card.rank] += 1
        else:
            counts[card.rank] = 1
    return counts


def is_flush(cards: list[Card]) -> bool:
    if len(cards) != 5:
        return False
    if not cards:
        return False
    first_suit = cards[0].suit
    for card in cards:
        if card.suit != first_suit:
            return False
    return True


def is_straight(cards: list[Card]) -> bool:
    if len(cards) != 5:
        return False
    values = []
    for card in cards:
        values.append(rank_number(card))
    values.sort()
    for i in range(1, len(values)):
        if values[i] != values[i - 1] + 1:
            return False
    return True


def classify_hand(cards: list[Card]) -> str:
    counts = rank_counts(cards)
    flush = is_flush(cards)
    straight = is_straight(cards)

    if straight and flush:
        return "Straight Flush"
    if counts == [4, 1] or counts == [4]:
        return "Four of a Kind"
    if counts == [3, 2]:
        return "Full House"
    if flush:
        return "Flush"
    if straight:
        return "Straight"
    if counts == [3, 1, 1] or counts == [3, 1] or counts == [3]:
        return "Three of a Kind"
    if counts == [2, 2, 1] or counts == [2, 2]:
        return "Two Pair"
    if counts == [2, 1, 1, 1] or counts == [2, 1, 1] or counts == [2, 1] or counts == [2]:
        return "Pair"
    return "High Card"


def scoring_cards(cards: list[Card], category: str) -> list[Card]:
    if category in ["Straight", "Flush", "Full House", "Straight Flush"]:
        return cards[:]
    rank_count = count_by_rank(cards)
    if category == "High Card":
        highest = cards[0]
        for card in cards:
            if rank_number(card) > rank_number(highest):
                highest = card
        return [highest]
    if category == "Four of a Kind":
        result = []
        for card in cards:
            if rank_count[card.rank] == 4:
                result.append(card)
        return result
    if category == "Three of a Kind":
        result = []
        for card in cards:
            if rank_count[card.rank] == 3:
                result.append(card)
        return result
    if category == "Two Pair":
        result = []
        for card in cards:
            if rank_count[card.rank] == 2:
                result.append(card)
        return result
    if category == "Pair":
        result = []
        for card in cards:
            if rank_count[card.rank] == 2:
                result.append(card)
        return result
    return cards[:]


# -------------------------
# Scoring helpers
# -------------------------

def base_chips(category: str) -> int:
    return BASE_CHIPS_TABLE[category]


def base_multiplier(category: str) -> int:
    return BASE_MULTIPLIER_TABLE[category]


def joker_bonus(cards_that_score: list[Card], category: str, jokers: list[str], discards_remaining: int) -> tuple[int, int]:
    joker_chips = 0
    joker_multiplier = 0

    if "Chip Booster" in jokers:
        joker_chips += 25
    if "Mult Booster" in jokers:
        joker_multiplier += 4
    if "Pair Pal" in jokers and category in ["Pair", "Two Pair", "Full House", "Four of a Kind"]:
        joker_multiplier += 5
    if "Flush Fan" in jokers and category in ["Flush", "Straight Flush"]:
        joker_multiplier += 6
    if "Frugal Joker" in jokers:
        joker_chips += 10 * discards_remaining
    if "Odd Todd" in jokers:
        odd_ranks = ["Ace", "3", "5", "7", "9"]
        odd_count = 0
        for card in cards_that_score:
            if card.rank in odd_ranks:
                odd_count += 1
        joker_chips += 5 * odd_count

    return (joker_chips, joker_multiplier)


def score_hand(cards: list[Card], jokers: list[str], discards_remaining: int) -> ScoreResult:
    category = classify_hand(cards)
    cards_that_score = scoring_cards(cards, category)
    card_chips = 0
    for card in cards_that_score:
        card_chips += card_chip_value(card)

    base_chip_value = base_chips(category)
    base_mult_value = base_multiplier(category)
    joker_chips, joker_mult = joker_bonus(cards_that_score, category, jokers, discards_remaining)

    total_chips = base_chip_value + card_chips + joker_chips
    total_multiplier = base_mult_value + joker_mult
    total = total_chips * total_multiplier

    return ScoreResult(
        category=category,
        base_chips=base_chip_value,
        card_chips=card_chips,
        joker_chips=joker_chips,
        base_multiplier=base_mult_value,
        joker_multiplier=joker_mult,
        total=total,
    )


# -------------------------
# Selection and list helpers
# -------------------------

def selected_indices(selections: list[bool]) -> list[int]:
    result = []
    for i in range(len(selections)):
        if selections[i]:
            result.append(i)
    return result


def cards_at_indices(cards: list[Card], indices: list[int]) -> list[Card]:
    result = []
    for i in indices:
        if 0 <= i < len(cards):
            result.append(cards[i])
    return result


def remove_at_indices(cards: list[Card], indices: list[int]) -> None:
    sorted_indices = indices[:]
    sorted_indices.sort(reverse=True)
    for i in sorted_indices:
        if 0 <= i < len(cards):
            cards.pop(i)


# -------------------------
# Game state helpers
# -------------------------

def target_for_blind(blind: int) -> int:
    return BLIND_TARGETS[blind]


def begin_blind(state: State) -> None:
    state.target = target_for_blind(state.blind)
    state.blind_score = 0
    state.hands_remaining = HANDS_PER_BLIND
    state.discards_remaining = DISCARDS_PER_BLIND
    state.deck = shuffled_deck()
    state.hand = []
    draw_until_full(state.deck, state.hand, HAND_SIZE)
    state.phase = "game"
    state.message = f"Blind {state.blind} started. Reach {state.target} points."


def blind_reward(state: State) -> int:
    return 3 + state.hands_remaining


def check_round_status(state: State) -> str:
    if state.blind_score >= state.target:
        if state.blind == 3:
            return "won"
        return "shop"
    if state.hands_remaining <= 0:
        return "lost"
    return "playing"


def shop_inventory_for_blind(blind: int, owned_jokers: list[str]) -> list[str]:
    offered = SHOP_BY_BLIND.get(blind, [])
    result = []
    for joker in offered:
        if joker not in owned_jokers:
            result.append(joker)
    return result


def game_or_phase_page(state: State) -> Page:
    if state.phase == "welcome":
        return index(state)
    if state.phase == "game":
        return game_page(state)
    if state.phase == "shop":
        return shop_page(state)
    return end_page(state)


def parse_selection(select_0: bool, select_1: bool, select_2: bool, select_3: bool,
                    select_4: bool, select_5: bool, select_6: bool, select_7: bool) -> list[bool]:
    return [select_0, select_1, select_2, select_3, select_4, select_5, select_6, select_7]


# -------------------------
# UI builders
# -------------------------

def jokers_text(jokers: list[str]) -> str:
    if not jokers:
        return "None"
    return ", ".join(jokers)


def stat_box(label: str, value: str) -> PageContent:
    return Div(
        Span(label, classes=["stat-label"]),
        Span(value, classes=["stat-value"]),
        classes=["stat"]
    )


def status_message(message: str) -> PageContent:
    classes = ["message"]
    lower = message.lower()
    if "no " in lower or "not " in lower or "lost" in lower:
        classes.append("bad")
    return Div(message, classes=classes)


def card_slot_components(state: State) -> list[PageContent]:
    cards: list[PageContent] = []
    for i in range(HAND_SIZE):
        if i < len(state.hand):
            card = state.hand[i]
            cards.append(Div(
                Span(card_face(card), classes=["card-main"]),
                Span(card_name(card), classes=["card-name"]),
                Div(CheckBox(f"select_{i}"), Span("Select"), classes=["card-select"]),
                classes=["playing-card", card_color_class(card)]
            ))
        else:
            cards.append(Div(
                Span("--", classes=["card-main"]),
                Span("Empty Slot", classes=["card-name"]),
                classes=["playing-card", "empty"]
            ))
    return [Header("Your Hand", 2), Div(*cards, classes=["card-grid"])]


def score_table(result: ScoreResult | None) -> PageContent:
    if result is None:
        return "No hand scored yet."
    rows = [
        ["Field", "Value"],
        ["Hand Category", result.category],
        ["Base Chips", str(result.base_chips)],
        ["Card Chips", str(result.card_chips)],
        ["Joker Chip Bonus", str(result.joker_chips)],
        ["Base Multiplier", str(result.base_multiplier)],
        ["Joker Multiplier Bonus", str(result.joker_multiplier)],
        ["Final Score", str(result.total)],
    ]
    return Table(rows)


def shop_table(available_jokers: list[str]) -> PageContent:
    rows = [["Joker", "Effect", "Price"]]
    for joker in available_jokers:
        rows.append([joker, JOKER_DESCRIPTIONS[joker], f"${JOKER_PRICE}"])
    if len(rows) == 1:
        rows.append(["None", "No new Jokers available", "-"])
    return Table(rows)


# -------------------------
# Routes
# -------------------------


@route
def index(state: State) -> Page:
    if state.phase != "welcome":
        return game_or_phase_page(state)

    return Page(state, [
        Div(
            Div(
                Header("Mini-Balatro", 1),
                "Beat three blinds by playing and discarding smart poker hands.",
                LineBreak(),
                "Hand Score = Chips x Multiplier",
                classes=["hero"]
            ),
            Div(
                Header("How This Run Works", 2),
                "Each blind gives 4 playable hands and 3 discards.",
                LineBreak(),
                "Defeat Blind 1 and 2 to visit the shop and buy one Joker each stop.",
                LineBreak(),
                "Own up to two Jokers total and push through Blind 3 to win.",
                LineBreak(),
                Div(Button("Start New Run", "start_game"), classes=["actions"]),
                classes=["panel"]
            ),
            classes=["screen"]
        )
    ])


@route
def start_game(state: State) -> Page:
    state.blind = 1
    state.money = 0
    state.jokers = []
    state.last_result = None
    state.purchased_this_shop = False
    begin_blind(state)
    return game_page(state)


@route
def game_page(state: State) -> Page:
    if state.phase != "game":
        return game_or_phase_page(state)

    return Page(state, [
        Div(
            Div(
                Header("Mini-Balatro", 1),
                f"Blind {state.blind} in progress",
                classes=["hero"]
            ),
            Div(
                Header("Round Stats", 2),
                Div(
                    stat_box("Blind", str(state.blind)),
                    stat_box("Target", str(state.target)),
                    stat_box("Score", str(state.blind_score)),
                    stat_box("Hands", str(state.hands_remaining)),
                    stat_box("Discards", str(state.discards_remaining)),
                    stat_box("Money", f"${state.money}"),
                    classes=["hud-grid"]
                ),
                LineBreak(),
                Div(f"Jokers: {jokers_text(state.jokers)}"),
                classes=["panel"]
            ),
            Div(
                Header("Status", 2),
                status_message(state.message),
                classes=["panel"]
            ),
            Div(*card_slot_components(state), classes=["panel"]),
            Div(
                Button("Play Selected Cards", "play_selected"),
                Button("Discard Selected Cards", "discard_selected"),
                classes=["actions", "panel"]
            ),
            Div(
                Header("Previous Scoring Breakdown", 2),
                score_table(state.last_result),
                classes=["panel"]
            ),
            classes=["screen"]
        )
    ])


def validate_selection_count(indices: list[int]) -> str:
    count = len(indices)
    if count == 0:
        return "Select at least one card."
    if count > MAX_SELECT:
        return "You can select at most five cards."
    return ""


@route
def play_selected(state: State,
                  select_0: bool = False,
                  select_1: bool = False,
                  select_2: bool = False,
                  select_3: bool = False,
                  select_4: bool = False,
                  select_5: bool = False,
                  select_6: bool = False,
                  select_7: bool = False) -> Page:
    if state.phase != "game":
        return game_or_phase_page(state)

    if state.hands_remaining <= 0:
        state.message = "No playable hands remaining."
        return game_page(state)

    selections = parse_selection(select_0, select_1, select_2, select_3, select_4, select_5, select_6, select_7)
    indices = selected_indices(selections)
    error = validate_selection_count(indices)
    if error:
        state.message = error
        return game_page(state)

    chosen_cards = cards_at_indices(state.hand, indices)
    result = score_hand(chosen_cards, state.jokers, state.discards_remaining)
    state.last_result = result
    state.blind_score += result.total
    state.hands_remaining -= 1
    remove_at_indices(state.hand, indices)
    draw_until_full(state.deck, state.hand, HAND_SIZE)

    status = check_round_status(state)
    if status == "playing":
        state.message = f"Played {result.category} for {result.total} points."
        return game_page(state)

    if status == "lost":
        state.phase = "lost"
        state.message = "You ran out of hands before reaching the target."
        return end_page(state)

    reward = blind_reward(state)
    state.money += reward
    state.message = f"Blind {state.blind} cleared. Earned ${reward}."
    if state.blind == 3:
        state.phase = "won"
        return end_page(state)

    state.phase = "shop"
    state.purchased_this_shop = False
    return shop_page(state)


@route
def discard_selected(state: State,
                     select_0: bool = False,
                     select_1: bool = False,
                     select_2: bool = False,
                     select_3: bool = False,
                     select_4: bool = False,
                     select_5: bool = False,
                     select_6: bool = False,
                     select_7: bool = False) -> Page:
    if state.phase != "game":
        return game_or_phase_page(state)

    if state.discards_remaining <= 0:
        state.message = "No discards remaining."
        return game_page(state)

    selections = parse_selection(select_0, select_1, select_2, select_3, select_4, select_5, select_6, select_7)
    indices = selected_indices(selections)
    error = validate_selection_count(indices)
    if error:
        state.message = error
        return game_page(state)

    remove_at_indices(state.hand, indices)
    state.discards_remaining -= 1
    draw_until_full(state.deck, state.hand, HAND_SIZE)
    state.message = "Cards discarded."
    return game_page(state)


@route
def shop_page(state: State) -> Page:
    if state.phase != "shop":
        return game_or_phase_page(state)

    available = shop_inventory_for_blind(state.blind, state.jokers)
    buy_buttons: list[PageContent] = []
    for joker in available:
        buy_buttons.append(Button(
            f"Buy {joker}",
            "buy_joker",
            arguments=[Argument("joker_name", joker)]
        ))

    return Page(state, [
        Div(
            Div(
                Header("Joker Shop", 1),
                "Buy one Joker or skip to the next blind.",
                classes=["hero"]
            ),
            Div(
                Div(
                    stat_box("Money", f"${state.money}"),
                    stat_box("Owned Jokers", str(len(state.jokers))),
                    classes=["hud-grid"]
                ),
                LineBreak(),
                Div(f"Jokers: {jokers_text(state.jokers)}"),
                classes=["panel"]
            ),
            Div(status_message(state.message), classes=["panel"]),
            Div(
                Header("Available Jokers", 2),
                shop_table(available),
                Div(*buy_buttons, Button("Skip Shop", "skip_shop"), classes=["shop-buttons"]),
                classes=["panel"]
            ),
            classes=["screen"]
        )
    ])


@route
def buy_joker(state: State, joker_name: str) -> Page:
    if state.phase != "shop":
        return game_or_phase_page(state)

    available = shop_inventory_for_blind(state.blind, state.jokers)

    if state.purchased_this_shop:
        state.message = "You already purchased one Joker in this shop."
        return shop_page(state)
    if len(state.jokers) >= MAX_JOKERS:
        state.message = "You already have the maximum number of Jokers."
        return shop_page(state)
    if joker_name in state.jokers:
        state.message = "You already own that Joker."
        return shop_page(state)
    if joker_name not in available:
        state.message = "That Joker is not available in this shop."
        return shop_page(state)
    if state.money < JOKER_PRICE:
        state.message = "Not enough money to buy that Joker."
        return shop_page(state)

    state.money -= JOKER_PRICE
    state.jokers.append(joker_name)
    state.purchased_this_shop = True
    state.message = f"Bought {joker_name} for ${JOKER_PRICE}."
    return shop_page(state)


@route
def skip_shop(state: State) -> Page:
    if state.phase != "shop":
        return game_or_phase_page(state)

    state.blind += 1
    state.purchased_this_shop = False
    begin_blind(state)
    return game_page(state)


@route
def end_page(state: State) -> Page:
    if state.phase == "won":
        title = "You Win!"
    else:
        title = "Run Lost"

    return Page(state, [
        Div(
            Div(
                Header(title, 1),
                "Run Summary",
                classes=["hero"]
            ),
            Div(
                Div(
                    stat_box("Final Blind", str(state.blind)),
                    stat_box("Final Money", f"${state.money}"),
                    stat_box("Jokers Owned", str(len(state.jokers))),
                    classes=["hud-grid"]
                ),
                LineBreak(),
                Div(f"Jokers: {jokers_text(state.jokers)}"),
                LineBreak(),
                status_message(state.message),
                LineBreak(),
                Div(Button("Start New Run", "start_game"), classes=["actions"]),
                classes=["panel"]
            ),
            classes=["screen"]
        )
    ])


# -------------------------
# Tests
# -------------------------

def test_make_deck_size() -> None:
    deck = make_deck()
    assert_equal(52, len(deck))


def test_make_deck_suits_and_uniqueness() -> None:
    deck = make_deck()
    suits = []
    seen = []
    rank_counts_map = {}
    for card in deck:
        if card.suit not in suits:
            suits.append(card.suit)
        identity = (card.rank, card.suit)
        seen.append(identity)
        if card.rank in rank_counts_map:
            rank_counts_map[card.rank] += 1
        else:
            rank_counts_map[card.rank] = 1
    assert_equal(4, len(suits))
    assert_equal(52, len(set(seen)))
    assert_equal(4, rank_counts_map["Ace"])
    assert_equal(4, rank_counts_map["7"])


def test_card_chip_values() -> None:
    assert_equal(2, card_chip_value(Card("2", "Clubs")))
    assert_equal(9, card_chip_value(Card("9", "Hearts")))
    assert_equal(10, card_chip_value(Card("Jack", "Spades")))
    assert_equal(10, card_chip_value(Card("Queen", "Spades")))
    assert_equal(10, card_chip_value(Card("King", "Spades")))
    assert_equal(11, card_chip_value(Card("Ace", "Diamonds")))


def test_classify_each_category() -> None:
    assert_equal("High Card", classify_hand([
        Card("2", "Clubs"), Card("5", "Diamonds"), Card("9", "Hearts"), Card("Jack", "Spades")
    ]))
    assert_equal("Pair", classify_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("King", "Hearts"), Card("4", "Spades")
    ]))
    assert_equal("Two Pair", classify_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("King", "Hearts"), Card("King", "Spades"), Card("2", "Spades")
    ]))
    assert_equal("Three of a Kind", classify_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("8", "Hearts"), Card("King", "Spades"), Card("2", "Spades")
    ]))
    assert_equal("Straight", classify_hand([
        Card("7", "Clubs"), Card("8", "Diamonds"), Card("9", "Hearts"), Card("10", "Spades"), Card("Jack", "Spades")
    ]))
    assert_equal("Flush", classify_hand([
        Card("2", "Hearts"), Card("5", "Hearts"), Card("9", "Hearts"), Card("Jack", "Hearts"), Card("King", "Hearts")
    ]))
    assert_equal("Full House", classify_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("8", "Hearts"), Card("King", "Spades"), Card("King", "Hearts")
    ]))
    assert_equal("Four of a Kind", classify_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("8", "Hearts"), Card("8", "Spades"), Card("King", "Hearts")
    ]))
    assert_equal("Straight Flush", classify_hand([
        Card("10", "Hearts"), Card("Jack", "Hearts"), Card("Queen", "Hearts"), Card("King", "Hearts"), Card("Ace", "Hearts")
    ]))


def test_straight_and_flush_boundaries() -> None:
    assert_equal(False, is_straight([
        Card("7", "Clubs"), Card("8", "Diamonds"), Card("9", "Hearts"), Card("10", "Spades")
    ]))
    assert_equal(False, is_flush([
        Card("2", "Hearts"), Card("5", "Hearts"), Card("9", "Hearts"), Card("Jack", "Hearts")
    ]))
    assert_equal(True, is_straight([
        Card("10", "Clubs"), Card("Jack", "Diamonds"), Card("Queen", "Hearts"), Card("King", "Spades"), Card("Ace", "Hearts")
    ]))
    assert_equal(False, is_straight([
        Card("Queen", "Clubs"), Card("King", "Diamonds"), Card("Ace", "Hearts"), Card("2", "Spades"), Card("3", "Hearts")
    ]))
    assert_equal("Full House", classify_hand([
        Card("3", "Clubs"), Card("3", "Diamonds"), Card("3", "Hearts"), Card("9", "Spades"), Card("9", "Hearts")
    ]))
    assert_equal("Straight Flush", classify_hand([
        Card("6", "Spades"), Card("7", "Spades"), Card("8", "Spades"), Card("9", "Spades"), Card("10", "Spades")
    ]))


def test_scoring_without_jokers() -> None:
    result = score_hand([
        Card("8", "Clubs"), Card("8", "Diamonds"), Card("King", "Hearts"), Card("4", "Spades")
    ], [], 3)
    assert_equal("Pair", result.category)
    assert_equal(10, result.base_chips)
    assert_equal(16, result.card_chips)
    assert_equal(2, result.base_multiplier)
    assert_equal(52, result.total)


def test_scoring_with_jokers() -> None:
    pair_cards = [Card("8", "Clubs"), Card("8", "Diamonds"), Card("King", "Hearts"), Card("4", "Spades")]
    flush_cards = [Card("2", "Hearts"), Card("5", "Hearts"), Card("9", "Hearts"), Card("Jack", "Hearts"), Card("King", "Hearts")]

    chip_boost = score_hand(pair_cards, ["Chip Booster"], 3)
    assert_equal(102, chip_boost.total)

    mult_boost = score_hand(pair_cards, ["Mult Booster"], 3)
    assert_equal(156, mult_boost.total)

    pair_pal_yes = score_hand(pair_cards, ["Pair Pal"], 3)
    assert_equal(182, pair_pal_yes.total)

    pair_pal_no = score_hand(flush_cards, ["Pair Pal"], 3)
    assert_equal(284, pair_pal_no.total)

    flush_fan = score_hand(flush_cards, ["Flush Fan"], 3)
    assert_equal((35 + 36) * (4 + 6), flush_fan.total)

    frugal_3 = score_hand(pair_cards, ["Frugal Joker"], 3)
    frugal_1 = score_hand(pair_cards, ["Frugal Joker"], 1)
    assert_equal(112, frugal_3.total)
    assert_equal(72, frugal_1.total)

    odd_none = score_hand(pair_cards, ["Odd Todd"], 3)
    odd_one = score_hand([
        Card("9", "Clubs"), Card("9", "Diamonds"), Card("King", "Hearts"), Card("4", "Spades")
    ], ["Odd Todd"], 3)
    odd_many = score_hand([
        Card("Ace", "Clubs"), Card("Ace", "Diamonds"), Card("3", "Hearts"), Card("3", "Spades"), Card("King", "Hearts")
    ], ["Odd Todd"], 3)
    assert_equal(52, odd_none.total)
    assert_equal(76, odd_one.total)
    assert_equal(136, odd_many.total)

    two_jokers = score_hand(pair_cards, ["Chip Booster", "Pair Pal"], 3)
    assert_equal(357, two_jokers.total)


def test_selection_and_removal_helpers() -> None:
    assert_equal([], selected_indices([False, False, False]))
    assert_equal([1], selected_indices([False, True, False]))
    assert_equal([0, 1, 2, 3, 4], selected_indices([True, True, True, True, True]))
    assert_equal("You can select at most five cards.", validate_selection_count([0, 1, 2, 3, 4, 5]))

    cards = [
        Card("2", "Clubs"), Card("3", "Clubs"), Card("4", "Clubs"),
        Card("5", "Clubs"), Card("6", "Clubs")
    ]
    remove_at_indices(cards, [1, 3])
    assert_equal([Card("2", "Clubs"), Card("4", "Clubs"), Card("6", "Clubs")], cards)


def test_state_transitions() -> None:
    play_state = State(
        deck=[Card("9", "Hearts")],
        hand=[Card("8", "Clubs"), Card("8", "Diamonds"), Card("King", "Hearts")],
        blind=1,
        target=300,
        blind_score=0,
        hands_remaining=4,
        discards_remaining=3,
        money=0,
        jokers=[],
        phase="game",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    play_selected(play_state, True, True, False, False, False, False, False, False)
    assert_equal(3, play_state.hands_remaining)

    invalid_play_state = State(
        deck=[],
        hand=[Card("2", "Clubs")],
        blind=1,
        target=300,
        blind_score=0,
        hands_remaining=4,
        discards_remaining=3,
        money=0,
        jokers=[],
        phase="game",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    play_selected(invalid_play_state, False, False, False, False, False, False, False, False)
    assert_equal(4, invalid_play_state.hands_remaining)
    assert_equal(0, invalid_play_state.blind_score)

    discard_state = State(
        deck=[Card("9", "Hearts")],
        hand=[Card("8", "Clubs"), Card("8", "Diamonds")],
        blind=1,
        target=300,
        blind_score=0,
        hands_remaining=4,
        discards_remaining=3,
        money=0,
        jokers=[],
        phase="game",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    discard_selected(discard_state, True, False, False, False, False, False, False, False)
    assert_equal(2, discard_state.discards_remaining)
    assert_equal(0, discard_state.blind_score)
    assert_equal(4, discard_state.hands_remaining)

    reward_state = State(
        deck=[],
        hand=[Card("Ace", "Clubs")],
        blind=1,
        target=10,
        blind_score=0,
        hands_remaining=4,
        discards_remaining=3,
        money=0,
        jokers=[],
        phase="game",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    play_selected(reward_state, True, False, False, False, False, False, False, False)
    assert_equal("shop", reward_state.phase)
    assert_equal(6, reward_state.money)

    buy_state = State(
        deck=[],
        hand=[],
        blind=1,
        target=300,
        blind_score=300,
        hands_remaining=2,
        discards_remaining=3,
        money=6,
        jokers=[],
        phase="shop",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    buy_joker(buy_state, "Chip Booster")
    assert_equal(2, buy_state.money)
    assert_equal(["Chip Booster"], buy_state.jokers)

    poor_state = State(
        deck=[],
        hand=[],
        blind=1,
        target=300,
        blind_score=300,
        hands_remaining=2,
        discards_remaining=3,
        money=3,
        jokers=[],
        phase="shop",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    buy_joker(poor_state, "Chip Booster")
    assert_equal([], poor_state.jokers)
    assert_equal(3, poor_state.money)

    win_state = State(
        deck=[],
        hand=[Card("Ace", "Hearts")],
        blind=3,
        target=5,
        blind_score=0,
        hands_remaining=1,
        discards_remaining=2,
        money=0,
        jokers=[],
        phase="game",
        message="",
        last_result=None,
        purchased_this_shop=False,
    )
    play_selected(win_state, True, False, False, False, False, False, False, False)
    assert_equal("won", win_state.phase)


# Run tests before starting the server.
test_make_deck_size()
test_make_deck_suits_and_uniqueness()
test_card_chip_values()
test_classify_each_category()
test_straight_and_flush_boundaries()
test_scoring_without_jokers()
test_scoring_with_jokers()
test_selection_and_removal_helpers()
test_state_transitions()


start_server(State())