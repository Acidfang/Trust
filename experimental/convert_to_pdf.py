import markdown
from weasyprint import HTML, CSS
from pathlib import Path
from io import BytesIO

# Convert markdown files to PDF
files_to_convert = [
    "src/applications/ARIA_ANTIPATTERN_CHAINS.md",
]

for md_file in files_to_convert:
    md_path = Path(md_file)
    pdf_path = Path(str(md_path).replace('.md', '.pdf'))
    
    if not md_path.exists():
        print(f"✗ File not found: {md_path}")
        continue
    
    try:
        # Read the markdown file
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'codehilite', 'fenced_code', 'toc'])
        
        # Add CSS styling
        html_document = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 900px;
                    margin: 40px;
                }}
                h1 {{
                    color: #1e3a8a;
                    border-bottom: 3px solid #3b82f6;
                    padding-bottom: 10px;
                    page-break-after: avoid;
                }}
                h2 {{
                    color: #1e40af;
                    margin-top: 30px;
                    page-break-after: avoid;
                }}
                h3 {{
                    color: #1e40af;
                    margin-top: 20px;
                }}
                pre {{
                    background-color: #f3f4f6;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    border-left: 4px solid #3b82f6;
                }}
                code {{
                    font-family: 'Courier New', monospace;
                    background-color: #f3f4f6;
                    padding: 2px 6px;
                    border-radius: 3px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f3f4f6;
                    font-weight: bold;
                }}
                ul, ol {{
                    margin: 15px 0;
                }}
                li {{
                    margin: 8px 0;
                }}
                hr {{
                    border: none;
                    border-top: 2px solid #e5e7eb;
                    margin: 40px 0;
                }}
                strong {{
                    color: #1e40af;
                    font-weight: bold;
                }}
                em {{
                    font-style: italic;
                    color: #666;
                }}
                blockquote {{
                    border-left: 4px solid #3b82f6;
                    margin-left: 20px;
                    padding-left: 15px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF using WeasyPrint
        HTML(string=html_document).write_pdf(str(pdf_path))
        
        size_kb = pdf_path.stat().st_size / 1024
        print(f"✓ Created: {pdf_path}")
        print(f"  Size: {size_kb:.1f} KB")
    except Exception as e:
        print(f"✗ Error converting {md_path}: {e}")
        import traceback
        traceback.print_exc()
