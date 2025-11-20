
# ------------------------------------------
# Q1 – LALR Table Construction (Simple Version)
# ------------------------------------------
# This code merges LR(1) states into LALR states
# by grouping states with the same LR(0) core.
# It then builds LALR ACTION/GOTO tables.
# This version is intentionally simple and manual.

print("=== LALR TABLE GENERATOR (Simple Version) ===")

# ----------------------------
# 1) Read LR(1) states (only cores)
# ----------------------------
num_states = int(input("Enter number of LR(1) states: "))

lr_states = {}
for i in range(num_states):
    print(f"\nState {i}:")
    core = input("Enter LR(0) core (example: E->E+T , T->F ): ")
    lr_states[i] = core.strip()

# ----------------------------
# 2) Merge states with same core
# ----------------------------
merged = {}
for s, core in lr_states.items():
    if core not in merged:
        merged[core] = []
    merged[core].append(s)

print("\n=== LALR MERGED STATES ===")
mapping = {}
new_number = 0

for core, group in merged.items():
    print(f"\nNew State {new_number}: from old states {group}")
    for old in group:
        mapping[old] = new_number
    new_number += 1

# ----------------------------
# 3) Read LR ACTION table
# ----------------------------
print("\nEnter LR ACTION table.")
print("Format: state symbol action")
print("Example: 0 id shift3")
print("Type 'done' to finish.")

old_action = {}
while True:
    line = input("> ")
    if line == "done":
        break
    st, sym, act = line.split()
    st = int(st)
    old_action[(st, sym)] = act

# ----------------------------
# 4) Read LR GOTO table
# ----------------------------
print("\nEnter LR GOTO table.")
print("Format: state NonTerminal nextState")
print("Example: 0 E 1")
print("Type 'done' to finish.")

old_goto = {}
while True:
    line = input("> ")
    if line == "done":
        break
    st, sym, to = line.split()
    st = int(st)
    to = int(to)
    old_goto[(st, sym)] = to

# ----------------------------
# 5) Build LALR ACTION/GOTO by mapping old → new
# ----------------------------
new_action = {}
new_goto = {}

# ACTION
for (st, sym), act in old_action.items():
    ns = mapping[st]
    if (ns, sym) not in new_action:
        new_action[(ns, sym)] = act
    else:
        if new_action[(ns, sym)] != act:
            print("\n=== CONFLICT DETECTED ===")
            print(f"Conflict at state {ns} on symbol {sym}")
            print("Grammar is NOT LALR.")
            exit()

# GOTO
for (st, sym), to in old_goto.items():
    ns = mapping[st]
    new_to = mapping[to]
    new_goto[(ns, sym)] = new_to

# ----------------------------
# 6) Print LALR tables
# ----------------------------
print("\n=== FINAL LALR ACTION TABLE ===")
for (s, sym), act in sorted(new_action.items()):
    print(f"State {s} , on {sym} => {act}")

print("\n=== FINAL LALR GOTO TABLE ===")
for (s, sym), to in sorted(new_goto.items()):
    print(f"State {s} , goto {sym} => {to}")

print("\nNo conflicts found.")
print("Grammar is LALR ✓")
