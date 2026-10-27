'''
    Roman Numeral Calculator Engine
    a demo project assuming Python 3.8+ and Tkinter GUI
    may switch to online jupyternote version using ipywidgets if asked
'''

#import tariffs
import math
import tkinter as tk
from tkinter import messagebox

#init the class
class CalculatorMain:

    def __init__(self):
        # begin the dictionaries for roman numeral conversion
        
        #dict 1 : Roman -> Int value
        self.roman_to_int_dict = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        # dict 2 : Int value -> Roman
        self.int_to_roman_dict = {
            1000: 'M',  900: 'CM',
            500:  'D',  400: 'CD',
            100:  'C',  90:  'XC',
            50:   'L',  40:  'XL',
            10:   'X',  9:   'IX',
            5:    'V',  4:   'IV',
            1:    'I'
        }

        # dict 3 : base-12 -> Roman
        self.twelfths_to_roman_dict = {
            0:  '',
            1:  '.',      # 1/12 (uncia)
            2:  ':',      # 2/12 (1/6, sextans)
            3:  ':.',     # 3/12 (1/4, quadrans)
            4:  '::',     # 4/12 (1/3, triens)
            5:  '::.',    # 5/12 (quincunx)
            6:  'S',      # 6/12 (1/2, semis)
            7:  'S.',     # 7/12 (septunx)
            8:  'S:',     # 8/12 (2/3, bes)
            9:  'S:.',    # 9/12 (3/4, dodrans)
            10: 'S::',    # 10/12 (5/6, dextans)
            11: 'S::.'    # 11/12 (deunx)
        }

    #now we define the basic roman numeral conversion functions, which are used by the main funcs
    
    # Basic Roman convert funcs (1-3999)
    def _basic_roman_to_int(self, roman_str):
        total = 0
        n = len(roman_str)
        for i in range(n): #for loop to iterate through the string
            ch = roman_str[i]
            if ch not in self.roman_to_int_dict:
                raise ValueError("Invalid symbol '{}' in Roman numeral.".format(ch)) #we use a valueerror to catch bad people (who use bad symb)
            
            val = self.roman_to_int_dict[ch]
            # first rule of roman, the subtractive notation
            if (i + 1 < n) and (val < self.roman_to_int_dict.get(roman_str[i + 1], 0)):
                total -= val
            else:
                total += val
        return total

    def _basic_int_to_roman(self, num):
        #Converts a basic int into its numeral
        result = ""
        for val, symbol in self.int_to_roman_dict.items(): #we use the items() method to get the key-value pairs from the dictionary
            count = num // val #items allows us to iterate through the dictionary and get the key-value pairs
            result += symbol * count
            num = num % val #we then use mod to get the remain and continue
        return result

    def number_to_roman(self, number):
        #now convert any float / int into a full numeral str
        if abs(number) < 1e-9: #we have a rather large upper limit
            return "N" #this gives us us the zero numeral 

        sign = "-" if number < 0 else ""
        number = abs(number) #we then take the absolute value of the number to make it positive for conv

        whole = int(math.floor(number + 1e-9))
        frac = number - whole #then we get the fractional part of the number

        # Convert fractional part to nearest twelfth (uncia)
        twelfths = int(round(frac * 12))
        if twelfths == 12:
            whole += 1
            twelfths = 0

        if whole > 3999999: #we account for overflow, as the vinculum system only allows for 3,999,999 as the max
            raise OverflowError("Result exceeds maximum Vinculum limit (3,999,999).") #spell check did not know what this word meant

        # Build whole number part
        roman_whole = ""
        if whole >= 4000:
            thousands = whole // 1000 #here we use integer division to get the number of thousands or hundereds of thousands
            remainder = whole % 1000
            roman_whole = "({})".format(self._basic_int_to_roman(thousands)) #now we use format to build the vinculum part of the numeral
            if remainder > 0:
                roman_whole += self._basic_int_to_roman(remainder) #then for any remainder we just use the basic conversion function
        elif whole > 0:
            roman_whole = self._basic_int_to_roman(whole) #then we call §the basic conversion function for any number less than 4000

        # Build fractional part
        roman_frac = self.twelfths_to_roman_dict[twelfths]

        #here we return the final numeral, with the sign, whole part, and fractional part
        if roman_whole == "" and roman_frac == "":
            return "N"
        return sign + roman_whole + roman_frac

    #new function to convert roman numeral to number, with validation (yipeeeee)

    def roman_to_number(self, roman_str):
        """
        Parses and strictly validates a Roman numeral string (including negatives,
        Vinculum brackets, and base-12 fractions) into a Python float/int.
        """
        raw_input = roman_str.strip().upper() #we have to strip out the whitespace and make it uppercase to make it easier to parse
        if not raw_input:
            raise ValueError("Empty Roman numeral input.") #then we check for empty input and raise a valueerror if it is empty

        if raw_input == "N": #we can now handle the zero numeral
            return 0

        # Check for negative sign
        sign = 1
        s = raw_input
        if s.startswith("-"):
            sign = -1
            s = s[1:].strip()

        # Extract any trailing base-12 fraction characters ('S', ':', '.') you can read more about this at [cite]
        frac_chars = ""
        while len(s) > 0 and s[-1] in ('S', ':', '.'): #pretty standard while loop to extract the fraction characters from the end of the string
            frac_chars = s[-1] + frac_chars
            s = s[:-1]

        twelfths = 0 #then we convert the fraction characters into a number of twelfths
        for ch in frac_chars:
            if ch == 'S':
                twelfths += 6
            elif ch == ':':
                twelfths += 2
            elif ch == '.':
                twelfths += 1
        if twelfths >= 12:
            raise ValueError("Invalid fraction '{}' (>= 12/12).".format(frac_chars)) #just in case we have one more valueerror

        # Parse whole number part
        whole_val = 0
        if len(s) > 0:
            if s.startswith("("):
                # Handle Vinculum brackets (thousands separator)
                if ")" not in s:
                    raise ValueError("Unclosed Vinculum bracket '('.")
                close_idx = s.index(")")
                thousands_part = s[1:close_idx]
                remainder_part = s[close_idx + 1:]
                if not thousands_part: #in cases where the thousands is empty 
                    raise ValueError("Empty Vinculum brackets '()'.")
                whole_val = self._basic_roman_to_int(thousands_part) * 1000 #then we multiply the thousands part by 1000 to get the whole value
                if remainder_part:
                    whole_val += self._basic_roman_to_int(remainder_part)
            else:
                whole_val = self._basic_roman_to_int(s) #or we can just use the basic conversion function if there are no vinculum brackets

        total = sign * (whole_val + (twelfths / 12.0)) #take the sign into account and add the whole value and the fractional value together to get the total

        # Canonical Round-Trip Validation!
        canonical = self.number_to_roman(total)
        if canonical != raw_input:
            raise ValueError(
                #we use the google method of asking the user why dumb
                "Malformed numeral '{}'. Did you mean '{}' ({:g})?".format(
                    raw_input, canonical, total
                )
            )

        return int(total) if twelfths == 0 else total #return the total as an int if there are no twelfths, otherwise return it as a float

    #new function; this time we are going to evaluate the expression, which is the main function of the calculator
    #this is the main function that takes in the two roman numerals and the operator and returns the result in both roman and decimal form
    #it also handles the square root operator, which is a unary operator, and the other operators are binary operators

    def evaluate(self, num1_str, operator, num2_str=None):
        # we beign by executing an operation (+, -, *, /, ^, SQRT) and returns (roman_res, dec_res).
        val1 = self.roman_to_number(num1_str)

        if operator == "SQRT": #we handle the square root operator, which is a unary operator
            if val1 < 0:
                raise ValueError("Cannot take square root of a negative numeral.") #theres going to be a lot of valueerrors in this func, but they are all necessary to catch the user when they do something dumb, which is likely
            res = math.sqrt(val1)
            return self.number_to_roman(res), res

        val2 = self.roman_to_number(num2_str) #we then convert the second numeral to a number, which is necessary for the binary operators

        #and now we sit and do the actual math, which is the main part of the function, and we use a series of if statements to determine which operator to use

        if operator == '+': #i wont comment every single one of these, as they are all pretty self explanatory
            res = val1 + val2
        elif operator == '-':
            res = val1 - val2
        elif operator == '*':
            res = val1 * val2
        elif operator == '/':
            if abs(val2) < 1e-9:
                raise ZeroDivisionError("Division by N (Zero) is undefined.") #this one is important, as we dont want to divide by zero, i am told this is bad
            res = val1 / val2
        elif operator == '^':
            res = val1 ** val2
        else:
            raise ValueError("Unknown operator '{}'".format(operator)) #i mean, yeah just in case they try and idk like use grad

        return self.number_to_roman(res), res #and finally we spit out the result in both roman and decimal form




