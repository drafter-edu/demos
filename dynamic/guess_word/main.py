from bakery import assert_equal
from string import ascii_lowercase
from drafter import *
from random import choice
from dataclasses import dataclass


LEVELS = ["heat", "dogs", "jazz"]

set_website_title("Guess the Word!")


def choose_word(level: int) -> str:
    return LEVELS[level]


def reveal_letter(secret: str, guesses: list[str], index: int) -> str:
    if secret[index] in guesses:
        return secret[index]
    return "_"


assert_equal(reveal_letter("heat", ["h"], 0), "h")
assert_equal(reveal_letter("heat", ["h"], 1), "_")
assert_equal(reveal_letter("heat", ["h"], 2), "_")
assert_equal(reveal_letter("heat", ["h"], 3), "_")
assert_equal(reveal_letter("heat", ["x"], 0), "_")
assert_equal(reveal_letter("heat", ["t"], 3), "t")
assert_equal(reveal_letter("heat", ["r", "x", "q"], 0), "_")
assert_equal(reveal_letter("heat", ["r", "x", "h"], 0), "h")
assert_equal(reveal_letter("heat", ["r", "x", "h"], 1), "_")


def reveal(secret: str, guesses: list[str]) -> str:
    c0 = reveal_letter(secret, guesses, 0)
    c1 = reveal_letter(secret, guesses, 1)
    c2 = reveal_letter(secret, guesses, 2)
    c3 = reveal_letter(secret, guesses, 3)
    return c0 + c1 + c2 + c3


assert_equal(reveal("heat", ["h"]), "h___")
assert_equal(reveal("heat", ["a"]), "__a_")
assert_equal(reveal("heat", ["t"]), "___t")
assert_equal(reveal("heat", ["e", "a"]), "_ea_")
assert_equal(reveal("heat", ["x"]), "____")
assert_equal(reveal("heat", ["h", "e", "a", "t"]), "heat")
assert_equal(reveal("heat", ["h", "e", "a", "r"]), "hea_")


def is_win(secret: str, guesses: list[str]) -> bool:
    if secret[0] not in guesses:
        return False
    if secret[1] not in guesses:
        return False
    if secret[2] not in guesses:
        return False
    if secret[3] not in guesses:
        return False
    return True


assert_equal(is_win("heat", ["h"]), False)
assert_equal(is_win("heat", ["h", "e"]), False)
assert_equal(is_win("heat", ["h", "e", "a"]), False)
assert_equal(is_win("heat", ["h", "e", "a", "t"]), True)
assert_equal(is_win("heat", ["t", "e", "a", "h"]), True)
assert_equal(is_win("heat", ["t", "e", "a", "r", "h"]), True)


def is_loss(wrong: int) -> bool:
    return wrong >= 6


assert_equal(is_loss(0), False)
assert_equal(is_loss(5), False)
assert_equal(is_loss(6), True)
assert_equal(is_loss(7), True)


def in_secret(secret: str, character: str) -> bool:
    return character in secret


assert_equal(in_secret("heat", "h"), True)
assert_equal(in_secret("heat", "a"), True)
assert_equal(in_secret("heat", "t"), True)
assert_equal(in_secret("heat", "e"), True)
assert_equal(in_secret("heat", "x"), False)


def format_guess(guess: str) -> str:
    return guess.lower().strip()


assert_equal(format_guess(" H "), "h")
assert_equal(format_guess("      A "), "a")
assert_equal(format_guess("t"), "t")


def check_if_valid_guess(guess: str, guesses: list[str]) -> bool:
    return len(guess) == 1 and guess in ascii_lowercase and guess not in guesses


assert_equal(check_if_valid_guess("h", []), True)
assert_equal(check_if_valid_guess("H", []), False)
assert_equal(check_if_valid_guess("1", []), False)
assert_equal(check_if_valid_guess("", []), False)
assert_equal(check_if_valid_guess("hello", []), False)
assert_equal(check_if_valid_guess("oH", []), False)
assert_equal(check_if_valid_guess("!", []), False)
assert_equal(check_if_valid_guess("h", ["h"]), False)
assert_equal(check_if_valid_guess("h", ["x", "y", "h"]), False)
assert_equal(check_if_valid_guess("z", ["x", "y", "h"]), True)


def is_game_over(level: int) -> bool:
    return level > len(LEVELS) - 1


#### Drafter UI


@dataclass
class State:
    secret: str
    guesses: list[str]
    wrong: int
    level: int
    score: int


@route
def index(state: State) -> Page:
    return Page(
        state,
        [
            Header("Guess the Word"),
            Div("Level: ", str(state.level)),
            Button("Start", "next_level"),
        ],
    )


@route
def next_level(state: State) -> Page:
    state.level += 1
    state.secret = choose_word(state.level)
    state.guesses = []
    state.wrong = 0
    if is_game_over(state.level):
        return game_end(state)
    return play_level(state)


@route
def play_level(state: State) -> Page:
    so_far = reveal(state.secret, state.guesses)
    return Page(
        state,
        [
            Header("Level " + str(state.level)),
            Div("Word: ", so_far),
            "Guesses so far: ",
            BulletedList(state.guesses),
            "Guess a letter:",
            TextBox("guess"),
            Button("Submit", "submit_guess"),
        ],
    )


@route
def submit_guess(state: State, guess: str) -> Page:
    guess = format_guess(guess)
    if not check_if_valid_guess(guess, state.guesses):
        return play_level(state)

    state.guesses.append(guess)
    if not in_secret(state.secret, guess):
        state.wrong += 1

    if is_win(state.secret, state.guesses):
        state.score += state.level
        return win_level(state)

    if is_loss(state.wrong):
        return lose_level(state)

    return play_level(state)


@route
def win_level(state: State) -> Page:
    return Page(
        state,
        [
            Header("You Win!"),
            Div("The word was: ", state.secret),
            Button("Play Again", "next_level"),
        ],
    )


@route
def lose_level(state: State) -> Page:
    return Page(
        state,
        [
            Header("You Lost!"),
            Div("The word was: ", state.secret),
            Button("Play Again", "next_level"),
        ],
    )


@route
def game_end(state: State) -> Page:
    return Page(
        state,
        [
            Header("Game Over"),
            Div("The word was: ", state.secret),
            Div("Your final score is: ", state.score),
            Button("Play Again", "next_level"),
        ],
    )


start_server(State("", [], 0, -1, 0))

