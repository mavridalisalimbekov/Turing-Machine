# Turing-Machine

Single-file deterministic Turing Machine simulator in Python. No dependencies.

## Usage

```bash
python turing_machine.py                            # binary_increment (1011 -> 1100)
python turing_machine.py --example busy_beaver_2    # 2-state busy beaver (4 ones)
python turing_machine.py --input 111 --trace        # custom input, full trace
python turing_machine.py --max-steps 100 --trace
python -m unittest -v                               # run tests
```

Example output:

```
result: accept  steps: 7  state: q_accept
tape:   '1100'
```

## Library

```python
from turing_machine import TuringMachine

tm = TuringMachine(
    transitions={("q0", "_"): ("1", "R", "q0")},  # (state, read) -> (write, move, next)
    input_string="",
    start_state="q0",
    accept_states={"q_accept"},
)
tm.run()
tm.tape_string()   # trimmed tape
tm.steps           # step count
tm.history         # rendered trace frames
```

Moves: `L`, `R`, or `None` (stay). Tape infinite both directions; blank `_`.
Undefined transition = reject. `run()` returns `accept` / `reject` / `timeout`.

## Examples

- `binary_increment`: adds 1 to binary input (`1011` -> `1100`).
- `busy_beaver_2`: classic 2-state busy beaver, writes 4 ones in 6 steps.
