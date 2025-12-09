
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

def format_stack(stk):
    return "[" + ", ".join(str(s) for s in stk) + "]"

def print_row(stack, tokens, pointer, action, output):
    stack_str = format_stack(stack)
    input_str = " ".join(tokens[pointer:])
    # تنسيق أعمدة ثابتة العرض
    print(f"{stack_str:<18} | {input_str:<20} | {action:<10} | {output}")

stack = [0]
pointer = 0

print("\n=== Parsing Trace (Stack | Input | Action | Output) ===")
print(f"{'Stack':<18} | {'Input':<20} | {'Action':<10} | Output")
print("-" * 70)

while True:
    state = stack[-1]
    look = tokens[pointer]

    action = ACTION.get((state, look))

    if action is None:
        print_row(stack, tokens, pointer, "ERROR", "No valid action")
        print("=> ERROR: String rejected.")
        break

    # -------- SHIFT --------
    if action.startswith("shift"):
        # مثال: shift5 → 5
        next_state = int(action[5:])
        print_row(stack, tokens, pointer, action, "-")
        stack.append(next_state)
        pointer += 1

    # -------- REDUCE --------
    elif action.startswith("reduce"):
        prod_num = int(action[6:])      # reduce3 → 3

        # نجيب القاعدة من RULES
        rule = RULES[prod_num]          # مثلاً: "L -> id"
        head, rhs = rule.split("->")
        head = head.strip()
        rhs = rhs.strip()

        rhs_symbols = rhs.split() if rhs else []
        pop_count = len(rhs_symbols)

        output_msg = f"{head} -> {rhs if rhs else 'ε'}"
        print_row(stack, tokens, pointer, f"reduce{prod_num}", output_msg)

        # pop عدد رموز RHS
        for _ in range(pop_count):
            if len(stack) > 1:
                stack.pop()

        top = stack[-1]
        goto_state = GOTO.get((top, head))
        if goto_state is None:
            print_row(stack, tokens, pointer, "ERROR", f"Missing GOTO({top}, {head})")
            print("=> ERROR: String rejected.")
            break

        stack.append(goto_state)

    # -------- ACCEPT --------
    elif action == "accept":
        print_row(stack, tokens, pointer, "accept", "ACCEPT")
        print("=> ACCEPTED ✓")
        break

    # -------- UNKNOWN --------
    else:
        print_row(stack, tokens, pointer, action, "Unknown action")
        print("=> ERROR: String rejected.")
        break
