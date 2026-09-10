import re
import sys

def parse_file(filepath):
    print(f"--- {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The payload is in script tags. We want to extract ALL string literals
    # We can do this by finding all \"(.*?)\"
    
    # We remove <script> tags to just look at their contents?
    # No, the data IS inside the script tag.
    
    # Let's extract any string that has spaces, doesn't look like code, and is > 20 chars
    strings = re.findall(r'\\"(.*?)\\"', content)
    strings += re.findall(r'"([^"]*)"', content)
    
    texts = []
    for s in strings:
        if len(s) > 20 and ' ' in s and not s.startswith('http') and not re.match(r'^[\w\-_]+$', s):
            # rudimentary check for prose
            if len(re.findall(r'[a-zA-Z]', s)) > 10:
                texts.append(s)
                
    # Deduplicate
    seen = set()
    for t in texts:
        t = t.replace('\\n', '\n').replace('\\"', '"').strip()
        if t not in seen and len(t) > 30 and not t.startswith('{"'):
            seen.add(t)
            print(t)
            print('-'*40)

parse_file("/Users/aimalkhan/.gemini/antigravity/brain/c36859b7-e94b-4a39-8cc0-f43a92f453df/.system_generated/steps/6/content.md")
