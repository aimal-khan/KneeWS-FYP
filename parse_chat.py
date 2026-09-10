import json, re, sys, html

def extract_text(filepath, outpath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # ChatGPT shares often have a hydration state or the text is in the HTML.
    # Let's just strip all HTML tags and see what's left.
    # We remove <style> and <script> first.
    content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
    
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', ' ', content)
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r' +', ' ', text)
    
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(text.strip())

base_dir = "/Users/aimalkhan/.gemini/antigravity/brain/c36859b7-e94b-4a39-8cc0-f43a92f453df"
for i, step in enumerate([3, 4, 5, 6]):
    extract_text(f"{base_dir}/.system_generated/steps/{step}/content.md", f"{base_dir}/scratch/chat_{i+1}.txt")

print("Done parsing")
