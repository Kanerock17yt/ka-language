# ka.py
import sys
import os
import interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python ka.py <filename.ka>")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith('.ka'):
        print("Error: You can only run files with a '.ka' extension!")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    interpreter.run_code(lines)

if __name__ == "__main__":
    main()
