# Universal TDD Framework

A platform-agnostic Test-Driven Development workflow automation framework that works with any programming language and testing framework.

## Features

### 🔄 **Universal TDD Cycle**
- **RED**: Write failing tests
- **GREEN**: Write minimal code to pass
- **REFACTOR**: Improve code while keeping tests green  
- **COVER**: Add comprehensive test coverage
- **COMMIT**: Commit when cycle complete

### 🌐 **Multi-Platform Support**
- **Automatic Detection**: Supports .NET, Node.js, Python, Go, Rust, and Make
- **Configurable Commands**: Custom test/build commands per project
- **Framework Agnostic**: Works with any testing framework

### 📊 **Intelligent Automation**
- **Phase Detection**: Auto-detects current TDD phase from test results
- **Progress Tracking**: Maintains session state across development cycles
- **Smart Advancement**: Auto-advance when phase conditions are met

### 🎨 **Rich Output**
- **Colorized Output**: Phase-specific colors and emojis
- **Progress Visualization**: Clear status and completion indicators
- **Configurable Display**: Disable colors/emojis for CI environments

## Quick Start

### 1. Initialize TDD Session
```bash
./tdd/scripts/tdd-cycle.sh init "user-authentication-feature"
```

### 2. Run Tests
```bash
./tdd/scripts/tdd-cycle.sh test           # Normal mode
./tdd/scripts/tdd-cycle.sh test verbose   # Verbose output
./tdd/scripts/tdd-cycle.sh test quiet     # Minimal output
```

### 3. Watch Tests Continuously  
```bash
./tdd/scripts/tdd-cycle.sh watch 5        # Check every 5 seconds
```

### 4. Advance Through Phases
```bash
./tdd/scripts/tdd-cycle.sh advance        # Auto-advance when ready
./tdd/scripts/tdd-cycle.sh complete RED   # Manual phase completion
```

### 5. Check Status
```bash
./tdd/scripts/tdd-cycle.sh status         # Show current status
./tdd/scripts/tdd-cycle.sh platform       # Show platform info
```

## Supported Platforms

| Platform | Detection Files | Test Command | Build Command |
|----------|----------------|--------------|---------------|
| **.NET** | `*.csproj`, `*.sln` | `dotnet test` | `dotnet build` |
| **Node.js** | `package.json` | `npm test` | `npm run build` |
| **Python** | `requirements.txt`, `pyproject.toml` | `pytest` | `python -m build` |
| **Go** | `go.mod` | `go test ./...` | `go build ./...` |
| **Rust** | `Cargo.toml` | `cargo test` | `cargo build` |
| **Make** | `Makefile` | `make test` | `make build` |

## Configuration

### Project Configuration
Create `.tdd/config.json` in your project root:

```json
{
  "platform": "nodejs",
  "tdd": {
    "progress_file": "PROGRESS.md",
    "auto_advance": true,
    "break_enforcement": false,
    "phases": ["RED", "GREEN", "REFACTOR", "COVER", "COMMIT"]
  },
  "commands": {
    "build": "npm run build",
    "test": "npm test",
    "coverage": "npm run test:coverage"
  },
  "quality": {
    "coverage_threshold": 80,
    "enforce_thresholds": true
  }
}
```

### Global Configuration
Edit `tdd/config/defaults.json` for framework defaults:

```json
{
  "tdd": {
    "colors": {
      "enabled": true,
      "red": "\\033[0;31m",
      "green": "\\033[0;32m"
    },
    "emojis": {
      "enabled": true,
      "red": "🔴",
      "green": "🟢"
    }
  }
}
```

## Architecture

### Modular Design
```
tdd/
├── core/                   # Platform-agnostic core logic
│   ├── progress-tracker.sh # TDD session state management
│   └── test-runner.sh      # Test execution and analysis
├── utils/                  # Shared utilities
│   ├── platform-detector.sh # Platform detection and commands
│   └── colors.sh           # Output formatting
├── config/                 # Configuration files
│   ├── platforms.json      # Platform-specific settings
│   └── defaults.json       # Default configuration
└── scripts/                # User-facing scripts
    └── tdd-cycle.sh        # Main TDD workflow orchestrator
```

