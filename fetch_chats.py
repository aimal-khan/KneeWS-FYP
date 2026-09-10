import sys
import json
import time
from playwright.sync_api import sync_playwright

urls = [
    "https://chatgpt.com/share/6a8db5b4-5b30-83ee-86fc-ba2ad46c2842",
    "https://chatgpt.com/share/6a8db5dc-8f8c-83e8-bfc1-2303d3ab9bf9",
    "https://chatgpt.com/share/6a8db5f1-f974-83ee-a718-dfdb4f2f7b7d",
    "https://chatgpt.com/share/6a8db600-0aa0-83ee-9c09-0828bd4b6366"
]

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, url in enumerate(urls):
            print(f"Fetching {url}...")
            page.goto(url)
            # Wait for the chat messages to load
            try:
                page.wait_for_selector('div[data-message-author-role]', timeout=15000)
                time.sleep(2) # Give it a bit more time to render
                text = page.evaluate('document.body.innerText')
                with open(f'chat_content_{i+1}.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Saved chat_content_{i+1}.txt")
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                # Save whatever we have
                text = page.evaluate('document.body.innerText')
                with open(f'chat_content_{i+1}.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
        
        browser.close()

if __name__ == '__main__':
    run()
