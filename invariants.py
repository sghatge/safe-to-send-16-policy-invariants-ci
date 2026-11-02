"""Policy regression tests for AI agents: things that must stay true whatever the policy says.

Write your non-negotiables once ("an agent can never run a SQL write", "a 200k send always
needs two humans"). CI checks every policy change against them and fails the pull request,
naming the invariant that broke. Standard library only.
"""
import json
import sys

HUMAN = {"needs_approval", "needs_approval_x2"}


def matches(rule, call):
    for key, expected in rule.get("when", {}).items():
        if key.endswith("_over"):
            if not call.get(key[:-5], 0) > expected:
                return False
        elif call.get(key) != expected:
            return False
    return True


def evaluate(policy, call):
    for rule in policy.get("tools", {}).get(call["tool"], []):
        if matches(rule, call):
            return rule["decision"]
    return "block"


def check(policy, invariants):
    broken = []
    for inv in invariants:
        got = evaluate(policy, inv["call"])
        allowed = set(inv["expect_one_of"])
        if got not in allowed:
            broken.append(f"{inv['id']}: {inv['rule']} (policy now says '{got}')")
    return broken


def main(policy_path, inv_path="invariants.json"):
    with open(policy_path, encoding="utf-8") as fh:
        policy = json.load(fh)
    with open(inv_path, encoding="utf-8") as fh:
        invariants = json.load(fh)
    broken = check(policy, invariants)
    print(f"{policy_path}: {len(invariants) - len(broken)}/{len(invariants)} invariants hold")
    for b in broken:
        print(f"  BROKEN {b}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]) if len(sys.argv) > 1 else main("policies/current.json"))
