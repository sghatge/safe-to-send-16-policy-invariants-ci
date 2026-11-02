import json
import unittest

from invariants import check

with open("invariants.json", encoding="utf-8") as fh:
    INV = json.load(fh)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


class InvariantsTest(unittest.TestCase):
    def test_current_policy_holds(self):
        self.assertEqual(check(load("policies/current.json"), INV), [])

    def test_speedup_pr_breaks_three(self):
        broken = check(load("policies/proposed_speedup.json"), INV)
        self.assertEqual([b.split(":")[0] for b in broken], ["INV-04", "INV-05", "INV-07"])

    def test_empty_policy_blocks_everything_but_breaks_human_rules(self):
        broken = {b.split(":")[0] for b in check({"tools": {}}, INV)}
        self.assertEqual(broken, {"INV-04", "INV-05"})


if __name__ == "__main__":
    unittest.main()
