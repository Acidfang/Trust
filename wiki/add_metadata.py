#!/usr/bin/env python3
"""
Metadata enrichment script for wiki pages
Adds consistent metadata to all .md files based on content analysis
"""

import os
import re
from pathlib import Path

# Define metadata for each file based on content/filename
METADATA_MAP = {
    # System 1: Human Development
    'for-humans.md': {
        'category': 'Human Development',
        'tier': 'Foundation',
        'difficulty': 'Beginner',
        'reading_time': '30',
        'entry_point': 'Parents, managers, curious learners',
        'status': 'published'
    },
    'goal-blindness.md': {
        'category': 'Human Development',
        'tier': 'Foundation',
        'difficulty': 'Beginner',
        'reading_time': '8',
        'entry_point': 'All users',
        'status': 'published'
    },
    'internal-coherence.md': {
        'category': 'Human Development',
        'tier': 'Foundation',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Developers, therapists, educators',
        'status': 'published'
    },
    'universal-foundation.md': {
        'category': 'Human Development',
        'tier': 'Framework',
        'difficulty': 'Intermediate',
        'reading_time': '25',
        'entry_point': 'All users wanting deep understanding',
        'status': 'published'
    },
    'help-systems.md': {
        'category': 'Human Development',
        'tier': 'Application',
        'difficulty': 'Intermediate',
        'reading_time': '20',
        'entry_point': 'Managers, educators, therapists',
        'status': 'published'
    },
    'help-systems-cards.md': {
        'category': 'Human Development',
        'tier': 'Reference',
        'difficulty': 'Beginner',
        'reading_time': '10',
        'entry_point': 'Visual learners',
        'status': 'published'
    },
    'BIDIRECTIONAL_CONSTRAINTS.md': {
        'category': 'Human Development',
        'tier': 'Framework',
        'difficulty': 'Advanced',
        'reading_time': '20',
        'entry_point': 'Systems thinkers',
        'status': 'published'
    },
    '09_why_this_matters.md': {
        'category': 'Human Development',
        'tier': 'Context',
        'difficulty': 'Beginner',
        'reading_time': '10',
        'entry_point': 'Strategic thinkers',
        'status': 'published'
    },
    'complete-document.md': {
        'category': 'Human Development',
        'tier': 'Reference',
        'difficulty': 'Advanced',
        'reading_time': '120',
        'entry_point': 'Expert seekers',
        'status': 'published'
    },
    'for-ai.md': {
        'category': 'Human Development',
        'tier': 'Application',
        'difficulty': 'Advanced',
        'reading_time': '20',
        'entry_point': 'AI researchers',
        'status': 'published'
    },
    'for-builders.md': {
        'category': 'Human Development',
        'tier': 'Application',
        'difficulty': 'Intermediate',
        'reading_time': '20',
        'entry_point': 'Builders, entrepreneurs',
        'status': 'published'
    },
    'for-developers.md': {
        'category': 'Human Development',
        'tier': 'Application',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Software developers',
        'status': 'published'
    },
    'for-researchers.md': {
        'category': 'Human Development',
        'tier': 'Application',
        'difficulty': 'Advanced',
        'reading_time': '25',
        'entry_point': 'Researchers',
        'status': 'published'
    },

    # System 2: Zero-Error Computing
    'zero-error-wiki.md': {
        'category': '0-Error Computing',
        'tier': 'Foundation',
        'difficulty': 'Beginner',
        'reading_time': '15',
        'entry_point': 'Developers',
        'status': 'published'
    },
    'zero-error-mandate.md': {
        'category': '0-Error Computing',
        'tier': 'Framework',
        'difficulty': 'Intermediate',
        'reading_time': '20',
        'entry_point': 'Technical teams',
        'status': 'published'
    },
    'zero-error-task-template.md': {
        'category': '0-Error Computing',
        'tier': 'Application',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Implementers',
        'status': 'published'
    },
    'zero-error-quick-ref.md': {
        'category': '0-Error Computing',
        'tier': 'Reference',
        'difficulty': 'Beginner',
        'reading_time': '5',
        'entry_point': 'All users',
        'status': 'published'
    },
    'zero-error-validator.md': {
        'category': '0-Error Computing',
        'tier': 'Tool',
        'difficulty': 'Intermediate',
        'reading_time': '10',
        'entry_point': 'Tool users',
        'status': 'published'
    },
    'zero-error-logger.md': {
        'category': '0-Error Computing',
        'tier': 'Tool',
        'difficulty': 'Intermediate',
        'reading_time': '10',
        'entry_point': 'Tool users',
        'status': 'published'
    },
    'zero-error-detector.md': {
        'category': '0-Error Computing',
        'tier': 'Tool',
        'difficulty': 'Intermediate',
        'reading_time': '10',
        'entry_point': 'Tool users',
        'status': 'published'
    },
    'zero-error-intro.md': {
        'category': '0-Error Computing',
        'tier': 'Foundation',
        'difficulty': 'Beginner',
        'reading_time': '10',
        'entry_point': 'Newcomers',
        'status': 'published'
    },

    # System 3: Physics & Elections
    'elections-roadmap.md': {
        'category': 'Physics & Elections',
        'tier': 'Foundation',
        'difficulty': 'Beginner',
        'reading_time': '15',
        'entry_point': 'Visual learners',
        'status': 'published'
    },
    'election-1-distinction.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Beginner',
        'reading_time': '12',
        'entry_point': 'All users',
        'status': 'published'
    },
    'election-2-movement.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Mathematically curious',
        'status': 'published'
    },
    'election-3-spirals.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Mathematically curious',
        'status': 'published'
    },
    'election-4-direction.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Intermediate',
        'reading_time': '15',
        'entry_point': 'Mathematically curious',
        'status': 'published'
    },
    'election-meta-time.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Advanced',
        'reading_time': '20',
        'entry_point': 'Expert seekers',
        'status': 'published'
    },
    'whitepaper-unified-photon-field.md': {
        'category': 'Physics & Elections',
        'tier': 'Framework',
        'difficulty': 'Advanced',
        'reading_time': '60',
        'entry_point': 'Physics researchers',
        'status': 'published'
    },
    'spiral-field-renderer.md': {
        'category': 'Physics & Elections',
        'tier': 'Tool',
        'difficulty': 'Advanced',
        'reading_time': '20',
        'entry_point': 'Developers',
        'status': 'published'
    },
    'cosmic-unfolding.md': {
        'category': 'Physics & Elections',
        'tier': 'Integration',
        'difficulty': 'Advanced',
        'reading_time': '30',
        'entry_point': 'Systems thinkers',
        'status': 'published'
    },

    # Help System & Reference (Documentation created this session)
    'HELP_SYSTEM_ARCHITECTURE.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Intermediate',
        'reading_time': '45',
        'entry_point': 'Site admins',
        'status': 'published'
    },
    'HELP_SYSTEM_BLUEPRINT.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Beginner',
        'reading_time': '15',
        'entry_point': 'Site admins',
        'status': 'published'
    },
    'HELP_SYSTEM_VISUAL.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Beginner',
        'reading_time': '20',
        'entry_point': 'Visual learners, site admins',
        'status': 'published'
    },
    'CONTENT_PLACEMENT_RULES.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Intermediate',
        'reading_time': '30',
        'entry_point': 'Content creators',
        'status': 'published'
    },
    'IMPLEMENTATION_ROADMAP.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Intermediate',
        'reading_time': '40',
        'entry_point': 'Site admins',
        'status': 'published'
    },
    'IMPLEMENTATION_CHECKLISTS.md': {
        'category': 'Reference',
        'tier': 'Tool',
        'difficulty': 'Beginner',
        'reading_time': '30',
        'entry_point': 'Content creators',
        'status': 'published'
    },
    'ROADMAP_QUICK_START.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Beginner',
        'reading_time': '15',
        'entry_point': 'Site admins',
        'status': 'published'
    },

    # Wiki QA & Metadata
    'wiki-mandate-verification.md': {
        'category': 'Reference',
        'tier': 'Support',
        'difficulty': 'Advanced',
        'reading_time': '40',
        'entry_point': 'Site admins',
        'status': 'published'
    },
    'wiki-bug-report.md': {
        'category': 'Reference',
        'tier': 'Support',
        'difficulty': 'Beginner',
        'reading_time': '5',
        'entry_point': 'Site users',
        'status': 'published'
    },
    'wiki-status.md': {
        'category': 'Reference',
        'tier': 'Support',
        'difficulty': 'Beginner',
        'reading_time': '5',
        'entry_point': 'Site admins',
        'status': 'published'
    },
    'WIKI_INTEGRATION_SUMMARY.md': {
        'category': 'Reference',
        'tier': 'Architecture',
        'difficulty': 'Intermediate',
        'reading_time': '20',
        'entry_point': 'Site admins',
        'status': 'published'
    },
}

