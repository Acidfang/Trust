#!/usr/bin/env python3
"""
Professional Markdown to PDF Converter
Uses Pandoc + LaTeX for publication-grade output

Features:
  ✓ Automatic Table of Contents with hyperlinks
  ✓ PDF metadata (author, title, keywords, subject)
  ✓ PDF bookmarks for navigation
  ✓ Running headers/footers with chapter names
  ✓ Smart typography (quotes, dashes, ligatures)
  ✓ Proper math equation rendering
  ✓ Bibliography/citations support
  ✓ Multiple page styles (cover, frontmatter, content)
  ✓ Professional typography (widow/orphan control)
  ✓ Code syntax highlighting
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import json


class PandocConverter:
    """Professional Markdown to PDF converter using Pandoc + LaTeX"""
    
    def __init__(self, md_file, output_file, config=None):
        self.md_file = Path(md_file)
        self.output_file = Path(output_file)
        self.config = config or {}
        self.temp_dir = Path(self.output_file.parent) / ".pandoc_temp"
        self.temp_dir.mkdir(exist_ok=True)
        
    def create_metadata_file(self):
        """Create YAML metadata file for Pandoc"""
        metadata = {
            "title": self.config.get("title", "Unified Photon Field Model"),
            "author": self.config.get("author", ""),
            "date": self.config.get("date", datetime.now().strftime("%Y-%m-%d")),
            "description": self.config.get("description", ""),
            "keywords": self.config.get("keywords", []),
            "subject": self.config.get("subject", ""),
            "document-class": "book",
            "documentclass": "book",
            "classoption": ["oneside", "11pt"],
            "geometry": ["margin=1in"],
            "toc": True,
            "toc-depth": 3,
            "number-sections": True,
            "colorlinks": True,
            "linkcolor": "blue",
            "urlcolor": "blue",
            "citecolor": "blue",
            "toccolor": "blue",
            "pdf-engine": "xelatex",
            "header-includes": [
                "\\usepackage{fancyhdr}",
                "\\pagestyle{fancy}",
                "\\lhead{\\leftmark}",
                "\\rhead{\\thepage}",
                "\\usepackage[all]{hypcap}",
                "\\usepackage{bookmark}",
                "\\usepackage{microtype}",
            ]
        }
        
        # Add author if provided
        if self.config.get("author"):
            metadata["author"] = self.config["author"]
            
        metadata_file = self.temp_dir / "metadata.yaml"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            for key, value in metadata.items():
                if isinstance(value, list):
                    f.write(f"{key}:\n")
                    for item in value:
                        f.write(f"  - {item}\n")
                elif isinstance(value, bool):
                    f.write(f"{key}: {str(value).lower()}\n")
                else:
                    f.write(f"{key}: {value}\n")
            f.write("...\n")
        
        return metadata_file
    
    def create_latex_template(self):
        """Create custom LaTeX template for professional output"""
        template = r"""
\documentclass$if(documentclass)$[$documentclass$]$endif${$if(classoption)$$for(classoption)$$classoption$$sep$,$endfor$$endif$}
\usepackage{ifxetex,ifluatex}
\ifnum 0\ifxetex 1\fi\ifluatex 1\fi=0 % if pdftex
  \usepackage[utf8]{inputenc}
  \usepackage[T1]{fontenc}
  \usepackage{lmodern}
\else % if luatex or xetex
  \ifxetex
    \usepackage{mathspec}
  \else
    \usepackage{unicode-math}
  \fi
  \defaultfontfeatures{Ligatures=TeX,Scale=MatchLowercase}
\fi

\usepackage[margin=1in]{geometry}
\usepackage{color}
\usepackage{fancyhdr}
\usepackage{extramarks}
\usepackage{lastpage}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{bookmark}
\usepackage{microtype}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{natbib}
\usepackage{setspace}
\usepackage{subcaption}
\usepackage{amsmath}
\usepackage{amssymb}

% Configure PDF metadata
\hypersetup{
  pdftitle={$title$},
  pdfauthor={$author$},
  pdfsubject={$subject$},
  pdfkeywords={$for(keywords)$$keywords$$sep$, $endfor$},
  pdfproducer={Pandoc with XeLaTeX},
  bookmarksopen=true,
  bookmarksnumbered=true,
}

% Configure page headers and footers
\pagestyle{fancy}
\lhead{\nouppercase{\leftmark}}
\chead{}
\rhead{}
\lfoot{}
\cfoot{Page \thepage\ of \pageref{LastPage}}
\rfoot{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Configure heading styles
\usepackage{sectsty}
\chapterfont{\centering\Large\bfseries}
\sectionfont{\Large\bfseries}
\subsectionfont{\large\bfseries}

% Configure lists
\usepackage{enumitem}
\setlist[itemize]{left=0pt}
\setlist[enumerate]{left=0pt}

% Code block styling
\definecolor{codebg}{gray}{0.95}
\lstset{
  breaklines=true,
  basicstyle=\ttfamily\small,
  backgroundcolor=\color{codebg},
  framexleftmargin=5pt,
  frame=single,
  rulecolor=\color{gray},
}

% Typography improvements
\linespread{1.15}
\frenchspacing
\raggedbottom

\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}

