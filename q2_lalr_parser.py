
# ------------------------------------------
# Q2 – LALR Parsing Simulation (Simple Version)
# ------------------------------------------
# This code simulates parsing using:
# - LALR ACTION table
# - LALR GOTO table
# using the classic 3-column method:
# Stack | Input | Action
#
# This version is intentionally simple for student-level projects.

print("=== LALR PARSER (Simple Version) ===")

# ----------------------------
# 1) Read ACTION table
# ----------------------------
print("\nEnter LALR ACTION table.")
print("Format: state symbol action")
print("Example: 0 id shift3")
print("Type 'done' to finish.")

ACTION = {}
while True:
    line = input("> ")
    if line == "done":
        break

    st, sym, act = line.split()
    st = int(st)
    ACTION[(st, sym)] = act

# ----------------------------
# 2) Read GOTO table
# ----------------------------
print("\nEnter LALR GOTO table.")
print("Format: state NonTerminal nextState")
print("Example: 0 E 1")
print("Type 'done' to finish.")

GOTO = {}
while True:
    line = input("> ")
    if line == "done":
        break

    st, sym, to = line.split()
    st = int(st)
    to = int(to)
    GOTO[(st, sym)] = to
# ----------------------------
# 3) Read grammar rules (for output of reduce)
# ----------------------------
print("\nEnter grammar rules (rule_number: Head -> RHS)")
print("Example: 4: L -> id")
print("Type 'done' to finish.\n")

RULES = {}

while True:
    line = input("> ").strip()
    if line.lower() == "done":
        break
    if not line:
        continue

    num_part, rule_part = line.split(":", 1)
    num = int(num_part.strip())
    RULES[num] = rule_part.strip()

# ----------------------------
# 4) Read input string
# ----------------------------
print("\nEnter input tokens separated by spaces:")
tokens = input("> ").split()
tokens.append("$")  # end marker

# ----------------------------
# 4) Parsing loop
# ----------------------------
stack = [0]
pointer = 0

print("\n=== Parsing Trace (Stack | Input | Action | Output) ===")

while True:
    state = stack[-1]
    look = tokens[pointer]

    action = ACTION.get((state, look))


    if action is None:
        print("=> ERROR: No valid action. String rejected.")
        break

    if action.startswith("shift"):
        print(f"{stack} | {' '.join(tokens[pointer:])} | {action} | -")
        # Extract next state number: shift5 → 5
        next_state = int(action[5:])
        stack.append(next_state)
        pointer += 1

    elif action.startswith("reduce"):
     prod_num = int(action[6:])

    # get rule automatically instead of asking user
     rule = RULES[prod_num] 
    
    # Split head and RHS
     head, rhs = rule.split("->")
     head = head.strip()
     rhs = rhs.strip()

    # Count RHS symbols = pop_count
     rhs_symbols = rhs.split()
     pop_count = len(rhs_symbols)

    # printing
     output_msg = f"{head} → {rhs}"
     print(f"{stack} | {' '.join(tokens[pointer:])} | reduce{prod_num} | {output_msg}")

    # pop
     for _ in range(pop_count):
        stack.pop()

    # 
     top = stack[-1]
     goto_state = GOTO.get((top, head))

     if goto_state is None:
        print("=> ERROR: Missing GOTO. Rejected.")
        break

     stack.append(goto_state)

    elif action == "accept":
      print(f"{stack} | {' '.join(tokens[pointer:])} | accept | ACCEPT")
      print("=> ACCEPTED ✓")
      break
