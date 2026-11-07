#!/usr/bin/env python3
"""Single-file Turing Machine simulator. No dependencies.

Transition format: {(state, symbol): (write, move, next_state)}
  move: 'L' | 'R' | None (stay)
"""
from __future__ import annotations

import argparse
import sys

BLANK = "_"
LEFT, RIGHT = "L", "R"


class TuringMachine:
    """Deterministic single-tape Turing Machine.

    Tape is infinite in both directions (dict-based). Default blank '_'.
    """

    def __init__(
        self,
        transitions: dict,
        input_string: str = "",
        *,
        blank: str = BLANK,
        start_state: str = "q0",
        accept_states: frozenset | set = frozenset({"q_accept"}),
        reject_state: str = "q_reject",
    ):
        self.transitions = transitions
        self.blank = blank
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.reject_state = reject_state
        self.state = start_state
        self.head = 0
        self.tape = {i: ch for i, ch in enumerate(input_string)}
        self.steps = 0
        self.history: list[str] = [self._render()]

    # --- core ---
    def _sym(self) -> str:
        return self.tape.get(self.head, self.blank)

    def _set(self, sym: str):
        if sym == self.blank:
            self.tape.pop(self.head, None)
        else:
            self.tape[self.head] = sym

    _DIR = {LEFT: -1, RIGHT: 1}

    def step(self) -> bool:
        """One step. Returns False when halted (no transition / accept / reject)."""
        if self.state in self.accept_states or self.state == self.reject_state:
            return False
        key = (self.state, self._sym())
        if key not in self.transitions:
            return False  # undefined transition = halt/reject-by-absence
        write, move, next_state = self.transitions[key]
        self._set(write)
        if move in self._DIR:
            self.head += self._DIR[move]
        elif move not in (None,):
            raise ValueError(f"invalid move {move!r}, expected 'L', 'R', or None (stay)")
        self.state = next_state
        self.steps += 1
        self.history.append(self._render())
        return self.state not in self.accept_states and self.state != self.reject_state

    def run(self, max_steps: int = 10_000) -> str:
        """Run to halt. Returns 'accept' | 'reject' | 'timeout'."""
        while self.steps < max_steps:
            if not self.step():
                break
        if self.state in self.accept_states:
            return "accept"
        if self.state == self.reject_state or (self.state, self._sym()) not in self.transitions:
            return "reject"
        return "timeout"

    # --- view ---
    def _render(self, window: int = 30) -> str:
        if not self.tape:
            return f"{self.state:>9} [_{''!r} ]"
        lo = min(min(self.tape), self.head) - 2
        hi = max(max(self.tape), self.head) + 2
        cells, marker = [], []
        for i in range(lo, hi + 1):
            cells.append(self.tape.get(i, self.blank))
            marker.append("^" if i == self.head else " ")
        return f"{self.state:>9} {''.join(cells)} \n{'':>9} {''.join(marker)}"

    def tape_string(self) -> str:
        """Trimmed tape contents (blanks trimmed), '' if all blank."""
        if not self.tape:
            return ""
        lo, hi = min(self.tape), max(self.tape)
        return "".join(self.tape.get(i, self.blank) for i in range(lo, hi + 1))

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"TuringMachine(state={self.state!r}, head={self.head}, steps={self.steps}, tape={self.tape_string()!r})"


# ---------------------------------------------------------------- examples

def binary_increment() -> TuringMachine:
    """Add 1 to a binary number, e.g. '1011' -> '1100'. Blank '_'."""
    # q0: scan right to end; q1: carry-propagate left
    t = {
        ("q0", "0"): ("0", "R", "q0"),
        ("q0", "1"): ("1", "R", "q0"),
        ("q0", BLANK): (BLANK, "L", "q1"),
        ("q1", "1"): ("0", "L", "q1"),          # carry: 1->0 keep going
        ("q1", "0"): ("1", None, "q_accept"),   # done
        ("q1", BLANK): ("1", None, "q_accept"), # overflow: prepend 1
    }
    return TuringMachine(t, "1011")


def busy_beaver_2() -> TuringMachine:
    """Classic 2-state busy beaver (4 ones, 6 steps)."""
    t = {
        ("A", "0"): ("1", "R", "B"),
        ("A", "1"): ("1", "L", "B"),
        ("B", "0"): ("1", "L", "A"),
        ("B", "1"): ("1", "R", "H"),
    }
    return TuringMachine(t, "", blank="0", start_state="A", accept_states=frozenset({"H"}), reject_state="H")


EXAMPLES = {"binary_increment": binary_increment, "busy_beaver_2": busy_beaver_2}


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Turing Machine simulator")
    p.add_argument("--example", choices=list(EXAMPLES), default="binary_increment")
    p.add_argument("--input", default=None, help="input tape (overrides example input)")
    p.add_argument("--max-steps", type=int, default=10_000)
    p.add_argument("--trace", action="store_true", help="print every step")
    args = p.parse_args(argv)

    tm = EXAMPLES[args.example]()
    if args.input is not None:
        tm.tape = {i: ch for i, ch in enumerate(args.input)}
        tm.history = [tm._render()]

    result = tm.run(args.max_steps)
    if args.trace:
        print("\n".join(tm.history))
    print(f"result: {result}  steps: {tm.steps}  state: {tm.state}")
    print(f"tape:   {tm.tape_string()!r}")
    return 0 if result == "accept" else 1


if __name__ == "__main__":
    sys.exit(main())
