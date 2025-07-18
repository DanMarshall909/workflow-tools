#!/usr/bin/env python3
"""
Rule Diff Tool for LLMs
Compare rules, track changes, and generate migration guides.

Usage:
    python rule-diff.py <rule1> <rule2>
    python rule-diff.py --category test-naming --language typescript
    python rule-diff.py --changes-since 2024-01-01
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from difflib import unified_diff, SequenceMatcher


class RuleDiffer:
    """Compare and analyze differences between rules."""
    
    def __init__(self):
        self.rules_dir = Path(__file__).parent.parent
        
    def diff_rules(self, rule1_path: Path, rule2_path: Path) -> Dict:
        """Compare two rule files and return structured diff."""
        from extract_rule_section import RuleExtractor
        
        # Extract data from both rules
        extractor1 = RuleExtractor(rule1_path)
        extractor2 = RuleExtractor(rule2_path)
        
        data1 = extractor1.extract_all()
        data2 = extractor2.extract_all()
        
        diff_result = {
            'metadata_changes': self._diff_metadata(data1['metadata'], data2['metadata']),
            'requirement_changes': self._diff_requirements(data1['requirements'], data2['requirements']),
            'antipattern_changes': self._diff_antipatterns(data1['antipatterns'], data2['antipatterns']),
            'example_changes': self._diff_examples(data1, data2),
            'summary': self._generate_summary(data1, data2)
        }
        
        return diff_result
    
    def _diff_metadata(self, meta1: Dict, meta2: Dict) -> Dict:
        """Compare metadata between rules."""
        changes = {
            'added': {},
            'removed': {},
            'modified': {}
        }
        
        all_keys = set(meta1.keys()) | set(meta2.keys())
        
        for key in all_keys:
            if key not in meta1:
                changes['added'][key] = meta2[key]
            elif key not in meta2:
                changes['removed'][key] = meta1[key]
            elif meta1[key] != meta2[key]:
                changes['modified'][key] = {
                    'old': meta1[key],
                    'new': meta2[key]
                }
        
        return changes
    
    def _diff_requirements(self, reqs1: List[Dict], reqs2: List[Dict]) -> Dict:
        """Compare requirements between rules."""
        changes = {
            'added': [],
            'removed': [],
            'modified': []
        }
        
        # Index by ID
        reqs1_by_id = {r['id']: r for r in reqs1}
        reqs2_by_id = {r['id']: r for r in reqs2}
        
        # Find changes
        for req_id in set(reqs1_by_id.keys()) | set(reqs2_by_id.keys()):
            if req_id not in reqs1_by_id:
                changes['added'].append(reqs2_by_id[req_id])
            elif req_id not in reqs2_by_id:
                changes['removed'].append(reqs1_by_id[req_id])
            elif reqs1_by_id[req_id] != reqs2_by_id[req_id]:
                changes['modified'].append({
                    'id': req_id,
                    'old': reqs1_by_id[req_id],
                    'new': reqs2_by_id[req_id],
                    'similarity': self._calculate_similarity(
                        reqs1_by_id[req_id]['requirement'],
                        reqs2_by_id[req_id]['requirement']
                    )
                })
        
        return changes
    
    def _diff_antipatterns(self, ants1: List[Dict], ants2: List[Dict]) -> Dict:
        """Compare antipatterns between rules."""
        # Similar structure to requirements
        changes = {
            'added': [],
            'removed': [],
            'modified': []
        }
        
        ants1_by_id = {a['id']: a for a in ants1}
        ants2_by_id = {a['id']: a for a in ants2}
        
        for ant_id in set(ants1_by_id.keys()) | set(ants2_by_id.keys()):
            if ant_id not in ants1_by_id:
                changes['added'].append(ants2_by_id[ant_id])
            elif ant_id not in ants2_by_id:
                changes['removed'].append(ants1_by_id[ant_id])
            elif ants1_by_id[ant_id] != ants2_by_id[ant_id]:
                changes['modified'].append({
                    'id': ant_id,
                    'old': ants1_by_id[ant_id],
                    'new': ants2_by_id[ant_id]
                })
        
        return changes
    
    def _diff_examples(self, data1: Dict, data2: Dict) -> Dict:
        """Compare examples between rules."""
        return {
            'good_examples': {
                'added': len(data2['good_examples']) - len(data1['good_examples']),
                'removed': 0 if len(data2['good_examples']) >= len(data1['good_examples']) else len(data1['good_examples']) - len(data2['good_examples']),
                'total_before': len(data1['good_examples']),
                'total_after': len(data2['good_examples'])
            },
            'bad_examples': {
                'added': len(data2['bad_examples']) - len(data1['bad_examples']),
                'removed': 0 if len(data2['bad_examples']) >= len(data1['bad_examples']) else len(data1['bad_examples']) - len(data2['bad_examples']),
                'total_before': len(data1['bad_examples']),
                'total_after': len(data2['bad_examples'])
            }
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _generate_summary(self, data1: Dict, data2: Dict) -> Dict:
        """Generate a summary of changes."""
        summary = {
            'severity_changed': False,
            'category_changed': False,
            'language_changed': False,
            'breaking_changes': []
        }
        
        meta1 = data1['metadata']
        meta2 = data2['metadata']
        
        if meta1.get('severity') != meta2.get('severity'):
            summary['severity_changed'] = True
            summary['breaking_changes'].append(
                f"Severity changed from {meta1.get('severity')} to {meta2.get('severity')}"
            )
        
        if meta1.get('category') != meta2.get('category'):
            summary['category_changed'] = True
        
        if meta1.get('language') != meta2.get('language'):
            summary['language_changed'] = True
            summary['breaking_changes'].append(
                f"Language changed from {meta1.get('language')} to {meta2.get('language')}"
            )
        
        return summary
    
    def compare_category(self, category: str, language: Optional[str] = None) -> List[Dict]:
        """Compare all rules in a category."""
        with open(self.rules_dir / 'rules-index.json') as f:
            rules_index = json.load(f)
        
        # Filter rules
        rules = []
        for rule_id, rule_data in rules_index['rules'].items():
            if rule_data['category'] == category:
                if language is None or rule_data['language'] == language:
                    rules.append({
                        'rule_id': rule_id,
                        'summary': rule_data['summary'],
                        'severity': rule_data['severity'],
                        'file_path': rule_data['file_path']
                    })
        
        # Compare rules pairwise
        comparisons = []
        for i in range(len(rules)):
            for j in range(i + 1, len(rules)):
                rule1_path = self.rules_dir / rules[i]['file_path']
                rule2_path = self.rules_dir / rules[j]['file_path']
                
                similarity = self._calculate_rule_similarity(rule1_path, rule2_path)
                
                comparisons.append({
                    'rule1': rules[i]['rule_id'],
                    'rule2': rules[j]['rule_id'],
                    'similarity': similarity,
                    'both_severity': rules[i]['severity'] == rules[j]['severity']
                })
        
        return sorted(comparisons, key=lambda x: x['similarity'], reverse=True)
    
    def _calculate_rule_similarity(self, rule1_path: Path, rule2_path: Path) -> float:
        """Calculate overall similarity between two rules."""
        from extract_rule_section import RuleExtractor
        
        try:
            ext1 = RuleExtractor(rule1_path)
            ext2 = RuleExtractor(rule2_path)
            
            # Compare requirements
            reqs1 = [r['requirement'] for r in ext1.extract_requirements()]
            reqs2 = [r['requirement'] for r in ext2.extract_requirements()]
            
            # Simple Jaccard similarity
            set1 = set(' '.join(reqs1).lower().split())
            set2 = set(' '.join(reqs2).lower().split())
            
            if not set1 and not set2:
                return 0.0
            
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            
            return intersection / union if union > 0 else 0.0
        except:
            return 0.0
    
    def find_changes_since(self, date_str: str) -> List[Dict]:
        """Find all rules changed since a given date."""
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        changed_rules = []
        
        with open(self.rules_dir / 'rules-index.json') as f:
            rules_index = json.load(f)
        
        for rule_id, rule_data in rules_index['rules'].items():
            last_updated = datetime.strptime(rule_data['last_updated'], '%Y-%m-%d')
            
            if last_updated >= target_date:
                changed_rules.append({
                    'rule_id': rule_id,
                    'last_updated': rule_data['last_updated'],
                    'version': rule_data['version'],
                    'summary': rule_data['summary'],
                    'file_path': rule_data['file_path']
                })
        
        return sorted(changed_rules, key=lambda x: x['last_updated'], reverse=True)
    
    def generate_migration_guide(self, old_rule: Path, new_rule: Path) -> str:
        """Generate a migration guide between rule versions."""
        diff_data = self.diff_rules(old_rule, new_rule)
        
        guide = f"# Migration Guide\n\n"
        guide += f"Migrating from {old_rule.name} to {new_rule.name}\n\n"
        
        # Metadata changes
        if diff_data['metadata_changes']['modified']:
            guide += "## Metadata Changes\n\n"
            for key, change in diff_data['metadata_changes']['modified'].items():
                guide += f"- **{key}**: {change['old']} → {change['new']}\n"
            guide += "\n"
        
        # Requirement changes
        req_changes = diff_data['requirement_changes']
        if req_changes['added'] or req_changes['removed'] or req_changes['modified']:
            guide += "## Requirement Changes\n\n"
            
            if req_changes['added']:
                guide += "### New Requirements\n"
                for req in req_changes['added']:
                    guide += f"- **{req['id']}**: {req['requirement']}\n"
                guide += "\n"
            
            if req_changes['removed']:
                guide += "### Removed Requirements\n"
                for req in req_changes['removed']:
                    guide += f"- **{req['id']}**: {req['requirement']}\n"
                guide += "\n"
            
            if req_changes['modified']:
                guide += "### Modified Requirements\n"
                for change in req_changes['modified']:
                    guide += f"- **{change['id']}** (similarity: {change['similarity']:.0%})\n"
                    guide += f"  - Old: {change['old']['requirement']}\n"
                    guide += f"  - New: {change['new']['requirement']}\n"
                guide += "\n"
        
        # Breaking changes
        if diff_data['summary']['breaking_changes']:
            guide += "## ⚠️ Breaking Changes\n\n"
            for change in diff_data['summary']['breaking_changes']:
                guide += f"- {change}\n"
            guide += "\n"
        
        # Migration steps
        guide += "## Migration Steps\n\n"
        guide += "1. Review all modified requirements above\n"
        guide += "2. Update your codebase to comply with new requirements\n"
        guide += "3. Remove code that violates new antipatterns\n"
        guide += "4. Run validation tools to ensure compliance\n"
        
        return guide


def format_diff_output(diff_data: Dict) -> str:
    """Format diff data for human reading."""
    output = []
    
    # Summary
    summary = diff_data['summary']
    if summary['breaking_changes']:
        output.append("⚠️  BREAKING CHANGES DETECTED:")
        for change in summary['breaking_changes']:
            output.append(f"   - {change}")
        output.append("")
    
    # Metadata changes
    meta = diff_data['metadata_changes']
    if any(meta[k] for k in ['added', 'removed', 'modified']):
        output.append("METADATA CHANGES:")
        for key, value in meta['modified'].items():
            output.append(f"  {key}: {value['old']} → {value['new']}")
        output.append("")
    
    # Requirements
    reqs = diff_data['requirement_changes']
    if reqs['added']:
        output.append(f"REQUIREMENTS ADDED ({len(reqs['added'])}):")
        for req in reqs['added']:
            output.append(f"  + {req['id']}: {req['requirement']}")
        output.append("")
    
    if reqs['removed']:
        output.append(f"REQUIREMENTS REMOVED ({len(reqs['removed'])}):")
        for req in reqs['removed']:
            output.append(f"  - {req['id']}: {req['requirement']}")
        output.append("")
    
    if reqs['modified']:
        output.append(f"REQUIREMENTS MODIFIED ({len(reqs['modified'])}):")
        for change in reqs['modified']:
            output.append(f"  ~ {change['id']} (similarity: {change['similarity']:.0%})")
        output.append("")
    
    # Examples
    examples = diff_data['example_changes']
    output.append("EXAMPLE CHANGES:")
    output.append(f"  Good examples: {examples['good_examples']['total_before']} → {examples['good_examples']['total_after']}")
    output.append(f"  Bad examples: {examples['bad_examples']['total_before']} → {examples['bad_examples']['total_after']}")
    
    return "\n".join(output)


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    differ = RuleDiffer()
    
    if sys.argv[1] == '--category':
        # Compare rules in a category
        category = sys.argv[2]
        language = None
        if len(sys.argv) > 4 and sys.argv[3] == '--language':
            language = sys.argv[4]
        
        comparisons = differ.compare_category(category, language)
        
        print(f"Rule similarities in category '{category}':")
        for comp in comparisons[:10]:  # Top 10
            print(f"  {comp['rule1']} ↔ {comp['rule2']}: {comp['similarity']:.0%}")
    
    elif sys.argv[1] == '--changes-since':
        # Find changes since date
        date_str = sys.argv[2]
        changes = differ.find_changes_since(date_str)
        
        print(f"Rules changed since {date_str}:")
        for change in changes:
            print(f"  {change['rule_id']} (v{change['version']}) - {change['last_updated']}")
            print(f"    {change['summary']}")
    
    elif sys.argv[1] == '--migration':
        # Generate migration guide
        if len(sys.argv) < 4:
            print("Usage: rule-diff.py --migration <old-rule> <new-rule>")
            sys.exit(1)
        
        old_rule = Path(sys.argv[2])
        new_rule = Path(sys.argv[3])
        
        guide = differ.generate_migration_guide(old_rule, new_rule)
        print(guide)
    
    else:
        # Compare two specific rules
        rule1 = Path(sys.argv[1])
        rule2 = Path(sys.argv[2])
        
        if not rule1.exists():
            print(f"Error: {rule1} not found")
            sys.exit(1)
        if not rule2.exists():
            print(f"Error: {rule2} not found")
            sys.exit(1)
        
        diff_data = differ.diff_rules(rule1, rule2)
        print(format_diff_output(diff_data))


if __name__ == '__main__':
    main()