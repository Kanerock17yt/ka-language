# interpreter.py
import re
import sys
import time

def evaluate_condition(condition):
    """Safely evaluates a math or logical condition like '5 > 3' or '2 == 2'."""
    try:
        # Returns True or False safely using Python's evaluation engine
        return bool(eval(condition, {"__builtins__": None}, {}))
    except Exception:
        print(f"Logic Error: Could not evaluate condition '{condition}'")
        return False

def find_matching_bracket(lines, start_index):
    """Finds the line index of the closing bracket '}' that matches the opening block."""
    bracket_count = 0
    for i in range(start_index, len(lines)):
        line = lines[i].strip()
        if '{' in line:
            bracket_count += line.count('{')
        if '}' in line:
            bracket_count -= line.count('}')
            if bracket_count == 0:
                return i
    return -1

def run_code(lines):
    # Strip whitespace from lines while maintaining the list structure
    lines = [line.strip() for line in lines]
    line_pointer = 0

    # Loop through the program using a pointer index so we can jump around
    while line_pointer < len(lines):
        line = lines[line_pointer]

        # 1. Skip empty lines, comments, or standalone brackets
        if not line or line.startswith("//") or line == "}":
            line_pointer += 1
            continue

        # 2. Built-in command: exit()
        if line == "exit()":
            sys.exit(0)

        # 3. Built-in command: wait(seconds)
        wait_match = re.match(r'^wait\((\d+)\)$', line)
        if wait_match:
            time.sleep(int(wait_match.group(1)))
            line_pointer += 1
            continue

        # 4. Built-in command: ask("Prompt Text")
        ask_match = re.match(r'^ask\("(.*)"\)$', line)
        if ask_match:
            input(ask_match.group(1))
            line_pointer += 1
            continue

        # 5. Core command: say("Text")
        string_match = re.match(r'^say\("(.*)"\)$', line)
        if string_match:
            print(string_match.group(1))
            line_pointer += 1
            continue

        # 6. Core command: say(math)
        math_match = re.match(r'^say\(([^"].*)\)$', line)
        if math_match:
            try:
                print(eval(math_match.group(1), {"__builtins__": None}, {}))
            except Exception:
                print(f"Error: Invalid math expression '{math_match.group(1)}'")
            line_pointer += 1
            continue

        # 7. LOGIC: while condition {
        while_match = re.match(r'^while\s+(.+)\s*\{$', line)
        if while_match:
            condition = while_match.group(1)
            closing_index = find_matching_bracket(lines, line_pointer)
            
            if closing_index == -1:
                print("Syntax Error: Missing closing bracket '}' for while loop")
                sys.exit(1)
            
            # If the condition is true, run the next line. 
            # If false, jump completely past the closing bracket.
            if evaluate_condition(condition):
                line_pointer += 1
            else:
                line_pointer = closing_index + 1
            continue

        # 8. LOGIC: if condition {
        if_match = re.match(r'^if\s+(.+)\s*\{$', line)
        if if_match:
            condition = if_match.group(1)
            closing_index = find_matching_bracket(lines, line_pointer)
            
            if closing_index == -1:
                print("Syntax Error: Missing closing bracket '}' for if statement")
                sys.exit(1)
                
            if evaluate_condition(condition):
                line_pointer += 1  # Enter the block
            else:
                line_pointer = closing_index + 1  # Skip the block
            continue

        print(f"Syntax Error: Unknown command '{line}'")
        line_pointer += 1