### Key Principles

1. **Separation of Concerns**: Core logic separated from platform specifics
2. **Configuration-Driven**: Behavior controlled via JSON configuration
3. **Extensible**: Easy to add new platforms and commands
4. **Testable**: Each module can be tested independently

## Usage Examples

### Basic TDD Workflow
```bash
# Start new feature
./tdd/scripts/tdd-cycle.sh init "shopping-cart"

# Write failing test, then check status
./tdd/scripts/tdd-cycle.sh test
# Output: 🔴 RED phase condition met

# Write minimal code, then test again  
./tdd/scripts/tdd-cycle.sh test
# Output: 🟢 GREEN phase condition met

# Advance to next phase
./tdd/scripts/tdd-cycle.sh advance
# Output: ✅ Advanced to REFACTOR phase
```

### Continuous Development
```bash
# Watch tests continuously during development
./tdd/scripts/tdd-cycle.sh watch 10

# Add notes to progress
./tdd/scripts/tdd-cycle.sh note "Implemented user validation logic"

# Check overall status
./tdd/scripts/tdd-cycle.sh status
```

### Platform Validation
```bash
# Verify platform setup
./tdd/scripts/tdd-cycle.sh validate

# Show detected platform info
./tdd/scripts/tdd-cycle.sh platform
```

## Integration

### As Git Submodule
```bash
# Add to your project
git submodule add https://github.com/user/workflow-tools.git workflow-tools

# Use TDD framework
./workflow-tools/tdd/scripts/tdd-cycle.sh init "new-feature"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run TDD Tests
  run: |
    ./workflow-tools/tdd/scripts/tdd-cycle.sh test quiet
```

### IDE Integration
Add keyboard shortcuts for common TDD actions:
- **F5**: `./workflow-tools/tdd/scripts/tdd-cycle.sh test`
- **F6**: `./workflow-tools/tdd/scripts/tdd-cycle.sh advance`
- **F7**: `./workflow-tools/tdd/scripts/tdd-cycle.sh watch`

## Advanced Features

### Custom Commands
Override platform defaults in project config:
```json
{
  "commands": {
    "test": "npm run test:unit",
    "coverage": "npm run test:coverage -- --threshold=90"
  }
}
```

### Break Enforcement
Enable mandatory breaks for ADHD-friendly development:
```json
{
  "tdd": {
    "break_enforcement": true,
    "break_interval_minutes": 25
  }
}
```

### Phase Customization
Define custom TDD phases:
```json
{
  "tdd": {
    "phases": ["RED", "GREEN", "REFACTOR", "COVER", "REVIEW", "COMMIT"]
  }
}
```

## Requirements

### Minimal Requirements
- **Bash 4.0+**: Core shell functionality
- **git**: For progress tracking and integration

### Recommended
- **jq**: For advanced JSON configuration parsing
- **Platform Tools**: Language-specific build/test tools

### Platform-Specific
- **.NET**: `dotnet` CLI
- **Node.js**: `npm` or `yarn`
- **Python**: `python` and `pip`
- **Go**: `go` toolchain
- **Rust**: `cargo`

## Contributing

### Adding New Platforms
1. Update `config/platforms.json` with detection patterns and commands
2. Add test result parsing patterns
3. Test with real projects

### Extending Core Features
1. Add functionality to appropriate module (`core/`, `utils/`)
2. Update main script (`scripts/tdd-cycle.sh`)
3. Add configuration options to `config/defaults.json`

## License

MIT License - See LICENSE file for details.

## Credits

Extracted and universalized from the Anchor project's TDD automation system.
Designed for maximum portability and developer productivity.