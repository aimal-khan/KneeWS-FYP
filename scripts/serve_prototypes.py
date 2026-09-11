#!/usr/bin/env python3
"""
KneeWS Prototype Live Server
----------------------------
Serves both KneeWS prototypes locally with live-reload support:
- Port 8000: KneeWS Hub & Unified Router
- Port 8001: Walkthrough Prototype
- Port 8002: Dashboard Prototype

Features:
- Instant Server-Sent Events (SSE) live-reload on file edits in 02_Prototypes/
- Clean URL routing (/walkthrough, /dashboard, /walkthrough/optionb, etc.)
- No-cache headers for instant preview of any modifications
- Zero external dependencies (uses standard library only)
"""

import os
import sys
import time
import threading
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROTOTYPES_DIR = os.path.join(BASE_DIR, "02_Prototypes")
WALKTHROUGH_DIR = os.path.join(PROTOTYPES_DIR, "Walkthrough")
DASHBOARD_DIR = os.path.join(PROTOTYPES_DIR, "Dashboard")

# Track file modification times
last_change_time = time.time()
change_condition = threading.Condition()

def get_latest_mtime():
    latest = 0
    for root, _, files in os.walk(PROTOTYPES_DIR):
        for f in files:
            if f.endswith(('.html', '.js', '.css', '.json')):
                try:
                    p = os.path.join(root, f)
                    mt = os.path.getmtime(p)
                    if mt > latest:
                        latest = mt
                except OSError:
                    pass
    return latest

def watcher_thread():
    global last_change_time
    prev_mtime = get_latest_mtime()
    while True:
        time.sleep(0.5)
        curr_mtime = get_latest_mtime()
        if curr_mtime > prev_mtime:
            prev_mtime = curr_mtime
            with change_condition:
                last_change_time = time.time()
                change_condition.notify_all()

