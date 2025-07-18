#!/usr/bin/env python3
"""
Quick Start Example for LLM Rule Consumption
Demonstrates efficient rule loading and usage patterns.
"""

import json
import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from extract_rule_section import RuleExtractor
from rule_bundler import RuleBundler


def example_1_minimal_loading():
    """Example 1: Load only what you need."""
    print("=== Example 1: Minimal Context Loading ===\n")
    
    # Load a specific rule
    rule_path = Path(__file__).parent.parent / 'typescript/test-naming/jest-react-testing-library.md'
    if rule_path.exists():
        extractor = RuleExtractor(rule_path)
        
        # Get just the summary (minimal tokens)
        summary = extractor.extract_section('RULE_SUMMARY')
        print(f"Summary: {summary}\n")
        
        # Get just the requirements
        requirements = extractor.extract_requirements()
        print(f"Found {len(requirements)} requirements:")
        for req in requirements[:2]:  # Show first 2
            print(f"  - {req['id']}: {req['requirement']}")
        print()


def example_2_code_review():
    """Example 2: Review code for violations."""
    print("=== Example 2: Code Review ===\n")
    
    # Sample code to review
    test_code = """
    test('should return user data when API call succeeds', () => {
        // test implementation
    });
    """
    
    rule_path = Path(__file__).parent.parent / 'typescript/test-naming/jest-react-testing-library.md'
    if rule_path.exists():
        extractor = RuleExtractor(rule_path)
        
        # Get antipatterns to check against
        antipatterns = extractor.extract_antipatterns()
        
        # Simple check for 'should' in test name
        violations = []
        for antipattern in antipatterns:
            if antipattern['id'] == 'ANT001' and 'should' in test_code:
                violations.append({
                    'rule': 'ANT001',
                    'issue': antipattern['antipattern'],
                    'fix': antipattern['instead']
                })
        
        if violations:
            print("Violations found:")
            for v in violations:
                print(f"  - {v['rule']}: {v['issue']}")
                print(f"    Fix: {v['fix']}")
        print()


def example_3_task_bundling():
    """Example 3: Bundle rules for a specific task."""
    print("=== Example 3: Task-Based Bundling ===\n")
    
    bundler = RuleBundler()
    
    # Create bundle for TypeScript testing
    bundle = bundler.bundle_for_task("write unit tests for TypeScript React components")
    
    print(f"Task: write unit tests for TypeScript React components")
    print(f"Rules selected: {bundle['metadata']['rule_count']}")
    print(f"Estimated tokens: {bundle['metadata']['token_estimate']}")
    print(f"Context detected: {bundle['metadata']['context']}")
    print()
    
    # Show which rules were included
    print("Included rules:")
    for rule_id in list(bundle['rules'].keys())[:3]:  # Show first 3
        rule_data = bundle['rules'][rule_id]
        print(f"  - {rule_id} ({rule_data['metadata']['language']})")
        print(f"    Sections: {list(rule_data['sections'].keys())}")
    print()


def example_4_quick_reference():
    """Example 4: Load quick reference data."""
    print("=== Example 4: Quick Reference ===\n")
    
    # Load quick queries
    quick_queries_path = Path(__file__).parent.parent / 'llm-quick-queries.yaml'
    if quick_queries_path.exists():
        import yaml
        with open(quick_queries_path) as f:
            quick_data = yaml.safe_load(f)
        
        # Get test naming patterns
        test_patterns = quick_data['quick_queries']['test_naming']
        print("Quick test naming reference:")
        for key, value in test_patterns.items():
            print(f"  - {key}: {value.split('|')[0].strip()}")
        print()


def example_5_batch_validation():
    """Example 5: Validate multiple rules efficiently."""
    print("=== Example 5: Batch Rule Validation ===\n")
    
    from validate_rule import RuleValidator
    
    validator = RuleValidator()
    
    # Find TypeScript rules to validate
    rules_dir = Path(__file__).parent.parent
    ts_rules = list(rules_dir.glob('typescript/**/*.md'))[:3]  # First 3
    
    print(f"Validating {len(ts_rules)} TypeScript rules:")
    all_valid = True
    
    for rule_file in ts_rules:
        errors, warnings = validator.validate_file(rule_file)
        status = "✓" if not errors else "✗"
        print(f"  {status} {rule_file.name}")
        if errors:
            all_valid = False
            print(f"     Errors: {len(errors)}")
    
    print(f"\nAll valid: {'Yes' if all_valid else 'No'}")
    print()


def example_6_api_pattern():
    """Example 6: API-ready pattern."""
    print("=== Example 6: API Pattern ===\n")
    
    def check_test_naming(code: str, language: str = 'typescript'):
        """API function to check test naming compliance."""
        # In real implementation, would load from index
        rule_path = Path(__file__).parent.parent / f'{language}/test-naming/jest-react-testing-library.md'
        
        if not rule_path.exists():
            return {'error': 'Rule not found'}
        
        extractor = RuleExtractor(rule_path)
        antipatterns = extractor.extract_antipatterns()
        
        violations = []
        for pattern in antipatterns:
            # Simplified check - in real use would use regex
            if pattern['id'] == 'ANT001' and 'should' in code:
                violations.append({
                    'violation_id': pattern['id'],
                    'message': pattern['antipattern'],
                    'suggestion': pattern['instead']
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    # Test the API function
    result = check_test_naming("test('should work', () => {})")
    print(f"API Response: {json.dumps(result, indent=2)}")


if __name__ == '__main__':
    print("Workflow-Tools LLM Integration Examples\n")
    print("These examples demonstrate efficient rule consumption patterns.\n")
    
    examples = [
        example_1_minimal_loading,
        example_2_code_review,
        example_3_task_bundling,
        example_4_quick_reference,
        example_5_batch_validation,
        example_6_api_pattern
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}\n")
    
    print("\nFor more examples, see llm-api-examples.md")