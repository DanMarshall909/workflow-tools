#!/usr/bin/env python3
"""
LLM Rule Section Extractor
Extracts specific sections from workflow-tools rules for minimal context loading.

Usage:
    python extract-rule-section.py <rule-file> <section-name>
    python extract-rule-section.py typescript-test-naming.md requirements
    python extract-rule-section.py --json typescript-test-naming.md all
"""

import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union


class RuleExtractor:
    """Extracts sections from LLM-optimized rule files."""
    
    def __init__(self, rule_file: Path):
        self.rule_file = rule_file
        self.content = rule_file.read_text()
        self.metadata = self._extract_metadata()
        
    def _extract_metadata(self) -> Dict:
        """Extract YAML front matter."""
        if self.content.startswith('---'):
            end_marker = self.content.find('---', 3)
            if end_marker != -1:
                yaml_content = self.content[3:end_marker]
                return yaml.safe_load(yaml_content)
        return {}
    
    def extract_section(self, section_name: str) -> Optional[str]:
        """Extract a specific section by name."""
        # Check for extraction markers first
        marker_pattern = rf'<!-- EXTRACT:{section_name}:start -->(.*?)<!-- EXTRACT:{section_name}:end -->'
        match = re.search(marker_pattern, self.content, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Check for CAPS_SECTION_NAME
        section_name_upper = section_name.upper().replace('-', '_')
        section_pattern = rf'^## {section_name_upper}\n(.*?)(?=^##|\Z)'
        match = re.search(section_pattern, self.content, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return None
    
    def extract_examples(self, example_type: str = 'good') -> List[Dict[str, str]]:
        """Extract all examples of a specific type."""
        examples = []
        pattern = rf'### {example_type.upper()}_EXAMPLE_(\d+): (.*?)\n```(\w+)\n(.*?)```\n\*\*Why this is {example_type}\*\*: (.*?)(?=###|\Z)'
        
        for match in re.finditer(pattern, self.content, re.DOTALL):
            examples.append({
                'id': f'{example_type.upper()}_EXAMPLE_{match.group(1)}',
                'title': match.group(2),
                'language': match.group(3),
                'code': match.group(4).strip(),
                'explanation': match.group(5).strip()
            })
        
        return examples
    
    def extract_requirements(self) -> List[Dict[str, str]]:
        """Extract all requirements (REQ*)."""
        requirements = []
        req_section = self.extract_section('requirements')
        if not req_section:
            req_section = self.extract_section('MUST_FOLLOW')
        
        if req_section:
            pattern = r'\*\*\[(\w+)\]\*\* (.*?)(?:\n   - Rationale: (.*?))?(?:\n   - Impact: (.*?))?(?=\n\d+\.|\Z)'
            for match in re.finditer(pattern, req_section, re.DOTALL):
                requirements.append({
                    'id': match.group(1),
                    'requirement': match.group(2).strip(),
                    'rationale': match.group(3).strip() if match.group(3) else None,
                    'impact': match.group(4).strip() if match.group(4) else None
                })
        
        return requirements
    
    def extract_antipatterns(self) -> List[Dict[str, str]]:
        """Extract all anti-patterns (ANT*)."""
        antipatterns = []
        ant_section = self.extract_section('antipatterns')
        if not ant_section:
            ant_section = self.extract_section('MUST_NOT_DO')
        
        if ant_section:
            pattern = r'\*\*\[(\w+)\]\*\* (.*?)(?:\n   - Why: (.*?))?(?:\n   - Instead: (.*?))?(?=\n\d+\.|\Z)'
            for match in re.finditer(pattern, ant_section, re.DOTALL):
                antipatterns.append({
                    'id': match.group(1),
                    'antipattern': match.group(2).strip(),
                    'why': match.group(3).strip() if match.group(3) else None,
                    'instead': match.group(4).strip() if match.group(4) else None
                })
        
        return antipatterns
    
    def extract_patterns(self) -> Dict[str, List[Dict[str, str]]]:
        """Extract pattern matching rules."""
        patterns = {'good': [], 'bad': []}
        pattern_section = self.extract_section('patterns')
        
        if pattern_section:
            pattern_regex = r'- \*\*(PATTERN_(GOOD|BAD)_\d+)\*\*: `(.*?)`(?:\n  - Example: (.*?))?(?:\n  - Matches: (.*?))?(?:\n  - Avoid because: (.*?))?'
            
            for match in re.finditer(pattern_regex, pattern_section, re.DOTALL):
                pattern_type = 'good' if match.group(2) == 'GOOD' else 'bad'
                pattern_data = {
                    'id': match.group(1),
                    'pattern': match.group(3),
                    'example': match.group(4).strip() if match.group(4) else None,
                    'matches': match.group(5).strip() if match.group(5) else None
                }
                if pattern_type == 'bad' and match.group(6):
                    pattern_data['avoid_because'] = match.group(6).strip()
                patterns[pattern_type].append(pattern_data)
        
        return patterns
    
    def extract_all(self) -> Dict[str, Union[Dict, List, str]]:
        """Extract all sections and metadata."""
        return {
            'metadata': self.metadata,
            'rule_summary': self.extract_section('RULE_SUMMARY'),
            'requirements': self.extract_requirements(),
            'antipatterns': self.extract_antipatterns(),
            'good_examples': self.extract_examples('good'),
            'bad_examples': self.extract_examples('bad'),
            'patterns': self.extract_patterns(),
            'metrics': self.extract_section('metrics'),
            'automated_checks': self.extract_section('AUTOMATED_CHECKS')
        }


def main():
    """Command-line interface."""
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    # Parse arguments
    output_json = False
    args = sys.argv[1:]
    if args[0] == '--json':
        output_json = True
        args = args[1:]
    
    rule_file = Path(args[0])
    section_name = args[1]
    
    if not rule_file.exists():
        print(f"Error: Rule file '{rule_file}' not found")
        sys.exit(1)
    
    extractor = RuleExtractor(rule_file)
    
    if section_name == 'all':
        result = extractor.extract_all()
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            for key, value in result.items():
                if value:
                    print(f"\n=== {key.upper()} ===")
                    if isinstance(value, (dict, list)):
                        print(json.dumps(value, indent=2))
                    else:
                        print(value)
    else:
        # Try different extraction methods
        result = None
        
        if section_name == 'requirements':
            result = extractor.extract_requirements()
        elif section_name == 'antipatterns':
            result = extractor.extract_antipatterns()
        elif section_name == 'good_examples':
            result = extractor.extract_examples('good')
        elif section_name == 'bad_examples':
            result = extractor.extract_examples('bad')
        elif section_name == 'patterns':
            result = extractor.extract_patterns()
        else:
            result = extractor.extract_section(section_name)
        
        if result:
            if output_json and isinstance(result, (dict, list)):
                print(json.dumps(result, indent=2))
            else:
                print(result)
        else:
            print(f"Section '{section_name}' not found in {rule_file}")
            sys.exit(1)


if __name__ == '__main__':
    main()