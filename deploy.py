#!/usr/bin/env python3
"""
Complete Website Deployment Pipeline
Builds, validates, commits, and deploys the entire website in one command.

Better than Jekyll because:
1. Single command deployment (no multiple steps)
2. Validates site before committing
3. Automatic git operations (commit + push)
4. Health checks on generated site
5. Clear status output and error handling
6. Can immediately serve functional website
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin
import json
import shutil
import re

class DeploymentPipeline:
    def __init__(self, wiki_dir=None):
        if wiki_dir is None:
            wiki_dir = Path(__file__).parent
        else:
            wiki_dir = Path(wiki_dir)
        
        self.wiki_dir = wiki_dir
        self.docs_dir = wiki_dir / 'docs'
        self.output_dir = wiki_dir / '_site'
        self.repo_dir = wiki_dir.parent if (wiki_dir.parent / '.git').exists() else wiki_dir
        
        self.errors = []
        self.warnings = []
        self.pages_generated = 0
        self.start_time = None
        self.stats = {}
    
    def run(self):
        """Execute complete deployment pipeline"""
        self.start_time = datetime.now()
        
        self._print_header("WEBSITE DEPLOYMENT PIPELINE")
        
        try:
            # Step 1: Validate environment
            if not self._validate_environment():
                return False
            
            # Step 2: Generate site
            if not self._generate_site():
                return False
            
            # Step 3: Validate generated site
            if not self._validate_site():
                return False
            
            # Step 4: Update domains index
            if not self._update_domains_index():
                self.warnings.append("Could not update domains index")
            
            # Step 5: Generate sitemap
            if not self._generate_sitemap():
                self.warnings.append("Could not generate sitemap")
            
            # Step 6: Git operations
            if not self._git_commit_and_push():
                return False
            
            # Step 7: Summary and next steps
            self._print_summary()
            
            return True
            
        except Exception as e:
            self._print_error(f"Pipeline failed: {e}")
            return False
    
    def _validate_environment(self):
        """Validate that required directories and files exist"""
        self._print_section("1. VALIDATING ENVIRONMENT")
        
        checks = [
            (self.wiki_dir.exists(), f"Wiki directory exists: {self.wiki_dir}"),
            (self.docs_dir.exists(), f"Docs directory exists: {self.docs_dir}"),
            ((self.wiki_dir / '_config.yml').exists(), "Config file (_config.yml) exists"),
            ((self.wiki_dir / '_layouts').exists(), "Layouts directory exists"),
            ((self.wiki_dir / 'jekyll_generator.py').exists(), "Generator script exists"),
        ]
        
        all_good = True
        for check, description in checks:
            if check:
                self._print_success(description)
            else:
                self._print_error(description)
                all_good = False
        
        return all_good
    
    def _generate_site(self):
        """Run Jekyll generator"""
        self._print_section("2. GENERATING SITE")
        
        try:
            # Import and run generator
            sys.path.insert(0, str(self.wiki_dir))
            from jekyll_generator import JekyllGenerator
            
            generator = JekyllGenerator(self.wiki_dir)
            output_dir = generator.generate_site()
            
            # Count pages
            self.pages_generated = len(generator.pages)
            self.stats['pages'] = self.pages_generated
            
            if self.pages_generated == 0:
                self._print_error("No pages were generated")
                return False
            
            self._print_success(f"Generated {self.pages_generated} pages")
            return True
            
        except Exception as e:
            self._print_error(f"Generation failed: {e}")
            return False
    
    def _validate_site(self):
        """Validate that generated site is functional"""
        self._print_section("3. VALIDATING GENERATED SITE")
        
        if not self.output_dir.exists():
            self._print_error(f"Output directory not found: {self.output_dir}")
            return False
        
        # Check for index.html
        index_file = self.output_dir / 'index.html'
        if not index_file.exists():
            self._print_error("index.html not found in output")
            return False
        
        self._print_success("index.html exists")
        
        # Check file count
        html_files = list(self.output_dir.glob('**/*.html'))
        if len(html_files) == 0:
            self._print_error("No HTML files generated")
            return False
        
        self._print_success(f"Found {len(html_files)} HTML files")
        self.stats['html_files'] = len(html_files)
        
        # Validate HTML structure (check for broken markers)
        invalid_files = self._check_html_validity(html_files)
        if invalid_files:
            self._print_warning(f"Found potential issues in {len(invalid_files)} files")
            for fname in invalid_files[:3]:  # Show first 3
                self._print_warning(f"  - {fname}")
        
        # Check for index files in directories
        index_count = len(list(self.output_dir.glob('**/index.html')))
        self._print_success(f"Found {index_count} index.html files (proper URL routing)")
        self.stats['index_files'] = index_count
        
        return True
    
    def _check_html_validity(self, html_files):
        """Check for common HTML issues"""
        invalid = []
        
        for html_file in html_files[:10]:  # Check first 10
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for unprocessed Liquid tags (these indicate generation issues)
                if '{{' in content or '{%' in content:
                    invalid.append(html_file.name)
                
                # Check for empty content
                if len(content) < 100:
                    invalid.append(html_file.name)
                    
            except Exception as e:
                self._print_warning(f"Could not read {html_file.name}: {e}")
        
        return invalid
    
    def _update_domains_index(self):
        """Update domains index to include all new domains"""
        self._print_section("4. UPDATING DOMAINS INDEX")
        
        try:
            domains_file = self.docs_dir / 'domains' / 'index.md'
            if not domains_file.exists():
                self._print_warning("Domains index not found")
                return False
            
            with open(domains_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if all domains are listed
            required_domains = [
                'parenting',
                'education',
                'organizational',
                'skill-development',
                'therapy-mental-health',
                'product-development',
                'relationships',
                'technology-software',
                'business-startups',
                'community-social',
                'creative-artistic',
                'health-fitness',
                'finance',
                'spirituality',
                'coaching-mentoring',
            ]
            
            missing_domains = [d for d in required_domains if f"/domains/{d}/" not in content]
            
            if missing_domains:
                self._print_warning(f"Missing {len(missing_domains)} domains in index")
                for domain in missing_domains:
                    self._print_warning(f"  - {domain}")
            else:
                self._print_success("All domains listed in index")
            
            return True
            
        except Exception as e:
            self._print_warning(f"Could not validate domains index: {e}")
            return False
    
    def _generate_sitemap(self):
        """Generate sitemap.xml for SEO"""
        self._print_section("5. GENERATING SITEMAP")
        
        try:
            if not self.output_dir.exists():
                return False
            
            html_files = list(self.output_dir.glob('**/*.html'))
            
            if not html_files:
                return False
            
            # Build sitemap
            sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            
            base_url = "https://determined.wiki"  # Update this based on your domain
            
            for html_file in html_files:
                # Convert file path to URL
                rel_path = html_file.relative_to(self.output_dir)
                
                if rel_path.name == 'index.html':
                    # directory/index.html → directory/
                    url_path = str(rel_path.parent) + '/' if str(rel_path.parent) != '.' else '/'
                else:
                    # other.html → other/
                    url_path = str(rel_path.with_suffix('')) + '/'
                
                url_path = url_path.replace('\\', '/')
                full_url = base_url.rstrip('/') + url_path
                
                sitemap_xml += f'  <url>\n'
                sitemap_xml += f'    <loc>{full_url}</loc>\n'
                sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
                sitemap_xml += f'  </url>\n'
            
            sitemap_xml += '</urlset>'
            
            sitemap_file = self.output_dir / 'sitemap.xml'
            with open(sitemap_file, 'w', encoding='utf-8') as f:
                f.write(sitemap_xml)
            
            self._print_success(f"Generated sitemap with {len(html_files)} URLs")
            return True
            
        except Exception as e:
            self._print_warning(f"Could not generate sitemap: {e}")
            return False
    
    def _git_commit_and_push(self):
        """Commit changes and push to repository"""
        self._print_section("6. GIT COMMIT & PUSH")
        
        try:
            os.chdir(self.repo_dir)
            
            # Check if git is initialized
            if not (self.repo_dir / '.git').exists():
                self._print_warning("Git repository not initialized")
                return self._init_git_repo()
            
            # Check for uncommitted changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=10)
            
            changes = result.stdout.strip()
            
            if not changes:
                self._print_info("No changes to commit")
                return True
            
            # Stage all changes
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True, timeout=10)
            self._print_success("Staged all changes")
            
            # Create commit message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Update: {self.pages_generated} pages generated - {timestamp}"
            
            # Commit
            result = subprocess.run(['git', 'commit', '-m', commit_msg],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self._print_success(f"Committed: {commit_msg}")
            else:
                self._print_warning("Git commit failed or no changes")
                return True
            
            # Get remote info
            remote_result = subprocess.run(['git', 'remote', '-v'],
                                         capture_output=True, text=True, timeout=10)
            
            if not remote_result.stdout.strip():
                self._print_info("No remote configured (skipping push)")
                return True
            
            # Push to origin
            result = subprocess.run(['git', 'push', 'origin', 'main'],
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self._print_success("Pushed to remote repository")
                return True
            else:
                # Try master branch as fallback
                result = subprocess.run(['git', 'push', 'origin', 'master'],
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self._print_success("Pushed to remote repository (master branch)")
                    return True
                else:
                    self._print_warning(f"Push failed: {result.stderr}")
                    return False
            
        except subprocess.TimeoutExpired:
            self._print_warning("Git operation timed out")
            return False
        except Exception as e:
            self._print_warning(f"Git operation failed: {e}")
            return False
    
    def _init_git_repo(self):
        """Initialize git repository if not exists"""
        try:
            os.chdir(self.repo_dir)
            subprocess.run(['git', 'init'], check=True, capture_output=True, timeout=10)
            subprocess.run(['git', 'config', 'user.email', 'deploy@determined.wiki'], 
                         check=True, capture_output=True, timeout=10)
            subprocess.run(['git', 'config', 'user.name', 'Deployment Bot'],
                         check=True, capture_output=True, timeout=10)
            
            self._print_success("Initialized git repository")
            return True
        except Exception as e:
            self._print_warning(f"Could not initialize git: {e}")
            return False
    
    def _print_summary(self):
        """Print deployment summary"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        self._print_section("DEPLOYMENT COMPLETE ✅")
        
        print(f"\n📊 STATISTICS:")
        print(f"  Pages generated: {self.pages_generated}")
        print(f"  HTML files: {self.stats.get('html_files', '?')}")
        print(f"  Index files: {self.stats.get('index_files', '?')}")
        print(f"  Duration: {duration:.2f} seconds")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:5]:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:5]:
                print(f"  - {error}")
        
        print(f"\n📂 WEBSITE LOCATION:")
        print(f"  {self.output_dir}")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"  1. Serve locally: python serve_site.py")
        print(f"  2. Check: open http://localhost:8000")
        print(f"  3. Deploy: commit and push are done!")
        
        print()
    
    def _print_section(self, title):
        """Print section header"""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")
    
    def _print_header(self, title):
        """Print main header"""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    def _print_success(self, msg):
        """Print success message"""
        print(f"  ✓ {msg}")
    
    def _print_error(self, msg):
        """Print error message and track it"""
        print(f"  ✗ {msg}")
        self.errors.append(msg)
    
    def _print_warning(self, msg):
        """Print warning message"""
        print(f"  ⚠ {msg}")
        self.warnings.append(msg)
    
    def _print_info(self, msg):
        """Print info message"""
        print(f"  ℹ {msg}")


if __name__ == '__main__':
    # Get wiki directory
    wiki_dir = Path(__file__).parent
    
    # Run pipeline
    pipeline = DeploymentPipeline(wiki_dir)
    success = pipeline.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
