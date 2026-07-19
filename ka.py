# ka.py
import sys
import os
import re
import time
import requests

# CLI metadata & flags (moved from file-bottom comment request)
VERSION = "1.0"

# Add this global dictionary for variables
variables = {}

def run_help():
    print("Usage:")
    print("  python ka.py <filename.ka>")
    print("  python ka.py -v | --version")
    print("  python ka.py -h | --help")
    print("Run Test:")
    print("  run.bat")

def cli_handle_flags():
    # Check for common flags before normal execution
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-v", "--version"):
            print(f"KA {VERSION}")
            sys.exit(0)
        if arg in ("-h", "--help"):
            run_help()
            sys.exit(0)

cli_handle_flags()

def evaluate_condition(condition):
    """Safely evaluates a math or logical condition like '5 > 3' or '2 == 2'."""
    try:
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
        
        # 9. webhook("URL_or_Var", "Message_or_Var")
        webhook_match = re.match(r'^webhook\("(.*?)",\s*"(.*)"\)$', line)
        if webhook_match:
            # Helper function to check if the input is a variable, otherwise return as literal
            def resolve(value):
                return variables.get(value, value)

            url = resolve(webhook_match.group(1))
            content = resolve(webhook_match.group(2))
            
            try:
                requests.post(url, json={"content": content})
                print("Webhook: Message sent successfully!")
            except Exception as e:
                print(f"Webhook Error: Could not send message. {e}")
            line_pointer += 1
            continue
        
        # 10. input_to("Variable_Name", "Prompt Text")
        input_match = re.match(r'^input_to\("(.*?)",\s*"(.*)"\)$', line)
        if input_match:
            var_name = input_match.group(1)
            prompt = input_match.group(2)
            # Store the user's input into the variables dictionary
            variables[var_name] = input(prompt)
            line_pointer += 1
            continue

        print(f"Syntax Error: Unknown command '{line}'")
        line_pointer += 1

def main():
    if len(sys.argv) < 2:
        run_help()
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith('.ka'):
        print("Error: You can only run files with a '.ka' extension!")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    print(f"Running {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    run_code(lines)

if __name__ == "__main__":
    main()