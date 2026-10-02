# LALR Parser Generator

A Python command-line implementation of two core LALR(1) parsing tasks: constructing LALR tables from user-provided LR(1) states and parsing tables, and simulating input parsing using ACTION and GOTO tables.

## Features

- Groups LR(1) states that share identical LR(0) core strings.
- Assigns new state numbers to merged groups.
- Remaps shift targets and GOTO transitions to the new state numbers.
- Detects conflicting ACTION entries introduced during state merging.
- Reports shift/shift, shift/reduce, reduce/shift, and reduce/reduce conflicts.
- Simulates shift, reduce, accept, and error actions.
- Displays the stack, remaining input, action, and applied production during parsing.

## Project Files

- `q1_lalr_table.py` — reads LR(1) state cores and existing ACTION/GOTO entries, merges compatible states, detects conflicts, and prints the resulting LALR tables.
- `q2_lalr_parser.py` — reads an LALR ACTION table, GOTO table, grammar productions, and tokenized input string, then simulates the parsing process.

## Requirements

- Python 3
- No external packages are required.

## How to Run

Clone the repository and enter its directory:

```bash
git clone https://github.com/r26th/lalr-parser-generator.git
cd lalr-parser-generator
```

Run the table-construction program:

```bash
python q1_lalr_table.py
```

Run the parsing simulation:

```bash
python q2_lalr_parser.py
```

Both programs request their data interactively in the terminal and display the expected input format before each section.

## Input Notes

- LR(0) core strings must be entered consistently because states are grouped by exact string equality.
- ACTION entries for the table-construction program use values such as `s3` for a shift.
- Parser actions use values such as `shift3`, `reduce4`, or `accept`.
- Grammar symbols and input tokens should be separated by spaces when prompted.

## Project Scope

The project converts user-provided LR(1) states and parsing tables into LALR tables, detects conflicts introduced during state merging, and simulates the parsing of tokenized input strings.
