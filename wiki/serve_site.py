#!/usr/bin/env python3
"""
Local server to view the generated Jekyll site
"""

import http.server
import socketserver
import os
from pathlib import Path
from urllib.parse import urlparse

PORT = 4000

class JekyllHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        path = self.path.strip('/')
        
        # Handle root
        if path == '' or path == 'index.html':
            self.path = '/_site/index.html'
            return super().do_GET()
        
        # Try exact match first
        test_file = Path('_site') / path
        if test_file.exists() and test_file.is_file():
            self.path = f'/_site/{path}'
            return super().do_GET()
        
        # Try as directory with index.html
        test_index = Path('_site') / path / 'index.html'
        if test_index.exists():
            self.path = f'/_site/{path}/index.html'
            return super().do_GET()
        
        # Try adding .html extension
        test_html = Path('_site') / (path + '.html')
        if test_html.exists():
            self.path = f'/_site/{path}.html'
            return super().do_GET()
        
        # Try removing trailing slash and adding .html
        if path.endswith('/'):
            path = path.rstrip('/')
        test_html = Path('_site') / (path + '.html')
        if test_html.exists():
            self.path = f'/_site/{path}.html'
            return super().do_GET()
        
        # Not found
        self.send_error(404, f'File not found: {path}')
    
    def end_headers(self):
        # Set proper content type with UTF-8 charset
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), JekyllHandler) as httpd:
        print("\n" + "="*70)
        print(f"🔄 Local Jekyll Preview Server")
        print("="*70)
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"📁 Serving from: _site/")
        print(f"\nPress Ctrl+C to stop")
        print("="*70 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ Server stopped")
