import json, re, sys, html
from urllib.parse import unquote

def extract_chat(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Try to find all json strings in the script tags and dump text
    scripts = re.findall(r'<script.*?>(.*?)</script>', content, flags=re.DOTALL)
    for s in scripts:
        if 'window.__remixContext' in s:
            match = re.search(r'window.__remixContext = (.*?);', s)
            if match:
                try:
                    data = json.loads(match.group(1))
                    print(json.dumps(data, indent=2)[:1000])
                    # Try to extract messages if it's there
                except:
                    pass
        elif '{"props"' in s or '{"state"' in s or '{"pageProps"' in s or '{"authStatus"' in s or '{"type":"chat"' in s or 'title' in s:
            # this might be it
            pass
            
    # Sometimes it's just inside __REMIX_ROUTE_DATA__ or similar
    # Let's just find anything resembling typical chat message "content": "..."
    # A simple way to get all text from JSON in the file is to look for "parts": ["..."] or "text": "..."
    matches = re.findall(r'"parts":\s*\[\s*"(.*?)"\s*\]', content)
    if matches:
        for m in matches:
            print("MESSAGE PART:")
            print(m[:500])
    else:
        # try simple text extraction of any long string
        strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content)
        long_strings = [s for s in strings if len(s) > 100]
        if long_strings:
            print(f"Found {len(long_strings)} long strings.")
            for ls in long_strings[:5]: # print first 5
                print(ls[:200])

base_dir = "/Users/aimalkhan/.gemini/antigravity/brain/c36859b7-e94b-4a39-8cc0-f43a92f453df"
print("File 3")
extract_chat(f"{base_dir}/.system_generated/steps/3/content.md")
print("File 4")
extract_chat(f"{base_dir}/.system_generated/steps/4/content.md")
