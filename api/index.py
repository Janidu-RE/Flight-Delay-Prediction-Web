import subprocess
import sys
import os

def handler(request, response):
    """
    Vercel serverless entry point.
    Launches the Streamlit app as a subprocess and proxies the response.
    Note: Vercel's serverless environment has a short execution timeout.
    For persistent hosting, consider Streamlit Community Cloud or Railway.
    """
    port = int(os.environ.get("PORT", 8501))
    app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")

    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", app_path,
         "--server.port", str(port),
         "--server.headless", "true",
         "--server.enableCORS", "false",
         "--server.enableXsrfProtection", "false"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    response.status_code = 200
    response.headers["Content-Type"] = "text/html"
    response.body = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta http-equiv='refresh' content='3;url=http://localhost:{port}'>
        <title>Redirecting to Flight Delay Predictor...</title>
        <style>
          body {{ font-family: sans-serif; display:flex; align-items:center;
                  justify-content:center; height:100vh; margin:0;
                  background:#0e1117; color:#fafafa; }}
          a {{ color:#4fc3f7; }}
        </style>
      </head>
      <body>
        <div>
          <h2>✈️ Launching Flight Delay Predictor…</h2>
          <p>If not redirected automatically, <a href='http://localhost:{port}'>click here</a>.</p>
        </div>
      </body>
    </html>
    """
    return response