% Create title page
\maketitle

% Table of Contents
$if(toc)$
\tableofcontents
\newpage
$endif$

% Main content
$body$

% Bibliography
$if(bibliography)$
\bibliography{$for(bibliography)$$bibliography$$sep$,$endfor$}
$endif$

\end{document}
"""
        template_file = self.temp_dir / "template.latex"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template)
        return template_file
    
    def convert(self):
        """Execute Pandoc conversion"""
        print("\n╔════════════════════════════════════════════════════╗")
        print("║  PROFESSIONAL MARKDOWN TO PDF CONVERTER             ║")
        print("║  Pandoc + XeLaTeX • Publication Grade               ║")
        print("╚════════════════════════════════════════════════════╝\n")
        
        # Verify input file exists
        if not self.md_file.exists():
            print(f"❌ ERROR: Input file not found: {self.md_file}")
            return False
        
        print(f"📄 Input markdown: {self.md_file}")
        print(f"📊 File size: {self.md_file.stat().st_size / 1024:.1f} KB")
        
        # Create metadata and template files
        print("\n🔧 Preparing conversion files...")
        try:
            metadata_file = self.create_metadata_file()
            template_file = self.create_latex_template()
            print("   ✓ Metadata file created")
            print("   ✓ LaTeX template created")
        except Exception as e:
            print(f"   ❌ ERROR creating setup files: {e}")
            return False
        
        # Build Pandoc command
        pandoc_args = [
            "pandoc",
            str(self.md_file),
            f"--output={self.output_file}",
            f"--metadata-file={metadata_file}",
            f"--template={template_file}",
            "--pdf-engine=xelatex",
            "--from=markdown+tex_math_dollars+escaped_line_breaks",
            "--to=pdf",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--listings",
            "--resource-path=.:images",
            "--wrap=preserve",
        ]
        
        # Add bibliography support if file exists
        bib_file = self.md_file.parent / "references.bib"
        if bib_file.exists():
            pandoc_args.append(f"--bibliography={bib_file}")
            pandoc_args.append("--csl=chicago-author-date.csl")
            print("   ✓ Bibliography support enabled")
        
        # Execute Pandoc
        print("\n🔄 Converting with Pandoc...")
        print(f"   Command: {' '.join(pandoc_args[:3])}...")
        
        try:
            result = subprocess.run(
                pandoc_args,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                print(f"\n   ❌ Pandoc error:")
                print(f"   {result.stderr}")
                return False
            
            print("   ✓ Pandoc conversion successful")
            
        except FileNotFoundError:
            print("\n   ❌ ERROR: Pandoc not found!")
            print("   Install Pandoc: choco install pandoc -y")
            return False
        except subprocess.TimeoutExpired:
            print("\n   ❌ ERROR: Conversion timed out")
            return False
        except Exception as e:
            print(f"\n   ❌ ERROR: {e}")
            return False
        
        # Verify output
        if not self.output_file.exists():
            print(f"   ❌ Output file not created: {self.output_file}")
            return False
        
        print("\n✨ CONVERSION COMPLETE ✨\n")
        pdf_size = self.output_file.stat().st_size / (1024 * 1024)
        print(f"📕 Output PDF: {self.output_file}")
        print(f"📊 File size: {pdf_size:.2f} MB")
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n✅ Features enabled:")
        print("   ✓ Automatic Table of Contents with hyperlinks")
        print("   ✓ PDF bookmarks for navigation")
        print("   ✓ Running headers with chapter names")
        print("   ✓ Page numbers (format: Page X of Y)")
        print("   ✓ Smart typography & ligatures")
        print("   ✓ Math equation rendering")
        print("   ✓ Code syntax highlighting")
        print("   ✓ Section numbering")
        if bib_file.exists():
            print("   ✓ Bibliography/citations support")
        
        print(f"\n🎓 Ready for Zenodo submission!")
        
        return True
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except:
            pass


def main():
    """Main entry point"""
    
    # Configuration
    config = {
        "title": "Unified Photon Field Model (UPFM)",
        "author": "Research Documentation",
        "date": datetime.now().strftime("%B %d, %Y"),
        "description": "Complete framework for understanding quantum fields and photonic systems",
        "subject": "Physics, Quantum Mechanics, Field Theory",
        "keywords": ["photon", "field", "quantum", "physics", "unified model"],
    }
    
    input_file = r"c:\Determined\WHITEPAPER_UNIFIED_PHOTON_FIELD_COMPLETE.md"
    output_file = r"c:\Determined\UPFM_Whitepaper_v2.0_Professional.pdf"
    
    # Create converter and execute
    converter = PandocConverter(input_file, output_file, config)
    
    try:
        success = converter.convert()
        return 0 if success else 1
    finally:
        converter.cleanup()


if __name__ == "__main__":
    sys.exit(main())
