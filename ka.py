# ka.py
import sys
import os
import re
import time
import requests

# CLI metadata & flags (moved from file-bottom comment request)
VERSION = "1.3"

# Global variables for the KA runtime
variables = {}

def interpolate_string(text):
    """Replace {variable} placeholders inside string literals."""
    def replace(match):
        key = match.group(1)
        return str(variables.get(key, ""))
    return re.sub(r'\{([^}]+)\}', replace, text)


def parse_value(value):
    """Resolve a raw KA value into a Python value.
    Supports string literals, variables, and expressions.
    """
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return interpolate_string(value[1:-1])
    if value in variables:
        return variables[value]
    try:
        return eval(value, {"__builtins__": None}, variables)
    except Exception:
        return value

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
        if arg in ("-t", "--test"):
            print("Running test script...")
            if os.path.exists("test.ka"):
                with open("test.ka", 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                run_code(lines)
            else:
                print("Error: test.ka not found.")
            sys.exit(0)
        if arg in ("-c", "--credits"):
            print(f"KA Language {VERSION} by Kane_rock17yt")
            sys.exit(0)

cli_handle_flags()

def evaluate_condition(condition):
    """Safely evaluates a math or logical condition like '5 > 3' or '2 == 2'."""
    try:
        return bool(eval(condition, {"__builtins__": None}, variables))
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

    while line_pointer < len(lines):
        line = lines[line_pointer]

        if not line or line.startswith("//") or line == "}":
            line_pointer += 1
            continue

        exit_match = re.match(r'^exit\(\s*(\d+)\s*\)$', line)
        if exit_match:
            exit_code = int(exit_match.group(1))
            if exit_code == 1:
                print("Succesfuly Executed Task!")
            else:
                print("Failed to execute task.")
            sys.exit(0)

        if line == "exit()":
            print("Failed to execute task.")
            sys.exit(0)

        wait_match = re.match(r'^wait\((\d+)\)$', line)
        if wait_match:
            time.sleep(int(wait_match.group(1)))
            line_pointer += 1
            continue

        ask_match = re.match(r'^ask\("(.*)"\)$', line)
        if ask_match:
            input(interpolate_string(ask_match.group(1)))
            line_pointer += 1
            continue

        set_match = re.match(r'^set\("(.*?)",\s*(.+)\)$', line)
        if set_match:
            var_name = set_match.group(1)
            raw_value = set_match.group(2)
            variables[var_name] = parse_value(raw_value)
            line_pointer += 1
            continue

        string_match = re.match(r'^say\("(.*)"\)$', line)
        if string_match:
            print(interpolate_string(string_match.group(1)))
            line_pointer += 1
            continue

        say_match = re.match(r'^say\((.+)\)$', line)
        if say_match:
            expression = say_match.group(1)
            try:
                result = parse_value(expression)
                print(result)
            except Exception:
                print(f"Error: Invalid expression '{expression}'")
            line_pointer += 1
            continue

        while_match = re.match(r'^while\s+(.+)\s*\{$', line)
        if while_match:
            condition = while_match.group(1)
            closing_index = find_matching_bracket(lines, line_pointer)
            if closing_index == -1:
                print("Syntax Error: Missing closing bracket '}' for while loop")
                sys.exit(1)
            if evaluate_condition(condition):
                line_pointer += 1
            else:
                line_pointer = closing_index + 1
            continue

        if_match = re.match(r'^if\s+(.+)\s*\{$', line)
        if if_match:
            condition = if_match.group(1)
            closing_index = find_matching_bracket(lines, line_pointer)
            if closing_index == -1:
                print("Syntax Error: Missing closing bracket '}' for if statement")
                sys.exit(1)
            if evaluate_condition(condition):
                line_pointer += 1
            else:
                line_pointer = closing_index + 1
            continue

        webhook_match = re.match(r'^webhook\((.+),\s*(.+)\)$', line)
        if webhook_match:
            url = parse_value(webhook_match.group(1))
            content = parse_value(webhook_match.group(2))
            try:
                requests.post(url, json={"content": content})
                print("Webhook: Message sent successfully!")
            except Exception as e:
                print(f"Webhook Error: Could not send message. {e}")
            line_pointer += 1
            continue

        input_match = re.match(r'^input_to\("(.*?)",\s*"(.*)"\)$', line)
        if input_match:
            var_name = input_match.group(1)
            prompt = interpolate_string(input_match.group(2))
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