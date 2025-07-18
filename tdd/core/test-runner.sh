#!/bin/bash
# TDD Test Runner - Platform-agnostic test execution and analysis
# Handles test execution and result parsing for any platform

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../utils/platform-detector.sh"
source "$SCRIPT_DIR/../utils/colors.sh"
source "$SCRIPT_DIR/progress-tracker.sh"

# Run tests and return structured results
run_tests() {
    local mode="${1:-normal}"  # quiet, normal, verbose
    local platform
    platform=$(detect_platform)
    
    print_command "Running tests in $mode mode for $platform"
    
    # Get appropriate test command
    local test_cmd
    case "$mode" in
        "quiet")
            test_cmd=$(get_platform_command "$platform" "test_quiet")
            ;;
        "verbose")
            test_cmd=$(get_platform_command "$platform" "test_verbose")
            ;;
        *)
            test_cmd=$(get_platform_command "$platform" "test")
            ;;
    esac
    
    if [[ -z "$test_cmd" ]]; then
        print_phase_message "ERROR" "No test command configured for platform: $platform"
        return 1
    fi
    
    # Execute tests and capture output
    local test_output
    local test_exit_code
    local temp_file
    temp_file=$(mktemp)
    
    print_phase_message "INFO" "Executing: $test_cmd"
    
    # Run command and capture both stdout and stderr
    eval "$test_cmd" 2>&1 | tee "$temp_file"
    test_exit_code=${PIPESTATUS[0]}
    
    test_output=$(cat "$temp_file")
    rm -f "$temp_file"
    
    # Parse test results
    parse_test_results "$platform" "$test_output" "$test_exit_code"
}

# Parse test output and extract metrics
parse_test_results() {
    local platform="$1"
    local test_output="$2"
    local exit_code="$3"
    
    # Load test patterns for platform
    get_test_patterns "$platform"
    
    # Extract test counts using platform-specific patterns
    local passed_count=0
    local failed_count=0
    local total_count=0
    
    if [[ -n "$TEST_PATTERN_PASSED" ]]; then
        passed_count=$(echo "$test_output" | grep -oE "$TEST_PATTERN_PASSED" | grep -oE '[0-9]+' | tail -1)
        passed_count=${passed_count:-0}
    fi
    
    if [[ -n "$TEST_PATTERN_FAILED" ]]; then
        failed_count=$(echo "$test_output" | grep -oE "$TEST_PATTERN_FAILED" | grep -oE '[0-9]+' | tail -1)
        failed_count=${failed_count:-0}
    fi
    
    if [[ -n "$TEST_PATTERN_TOTAL" ]]; then
        total_count=$(echo "$test_output" | grep -oE "$TEST_PATTERN_TOTAL" | grep -oE '[0-9]+' | tail -1)
        total_count=${total_count:-$((passed_count + failed_count))}
    fi
    
    # Export results for other scripts
    export TDD_TEST_PASSED="$passed_count"
    export TDD_TEST_FAILED="$failed_count"
    export TDD_TEST_TOTAL="$total_count"
    export TDD_TEST_EXIT_CODE="$exit_code"
    
    # Display results
    print_section "Test Results"
    print_colored "$GREEN" "✓ Passed: $passed_count"
    print_colored "$RED" "✗ Failed: $failed_count"
    print_colored "$BLUE" "📊 Total: $total_count"
    print_colored "$CYAN" "Exit Code: $exit_code"
    
    # Determine TDD phase status
    analyze_tdd_phase_status "$passed_count" "$failed_count" "$exit_code"
    
    return "$exit_code"
}

