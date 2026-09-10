import re
import sys

def dump_prose(filepath):
    print(f"--- {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all strings in quotes that are at least 30 characters long
    strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content)
    prose = []
    for s in strings:
        # Check if it looks like English text (spaces, standard chars, not a URL, not CSS)
        if len(s) > 50 and ' ' in s and not s.startswith('http') and '{' not in s and '<' not in s:
            # Unescape
            s = s.encode('utf-8').decode('unicode_escape', errors='ignore')
            prose.append(s)
            
    # Also find any text not in quotes if the hydration is raw
    # ChatGPT's Flight payload contains literal strings surrounded by quotes, so the above should work.
    
    # We will deduplicate and print
    seen = set()
    for p in prose:
        if p not in seen:
            seen.add(p)
            print(p)
            print()

for i in [3,4,5,6]:
    dump_prose(f"/Users/aimalkhan/.gemini/antigravity/brain/c36859b7-e94b-4a39-8cc0-f43a92f453df/.system_generated/steps/{i}/content.md")