LIVE_RELOAD_SCRIPT = """
<!-- KneeWS Live Reload Client -->
<script>
(function() {
  if (window.__kneews_livereload) return;
  window.__kneews_livereload = true;
  var es = new EventSource('/events');
  es.onmessage = function(e) {
    if (e.data === 'reload') {
      console.log('[KneeWS LiveReload] File modification detected. Reloading...');
      window.location.reload();
    }
  };
  es.onerror = function() {
    // EventSource automatically attempts reconnection
  };
  console.log('[KneeWS LiveReload] Active and monitoring for edits');
})();
</script>
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KneeWS — Local Live Prototypes</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0C1218;
      --card-bg: #151F28;
      --card-hover: #1A2733;
      --border: #233444;
      --border-accent: #2C6E97;
      --accent: #298EC6;
      --accent-bright: #38A9E6;
      --text: #F0F4F8;
      --text-muted: #8E9EA9;
      --tag-green: #2E7D5B;
      --tag-green-bg: #11281E;
      --tag-amber: #A47414;
      --tag-amber-bg: #2C200C;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 48px 24px;
    }
    .container {
      max-width: 980px;
      width: 100%;
    }
    header {
      margin-bottom: 40px;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #10261D;
      color: #5CD69C;
      border: 1px solid #1D4734;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 500;
      font-family: "IBM Plex Mono", monospace;
      margin-bottom: 16px;
    }
    .status-dot {
      width: 8px;
      height: 8px;
      background: #34D399;
      border-radius: 50%;
      box-shadow: 0 0 8px #34D399;
      animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }
    h1 {
      font-size: 32px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 10px;
    }
    h1 span {
      color: var(--accent-bright);
    }
    p.lead {
      color: var(--text-muted);
      font-size: 16px;
      max-width: 680px;
      line-height: 1.6;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
      gap: 24px;
      margin-bottom: 36px;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      position: relative;
    }
    .card:hover {
      border-color: var(--border-accent);
      background: var(--card-hover);
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    .card-top {
      margin-bottom: 24px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 14px;
    }
    .card-title {
      font-size: 20px;
      font-weight: 600;
    }
    .card-badge {
      font-size: 11px;
      font-family: "IBM Plex Mono", monospace;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 600;
      background: #1A3448;
      color: #6CBDEC;
      border: 1px solid #234E6F;
    }
    .card-desc {
      color: var(--text-muted);
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 16px;
    }
    .features-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 13px;
      color: #AEC1D0;
    }
    .features-list li {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .features-list li::before {
      content: "•";
      color: var(--accent-bright);
      font-weight: bold;
    }
    .actions {
      display: flex;
      flex-direction: column;
      gap: 10px;
      border-top: 1px solid var(--border);
      padding-top: 20px;
    }
    .btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 11px 16px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 500;
      font-size: 14px;
      transition: all 0.15s ease;
    }
    .btn-primary {
      background: var(--accent);
      color: #FFFFFF;
    }
    .btn-primary:hover {
      background: var(--accent-bright);
    }
    .btn-secondary {
      background: #1D2B37;
      color: #D3E0EA;
      border: 1px solid #2B3D4F;
    }
    .btn-secondary:hover {
      background: #253747;
      color: #FFF;
    }
    .btn .arrow {
      font-family: "IBM Plex Mono", monospace;
    }
    .port-links {
      display: flex;
      gap: 12px;
      margin-top: 6px;
      font-size: 12px;
      color: var(--text-muted);
      font-family: "IBM Plex Mono", monospace;
    }
    .port-links a {
      color: #6DBDEC;
      text-decoration: none;
    }
    .port-links a:hover {
      text-decoration: underline;
    }
    .info-box {
      background: #111A22;
      border: 1px solid #1E2D3B;
      border-radius: 10px;
      padding: 20px 24px;
      font-size: 13.5px;
      color: #A6BAC8;
      line-height: 1.6;
    }
    .info-box b {
      color: #F0F4F8;
    }
    .info-box code {
      background: #1B2936;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: "IBM Plex Mono", monospace;
      color: #79C2EC;
      font-size: 12.5px;
    }
    .quick-specs {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #1C2B38;
      font-size: 12px;
    }
    .spec-item span {
      display: block;
      color: var(--text-muted);
      margin-bottom: 2px;
    }
    .spec-item strong {
      color: #E2ECF3;
      font-family: "IBM Plex Mono", monospace;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="status-badge">
        <span class="status-dot"></span> LIVE RELOAD ACTIVE (02_Prototypes/*)
      </div>
      <h1>KneeWS <span>Interactive Prototypes</span></h1>
      <p class="lead">
        Noise-Aware Weak Supervision from Multilingual Radiology Reports for Multi-Label Knee MRI Interpretation.
        Choose a prototype below to review and test locally.
      </p>
    </header>

    <div class="grid">
      <!-- Card 1: Walkthrough -->
      <div class="card">
        <div class="card-top">
          <div class="card-header">
            <h2 class="card-title">Walkthrough Demo</h2>
            <span class="card-badge">6-STEP PITCH</span>
          </div>
          <p class="card-desc">
            Guided interactive presentation flow recommended for defense pitches (~90s). Step-by-step walkthrough demonstrating unmentioned finding sorting, label calibration, and tri-state decisioning.
          </p>
          <ul class="features-list">
            <li>Step 1: Reading multilingual reports (named vs unmentioned)</li>
            <li>Step 2: Standard practice vs KneeWS noise filtering</li>
            <li>Step 3: Four supervision rules / "Reveal the 58"</li>
            <li>Step 5: Model abstention toggling & specialist referral</li>
          </ul>
        </div>
        <div class="actions">
          <a href="/Walkthrough/kneews_walkthrough.html" class="btn btn-primary" target="_blank">
            <span>Launch Primary Walkthrough</span>
            <span class="arrow">→</span>
          </a>
          <a href="/Walkthrough/kneews_walkthrough_optionb.html" class="btn btn-secondary" target="_blank">
            <span>Launch Option B Walkthrough</span>
            <span class="arrow">→</span>
          </a>
          <div class="port-links">
            <span>Dedicated port:</span>
            <a href="http://localhost:8001" target="_blank">http://localhost:8001</a>
          </div>
        </div>
      </div>

      <!-- Card 2: Dashboard -->
      <div class="card">
        <div class="card-top">
          <div class="card-header">
            <h2 class="card-title">Dashboard Explorer</h2>
            <span class="card-badge">11 SCREENS</span>
          </div>
          <p class="card-desc">
            Comprehensive feature explorer mapped 1:1 against the 10 registered FYP features. Full DICOM-style MRI viewer, disagreement explorer, multi-institution workbench, and experiment race.
          </p>
          <ul class="features-list">
            <li>Multi-slice multi-series DICOM slice viewer (F1/F2)</li>
            <li>Multilingual report parsing & label matrix (F3/F4)</li>
            <li>Confident Learning & noise filter workbench (F5)</li>
            <li>Referral category generator & audit log (F8/F9)</li>
          </ul>
        </div>
        <div class="actions">
          <a href="/Dashboard/kneews_primary.html" class="btn btn-primary" target="_blank">
            <span>Launch Primary Dashboard</span>
            <span class="arrow">→</span>
          </a>
          <a href="/Dashboard/kneews_optionb.html" class="btn btn-secondary" target="_blank">
            <span>Launch Option B Dashboard</span>
            <span class="arrow">→</span>
          </a>
          <div class="port-links">
            <span>Dedicated port:</span>
            <a href="http://localhost:8002" target="_blank">http://localhost:8002</a>
          </div>
        </div>
      </div>
    </div>

    <div class="info-box">
      <b>💡 Live Review & Development Mode:</b>
      Any edits made to files inside <code>02_Prototypes/Dashboard/</code> or <code>02_Prototypes/Walkthrough/</code> will automatically trigger an instant browser reload in real-time. Responses are served with <code>no-cache</code> headers so changes take effect immediately.
      
      <div class="quick-specs">
        <div class="spec-item">
          <span>Unified Hub</span>
          <strong>http://localhost:8000</strong>
        </div>
        <div class="spec-item">
          <span>Walkthrough Server</span>
          <strong>http://localhost:8001</strong>
        </div>
        <div class="spec-item">
          <span>Dashboard Server</span>
          <strong>http://localhost:8002</strong>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class PrototypeHandler(BaseHTTPRequestHandler):
    default_prototype = None  # None for hub, 'walkthrough' or 'dashboard' for dedicated servers

    def log_message(self, format, *args):
        # Silence normal log noise to keep terminal clean
        pass

    def send_no_cache_headers(self, content_type="text/html; charset=utf-8"):
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")

    def handle_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Send initial connected event
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return

        client_last_time = last_change_time
        while True:
            try:
                with change_condition:
                    change_condition.wait(timeout=1.0)
                    if last_change_time > client_last_time:
                        client_last_time = last_change_time
                        self.wfile.write(b"data: reload\n\n")
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                break
            except Exception:
                break

    def do_GET(self):
        clean_path = self.path.split("?")[0].rstrip("/")

        # SSE endpoint
        if clean_path == "/events":
            self.handle_sse()
            return

        # Dedicated Walkthrough Server (Port 8001)
        if self.default_prototype == "walkthrough":
            if clean_path in ("", "/"):
                self.serve_file(os.path.join(WALKTHROUGH_DIR, "kneews_walkthrough.html"))
                return
            elif clean_path in ("/b", "/optionb", "/option-b"):
                self.serve_file(os.path.join(WALKTHROUGH_DIR, "kneews_walkthrough_optionb.html"))
                return

        # Dedicated Dashboard Server (Port 8002)
        if self.default_prototype == "dashboard":
            if clean_path in ("", "/"):
                self.serve_file(os.path.join(DASHBOARD_DIR, "kneews_primary.html"))
                return
            elif clean_path in ("/b", "/optionb", "/option-b"):
                self.serve_file(os.path.join(DASHBOARD_DIR, "kneews_optionb.html"))
                return

        # Root hub page (Port 8000)
        if clean_path in ("", "/"):
            self.serve_html_content(INDEX_HTML)
            return

        # Convenience friendly routes on main server
        if clean_path == "/walkthrough":
            self.serve_file(os.path.join(WALKTHROUGH_DIR, "kneews_walkthrough.html"))
            return
        if clean_path in ("/walkthrough/optionb", "/walkthrough-optionb"):
            self.serve_file(os.path.join(WALKTHROUGH_DIR, "kneews_walkthrough_optionb.html"))
            return
        if clean_path == "/dashboard":
            self.serve_file(os.path.join(DASHBOARD_DIR, "kneews_primary.html"))
            return
        if clean_path in ("/dashboard/optionb", "/dashboard-optionb"):
            self.serve_file(os.path.join(DASHBOARD_DIR, "kneews_optionb.html"))
            return

        # Generic file lookup inside 02_Prototypes
        rel_path = clean_path.lstrip("/")
        candidate = os.path.abspath(os.path.join(PROTOTYPES_DIR, rel_path))
        if candidate.startswith(PROTOTYPES_DIR) and os.path.isfile(candidate):
            self.serve_file(candidate)
            return

        # Also check relative to BASE_DIR
        candidate2 = os.path.abspath(os.path.join(BASE_DIR, rel_path))
        if candidate2.startswith(BASE_DIR) and os.path.isfile(candidate2):
            self.serve_file(candidate2)
            return

        # 404
        self.send_response(404)
        self.send_no_cache_headers("text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

    def serve_html_content(self, html_str):
        if "<script>" in html_str and "KneeWS Live Reload Client" not in html_str:
            html_str = html_str + LIVE_RELOAD_SCRIPT
        encoded = html_str.encode("utf-8")
        self.send_response(200)
        self.send_no_cache_headers("text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def serve_file(self, file_path):
        mime, _ = mimetypes.guess_type(file_path)
        if not mime:
            mime = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            if mime.startswith("text/html"):
                decoded = content.decode("utf-8", errors="replace")
                decoded = decoded + LIVE_RELOAD_SCRIPT
                content = decoded.encode("utf-8")
                mime = "text/html; charset=utf-8"

            self.send_response(200)
            self.send_no_cache_headers(mime)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.send_no_cache_headers("text/plain")
            self.end_headers()
            self.wfile.write(f"500 Internal Error: {e}".encode("utf-8"))

def make_handler(prototype_type=None):
    class CustomHandler(PrototypeHandler):
        default_prototype = prototype_type
    return CustomHandler

def run_server(port, handler_class, name):
    server = ThreadedHTTPServer(("0.0.0.0", port), handler_class)
    print(f"[{name}] Serving live at http://localhost:{port}")
    server.serve_forever()

def main():
    # Start background file watcher
    t_watcher = threading.Thread(target=watcher_thread, daemon=True)
    t_watcher.start()

    # Port 8000: Hub & Unified Router
    t8000 = threading.Thread(target=run_server, args=(8000, make_handler(None), "Hub & Unified Server"), daemon=True)
    t8000.start()

    # Port 8001: Dedicated Walkthrough
    t8001 = threading.Thread(target=run_server, args=(8001, make_handler("walkthrough"), "Walkthrough Server"), daemon=True)
    t8001.start()

    # Port 8002: Dedicated Dashboard
    t8002 = threading.Thread(target=run_server, args=(8002, make_handler("dashboard"), "Dashboard Server"), daemon=True)
    t8002.start()

    print("\n" + "="*65)
    print("  KneeWS Prototypes Live Development Server Ready!")
    print("="*65)
    print("  ► Unified Hub:        http://localhost:8000")
    print("  ► Walkthrough Demo:   http://localhost:8001  (or :8000/walkthrough)")
    print("  ► Dashboard Explorer: http://localhost:8002  (or :8000/dashboard)")
    print("  ► Option B versions:  http://localhost:8001/optionb")
    print("                        http://localhost:8002/optionb")
    print("="*65)
    print("  Live-reload is active: edit any HTML/JS file to auto-reload.")
    print("="*65 + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")

if __name__ == "__main__":
    main()
