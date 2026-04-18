#!/usr/bin/env python3
"""
Cold Hard Truth Book Production System
Generates EPUB, PDF, and web app from markdown tier files
"""

import re
import os
import json
from pathlib import Path
from datetime import datetime

class BookBuilder:
    def __init__(self, source_dir, output_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tiers = {
            '-1': 'Self (Coherence)',
            '0': 'Formation (Compatibility)',
            '1': 'Resolution (Conflict)',
            '2': 'Maintenance (Stability)',
            '3': 'Evolution (Growth)'
        }
        
        self.tier_files = {
            '-1': 'cold_hard_truth_tier_minus1_v4.md',
            '0': 'cold_hard_truth_tier_0_v3.md',
            '1': 'cold_hard_truth_tier_1_v3.md',
            '2': 'cold_hard_truth_tier_2_v4.md',
            '3': 'cold_hard_truth_tier_3.md'
        }
        
        self.states_by_tier = {}
        self.entry_markers = {}
        self.choice_paths = {}
        
    def read_tier_file(self, tier_num):
        """Read a tier file and extract content"""
        filepath = self.source_dir / self.tier_files[tier_num]
        with open(filepath, 'r') as f:
            content = f.read()
        return content
    
    def extract_states(self, content, tier_num):
        """Extract state definitions from tier content"""
        states = []
        # Pattern to find state headers like ### STATE T1.1 — NAME
        pattern = r'^### STATE (T[\-\d\.]+)\s*—\s*([^\n]+)'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            state_id = match.group(1)
            state_name = match.group(2).strip()
            states.append({
                'id': state_id,
                'name': state_name,
                'tier': tier_num
            })
        
        self.states_by_tier[tier_num] = states
        return states
    
    def extract_entry_markers(self, content):
        """Extract all entry markers from content"""
        markers = set()
        # Pattern to find [entry: marker name]
        pattern = r'\[entry:\s*([^\]]+)\]'
        
        for match in re.finditer(pattern, content):
            marker = match.group(1).strip()
            markers.add(marker)
        
        return markers
    
    def build_decision_matrix(self):
        """Build a matrix of all possible paths through the tiers"""
        matrix = {
            'system_rules': self._extract_system_rules(),
            'tiers': {},
            'entry_markers': {},
            'cross_tier_connections': []
        }
        
        # Parse each tier
        for tier_num in ['-1', '0', '1', '2', '3']:
            content = self.read_tier_file(tier_num)
            states = self.extract_states(content, tier_num)
            markers = self.extract_entry_markers(content)
            
            matrix['tiers'][tier_num] = {
                'name': self.tiers[tier_num],
                'states': [s['id'] for s in states],
                'entry_markers': list(markers)
            }
            
            for marker in markers:
                if marker not in matrix['entry_markers']:
                    matrix['entry_markers'][marker] = []
                matrix['entry_markers'][marker].append(tier_num)
        
        return matrix
    
    def _extract_system_rules(self):
        """Extract the six system rules"""
        content = self.read_tier_file('-1')
        
        rules_pattern = r'\*\*Rule \d+ -- ([^\*]+)\*\*\n\n(.*?)(?=\n\n---|\*\*Rule \d+|$)'
        rules = []
        
        for match in re.finditer(rules_pattern, content, re.DOTALL):
            rule_name = match.group(1).strip()
            rule_text = match.group(2).strip()
            rules.append({
                'name': rule_name,
                'text': rule_text[:200] + '...' if len(rule_text) > 200 else rule_text
            })
        
        return rules[:6]
    
    def build_unified_book(self):
        """Combine all tiers into a single book with unified structure"""
        book_content = []
        
        # Build front matter
        book_content.append(self._build_front_matter())
        
        # Build table of contents
        toc = self._build_table_of_contents()
        book_content.append(toc)
        
        # Build system rules section
        book_content.append(self._build_system_rules_section())
        
        # Include all tiers
        for tier_num in ['-1', '0', '1', '2', '3']:
            content = self.read_tier_file(tier_num)
            # Remove duplicate front matter from individual tier
            content = re.sub(r'^# FRONT MATTER.*?---\n', '', content, flags=re.DOTALL)
            book_content.append('\n\n---\n\n')
            book_content.append(content)
        
        # Build decision matrix section
        matrix = self.build_decision_matrix()
        book_content.append(self._build_matrix_section(matrix))
        
        # Build index
        book_content.append(self._build_index())
        
        book_text = '\n\n'.join(book_content)
        return book_text
    
    def _build_front_matter(self):
        """Build unified front matter"""
        return '''# THE COLD HARD TRUTH
## On the Path to Stability in Chosen Futures

### Your Decisions. Your Outcomes. No Shortcuts.

---

## About This Book

This book is interactive. It does not tell you what to do. It shows you what happens based on what you choose.

Every section presents a real situation. You identify where you are in it. You choose a path. You follow the page reference. You deal with what comes next.

There are no good choices and bad choices.

There are only choices with consequences you can trace.

---

## Book Structure

This book is organized in five progressive tiers, each representing a layer of stability that must be built before the next can hold.

**Tier -1: Self (Coherence)**
Understanding your actual internal state before building anything external.

**Tier 0: Formation (Compatibility)**
Establishing whether a real connection is forming.

**Tier 1: Resolution (Conflict)**
Resolving conflicts at their source rather than managing them on the surface.

**Tier 2: Maintenance (Stability)**
Maintaining what was built over time.

**Tier 3: Evolution (Growth)**
Enabling growth and development within the structure.

---

## How to Read This Book

1. Start at the beginning of your tier or the state that applies to your current situation
2. Read the situation, observed state, and unresolved elements
3. Choose A, B, or C
4. Follow the page reference provided
5. Track your entry markers and path through the prerequisite sheets
6. Complete each tier's prerequisite sheet before continuing

For reference: use the Decision Matrix at the end of the book to see all possible states and paths.

---

## What Entry Markers Are

Throughout this book you will encounter entry markers like [entry: marker name].

Entry markers are labels that show how you arrived at a state and what you are carrying. They do not clear when you move to a new state. They clear only when the tension that produced them is explicitly resolved through the B path.

Keep track of all entry markers you carry. They determine what you must resolve before proceeding to the next tier.

---
'''

    def _build_table_of_contents(self):
        """Build comprehensive table of contents"""
        toc = '# COMPLETE TABLE OF CONTENTS\n\n'
        
        for tier_num in ['-1', '0', '1', '2', '3']:
            content = self.read_tier_file(tier_num)
            states = self.extract_states(content, tier_num)
            
            toc += f'\n## Tier {tier_num}: {self.tiers[tier_num]}\n\n'
            toc += f'- Opening statement\n'
            
            for state in states:
                toc += f'- {state["id"]} — {state["name"]}\n'
            
            toc += f'- Tier {tier_num} Prerequisite Sheet\n'
        
        return toc
    
    def _build_system_rules_section(self):
        """Build the unified system rules section"""
        content = self.read_tier_file('-1')
        
        # Extract the system rules section
        rules_section = re.search(
            r'## System Rules \(Apply Across All Tiers\).*?(?=---)',
            content,
            re.DOTALL
        )
        
        if rules_section:
            return f'# SYSTEM RULES (Apply Across All Tiers)\n\n{rules_section.group()}'
        
        return ''
    
    def _build_matrix_section(self, matrix):
        """Build the decision matrix reference section"""
        section = '# DECISION MATRIX & REFERENCE GUIDE\n\n'
        section += 'This section provides a complete map of all states, choices, and consequences.\n\n'
        
        section += '## System Rules Overview\n\n'
        for rule in matrix['system_rules']:
            section += f'**{rule["name"]}**\n\n{rule["text"]}\n\n'
        
        section += '## All States by Tier\n\n'
        for tier_num in sorted(matrix['tiers'].keys(), key=lambda x: int(x) if x != '-1' else -1):
            tier_info = matrix['tiers'][tier_num]
            section += f'\n### Tier {tier_num}: {tier_info.get("name", self.tiers.get(tier_num, ""))} \n\n'
            section += 'States: ' + ', '.join(tier_info['states']) + '\n\n'
        
        section += '## Entry Markers Across All Tiers\n\n'
        for marker in sorted(matrix['entry_markers'].keys()):
            tiers = matrix['entry_markers'][marker]
            section += f'- **{marker}** — appears in Tier(s): {", ".join(tiers)}\n'
        
        return section
    
    def _build_index(self):
        """Build comprehensive index"""
        index = '# COMPREHENSIVE INDEX\n\n'
        
        index += '## Quick Reference\n\n'
        index += '- **For self work:** Start at Tier -1, State T-1.1\n'
        index += '- **For connection issues:** Start at Tier 0, State T0.1\n'
        index += '- **For relationship conflict:** Start at Tier 1, State T1.1\n'
        index += '- **For maintaining what you built:** Start at Tier 2, State T2.1\n'
        index += '- **For growth and expansion:** Start at Tier 3, State T3.1\n\n'
        
        index += '## Understanding the System\n\n'
        index += '- Entry markers persist through tiers until resolved at their source\n'
        index += '- Choices A, B, C have consistent meaning across all states\n'
        index += '- Prerequisite sheets must be completed before advancing to next tier\n'
        index += '- All choices are traceable through valid transitions\n\n'
        
        return index
    
    def save_markdown(self, content):
        """Save as markdown"""
        output_file = self.output_dir / 'THE_COLD_HARD_TRUTH_Complete.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Markdown book saved: {output_file}')
        return output_file
    
    def save_decision_matrix_json(self):
        """Save decision matrix as JSON"""
        matrix = self.build_decision_matrix()
        output_file = self.output_dir / 'decision_matrix.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(matrix, f, indent=2)
        print(f'✓ Decision matrix saved: {output_file}')
        return output_file
    
    def generate_epub(self, markdown_content):
        """Generate EPUB format (requires ebooklib)"""
        try:
            from ebooklib import epub
            
            book = epub.EpubBook()
            book.set_identifier('coldtruth-2026')
            book.set_title('The Cold Hard Truth: On the Path to Stability in Chosen Futures')
            book.set_language('en')
            book.add_author('Self-Directed Practice')
            
            # Create chapters from markdown
            chapters = markdown_content.split('\n# ')
            for i, chapter in enumerate(chapters[1:], 1):
                c = epub.EpubHtml()
                c.set_id(f'chap_{i}')
                c.set_file_name(f'chap_{i:02d}.xhtml')
                c.content = f'<h1>{chapter.split(chr(10))[0]}</h1>\n<p>' + \
                           chapter.split('\n', 1)[1].replace('\n\n', '</p>\n<p>') + '</p>'
                book.add_item(c)
            
            # Add TOC
            book.toc = tuple(book.items)
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            
            output_file = self.output_dir / 'THE_COLD_HARD_TRUTH_Complete.epub'
            epub.write_epub(output_file, book, {})
            print(f'✓ EPUB generated: {output_file}')
            return output_file
        except ImportError:
            print('⚠ ebooklib not installed. Install with: pip install ebooklib')
            return None
    
    def generate_pdf(self, markdown_content):
        """Generate PDF format (requires reportlab)"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
            
            output_file = self.output_dir / 'THE_COLD_HARD_TRUTH_Complete.pdf'
            doc = SimpleDocTemplate(str(output_file), pagesize=letter,
                                  rightMargin=0.75*inch, leftMargin=0.75*inch,
                                  topMargin=1*inch, bottomMargin=1*inch)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#000000',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph('The Cold Hard Truth', title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Parse markdown and add to story
            sections = markdown_content.split('\n## ')
            for section in sections:
                lines = section.split('\n')
                if lines:
                    # Add heading
                    story.append(Paragraph(f'<b>{lines[0]}</b>', styles['Heading2']))
                    story.append(Spacer(1, 0.15*inch))
                    
                    # Add content
                    for line in lines[1:]:
                        if line.strip():
                            story.append(Paragraph(line.strip(), styles['BodyText']))
                    
                    story.append(PageBreak())
            
            doc.build(story)
            print(f'✓ PDF generated: {output_file}')
            return output_file
        except ImportError:
            print('⚠ reportlab not installed. Install with: pip install reportlab')
            return None
    
    def create_web_structure(self):
        """Create structure for web app version"""
        web_dir = self.output_dir / 'web_app'
        web_dir.mkdir(exist_ok=True)
        
        # Create basic HTML template
        matrix = self.build_decision_matrix()
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Cold Hard Truth - Interactive Guide</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Georgia', serif;
            background: #f5f5f0;
            color: #333;
            line-height: 1.8;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }
        header {
            text-align: center;
            margin-bottom: 3rem;
            border-bottom: 2px solid #333;
            padding-bottom: 2rem;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        h2 {
            font-size: 1.8rem;
            margin: 2rem 0 1rem 0;
        }
        .state-box {
            background: white;
            padding: 2rem;
            margin: 1.5rem 0;
            border-left: 4px solid #333;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .choices {
            display: grid;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .choice {
            padding: 1rem;
            background: #f9f9f9;
            border: 1px solid #ddd;
            cursor: pointer;
            transition: all 0.3s;
        }
        .choice:hover {
            background: #efefef;
            border-color: #333;
        }
        .choice-label {
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .consequence {
            color: #666;
            font-size: 0.95rem;
        }
        nav {
            margin: 2rem 0;
            padding: 1rem;
            background: white;
            border-radius: 4px;
        }
        .tier-section {
            margin: 3rem 0;
        }
        footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Cold Hard Truth</h1>
            <p style="font-size: 1.1rem; color: #666;">On the Path to Stability in Chosen Futures</p>
            <p style="margin-top: 1rem; font-style: italic;">Your Decisions. Your Outcomes. No Shortcuts.</p>
        </header>

        <nav>
            <h3>Navigate by Tier</h3>
            <ul style="list-style: none; padding: 1rem 0;">
                <li><a href="#tier-minus1">Tier -1: Self (Coherence)</a></li>
                <li><a href="#tier-0">Tier 0: Formation (Compatibility)</a></li>
                <li><a href="#tier-1">Tier 1: Resolution (Conflict)</a></li>
                <li><a href="#tier-2">Tier 2: Maintenance (Stability)</a></li>
                <li><a href="#tier-3">Tier 3: Evolution (Growth)</a></li>
            </ul>
        </nav>

        <div id="content">
            <!-- Content will be loaded here -->
            <p>Loading complete guide... <a href="THE_COLD_HARD_TRUTH_Complete.md">Or download the full markdown version</a></p>
        </div>

        <footer>
            <p>The Cold Hard Truth © 2026</p>
            <p>Self-directed practice. Observable evidence. Real resolution.</p>
        </footer>
    </div>

    <script>
        // Basic navigation script
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Interactive guide loaded. States available:');
            console.log(%s);
        });
    </script>
</body>
</html>
''' % json.dumps(matrix, indent=2)
        
        index_file = web_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save matrix as JSON for web app
        matrix_file = web_dir / 'states.json'
        with open(matrix_file, 'w', encoding='utf-8') as f:
            json.dump(matrix, f, indent=2)
        
        print(f'✓ Web structure created: {web_dir}')
        return web_dir
    
    def build_all(self):
        """Build all output formats"""
        print('\n' + '='*60)
        print('COLD HARD TRUTH - BOOK PRODUCTION SYSTEM')
        print('='*60 + '\n')
        
        print('Building unified book from tier files...')
        markdown_content = self.build_unified_book()
        
        print('Saving outputs...\n')
        
        # Save markdown
        self.save_markdown(markdown_content)
        
        # Save decision matrix
        self.save_decision_matrix_json()
        
        # Create web structure
        self.create_web_structure()
        
        # Try to generate EPUB
        print('\nAttempting EPUB generation...')
        self.generate_epub(markdown_content)
        
        # Try to generate PDF
        print('Attempting PDF generation...')
        self.generate_pdf(markdown_content)
        
        print('\n' + '='*60)
        print('BOOK PRODUCTION COMPLETE')
        print('='*60)
        print(f'\nAll outputs saved to: {self.output_dir}')
        print('\nGenerated files:')
        for file in sorted(self.output_dir.glob('**/*')):
            if file.is_file():
                size = file.stat().st_size
                print(f'  - {file.relative_to(self.output_dir)} ({size:,} bytes)')


if __name__ == '__main__':
    source = r'c:\Determined\docs\reference\tcht'
    output = r'c:\Determined\book_production\output'
    
    builder = BookBuilder(source, output)
    builder.build_all()
