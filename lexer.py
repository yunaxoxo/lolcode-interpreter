import re
import os
import sys

# --- token table ---
TOKEN_SPECS = [
    ("NEWLINE",    r"\n"),
    ("SKIP",       r"[ \t]+"),

    ("HAI",        r"HAI"),
    ("KTHXBYE",    r"KTHXBYE"),
    ("I_HAS_A",    r"I HAS A"),
    ("ITZ",        r"ITZ"),
    ("R",          r"R"),
    ("SUM_OF",     r"SUM OF"),
    ("DIFF_OF",    r"DIFF OF"),
    ("PRODUKT_OF", r"PRODUKT OF"),
    ("QUOSHUNT_OF", r"QUOSHUNT OF"),
    ("MOD_OF",     r"MOD OF"),
    ("BIGGR_OF",   r"BIGGR OF"),
    ("SMALLR_OF",  r"SMALLR OF"),
    ("BOTH_OF",    r"BOTH OF"),
    ("EITHER_OF",  r"EITHER OF"),
    ("WON_OF",     r"WON OF"),
    ("NOT",        r"NOT"),
    ("ANY_OF",     r"ANY OF"),
    ("ALL_OF",     r"ALL OF"),
    ("BOTH_SAEM",  r"BOTH SAEM"),
    ("DIFFRINT",   r"DIFFRINT"),
    ("SMOOSH",     r"SMOOSH"),
    ("MAEK",       r"MAEK"),
    ("A",          r"A"),
    ("IS_NOW_A",   r"IS NOW A"),
    ("VISIBLE",    r"VISIBLE"),
    ("GIMMEH",     r"GIMMEH"),
    ("O_RLY?",     r"O RLY\?"),
    ("YA_RLY",     r"YA RLY"),
    ("MEBBE",      r"MEBBE"),
    ("NO_WAI",     r"NO WAI"),
    ("OIC",        r"OIC"),
    ("WTF?",       r"WTF\?"),
    ("OMG",        r"OMG"),
    ("OMGWTF",     r"OMGWTF"),
    ("IM_IN_YR",   r"IM IN YR"),
    ("UPPIN",      r"UPPIN"),
    ("NERFIN",     r"NERFIN"),
    ("YR",         r"YR"),
    ("TIL",        r"TIL"),
    ("WILE",       r"WILE"),
    ("IM_OUTTA_YR", r"IM OUTTA YR"),
    ("HOW_IZ_I",    r"HOW IZ I"),
    ("IF_U_SAY_SO", r"IF U SAY SO"),
    ("GTFO",       r"GTFO"),
    ("FOUND_YR",   r"FOUND YR"),
    ("I_IZ",       r"I IZ"),
    ("MKAY",       r"MKAY"),

    ("NUMBAR",      r"-?\d+\.\d+"),
    ("NUMBR",     r"-?\d+"),
    
    ("YARN",       r"\".*?\""),
    ("TROOF",      r"WIN|FAIL"),
    ("TYPE",       r"NOOB|TROOF|NUMBR|NUMBAR|YARN|TYPE"),

    ("IDENTIFIER", r"[a-zA-Z][a-zA-Z0-9_]*"),
]

COMPILED_SPECS = [(name, re.compile(pattern)) for name, pattern in TOKEN_SPECS]
INPUT_FILE = "source.txt"

# --- tokenizer ---
def tokenize(source):
    """Turns LOLCODE source text into a list of tokens.

    Args:
        source: The full program text as one string.

    Returns:
        A list of (token_type, text, line_number) tuples.
    """
    tokens = []
    position = 0
    line_number = 1

    while position < len(source):
        for name, regex in COMPILED_SPECS:
            match = regex.match(source, position)

            if match:
                break
        else:
            raise SyntaxError(f"Line {line_number}: can't read '{source[position]}'")
        
        text = match.group()

        if name == "NEWLINE":
            tokens.append((name, text, line_number))
            line_number+=1
        elif name != "SKIP":
            tokens.append((name, text, line_number))
        
        position = match.end()
        

    return tokens

# --- file reaading --
def read_input(filepath):
    
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        sys.exit(1)
    
    with open(filepath, "r") as f:
        source = f.read()

    return source 

# --- test run ---
if __name__ == "__main__":
    source_text = read_input(INPUT_FILE)
    for token in tokenize(source_text):
        print(token)
