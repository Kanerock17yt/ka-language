<pre>
KKKKKKKKK    KKKKKKK               AAA               
K:::::::K    K:::::K              A:::A              
K:::::::K    K:::::K             A:::::A             
K:::::::K   K::::::K            A:::::::A            
KK::::::K  K:::::KKK           A:::::::::A           
  K:::::K K:::::K             A:::::A:::::A          
  K::::::K:::::K             A:::::A A:::::A         
  K:::::::::::K             A:::::A   A:::::A        
  K:::::::::::K            A:::::A     A:::::A       
  K::::::K:::::K          A:::::AAAAAAAAA:::::A      
  K:::::K K:::::K        A:::::::::::::::::::::A     
KK::::::K  K:::::KKK    A:::::AAAAAAAAAAAAA:::::A    
K:::::::K   K::::::K   A:::::A             A:::::A   
K:::::::K    K:::::K  A:::::A               A:::::A  
K:::::::K    K:::::K A:::::A                 A:::::A 
KKKKKKKKK    KKKKKKKAAAAAAA                   AAAAAAA
</pre>

# Ka v1.3
ka is a coding language created by **Kane_rock17yt**. You can download the newest version from the releases tab.

# IMPORTANT
THIS CODING LANGUAGE IS IN DEVELOPMENT. EXPECT BUGS AND ISSUES.

## How to use
Using the ka language is simple:
1. Ensure Python is installed.
2. Open a terminal.
3. Verify installation by typing `python -V` (Capital V).
4. Navigate to the folder where `ka.py` is located.
5. Execute your code by running `python ka.py yourfile.ka`.

## Commands & Syntax

| Command | Description | Example |
| :--- | :--- | :--- |
| `say("text")` | Prints text to the console with variable interpolation. | `say("Hello {name}")` |
| `say(expr)` | Evaluates and prints a math or variable expression. | `say(5 + 5)` |
| `set("var", value)` | Sets a variable to a string, number, or expression. | `set("count", 3)` |
| `ask("text")` | Displays a prompt to the user. | `ask("Press enter...")` |
| `input_to("var", "text")` | Asks user for input and saves it to a variable. | `input_to("url", "URL: ")` |
| `webhook("url", "msg")` | Sends a message to a Discord webhook. | `webhook("url", "msg")` |
| `wait(seconds)` | Pauses the script for a set time. | `wait(5)` |
| `exit(number)` | Stops execution and reports success only when the number is 1. | `exit(1)` |

### Logic Control
*   **`if condition { ... }`**: Executes code inside the brackets only if the condition is true.
*   **`while condition { ... }`**: Loops the code inside the brackets while the condition is true.

### Variables and interpolation
*   **`set("name", "value")`**: defines a new variable.
*   Use `{var}` inside `say("...")` to insert the variable value into output.
*   Variables may also be used in expressions, such as `say(a + b)`.

## CLI Flags
*   `python ka.py -h` / `--help`: Displays the help menu.
*   `python ka.py -v` / `--version`: Displays the current version number.
*   `python ka.py -t` / `--test`: Runs test file named `test.ka`.
*   `python ka.py -c` / `--credits`: Displays developer(s) that have worked on this project.

## Support
How to support this project:
- Share this with friends who have Python installed.
- Leave a comment encouraging continued development of this project.