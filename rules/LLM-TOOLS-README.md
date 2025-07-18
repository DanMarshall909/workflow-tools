# LLM Tools for Workflow-Tools Rules

This directory contains tools and utilities optimized for LLM consumption of workflow-tools rules.

## Overview

The LLM optimization system provides:

1. **Structured Rule Format** - Consistent YAML frontmatter and section naming
2. **Extraction Tools** - Pull specific sections to minimize context
3. **Validation Tools** - Ensure rules follow the optimized format
4. **API Examples** - Integration patterns for various LLM frameworks
5. **Diff Tools** - Compare rules and track changes
6. **Bundling System** - Smart context-aware rule packaging

## Tools

### 1. Rule Section Extractor (`extract-rule-section.py`)

Extract specific sections from rules for minimal context loading.

```bash
# Extract requirements only
python tools/extract-rule-section.py typescript-test-naming.md requirements

# Extract all sections as JSON
python tools/extract-rule-section.py --json typescript-test-naming.md all

# Extract antipatterns
python tools/extract-rule-section.py rule.md antipatterns
```

**Supported Sections:**
- `requirements` - MUST_FOLLOW rules
- `antipatterns` - MUST_NOT_DO rules
- `good_examples` - Positive examples
- `bad_examples` - Negative examples
- `patterns` - Pattern matching rules
- `metrics` - Measurement queries
- Any CAPS_SECTION_NAME

### 2. Rule Validator (`validate-rule.py`)

Validate rules against schema and structure requirements.

```bash
# Validate single rule
python tools/validate-rule.py typescript/test-naming/jest.md

# Validate all rules
python tools/validate-rule.py --all

# Auto-fix common issues
python tools/validate-rule.py --fix rule.md
```

**Validates:**
- YAML frontmatter schema
- Required sections presence
- ID format consistency (REQ###, ANT###)
- Extraction marker pairs
- Example counts

### 3. Rule Differ (`rule-diff.py`)

Compare rules and generate migration guides.

```bash
# Compare two rules
python tools/rule-diff.py old-rule.md new-rule.md

# Compare all rules in category
python tools/rule-diff.py --category test-naming --language typescript

# Find recent changes
python tools/rule-diff.py --changes-since 2024-01-01

# Generate migration guide
python tools/rule-diff.py --migration old.md new.md
```

### 4. Rule Bundler (`rule-bundler.py`)

Create optimized rule bundles based on context.

```bash
# Bundle for specific task
python tools/rule-bundler.py --task "review typescript code"

# Bundle by criteria
python tools/rule-bundler.py --language typescript --sections requirements,antipatterns

# Use predefined bundle
python tools/rule-bundler.py --bundle code-review --output review.json

# Create custom bundle
python tools/rule-bundler.py --create-bundle "my-bundle" rule1.md rule2.md

# Optimize bundle size
python tools/rule-bundler.py --optimize bundle.json --max-tokens 2000
```

**Predefined Bundles:**
- `typescript-testing` - TypeScript test writing
- `code-review` - Code review checklist
- `security-audit` - Security rules
- `git-workflow` - Git standards
- `quick-reference` - Minimal reference

## Rule Format

### YAML Frontmatter

```yaml
---
rule_id: unique-lowercase-id
category: test-naming|code-quality|security|git-workflow
language: typescript|csharp|python|universal
severity: required|recommended|optional
tags: [searchable, tags]
prerequisites: [prerequisite-rules]
related_rules: [related-rules]
version: 1.0.0
last_updated: 2024-01-20
---
```

### Section Structure

```markdown
## RULE_SUMMARY
One-line description of the rule

## MUST_FOLLOW
<!-- EXTRACT:requirements:start -->
1. **[REQ001]** Requirement description
   - Rationale: Why this matters
   - Impact: What happens if not followed
<!-- EXTRACT:requirements:end -->

## MUST_NOT_DO
<!-- EXTRACT:antipatterns:start -->
1. **[ANT001]** Anti-pattern description
   - Why: Explanation
   - Instead: Alternative
<!-- EXTRACT:antipatterns:end -->

## GOOD_EXAMPLE_001: Title
```language
// Code example
```
**Why this is good**: Explanation

## LLM_METADATA
```json
{
  "rule_relationships": {},
  "extraction_hints": {},
  "query_patterns": []
}
```
```

## Quick Start for LLMs

### 1. Find Relevant Rules

```python
# Load rules index
with open('rules-index.json') as f:
    rules = json.load(f)

# Find TypeScript testing rules
ts_test_rules = [
    r for r in rules['rules'].values()
    if r['language'] == 'typescript' and r['category'] == 'test-naming'
]
```

### 2. Extract Minimal Context

```python
from extract_rule_section import RuleExtractor

# Load only what you need
extractor = RuleExtractor('rule.md')
requirements = extractor.extract_requirements()
```

### 3. Check Compliance

```python
# Check code against antipatterns
antipatterns = extractor.extract_antipatterns()
for pattern in antipatterns:
    if pattern_matches(code, pattern):
        print(f"Violation: {pattern['id']} - {pattern['antipattern']}")
```

### 4. Bundle for Tasks

```python
from rule_bundler import RuleBundler

bundler = RuleBundler()
bundle = bundler.bundle_for_task("review React components")
# Returns optimized rule set with ~500-1000 tokens
```

## API Integration Examples

See `examples/llm-api-examples.md` for:

- OpenAI Function Calling
- Claude Tool Use
- LangChain Integration
- REST/GraphQL APIs
- Semantic Search
- Streaming Responses

## Performance Tips

1. **Cache Aggressively** - Rules change infrequently
2. **Use Bundles** - Pre-package common rule sets
3. **Extract Sections** - Load only needed parts
4. **Batch Operations** - Process multiple rules together
5. **Index Searches** - Use semantic embeddings for natural language queries

## Schema Files

- `schemas/rule-schema.json` - JSON Schema for metadata validation
- `schemas/rule-content-schema.yaml` - Content structure requirements

## Quick Queries

Use `llm-quick-queries.yaml` for fast lookups:

```yaml
quick_queries:
  test_naming:
    good_patterns: "Extract patterns from test-naming rules"
    fix_should_tests: "Migration steps for 'should' tests"
```

## Token Optimization

| Query Type | Typical Tokens | Sections Loaded |
|------------|---------------|-----------------|
| Rule Summary | ~50 | RULE_SUMMARY only |
| Code Review | ~200-500 | MUST_NOT_DO + bad examples |
| Code Generation | ~500-1000 | MUST_FOLLOW + good examples |
| Full Rule | ~2000-3000 | All sections |

## Contributing

When adding new rules:

1. Use the `templates/llm-optimized-rule-template.md`
2. Validate with `validate-rule.py`
3. Test extraction with `extract-rule-section.py`
4. Update `rules-index.json`

## Future Enhancements

- [ ] Embedding-based semantic search index
- [ ] Rule dependency resolver
- [ ] Auto-generated API clients
- [ ] Rule versioning system
- [ ] Interactive rule explorer