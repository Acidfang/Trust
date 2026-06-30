#!/usr/bin/env python3
"""
Simple preview server - serves the wiki directory with Python's built-in server
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Change to the wiki directory
wiki_dir = Path(__file__).parent
os.chdir(wiki_dir)

class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevent caching so refreshes always get fresh content
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()
    
    # Enable directory listing
    def translate_path(self, path):
        # Get the path normally
        return super().translate_path(path)

if __name__ == "__main__":
    port = 4000
    server = HTTPServer(("127.0.0.1", port), PreviewHandler)
    
    # Monkey-patch to enable directory listing
    original_do_GET = PreviewHandler.do_GET
    def do_GET_with_listing(self):
        # Call the original method
        try:
            original_do_GET(self)
        except:
            pass
    
    # Override to handle directory listing
    def custom_do_GET(self):
        if self.path.endswith('/'):
            # This is a directory request
            path = self.translate_path(self.path)
            if os.path.isdir(path):
                # Check if index.html exists
                if not os.path.exists(os.path.join(path, 'index.html')):
                    # List directory
                    self.list_directory(path)
                    return
        # Default behavior for files
        super(PreviewHandler, self).do_GET()
    
    PreviewHandler.do_GET = custom_do_GET
    
    print(f"✓ Preview Server running at http://localhost:{port}")
    print(f"  Open http://localhost:{port}/docs/ to view the wiki")
    print(f"\n  Current directory: {os.getcwd()}")
    print(f"  Serving files from: {wiki_dir}")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)

