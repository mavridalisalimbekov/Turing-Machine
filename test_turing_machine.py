import unittest
from turing_machine import busy_beaver_2, binary_increment, TuringMachine


class TestExamples(unittest.TestCase):
    def test_binary_increment_1011(self):
        tm = binary_increment()
        self.assertEqual(tm.run(), "accept")
        self.assertEqual(tm.tape_string(), "1100")  # 11 + 1 = 12

    def test_binary_increment_overflow(self):
        # 111 + 1 = 1000 (prepend path)
        tm = binary_increment()
        tm.tape = {i: ch for i, ch in enumerate("111")}
        self.assertEqual(tm.run(), "accept")
        self.assertEqual(tm.tape_string(), "1000")

    def test_busy_beaver_2(self):
        tm = busy_beaver_2()
        self.assertEqual(tm.run(100), "accept")
        self.assertEqual(tm.tape_string(), "1111")  # 4 ones
        self.assertEqual(tm.steps, 6)

    def test_reject_and_timeout(self):
        tm = TuringMachine({}, "1", start_state="q0")
        self.assertEqual(tm.run(), "reject")  # no transitions

        loop = {("q0", "_"): ("_", None, "q0")}
        tm = TuringMachine(loop, "", start_state="q0")
        self.assertEqual(tm.run(max_steps=10), "timeout")
        self.assertEqual(tm.steps, 10)

    def test_invalid_move(self):
        tm = TuringMachine({("q0", "_"): ("_", "X", "q0")}, "")
        with self.assertRaises(ValueError):
            tm.step()


if __name__ == "__main__":
    unittest.main()
