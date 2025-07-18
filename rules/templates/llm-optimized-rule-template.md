---
rule_id: [unique-lowercase-id]
category: [test-naming|code-quality|security|git-workflow|configuration]
language: [typescript|csharp|python|universal]
frameworks: [optional-framework-list]
severity: [required|recommended|optional]
tags: [tag1, tag2, tag3]
prerequisites: [optional-prerequisite-rules]
related_rules: [optional-related-rules]
version: 1.0.0
last_updated: 2024-01-20
---

# [Rule Title]

## RULE_SUMMARY
[One sentence summary that captures the essence of the rule]

## APPLIES_TO
- **Languages**: [language list or "All"]
- **Frameworks**: [framework list or "N/A"]  
- **File Patterns**: `[*.test.ts, *.spec.js]`
- **Development Phase**: [coding|testing|review|deployment]

## REQUIREMENTS

### MUST_FOLLOW
<!-- EXTRACT:requirements:start -->
1. **[REQ001]** [First requirement with clear ID]
   - Rationale: [Why this matters]
   - Impact: [What happens if not followed]

2. **[REQ002]** [Second requirement]
   - Rationale: [Why this matters]
   - Impact: [What happens if not followed]
<!-- EXTRACT:requirements:end -->

### MUST_NOT_DO
<!-- EXTRACT:antipatterns:start -->
1. **[ANT001]** [First anti-pattern with clear ID]
   - Why: [Explanation of why this is bad]
   - Instead: [What to do instead]

2. **[ANT002]** [Second anti-pattern]
   - Why: [Explanation]
   - Instead: [Alternative]
<!-- EXTRACT:antipatterns:end -->

## EXAMPLES

### GOOD_EXAMPLE_001: [Description]
```[language]
// Context: [Setup context]
[code example]
```
**Why this is good**: [Specific explanation]

### GOOD_EXAMPLE_002: [Description]
```[language]
[code example]
```
**Why this is good**: [Specific explanation]

### BAD_EXAMPLE_001: [Description]
```[language]
// Anti-pattern: [What's wrong]
[code example]
```
**Why this is bad**: [Specific explanation]
**Better approach**: See GOOD_EXAMPLE_001

### BAD_EXAMPLE_002: [Description]
```[language]
[code example]
```
**Why this is bad**: [Specific explanation]
**Better approach**: See GOOD_EXAMPLE_002

## PATTERNS

### Pattern Recognition
<!-- EXTRACT:patterns:start -->
- **PATTERN_GOOD_001**: `[pattern regex or description]`
  - Example: `user_can_[action]`
  - Matches: `user_can_login`, `user_can_reset_password`

- **PATTERN_BAD_001**: `[pattern regex or description]`
  - Example: `should_[anything]`
  - Avoid because: [reason]
<!-- EXTRACT:patterns:end -->

## AUTOMATED_CHECKS

### Linting Configuration
```[config-language]
// Tool: [ESLint/RuboCop/etc]
{
  "rules": {
    "[rule-name]": ["error", { "config": "value" }]
  }
}
```

### Validation Commands
```bash
# Check compliance
[command to check rule compliance]

# Auto-fix where possible
[command to auto-fix]
```

### CI Integration
```yaml
# Example GitHub Actions check
- name: Check [rule name]
  run: |
    [validation command]
```

## METRICS

### Measuring Compliance
<!-- EXTRACT:metrics:start -->
- **Metric**: [What to measure]
  - **Target**: [Desired value]
  - **Query**: `[command or search to measure]`
  
- **Metric**: Test naming compliance
  - **Target**: 100% business-focused names
  - **Query**: `grep -r "should\|Should" --include="*.test.*" | wc -l` (should be 0)
<!-- EXTRACT:metrics:end -->

### Success Indicators
- [Indicator 1]: [How to recognize success]
- [Indicator 2]: [How to recognize success]

## MIGRATION_GUIDE

### Adopting in Existing Code
1. **Step 1**: [First migration step]
   ```bash
   [helpful command]
   ```

2. **Step 2**: [Second step]
   ```bash
   [helpful command]
   ```

### Common Challenges
- **Challenge**: [Common issue]
  - **Solution**: [How to address]

## CONTEXT_AND_RATIONALE

### Why This Rule Exists
[Brief explanation of the problem this solves]

### Evidence and Research
- [Link to research/article]
- [Real-world case study]

### Trade-offs
- **Benefits**: [List benefits]
- **Costs**: [List any downsides]

## ENFORCEMENT_LEVEL

### When to Apply
- **Always**: [Scenarios where this is mandatory]
- **Usually**: [Scenarios where this is recommended]
- **Sometimes**: [Scenarios where this might not apply]

### Exceptions
- [Valid exception scenario 1]
- [Valid exception scenario 2]

## LLM_METADATA
<!-- This section helps LLMs understand relationships and context -->
```json
{
  "rule_relationships": {
    "depends_on": ["rule-id-1", "rule-id-2"],
    "enhances": ["rule-id-3"],
    "conflicts_with": [],
    "supersedes": []
  },
  "extraction_hints": {
    "key_concept": "[main concept]",
    "problem_solved": "[problem this addresses]",
    "applicable_contexts": ["context1", "context2"]
  },
  "query_patterns": [
    "How do I [action] in [language]?",
    "What is the best practice for [concept]?",
    "Show me examples of [pattern]"
  ]
}
```

---
<!-- LLM_INSTRUCTION: This rule can be summarized as: [one-line summary for quick reference] -->