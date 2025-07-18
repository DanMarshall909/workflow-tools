#!/bin/bash
# Platform Detection Utilities
# Detects project type and loads appropriate configuration

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TDD_ROOT="$(dirname "$SCRIPT_DIR")"

# Load platform configurations
PLATFORMS_CONFIG="$TDD_ROOT/config/platforms.json"
DEFAULTS_CONFIG="$TDD_ROOT/config/defaults.json"

# Detect current platform based on project files
detect_platform() {
    local current_dir="${1:-.}"
    
    # Check for platform-specific files
    if [[ -f "$current_dir/package.json" ]]; then
        echo "nodejs"
    elif find "$current_dir" -maxdepth 2 -name "*.csproj" -o -name "*.sln" | grep -q .; then
        echo "dotnet"
    elif [[ -f "$current_dir/requirements.txt" ]] || [[ -f "$current_dir/pyproject.toml" ]] || [[ -f "$current_dir/setup.py" ]]; then
        echo "python"
    elif [[ -f "$current_dir/go.mod" ]]; then
        echo "go"
    elif [[ -f "$current_dir/Cargo.toml" ]]; then
        echo "rust"
    elif [[ -f "$current_dir/Makefile" ]] || [[ -f "$current_dir/makefile" ]]; then
        echo "make"
    else
        echo "unknown"
    fi
}

# Get command for platform and action
get_platform_command() {
    local platform="$1"
    local action="$2"
    
    if ! command -v jq > /dev/null 2>&1; then
        echo "Error: jq is required for configuration parsing" >&2
        return 1
    fi
    
    # Try to get command from platform config
    local cmd
    cmd=$(jq -r ".platforms.${platform}.commands.${action} // empty" "$PLATFORMS_CONFIG" 2>/dev/null)
    
    if [[ -n "$cmd" && "$cmd" != "null" ]]; then
        echo "$cmd"
        return 0
    fi
    
    # Fallback to default commands
    cmd=$(jq -r ".fallback.commands.${action} // empty" "$PLATFORMS_CONFIG" 2>/dev/null)
    
    if [[ -n "$cmd" && "$cmd" != "null" ]]; then
        echo "$cmd"
        return 0
    fi
    
    # Ultimate fallback
    case "$action" in
        "build") echo "echo 'No build command configured'" ;;
        "test") echo "echo 'No test command configured'" ;;
        "test_quiet") echo "echo 'No quiet test command configured'" ;;
        "test_verbose") echo "echo 'No verbose test command configured'" ;;
        "coverage") echo "echo 'No coverage command configured'" ;;
        "format") echo "echo 'No format command configured'" ;;
        *) echo "echo 'Unknown action: $action'" ;;
    esac
}

# Get test output patterns for platform
get_test_patterns() {
    local platform="$1"
    
    if ! command -v jq > /dev/null 2>&1; then
        echo "Error: jq is required for configuration parsing" >&2
        return 1
    fi
    
    # Export patterns as environment variables
    export TEST_PATTERN_PASSED=$(jq -r ".platforms.${platform}.test_patterns.passed // \"([0-9]+).*pass\"" "$PLATFORMS_CONFIG")
    export TEST_PATTERN_FAILED=$(jq -r ".platforms.${platform}.test_patterns.failed // \"([0-9]+).*fail\"" "$PLATFORMS_CONFIG")
    export TEST_PATTERN_TOTAL=$(jq -r ".platforms.${platform}.test_patterns.total // \"([0-9]+).*test\"" "$PLATFORMS_CONFIG")
}

# Load configuration value
get_config_value() {
    local key="$1"
    local default_value="$2"
    
    if ! command -v jq > /dev/null 2>&1; then
        echo "${default_value:-}"
        return 0
    fi
    
    # Try project-specific config first (.tdd/config.json)
    if [[ -f ".tdd/config.json" ]]; then
        local value
        value=$(jq -r "$key // empty" ".tdd/config.json" 2>/dev/null)
        if [[ -n "$value" && "$value" != "null" ]]; then
            echo "$value"
            return 0
        fi
    fi
    
    # Fallback to defaults
    local value
    value=$(jq -r "$key // empty" "$DEFAULTS_CONFIG" 2>/dev/null)
    if [[ -n "$value" && "$value" != "null" ]]; then
        echo "$value"
    else
        echo "${default_value:-}"
    fi
}

# Check if command exists and is executable
check_command_available() {
    local cmd="$1"
    command -v $(echo "$cmd" | cut -d' ' -f1) > /dev/null 2>&1
}

# Validate platform setup
validate_platform_setup() {
    local platform="$1"
    
    echo "🔍 Validating platform setup for: $platform"
    
    # Check required commands
    local build_cmd test_cmd
    build_cmd=$(get_platform_command "$platform" "build")
    test_cmd=$(get_platform_command "$platform" "test")
    
    if ! check_command_available "$build_cmd"; then
        echo "❌ Build command not available: $build_cmd"
        return 1
    fi
    
    if ! check_command_available "$test_cmd"; then
        echo "❌ Test command not available: $test_cmd"
        return 1
    fi
    
    echo "✅ Platform setup validated"
    return 0
}

# Print platform information
show_platform_info() {
    local platform="$1"
    
    echo "📋 Platform Information:"
    echo "  Platform: $platform"
    echo "  Build: $(get_platform_command "$platform" "build")"
    echo "  Test: $(get_platform_command "$platform" "test")"
    echo "  Coverage: $(get_platform_command "$platform" "coverage")"
    echo "  Format: $(get_platform_command "$platform" "format")"
}

# Export functions for use by other scripts
export -f detect_platform
export -f get_platform_command
export -f get_test_patterns
export -f get_config_value
export -f check_command_available
export -f validate_platform_setup
export -f show_platform_info