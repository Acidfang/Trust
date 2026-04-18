#!/usr/bin/env python3
"""
Generate EPUB from markdown Cold Hard Truth complete book
"""

import re
from pathlib import Path
from ebooklib import epub

def markdown_to_epub(markdown_file, output_file):
    """Convert markdown to EPUB"""
    
    with open(markdown_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Create EPUB book
    book = epub.EpubBook()
    book.set_identifier('coldtruth-unified-2026')
    book.set_title('The Cold Hard Truth: On the Path to Stability in Chosen Futures')
    book.set_language('en')
    book.add_author('Self-Directed Practice')
    
    # Create title page
    title_chapter = epub.EpubHtml()
    title_chapter.uid = 'title'
    title_chapter.file_name = 'title.xhtml'
    title_chapter.content = '''
    <html>
    <body style="text-align: center; padding: 2em;">
        <h1>The Cold Hard Truth</h1>
        <h2>On the Path to Stability in Chosen Futures</h2>
        <p style="margin-top: 2em; font-style: italic;">Your Decisions. Your Outcomes. No Shortcuts.</p>
        <p style="margin-top: 3em; color: #666;">© 2026</p>
    </body>
    </html>
    '''
    book.add_item(title_chapter)
    
    # Split content into sections
    sections = content.split('\n# ')
    chapters = []
    
    for i, section in enumerate(sections[1:], 1):
        lines = section.split('\n', 1)
        title = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ''
        
        # Convert markdown formatting to HTML
        html_body = body.replace('\n\n', '</p>\n<p>')
        html_body = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_body)
        html_body = re.sub(r'_([^_]+)_', r'<em>\1</em>', html_body)
        
        # Create chapter
        chapter = epub.EpubHtml()
        chapter.uid = f'chap_{i:03d}'
        chapter.file_name = f'chap_{i:03d}.xhtml'
        chapter.title = title
        chapter.content = f'''
        <html>
        <body>
            <h1>{title}</h1>
            <p>{html_body}</p>
        </body>
        </html>
        '''
        
        book.add_item(chapter)
        chapters.append(chapter)
    
    # Add table of contents
    book.toc = tuple(chapters[:50])  # Limit TOC to first 50 chapters
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create styles
    style = '''
    body { font-family: Georgia, serif; line-height: 1.6; }
    h1 { margin-top: 1em; margin-bottom: 0.5em; }
    h2 { margin-top: 0.8em; margin-bottom: 0.3em; }
    p { margin-bottom: 0.5em; text-align: justify; }
    strong { font-weight: bold; }
    em { font-style: italic; }
    '''
    c = epub.EpubItem()
    c.file_name = 'style/main.css'
    c.media_type = 'text/css'
    c.content = style
    book.add_item(c)
    
    # Write EPUB file
    epub.write_epub(output_file, book, {})
    print(f'✓ EPUB generated successfully: {output_file}')


if __name__ == '__main__':
    markdown_file = Path(r'c:\Determined\book_production\output\THE_COLD_HARD_TRUTH_Complete.md')
    output_file = Path(r'c:\Determined\book_production\output\THE_COLD_HARD_TRUTH_Complete.epub')
    
    try:
        markdown_to_epub(str(markdown_file), str(output_file))
        print(f'File size: {output_file.stat().st_size / 1024:.2f} KB')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