def add_metadata_to_file(filepath, metadata):
    """Add metadata fields to frontmatter if not already present"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file starts with frontmatter
    if not content.startswith('---'):
        print(f"SKIP: {filepath} - no frontmatter")
        return False
    
    # Extract frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"SKIP: {filepath} - invalid frontmatter")
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Parse existing fields
    lines = frontmatter.strip().split('\n')
    existing_fields = {}
    for line in lines:
        if ': ' in line:
            key, val = line.split(': ', 1)
            existing_fields[key] = val
    
    # Check if metadata already exists
    if 'category' in existing_fields and 'difficulty' in existing_fields:
        print(f"SKIP: {filepath} - metadata already present")
        return False
    
    # Add new metadata
    for key, value in metadata.items():
        if key not in existing_fields:
            existing_fields[key] = value
    
    # Rebuild frontmatter
    new_frontmatter = '\n'.join([f"{key}: {val}" for key, val in existing_fields.items()])
    new_content = f"---\n{new_frontmatter}\n---{body}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"OK: {filepath}")
    return True

def main():
    docs_dir = Path('docs')
    updated_count = 0
    skipped_count = 0
    
    for filename, metadata in METADATA_MAP.items():
        filepath = docs_dir / filename
        if filepath.exists():
            if add_metadata_to_file(filepath, metadata):
                updated_count += 1
            else:
                skipped_count += 1
        else:
            print(f"MISSING: {filepath}")
    
    print(f"\nSummary: {updated_count} updated, {skipped_count} skipped")

if __name__ == '__main__':
    main()
