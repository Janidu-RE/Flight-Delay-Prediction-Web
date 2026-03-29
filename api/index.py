import subprocess
import sys
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless entry point.
    Vercel Python functions must expose a class named `handler` that
    inherits from BaseHTTPRequestHandler.

    NOTE: Vercel's serverless runtime cannot host a persistent Streamlit
    server. This handler returns a redirect page pointing to the live app
    hosted on Streamlit Community Cloud (update the URL below once deployed).
    """

    STREAMLIT_APP_URL = "https://share.streamlit.io"   # ← replace with your deployed URL

    def do_GET(self):
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="3;url={self.STREAMLIT_APP_URL}" />
  <title>✈️ Flight Delay Predictor</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', sans-serif;
      background: #0e1117;
      color: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      text-align: center;
    }}
    .card {{
      padding: 48px;
      border: 1px solid #262730;
      border-radius: 16px;
      background: #1a1c24;
      max-width: 480px;
    }}
    h1 {{ font-size: 2rem; margin-bottom: 12px; }}
    p  {{ color: #9ca3af; margin-bottom: 24px; font-size: 0.95rem; }}
    a  {{
      display: inline-block;
      padding: 12px 28px;
      background: #4fc3f7;
      color: #0e1117;
      border-radius: 8px;
      font-weight: 600;
      text-decoration: none;
    }}
    a:hover {{ background: #81d4fa; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>✈️ Flight Delay Predictor</h1>
    <p>Redirecting you to the live Streamlit app in 3 seconds…</p>
    <a href="{self.STREAMLIT_APP_URL}">Open App →</a>
  </div>
</body>
</html>"""

        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # silence default access logs in Vercel output
