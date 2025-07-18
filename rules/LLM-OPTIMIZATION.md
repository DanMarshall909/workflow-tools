# LLM Optimization Guide for Workflow-Tools Rules

This guide explains how rules are structured for optimal LLM consumption.

## Rule File Format

Each rule file follows this structure for easy parsing:

```markdown
---
rule_id: typescript-test-naming
category: test-naming
language: typescript
frameworks: [jest, react-testing-library]
severity: required
tags: [testing, naming, business-focused]
prerequisites: [universal-test-naming]
related_rules: [typescript-code-quality, eslint-config]
---

# [RULE_TITLE]

## RULE_SUMMARY
[One-line summary for quick extraction]

## APPLIES_TO
- Language: [language]
- Frameworks: [framework list]
- File patterns: [*.test.ts, *.spec.tsx]

## REQUIREMENTS

### MUST_FOLLOW
1. [Specific requirement with ID: REQ001]
2. [Specific requirement with ID: REQ002]

### MUST_NOT_DO
1. [Anti-pattern with ID: ANT001]
2. [Anti-pattern with ID: ANT002]

## EXAMPLES

### GOOD_EXAMPLE_001
```language
[code]
```
**Why**: [Explanation]

### BAD_EXAMPLE_001
```language
[code]
```
**Why not**: [Explanation]

## AUTOMATED_CHECKS
- Tool: [tool name]
- Config: [config reference]
- Command: `[command to run]`

## METRICS
- Adoption: [how to measure]
- Success: [what indicates compliance]
```

## Structured Data Formats

### 1. Rule Index (JSON)
```json
{
  "rules": {
    "typescript-test-naming": {
      "path": "typescript/test-naming/jest-react-testing-library.md",
      "category": "test-naming",
      "language": "typescript",
      "severity": "required",
      "dependencies": ["universal-test-naming"],
      "metrics": {
        "complexity": "low",
        "adoption_effort": "medium",
        "impact": "high"
      }
    }
  }
}
```

### 2. Quick Reference (YAML)
```yaml
quick_rules:
  test_naming:
    universal_principle: "Name tests as business scenarios"
    
    patterns:
      good:
        - pattern: "user_can_[action]"
          example: "user_can_login_with_valid_credentials"
        - pattern: "[business_rule]_is_enforced"
          example: "password_complexity_is_enforced"
      
      bad:
        - pattern: "should_[technical_detail]"
          reason: "Uses 'should' and focuses on implementation"
        - pattern: "test_[method_name]"
          reason: "Tied to implementation, not behavior"
```

### 3. Decision Records (Structured)
```markdown
---
decision_id: DR001
title: Business-Focused Test Names
status: accepted
date: 2024-01-20
tags: [testing, naming]
---

## DECISION
[Clear statement of decision]

## CONTEXT
[Background and problem]

## CONSEQUENCES_POSITIVE
- [Benefit 1]
- [Benefit 2]

## CONSEQUENCES_NEGATIVE
- [Drawback 1]
- [Drawback 2]

## ALTERNATIVES_CONSIDERED
1. [Alternative]: [Why rejected]
2. [Alternative]: [Why rejected]
```

## LLM-Friendly Features

### 1. Consistent Section Markers
All major sections use CAPS_WITH_UNDERSCORES for easy extraction:
- `RULE_SUMMARY`
- `MUST_FOLLOW`
- `MUST_NOT_DO`
- `GOOD_EXAMPLE_XXX`
- `BAD_EXAMPLE_XXX`

### 2. Structured Examples
Each example follows the pattern:
```
### [EXAMPLE_TYPE]_[NUMBER]
```[language]
[code]
```
**[Explanation_Type]**: [Explanation]
```

### 3. Machine-Readable Cross-References
```markdown
<!-- LLM_LINKS_START -->
- DEPENDS_ON: [rule-id-1, rule-id-2]
- RELATED_TO: [rule-id-3, rule-id-4]
- CONFLICTS_WITH: [rule-id-5]
<!-- LLM_LINKS_END -->
```

### 4. Extraction Patterns
For quick extraction of specific information:

```markdown
<!-- EXTRACT:requirements -->
1. [REQ001] Test names must describe business behavior
2. [REQ002] Test names must not include technical implementation
<!-- /EXTRACT:requirements -->
```

## Query Optimization

### Sample LLM Queries

1. **"Show me all MUST_FOLLOW rules for TypeScript testing"**
   - Parser looks for `language: typescript` + `MUST_FOLLOW` section

2. **"What are the BAD_EXAMPLE patterns for test naming?"**
   - Parser extracts all `BAD_EXAMPLE_XXX` sections from test-naming files

3. **"Give me the one-line summary of clean code principles"**
   - Parser extracts `RULE_SUMMARY` from clean-code file

### Structured Responses
Rules can be queried to return structured data:

```json
{
  "query": "test naming rules for typescript",
  "results": [
    {
      "rule_id": "typescript-test-naming",
      "summary": "Use business-focused test names without 'should' or technical details",
      "must_follow": ["describe business behavior", "use plain English"],
      "must_not_do": ["use 'should'", "include method names"],
      "example_good": "user_can_login_with_valid_credentials",
      "example_bad": "should_return_user_when_credentials_valid"
    }
  ]
}
```

## Implementation Guidelines

### 1. Converting Existing Rules
1. Add YAML front matter with metadata
2. Restructure sections with clear markers
3. Standardize example formats
4. Add extraction markers for key sections

### 2. New Rule Template
```markdown
---
rule_id: [unique-id]
category: [category]
language: [language or "universal"]
severity: [required|recommended|optional]
tags: [tag1, tag2]
---

# [Rule Title]

## RULE_SUMMARY
[One sentence summary]

## APPLIES_TO
- Language: [specifics]
- Context: [when to use]

## MUST_FOLLOW
<!-- EXTRACT:requirements -->
1. [REQ001] [Requirement]
<!-- /EXTRACT:requirements -->

## MUST_NOT_DO
<!-- EXTRACT:antipatterns -->
1. [ANT001] [Anti-pattern]
<!-- /EXTRACT:antipatterns -->

[Rest of template...]
```

### 3. Validation
Each rule file can be validated with:
```bash
# Check structure
./scripts/validate-rule-format.sh [rule-file]

# Extract metadata
./scripts/extract-rule-metadata.sh [rule-file]

# Generate index
./scripts/generate-rule-index.sh
```

## Benefits for LLMs

1. **Consistent Structure**: Predictable sections for reliable extraction
2. **Clear Boundaries**: Unambiguous section markers
3. **Metadata Rich**: Front matter provides context without parsing
4. **Query Optimized**: Structured for common question patterns
5. **Relationship Aware**: Clear dependencies and conflicts
6. **Example Focused**: Standardized format for pattern learning

## Usage with Claude/ChatGPT

### Optimal Context Loading
```markdown
Load only: 
- RULE_SUMMARY and MUST_FOLLOW from typescript-test-naming
- GOOD_EXAMPLE_001 from clean-code-principles
- Front matter from security guidelines
```

### Structured Queries
```markdown
Extract and format:
- All REQ### ids from typescript rules
- All security-related MUST_FOLLOW items
- Decision rationale from DR001
```

This optimization allows LLMs to:
- Load minimal context per query
- Extract specific sections reliably
- Understand relationships between rules
- Generate compliant code based on examples
- Validate code against requirements