# Analyze test results for TDD phase completion
analyze_tdd_phase_status() {
    local passed="$1"
    local failed="$2"
    local exit_code="$3"
    
    local current_phase
    current_phase=$(detect_current_phase)
    
    print_section "TDD Phase Analysis"
    
    case "$current_phase" in
        "RED")
            if [[ $failed -gt 0 ]]; then
                print_phase_message "RED" "RED phase condition met - tests are failing"
                print_colored "$GREEN" "✅ Ready to advance to GREEN phase"
                export TDD_PHASE_COMPLETE="true"
            else
                print_phase_message "WARNING" "RED phase incomplete - no failing tests found"
                print_colored "$YELLOW" "Write a failing test to complete RED phase"
                export TDD_PHASE_COMPLETE="false"
            fi
            ;;
        "GREEN")
            if [[ $failed -eq 0 && $passed -gt 0 ]]; then
                print_phase_message "GREEN" "GREEN phase condition met - all tests passing"
                print_colored "$GREEN" "✅ Ready to advance to REFACTOR phase"
                export TDD_PHASE_COMPLETE="true"
            else
                print_phase_message "WARNING" "GREEN phase incomplete - tests still failing"
                print_colored "$YELLOW" "Write minimal code to make tests pass"
                export TDD_PHASE_COMPLETE="false"
            fi
            ;;
        "REFACTOR"|"COVER")
            if [[ $failed -eq 0 && $passed -gt 0 ]]; then
                print_phase_message "$current_phase" "$current_phase phase - tests still passing"
                print_colored "$GREEN" "✅ Safe to continue refactoring/adding coverage"
                export TDD_PHASE_COMPLETE="true"
            else
                print_phase_message "ERROR" "Tests broken during $current_phase phase!"
                print_colored "$RED" "❌ Fix failing tests before continuing"
                export TDD_PHASE_COMPLETE="false"
            fi
            ;;
        "COMMIT")
            if [[ $failed -eq 0 && $passed -gt 0 ]]; then
                print_phase_message "COMMIT" "Ready to commit - all tests passing"
                export TDD_PHASE_COMPLETE="true"
            else
                print_phase_message "ERROR" "Cannot commit with failing tests"
                export TDD_PHASE_COMPLETE="false"
            fi
            ;;
        *)
            print_phase_message "INFO" "No active TDD session or unknown phase"
            export TDD_PHASE_COMPLETE="unknown"
            ;;
    esac
}

# Run build before tests
run_build() {
    local platform
    platform=$(detect_platform)
    
    local build_cmd
    build_cmd=$(get_platform_command "$platform" "build")
    
    if [[ -z "$build_cmd" ]] || [[ "$build_cmd" == *"No build command"* ]]; then
        print_phase_message "INFO" "No build command configured, skipping build"
        return 0
    fi
    
    print_command "Building project: $build_cmd"
    
    if eval "$build_cmd"; then
        print_phase_message "SUCCESS" "Build completed successfully"
        return 0
    else
        print_phase_message "ERROR" "Build failed"
        return 1
    fi
}

# Run tests with build
run_tests_with_build() {
    local mode="${1:-normal}"
    
    print_section "TDD Test Execution"
    
    # Build first if configured
    if ! run_build; then
        print_phase_message "ERROR" "Build failed, cannot run tests"
        return 1
    fi
    
    # Run tests
    run_tests "$mode"
}

# Suggest next action based on test results and TDD phase
suggest_next_action() {
    local current_phase
    current_phase=$(detect_current_phase)
    
    if [[ "$TDD_PHASE_COMPLETE" == "true" ]]; then
        local next_phase
        next_phase=$(get_next_phase "$current_phase")
        
        print_section "Next Action"
        case "$next_phase" in
            "GREEN")
                print_phase_message "GREEN" "Write minimal code to make the failing test pass"
                ;;
            "REFACTOR")
                print_phase_message "REFACTOR" "Clean up code while keeping tests green"
                ;;
            "COVER")
                print_phase_message "COVER" "Add more test cases for better coverage"
                ;;
            "COMMIT")
                print_phase_message "COMMIT" "Commit your changes and start next cycle"
                ;;
            "COMPLETE")
                print_phase_message "SUCCESS" "TDD cycle complete! Start new feature."
                ;;
        esac
        
        print_colored "$CYAN" "Run: ./tdd/scripts/tdd-cycle.sh advance"
    else
        print_section "Current Phase"
        case "$current_phase" in
            "RED")
                print_phase_message "RED" "Continue writing failing tests"
                ;;
            "GREEN")
                print_phase_message "GREEN" "Fix failing tests with minimal code"
                ;;
            *)
                print_phase_message "INFO" "Fix issues before advancing"
                ;;
        esac
    fi
}

# Watch tests continuously
watch_tests() {
    local interval="${1:-10}"
    local watch_mode="${2:-normal}"
    
    print_section "TDD Test Watcher"
    print_phase_message "INFO" "Watching tests every $interval seconds (Ctrl+C to stop)"
    
    while true; do
        clear
        print_section "TDD Test Watcher - $(date)"
        
        run_tests_with_build "$watch_mode"
        suggest_next_action
        
        print_colored "$CYAN" "Next check in $interval seconds..."
        sleep "$interval"
    done
}

# Export functions for use by other scripts
export -f run_tests
export -f parse_test_results
export -f analyze_tdd_phase_status
export -f run_build
export -f run_tests_with_build
export -f suggest_next_action
export -f watch_tests