#!/bin/bash
# Universal TDD Cycle Manager
# Platform-agnostic TDD workflow automation
# Usage: ./tdd/scripts/tdd-cycle.sh <action> [args]

set -e

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TDD_ROOT="$(dirname "$SCRIPT_DIR")"

# Load core modules
source "$TDD_ROOT/utils/platform-detector.sh"
source "$TDD_ROOT/utils/colors.sh"
source "$TDD_ROOT/core/progress-tracker.sh"
source "$TDD_ROOT/core/test-runner.sh"

# Display usage information
show_usage() {
    cat << EOF
Universal TDD Cycle Manager

USAGE:
    $0 <action> [arguments]

ACTIONS:
    init <feature-name>     Initialize new TDD session
    status                  Show current TDD status
    test [mode]            Run tests (mode: quiet|normal|verbose)
    watch [interval]       Watch tests continuously
    advance                Advance to next TDD phase
    complete <phase>       Mark current phase complete
    note "<message>"       Add note to progress
    platform              Show platform information
    validate              Validate platform setup
    cleanup               Archive current session
    help                  Show this help

EXAMPLES:
    $0 init "user-authentication"
    $0 test verbose
    $0 watch 5
    $0 advance
    $0 complete RED
    $0 note "Added user validation test"

CONFIGURATION:
    Create .tdd/config.json in your project to override defaults.
    See tdd/config/defaults.json for available options.

EOF
}

# Initialize project-specific TDD configuration
init_project_config() {
    local platform
    platform=$(detect_platform)
    
    if [[ ! -d ".tdd" ]]; then
        mkdir -p ".tdd"
        print_phase_message "INFO" "Created .tdd directory for project configuration"
    fi
    
    if [[ ! -f ".tdd/config.json" ]]; then
        cat > ".tdd/config.json" << EOF
{
  "platform": "$platform",
  "tdd": {
    "progress_file": "PROGRESS.md",
    "auto_advance": true,
    "break_enforcement": false
  },
  "quality": {
    "coverage_threshold": 80,
    "enforce_thresholds": true
  },
  "commands": {
    "custom_build": "",
    "custom_test": "",
    "custom_coverage": ""
  }
}
EOF
        print_phase_message "SUCCESS" "Created .tdd/config.json with $platform defaults"
        print_colored "$CYAN" "Edit .tdd/config.json to customize TDD workflow"
    fi
}

# Auto-advance to next phase if conditions are met
auto_advance_phase() {
    local auto_advance
    auto_advance=$(get_config_value ".tdd.auto_advance" "true")
    
    if [[ "$auto_advance" != "true" ]]; then
        return 0
    fi
    
    if [[ "$TDD_PHASE_COMPLETE" == "true" ]]; then
        local current_phase next_phase
        current_phase=$(detect_current_phase)
        next_phase=$(get_next_phase "$current_phase")
        
        if [[ "$next_phase" != "COMPLETE" ]]; then
            print_phase_message "INFO" "Auto-advancing from $current_phase to $next_phase"
            mark_phase_complete "$current_phase"
            add_progress_note "Auto-advanced from $current_phase to $next_phase"
        fi
    fi
}

# Main script logic
main() {
    local action="${1:-help}"
    
    # Initialize colors and platform detection
    init_colors
    init_emojis
    
    case "$action" in
        "init")
            local feature_name="$2"
            if [[ -z "$feature_name" ]]; then
                print_phase_message "ERROR" "Feature name required for init"
                echo "Usage: $0 init <feature-name>"
                exit 1
            fi
            
            init_project_config
            init_tdd_session "$feature_name"
            ;;
            
        "status")
            local platform
            platform=$(detect_platform)
            print_section "TDD Status" "$BLUE"
            show_platform_info "$platform"
            echo
            show_tdd_status
            ;;
            
        "test")
            local mode="${2:-normal}"
            run_tests_with_build "$mode"
            suggest_next_action
            auto_advance_phase
            ;;
            
        "watch")
            local interval="${2:-10}"
            local mode="${3:-normal}"
            watch_tests "$interval" "$mode"
            ;;
            
        "advance")
            local current_phase
            current_phase=$(detect_current_phase)
            
            if [[ "$current_phase" == "NONE" ]]; then
                print_phase_message "ERROR" "No active TDD session"
                exit 1
            fi
            
            # Run tests first to validate advancement
            run_tests_with_build "quiet"
            
            if [[ "$TDD_PHASE_COMPLETE" == "true" ]]; then
                mark_phase_complete "$current_phase"
                add_progress_note "Advanced from $current_phase phase"
                print_phase_message "SUCCESS" "Advanced to next phase"
            else
                print_phase_message "ERROR" "Cannot advance - phase conditions not met"
                suggest_next_action
                exit 1
            fi
            ;;
            
        "complete")
            local phase="$2"
            if [[ -z "$phase" ]]; then
                print_phase_message "ERROR" "Phase name required"
                echo "Usage: $0 complete <RED|GREEN|REFACTOR|COVER|COMMIT>"
                exit 1
            fi
            
            mark_phase_complete "$phase"
            add_progress_note "Manually completed $phase phase"
            ;;
            
        "note")
            local message="$2"
            if [[ -z "$message" ]]; then
                print_phase_message "ERROR" "Note message required"
                echo "Usage: $0 note \"<message>\""
                exit 1
            fi
            
            add_progress_note "$message"
            print_phase_message "SUCCESS" "Note added to progress"
            ;;
            
        "platform")
            local platform
            platform=$(detect_platform)
            show_platform_info "$platform"
            validate_platform_setup "$platform"
            ;;
            
        "validate")
            local platform
            platform=$(detect_platform)
            print_section "Platform Validation"
            
            if validate_platform_setup "$platform"; then
                print_phase_message "SUCCESS" "Platform setup is valid"
            else
                print_phase_message "ERROR" "Platform setup validation failed"
                exit 1
            fi
            ;;
            
        "cleanup")
            cleanup_session
            ;;
            
        "help"|"--help"|"-h")
            show_usage
            ;;
            
        *)
            print_phase_message "ERROR" "Unknown action: $action"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    # Check for jq (recommended but not required)
    if ! command -v jq > /dev/null 2>&1; then
        print_phase_message "WARNING" "jq not found - using fallback parsing (install jq for better experience)"
    fi
    
    # Platform-specific dependency checks would go here
    local platform
    platform=$(detect_platform)
    
    if [[ "$platform" == "unknown" ]]; then
        print_phase_message "WARNING" "Unknown platform - some features may not work correctly"
    fi
}

# Run dependency check and main function
check_dependencies
main "$@"