# alright GUI time, this is going to be a bit more complicated, as python is in an incredible twist not the best front end framework


#we start by inventig a gui class
class RomanCalculatorGUI:
    #now we want to build it up in stages, so we start with the init function, which is the main function that sets up the GUI and the calculator engine

    def __init__(self, root, engine): #we do a base innit 
        self.root = root
        self.engine = engine
        self.root.title("SPQR - Roman Numeral Desktop Calculator") # Set the title of the window
        self.root.geometry("460x620") #define an "REASONABLE WINDOW" im told 4k is still not standard 
        self.root.configure(bg="#2b2b2b") # Set background color to dark gray as we live in the modern age of dark modes
        self.root.resizable(False, False) # Disable window resizing for a fixed layout, this makes my life easier

        # Calculator state variables
        self.first_operand = ""
        self.current_operator = ""
        self.current_input = ""
        self.just_evaluated = False

        self._build_interface()

    def _build_interface(self):
        # right now we must build a frame
        display_frame = tk.Frame(self.root, bg="#1e1e1e", bd=4, relief=tk.SUNKEN) #we use a sunked frame because skeoumorphism is cool, and its 2012 again
        display_frame.pack(fill=tk.X, padx=14, pady=(14, 8))

        # Expression / status line (top small text)
        self.expr_label = tk.Label(
            display_frame, text="Enter Roman Numeral", anchor="e",
            bg="#1e1e1e", fg="#aaaaaa", font=("Consolas", 11), padx=10, pady=2 #graphic design is my passion
        )
        self.expr_label.pack(fill=tk.X)

        # Main Roman Numeral display (large gold text, romans like gold)
        self.roman_display = tk.Label(
            display_frame, text="N", anchor="e",
            bg="#1e1e1e", fg="#f5c542", font=("Georgia", 26, "bold"), padx=10, pady=4
        )
        self.roman_display.pack(fill=tk.X)

        # Live Arabic/Decimal translation bar (bottom green text)
        self.arabic_display = tk.Label(
            display_frame, text="Decimal: 0", anchor="e",
            bg="#1e1e1e", fg="#66bb6a", font=("Consolas", 11), padx=10, pady=4 #green is the color of money, and we like money
        )
        self.arabic_display.pack(fill=tk.X)

        #grid frame. as for the past 65 years we have just accepted this as peak UX i guess (ref ANITA MK-8)
        keypad_frame = tk.Frame(self.root, bg="#2b2b2b")
        keypad_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

        # 2D Array of Calculator Buttons: (Text, Row, Col, Colour) im using "ti 89" style colors, so grey and white and then also using green and red for contrast
        #i may if so inclined go to a casio style blue, white and black, not sure yet
        buttons = [
            # Row 0: Clear, Backspace, Vinculum brackets, Zero
            ("CLR", 0, 0, "#b71c1c"), ("DEL", 0, 1, "#c62828"),
            ("(",   0, 2, "#455a64"), (")",   0, 3, "#455a64"), ("N (0)", 0, 4, "#455a64"),

            # Row 1: High Roman numerals + Power/Root
            ("D",   1, 0, "#f0f0f0"), ("M",   1, 1, "#f0f0f0"),
            ("^",   1, 2, "#8a8f99"), ("SQRT",1, 3, "#8a8f99"), ("/",     1, 4, "#8a8f99"),

            # Row 2: Mid Roman numerals + Multiply/Subtract (hehe mid)
            ("L",   2, 0, "#f0f0f0"), ("C",   2, 1, "#f0f0f0"),
            ("S (1/2)", 2, 2, "#8a8f99"), ("*", 2, 3, "#8a8f99"), ("-",   2, 4, "#8a8f99"),

            # Row 3: Low Roman numerals + Fractions + Add/Equals
            ("I",   3, 0, "#f0f0f0"), ("V",   3, 1, "#f0f0f0"), ("X",     3, 2, "#f0f0f0"),
            (": (2/12)", 3, 3, "#8a8f99"), ("+", 3, 4, "#8a8f99"),

            # Row 4: dot + Negative toggle + Wide Equals button
            (". (1/12)", 4, 0, "#8a8f99"), ("+/-", 4, 1, "#455a64"),
        ]

        #alright now we just need to iterate through the buttons and create them, which is pretty standard stuff
        for (text, r, c, color) in buttons:
            btn = tk.Button(
                keypad_frame, text=text, bg=color,
                fg="#111111" if color == "#f0f0f0" else "white", #we do this to have black on light
                activebackground="#616161", activeforeground="white",
                font=("Segoe UI", 11, "bold"), bd=1, relief=tk.RAISED,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Wide '=' button across columns 2, 3, 4 of Row 4
        eq_btn = tk.Button(
            keypad_frame, text="= (CALCULATE)", bg="#2e7d32", fg="white", #graphic design is my passion, and green is the color of money, and we like money
            activebackground="#43a047", activeforeground="white",
            font=("Segoe UI", 12, "bold"), bd=1, relief=tk.RAISED,
            command=lambda: self.on_button_click("=")
        )
        eq_btn.grid(row=4, column=2, columnspan=3, sticky="nsew", padx=3, pady=3)
        #we do this each time to make sure the buttons are evenly spaced and look nice, as we are not animals
        for i in range(5):
            keypad_frame.rowconfigure(i, weight=1)
            keypad_frame.columnconfigure(i, weight=1)

        # and we add this history frame at the bottom
        hist_frame = tk.Frame(self.root, bg="#2b2b2b")
        hist_frame.pack(fill=tk.X, padx=14, pady=(4, 12))

        tk.Label(
            hist_frame, text="Calculation History (Roman & Decimal):",
            bg="#2b2b2b", fg="#bbbbbb", font=("Segoe UI", 9, "bold"), anchor="w" #idk default fonts and stuff, im not a typographer
        ).pack(fill=tk.X)

        self.history_list = tk.Listbox(
            hist_frame, height=5, bg="#1e1e1e", fg="#e0e0e0",
            font=("Consolas", 10), bd=2, relief=tk.SUNKEN
        )
        self.history_list.pack(fill=tk.X, pady=2)

    # Update display labels based on current state
    def _update_displays(self): #live display so cool much wow
        shown_text = self.current_input if self.current_input else "N"
        self.roman_display.config(text=shown_text) #we show the current input, or "N" if empty, in the main roman display

        # Build top expression line
        if self.first_operand and self.current_operator:
            self.expr_label.config(text="{} {}".format(self.first_operand, self.current_operator))
        else:
            self.expr_label.config(text="Ready")

        # Try live-validating the current input to show its decimal value
        if not self.current_input:
            self.arabic_display.config(text="Decimal: 0", fg="#66bb6a")
        else:
            try:
                val = self.engine.roman_to_number(self.current_input)
                self.arabic_display.config(text="Decimal: {:g}".format(val), fg="#66bb6a") #if we can convert it to a number, we show the decimal value in green
            except ValueError as err:
                # Show syntax hint if currently malformed (e.g. 'IIII')
                self.arabic_display.config(text=str(err), fg="#ef5350")

    def on_button_click(self, label):
        # Extract symbol from labels like "S (1/2)" -> "S"
        symbol = label.split(" ")[0]

        #now for the button click handler
        if symbol == "CLR": #we do this for clear
            self.first_operand = ""
            self.current_operator = ""
            self.current_input = ""
            self.just_evaluated = False
            self._update_displays()
            return

        if symbol == "DEL": #delete is a bit more complicated, as we have to check if we just evaluated an expression, in which case we clear the input, otherwise we just delete the last character
            if self.just_evaluated:
                self.current_input = ""
                self.just_evaluated = False
            else:
                self.current_input = self.current_input[:-1]
            self._update_displays()
            return

        if symbol == "+/-": #then for the negative toggle, we just check if the current input starts with a negative sign, and if it does we remove it, otherwise we add it to the front
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            elif self.current_input and self.current_input != "N":
                self.current_input = "-" + self.current_input
            self._update_displays()
            return

        # Square Root operator
        if symbol == "SQRT":
            target = self.current_input if self.current_input else "N"
            try:
                rom_res, dec_res = self.engine.evaluate(target, "SQRT") #we take the current input and evaluate it with the square root operator, which is a unary operator
                log_entry = "SQRT({}) = {}  [{:g}]".format(target, rom_res, dec_res)
                self.history_list.insert(0, log_entry)
                self.current_input = rom_res
                self.first_operand = ""
                self.current_operator = ""
                self.just_evaluated = True #we set the just_evaluated flag to true so that the next time the user enters a numeral, it will clear the current input
                self._update_displays()
            except Exception as e:
                messagebox.showerror("Calculation Error", str(e)) #finally we catch any errors and show them in a messagebox
            return

        # Binary operators (+, -, *, /, ^)
        if symbol in ('+', '-', '*', '/', '^'):
            if not self.current_input:
                self.current_input = "N"
            try:
                # Validate first operand before locking it in
                self.engine.roman_to_number(self.current_input)
                self.first_operand = self.current_input
                self.current_operator = symbol
                self.current_input = ""
                self.just_evaluated = False
                self._update_displays()
            except Exception as e:
                messagebox.showwarning("Invalid Roman Numeral", str(e)) #same thing here, we catch any errors and show them in a messagebox
            return

        # Equals (=)
        if symbol == "=":
            if not self.first_operand or not self.current_operator: #now we check if we have a first operand and an operator, if not we just return
                return
            second_operand = self.current_input if self.current_input else "N" #if the current input is empty, we treat it as "N" (zero)
            try:
                rom_res, dec_res = self.engine.evaluate(
                    self.first_operand, self.current_operator, second_operand
                ) #we then evaluate the expression with the first operand, operator, and second operand, and get the result in both roman and decimal form
                log_entry = "{} {} {} = {}  [{:g}]".format(
                    self.first_operand, self.current_operator, second_operand, rom_res, dec_res
                ) #finally we log the calculation in the history list, and update the displays with the result
                self.history_list.insert(0, log_entry)
                self.expr_label.config(text="{} {} {} =".format(
                    self.first_operand, self.current_operator, second_operand
                )) #we update the expression label to show the current calculation
                self.current_input = rom_res
                self.first_operand = ""
                self.current_operator = ""
                self.just_evaluated = True
                self.roman_display.config(text=rom_res)
                self.arabic_display.config(text="Decimal: {:g}".format(dec_res), fg="#66bb6a") #green again
            except Exception as e:
                messagebox.showerror("Calculation Error", str(e))
            return

        # Otherwise, it's a Roman numeral character (I, V, X, L, C, D, M, (, ), N, S, :, .)
        if self.just_evaluated:
            self.current_input = ""
            self.just_evaluated = False

        if symbol == "N": #if the user enters "N" (zero), we reset the current input to "N"
            self.current_input = "N"
        else:
            if self.current_input == "N":
                self.current_input = symbol
            else:
                self.current_input += symbol #we append the symbol to the current input, which is a string

        self._update_displays() #and we are done


# test suite
#'''
def run_automated_tests(engine):
    print("=" * 72)
    print(" ROMAN NUMERAL CALCULATOR - AUTOMATED VERIFICATION SUITE")
    print("=" * 72)
    print("{:<22} | {:<14} | {:<12} | {:<16}".format(
        "Roman Expression", "Roman Result", "Decimal", "Feature Tested"
    ))
    print("-" * 72)

    tests = [
        ("XIV", "+", "XXVI",     "Standard Addition"),
        ("MCMXCIV", "+", "VI",   "Subtractive Carry (1994+6)"),
        ("L", "-", "L",          "Zero / Nulla ('N')"),
        ("X", "-", "XXV",        "Negative Result (-15)"),
        ("C", "*", "L",          "Vinculum >3999 (5,000)"),
        ("(V)", "+", "D",        "Vinculum Input (5,500)"),
        ("X", "/", "IV",         "Semis Fraction (2.5 -> IIS)"),
        ("X", "/", "III",        "Unciae Fraction (3.33 -> III::)"),
        ("IIS", "*", "II",       "Fraction Input (2.5 * 2 = 5)"),
        ("XII", "^", "III",      "Exponentiation (12^3 = 1728)"),
    ]

    for n1, op, n2, desc in tests:
        rom_res, dec_res = engine.evaluate(n1, op, n2)
        expr_str = "{} {} {}".format(n1, op, n2)
        print("{:<22} | {:<14} | {:<12.4g} | {:<16}".format(
            expr_str, rom_res, dec_res, desc
        ))

    print("-" * 72)
    print("Testing Syntax Validation (Illegal Numeral Catching):")
    for bad_input in ["IIII", "VV", "IC", "XXXX"]:
        try:
            engine.roman_to_number(bad_input)
        except ValueError as err:
            print("  [Caught] {:<6} -> {}".format(bad_input, err))
    print("=" * 72)
#'''

if __name__ == "__main__":
    engine = CalculatorMain()
    
    #test suite RBF
    run_automated_tests(engine)

    #we launch the GUI
    try:
        
        print("\n[+] Launching SPQR Roman Numeral Desktop Calculator GUI...")
        root = tk.Tk()
        app = RomanCalculatorGUI(root, engine)
        root.mainloop()
    except tk.TclError: #in the event of headless
        print("\n[!] No desktop display detected (running on headless server).")
        print("    Use engine.evaluate(num1, op, num2) directly in notebook cells.") #(me when i SSH into my house because the uni pc is that bad)