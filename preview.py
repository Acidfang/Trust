#!/usr/bin/env python3
"""
Simple Jekyll-like renderer for preview
Converts markdown files with YAML frontmatter to HTML for local preview
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import markdown
import yaml

class JekyllPreviewHandler(SimpleHTTPRequestHandler):
    """HTTP handler that converts markdown to HTML on the fly"""
    
    def do_GET(self):
        # Normalize path
        path = self.path.lstrip("/")
        
        # Handle root and docs index
        if path == "" or path == "/" or path == "docs" or path == "docs/":
            self.send_docs_index()
            return
        
        # Check if it's a markdown file request
        if path.startswith("docs/") and path.endswith(".md"):
            self.send_rendered_markdown(path)
            return
        
        # Otherwise serve as static file
        super().do_GET()
    
    def send_docs_index(self):
        """Send a directory listing of docs"""
        docs_dir = Path("docs")
        if not docs_dir.exists():
            self.send_error(404, "docs directory not found")
            return
        
        files = sorted([f.name for f in docs_dir.glob("*.md")])
        
        html = """<html>
<head>
    <title>Wiki Preview - Docs</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
            margin: 40px; 
            max-width: 800px;
        }
        h1 { color: #0366d6; }
        a { color: #0366d6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { list-style: none; padding: 0; }
        li { padding: 12px 0; border-bottom: 1px solid #eee; }
        .status { background: #28a745; color: white; padding: 8px 12px; border-radius: 4px; display: inline-block; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="status">✓ Preview Server Running</div>
    <h1>📚 Wiki Documentation</h1>
    <p>Click a document to preview with Jekyll rendering:</p>
    <ul>
"""
        
        for file in files:
            url = f"/docs/{file}"
            display_name = file.replace(".md", "").replace("-", " ").title()
            html += f'<li><a href="{url}">📄 {display_name}</a></li>\n'
        
        html += """    </ul>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode()))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_rendered_markdown(self, file_path):
        """Render a markdown file with Jekyll processing"""
        # Construct full path
        full_path = Path(file_path)
        
        if not full_path.exists():
            self.send_error(404, f"File not found: {file_path}")
            return
        
        # Read the markdown file
        try:
            content = full_path.read_text(encoding="utf-8")
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")
            return
        
        # Parse YAML frontmatter
        frontmatter = {}
        markdown_content = content
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    markdown_content = parts[2].strip()
                except Exception as e:
                    pass
        
        # Convert markdown to HTML
        try:
            html_body = markdown.markdown(
                markdown_content,
                extensions=['extra', 'codehilite', 'toc']
            )
        except Exception as e:
            html_body = f"<p><strong>Markdown Error:</strong> {e}</p><pre>{markdown_content}</pre>"
        
        # Get title and description
        title = frontmatter.get("title", full_path.stem.replace("-", " ").title())
        description = frontmatter.get("description", "")
        
        # Create full HTML document with Jekyll-like styling
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: #fff;
        }}
        .page-container {{
            max-width: 960px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .page-header {{
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eaecef;
        }}
        .page-header h1 {{
            font-size: 2em;
            color: #0366d6;
            margin-bottom: 10px;
        }}
        .page-header p {{
            color: #6a737d;
            font-size: 0.95em;
        }}
        .page-content {{
            color: #24292e;
        }}
        .page-content h2 {{
            font-size: 1.5em;
            margin: 24px 0 16px 0;
            padding-top: 24px;
            border-top: 1px solid #eaecef;
            font-weight: 600;
        }}
        .page-content h3 {{
            font-size: 1.25em;
            margin: 16px 0 8px 0;
            font-weight: 600;
        }}
        .page-content p {{
            margin-bottom: 16px;
        }}
        .page-content code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.85em;
        }}
        .page-content pre {{
            background: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin-bottom: 16px;
            border: 1px solid #eaecef;
        }}
        .page-content pre code {{
            background: none;
            padding: 0;
            font-size: 0.9em;
        }}
        .page-content blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0 0 16px 0;
        }}
        .page-content a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .page-content a:hover {{
            text-decoration: underline;
        }}
        .page-content ul, .page-content ol {{
            margin-left: 2em;
            margin-bottom: 16px;
        }}
        .page-content li {{
            margin-bottom: 8px;
        }}
        .page-content table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        .page-content table th,
        .page-content table td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
            text-align: left;
        }}
        .page-content table th {{
            background: #f6f8fa;
            font-weight: 600;
        }}
        .back-link {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eaecef;
        }}
        .back-link a {{
            color: #0366d6;
        }}
    </style>
</head>
<body>
    <div class="page-container">
        <div class="page-header">
            <h1>{title}</h1>
            {'<p>' + description + '</p>' if description else ''}
        </div>
        <div class="page-content">
            {html_body}
        </div>
        <div class="back-link">
            <a href="/docs/">&larr; Back to docs</a>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode()))
        self.end_headers()
        self.wfile.write(html.encode())

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    port = 4000
    server = HTTPServer(("127.0.0.1", port), JekyllPreviewHandler)
    print(f"🚀 Jekyll Preview Server running at http://localhost:{port}")
    print(f"   Browse at: http://localhost:{port}/docs/")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)
