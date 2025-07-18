#!/usr/bin/env python3
"""
Rule Validator for LLM-Optimized Format
Validates workflow-tools rules against the schema and content structure.

Usage:
    python validate-rule.py <rule-file>
    python validate-rule.py --all
    python validate-rule.py --fix <rule-file>
"""

import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class RuleValidator:
    """Validates rule files against schema and structure requirements."""
    
    def __init__(self):
        self.schema_dir = Path(__file__).parent.parent / 'schemas'
        self.metadata_schema = self._load_json_schema()
        self.content_schema = self._load_content_schema()
        self.errors = []
        self.warnings = []
        
    def _load_json_schema(self) -> Dict:
        """Load the JSON schema for metadata validation."""
        schema_file = self.schema_dir / 'rule-schema.json'
        if schema_file.exists():
            return json.loads(schema_file.read_text())
        return {}
    
    def _load_content_schema(self) -> Dict:
        """Load the YAML schema for content structure validation."""
        schema_file = self.schema_dir / 'rule-content-schema.yaml'
        if schema_file.exists():
            return yaml.safe_load(schema_file.read_text())
        return {}
    
    def validate_file(self, rule_file: Path) -> Tuple[List[str], List[str]]:
        """Validate a single rule file."""
        self.errors = []
        self.warnings = []
        
        if not rule_file.exists():
            self.errors.append(f"File not found: {rule_file}")
            return self.errors, self.warnings
        
        content = rule_file.read_text()
        
        # Validate metadata
        metadata = self._extract_metadata(content)
        if metadata:
            self._validate_metadata(metadata)
        else:
            self.errors.append("No YAML front matter found")
        
        # Validate content structure
        self._validate_content_structure(content)
        
        # Validate extraction markers
        self._validate_extraction_markers(content)
        
        # Validate ID formats
        self._validate_id_formats(content)
        
        return self.errors, self.warnings
    
    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract YAML front matter."""
        if content.startswith('---'):
            end_marker = content.find('---', 3)
            if end_marker != -1:
                yaml_content = content[3:end_marker]
                try:
                    return yaml.safe_load(yaml_content)
                except yaml.YAMLError as e:
                    self.errors.append(f"Invalid YAML metadata: {e}")
        return None
    
    def _validate_metadata(self, metadata: Dict):
        """Validate metadata against JSON schema."""
        # Check required fields
        required_fields = self.metadata_schema.get('required', [])
        for field in required_fields:
            if field not in metadata:
                self.errors.append(f"Missing required metadata field: {field}")
        
        # Validate field values
        properties = self.metadata_schema.get('properties', {})
        for field, value in metadata.items():
            if field in properties:
                self._validate_field(field, value, properties[field])
    
    def _validate_field(self, field: str, value, schema: Dict):
        """Validate a single metadata field."""
        # Type validation
        expected_type = schema.get('type')
        if expected_type == 'string' and not isinstance(value, str):
            self.errors.append(f"{field}: Expected string, got {type(value).__name__}")
        elif expected_type == 'array' and not isinstance(value, list):
            self.errors.append(f"{field}: Expected array, got {type(value).__name__}")
        
        # Enum validation
        if 'enum' in schema and value not in schema['enum']:
            self.errors.append(f"{field}: Invalid value '{value}'. Must be one of: {schema['enum']}")
        
        # Pattern validation
        if 'pattern' in schema and isinstance(value, str):
            if not re.match(schema['pattern'], value):
                self.errors.append(f"{field}: Value '{value}' doesn't match pattern {schema['pattern']}")
        
        # Format validation
        if schema.get('format') == 'date' and isinstance(value, str):
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                self.errors.append(f"{field}: Invalid date format. Use YYYY-MM-DD")
    
    def _validate_content_structure(self, content: str):
        """Validate the content follows the required structure."""
        required_sections = self.content_schema.get('required_sections', [])
        
        for section in required_sections:
            if f"## {section}" not in content:
                self.errors.append(f"Missing required section: {section}")
        
        # Check for proper section formatting
        if "## MUST_FOLLOW" in content and "### MUST_FOLLOW" not in content:
            if not re.search(r'\*\*\[REQ\d+\]\*\*', content):
                self.warnings.append("MUST_FOLLOW section should use REQ### format")
        
        if "## MUST_NOT_DO" in content and "### MUST_NOT_DO" not in content:
            if not re.search(r'\*\*\[ANT\d+\]\*\*', content):
                self.warnings.append("MUST_NOT_DO section should use ANT### format")
    
    def _validate_extraction_markers(self, content: str):
        """Validate extraction markers are properly formatted."""
        markers = re.findall(r'<!-- EXTRACT:(\w+):(start|end) -->', content)
        
        start_markers = {m[0] for m in markers if m[1] == 'start'}
        end_markers = {m[0] for m in markers if m[1] == 'end'}
        
        # Check for matching start/end markers
        for marker in start_markers:
            if marker not in end_markers:
                self.errors.append(f"Missing end marker for EXTRACT:{marker}")
        
        for marker in end_markers:
            if marker not in start_markers:
                self.errors.append(f"Missing start marker for EXTRACT:{marker}")
        
        # Check for standard marker names
        standard_names = {'requirements', 'antipatterns', 'patterns', 'metrics'}
        for marker in start_markers:
            if marker not in standard_names:
                self.warnings.append(f"Non-standard extraction marker: {marker}")
    
    def _validate_id_formats(self, content: str):
        """Validate ID formats throughout the content."""
        # Check REQ IDs
        req_ids = re.findall(r'\*\*\[(REQ\d+)\]\*\*', content)
        self._check_sequential_ids(req_ids, 'REQ')
        
        # Check ANT IDs
        ant_ids = re.findall(r'\*\*\[(ANT\d+)\]\*\*', content)
        self._check_sequential_ids(ant_ids, 'ANT')
        
        # Check example naming
        good_examples = re.findall(r'### (GOOD_EXAMPLE_\d+)', content)
        bad_examples = re.findall(r'### (BAD_EXAMPLE_\d+)', content)
        
        if len(good_examples) < 2:
            self.warnings.append("Should have at least 2 GOOD_EXAMPLE sections")
        if len(bad_examples) < 1:
            self.warnings.append("Should have at least 1 BAD_EXAMPLE section")
    
    def _check_sequential_ids(self, ids: List[str], prefix: str):
        """Check if IDs are sequential starting from 001."""
        if not ids:
            return
        
        numbers = []
        for id_str in ids:
            match = re.match(f'{prefix}(\\d+)', id_str)
            if match:
                numbers.append(int(match.group(1)))
        
        numbers.sort()
        for i, num in enumerate(numbers, 1):
            if num != i:
                self.warnings.append(f"{prefix} IDs are not sequential. Expected {prefix}{i:03d}, found {prefix}{num:03d}")
                break
    
    def fix_common_issues(self, rule_file: Path) -> bool:
        """Attempt to fix common formatting issues."""
        content = rule_file.read_text()
        original = content
        
        # Fix ID formatting (REQ1 -> REQ001)
        content = re.sub(r'\*\*\[REQ(\d)\]\*\*', lambda m: f'**[REQ00{m.group(1)}]**', content)
        content = re.sub(r'\*\*\[REQ(\d\d)\]\*\*', lambda m: f'**[REQ0{m.group(1)}]**', content)
        content = re.sub(r'\*\*\[ANT(\d)\]\*\*', lambda m: f'**[ANT00{m.group(1)}]**', content)
        content = re.sub(r'\*\*\[ANT(\d\d)\]\*\*', lambda m: f'**[ANT0{m.group(1)}]**', content)
        
        # Fix example naming
        content = re.sub(r'### Good Example (\d)', lambda m: f'### GOOD_EXAMPLE_00{m.group(1)}', content)
        content = re.sub(r'### Bad Example (\d)', lambda m: f'### BAD_EXAMPLE_00{m.group(1)}', content)
        
        # Add missing extraction markers
        if '## MUST_FOLLOW' in content and '<!-- EXTRACT:requirements:start -->' not in content:
            content = content.replace(
                '### MUST_FOLLOW\n',
                '### MUST_FOLLOW\n<!-- EXTRACT:requirements:start -->\n'
            )
            # Find the end of MUST_FOLLOW section
            next_section = re.search(r'\n### (?!MUST_FOLLOW)', content)
            if next_section:
                content = content[:next_section.start()] + '<!-- EXTRACT:requirements:end -->\n' + content[next_section.start():]
        
        if content != original:
            rule_file.write_text(content)
            return True
        return False


def validate_all_rules():
    """Validate all rule files in the rules directory."""
    rules_dir = Path(__file__).parent.parent
    rule_files = list(rules_dir.glob('**/*.md'))
    rule_files = [f for f in rule_files if not any(p in f.parts for p in ['templates', 'tools', 'schemas'])]
    
    validator = RuleValidator()
    all_valid = True
    
    for rule_file in sorted(rule_files):
        errors, warnings = validator.validate_file(rule_file)
        
        if errors or warnings:
            all_valid = False
            print(f"\n{rule_file}:")
            for error in errors:
                print(f"  ERROR: {error}")
            for warning in warnings:
                print(f"  WARNING: {warning}")
    
    if all_valid:
        print(f"✓ All {len(rule_files)} rules are valid!")
    else:
        print(f"\n❌ Validation completed with issues")
    
    return all_valid


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        success = validate_all_rules()
        sys.exit(0 if success else 1)
    
    fix_mode = False
    if sys.argv[1] == '--fix':
        fix_mode = True
        if len(sys.argv) < 3:
            print("Error: --fix requires a rule file argument")
            sys.exit(1)
        rule_file = Path(sys.argv[2])
    else:
        rule_file = Path(sys.argv[1])
    
    validator = RuleValidator()
    
    if fix_mode:
        print(f"Attempting to fix common issues in {rule_file}...")
        if validator.fix_common_issues(rule_file):
            print("✓ Fixed some issues. Re-validating...")
        else:
            print("No automatic fixes applied.")
    
    errors, warnings = validator.validate_file(rule_file)
    
    if errors or warnings:
        print(f"\nValidation results for {rule_file}:")
        for error in errors:
            print(f"  ERROR: {error}")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        sys.exit(1)
    else:
        print(f"✓ {rule_file} is valid!")


if __name__ == '__main__':
    main()