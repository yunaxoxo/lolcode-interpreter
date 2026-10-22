import re
import os
import sys

TOKEN_SPECS = [
    ("NEWLINE",       r"\n"),
    ("SKIP",          r"[ \t]+"),

    # --- Comments ---
    ("BLOCK_COMMENT", r"(?m)^\s*OBTW[\s\S]*?^\s*TLDR[^\n]*"),
    ("COMMENT",       r"BTW[^\n]*"),

    # --- Separators & Delimiters ---
    ("COMMA",         r","),
    ("AN",            r"\bAN\b"),
    ("EXCLAMATION",   r"!"),              # Suppresses newline in VISIBLE

    # --- Core Structure & Variables ---
    ("HAI",           r"\bHAI\b"),
    ("KTHXBYE",       r"\bKTHXBYE\b"),
    ("I_HAS_A",       r"\bI HAS A\b"),
    ("ITZ",           r"\bITZ\b"),
    ("R",             r"\bR\b"),

    # --- Math Operations ---
    ("SUM_OF",        r"\bSUM OF\b"),
    ("DIFF_OF",       r"\bDIFF OF\b"),
    ("PRODUKT_OF",    r"\bPRODUKT OF\b"),
    ("QUOSHUNT_OF",   r"\bQUOSHUNT OF\b"),
    ("MOD_OF",        r"\bMOD OF\b"),
    ("BIGGR_OF",      r"\bBIGGR OF\b"),
    ("SMALLR_OF",     r"\bSMALLR OF\b"),

    # --- Boolean & Logic ---
    ("BOTH_OF",       r"\bBOTH OF\b"),
    ("EITHER_OF",     r"\bEITHER OF\b"),
    ("WON_OF",        r"\bWON OF\b"),
    ("NOT",           r"\bNOT\b"),
    ("ANY_OF",        r"\bANY OF\b"),
    ("ALL_OF",        r"\bALL OF\b"),

    # --- Comparison ---
    ("BOTH_SAEM",     r"\bBOTH SAEM\b"),
    ("DIFFRINT",      r"\bDIFFRINT\b"),

    # --- String Operations & Casting ---
    ("SMOOSH",        r"\bSMOOSH\b"),
    ("MAEK",          r"\bMAEK\b"),
    ("A",             r"\bA\b"),
    ("IS_NOW_A",      r"\bIS NOW A\b"),

    # --- I/O ---
    ("VISIBLE",       r"\bVISIBLE\b"),
    ("GIMMEH",        r"\bGIMMEH\b"),

    # --- Conditionals ---
    ("O_RLY?",        r"\bO RLY\?"),
    ("YA_RLY",        r"\bYA RLY\b"),
    ("MEBBE",         r"\bMEBBE\b"),
    ("NO_WAI",        r"\bNO WAI\b"),
    ("OIC",           r"\bOIC\b"),

    # --- Switch Statement ---
    ("WTF?",          r"\bWTF\?"),
    ("OMGWTF",        r"\bOMGWTF\b"),
    ("OMG",           r"\bOMG\b"),

    # --- Loops ---
    ("IM_IN_YR",      r"\bIM IN YR\b"),
    ("UPPIN",         r"\bUPPIN\b"),
    ("NERFIN",        r"\bNERFIN\b"),
    ("YR",            r"\bYR\b"),
    ("TIL",           r"\bTIL\b"),
    ("WILE",          r"\bWILE\b"),
    ("IM_OUTTA_YR",   r"\bIM OUTTA YR\b"),

    # --- Functions ---
    ("HOW_IZ_I",      r"\bHOW IZ I\b"),
    ("IF_U_SAY_SO",   r"\bIF U SAY SO\b"),
    ("GTFO",          r"\bGTFO\b"),
    ("FOUND_YR",      r"\bFOUND YR\b"),
    ("I_IZ",          r"\bI IZ\b"),

    # --- Special Tokens ---
    ("MKAY",          r"\bMKAY\b"),
    ("SRS",           r"\bSRS\b"),

    # --- Literals & Types ---
    ("NUMBAR",        r"-?\d+\.\d+"),
    ("NUMBR",         r"-?\d+"),
    # Handles standard escapes (:), :"), multi-char interpolation (:{var}, :(1F600))
    ("YARN",          r'"(?:[^"\:]|:[)\(>":\n]|:\{[^\}]+\}|:\([0-9a-fA-F]+\))*"'),
    ("TROOF",         r"\b(WIN|FAIL)\b"),
    ("TYPE",          r"\b(NOOB|TROOF|NUMBR|NUMBAR|YARN|TYPE)\b"),
    ("NOOB",          r"\bNOOB\b"),

    # --- Identifiers ---
    ("IDENTIFIER",    r"[a-zA-Z][a-zA-Z0-9_]*"),
]

COMPILED_SPECS = [(name, re.compile(pattern)) for name, pattern in TOKEN_SPECS]
INPUT_FILE = "source.txt"

def tokenize(source):
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
            line_number += 1
        elif name == "BLOCK_COMMENT":
            line_number += text.count("\n")
        elif name not in ("SKIP", "COMMENT"):
            tokens.append((name, text, line_number))
        
        position = match.end()

    return tokens

def read_input(filepath):
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        sys.exit(1)
    
    with open(filepath, "r") as f:
        return f.read()

if __name__ == "__main__":
    source_text = read_input(INPUT_FILE)
    for token in tokenize(source_text):
        print(token)
