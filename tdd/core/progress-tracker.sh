#!/bin/bash
# TDD Progress Tracker - Core progress management functionality
# Handles progress state without platform-specific dependencies

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../utils/platform-detector.sh"
source "$SCRIPT_DIR/../utils/colors.sh"

# Get progress file location
get_progress_file() {
    get_config_value ".tdd.progress_file" "PROGRESS.md"
}

# Get TDD phases
get_tdd_phases() {
    # Try to get from config, fallback to default
    local phases_json
    phases_json=$(get_config_value ".tdd.phases" '["RED", "GREEN", "REFACTOR", "COVER", "COMMIT"]')
    
    # Convert JSON array to bash array
    if command -v jq > /dev/null 2>&1; then
        echo "$phases_json" | jq -r '.[]'
    else
        # Fallback if jq not available
        echo "RED"
        echo "GREEN"
        echo "REFACTOR"
        echo "COVER"
        echo "COMMIT"
    fi
}

# Check if progress file exists and has TDD content
has_active_tdd_session() {
    local progress_file
    progress_file=$(get_progress_file)
    
    [[ -f "$progress_file" ]] && grep -q "TDD Feature:" "$progress_file"
}

# Detect current TDD phase based on progress file
detect_current_phase() {
    local progress_file
    progress_file=$(get_progress_file)
    
    if ! has_active_tdd_session; then
        echo "NONE"
        return
    fi
    
    # Check phase completion based on checkmarks
    local phases
    readarray -t phases < <(get_tdd_phases)
    
    for phase in "${phases[@]}"; do
        if ! grep -q "- $phase: ✅" "$progress_file"; then
            echo "$phase"
            return
        fi
    done
    
    echo "READY_FOR_NEXT"
}

# Initialize new TDD session
init_tdd_session() {
    local feature_name="$1"
    local progress_file
    progress_file=$(get_progress_file)
    
    if [[ -z "$feature_name" ]]; then
        print_phase_message "ERROR" "Feature name is required"
        return 1
    fi
    
    print_phase_message "INFO" "Initializing TDD session: $feature_name"
    
    # Create progress file with TDD template
    cat > "$progress_file" << EOF
# TDD Feature: $feature_name

## Current Status
**Phase**: RED (Write failing test)

## TDD Cycle Progress
- RED: ❌ (Write a failing test)
- GREEN: ❌ (Write minimal code to pass)
- REFACTOR: ❌ (Improve code while keeping tests green)
- COVER: ❌ (Add more test cases for coverage)
- COMMIT: ❌ (Commit when cycle complete)

## Session Started
$(date "+%Y-%m-%d %H:%M:%S")

## Notes
- Follow TDD cycle strictly: RED → GREEN → REFACTOR → COVER → COMMIT
- Write only enough code to make tests pass
- Refactor when tests are green
- Aim for high test coverage
- Commit when cycle is complete

## Feature Description
$feature_name

## Test Cases to Implement
- [ ] Test case 1: 
- [ ] Test case 2: 
- [ ] Test case 3: 

## Implementation Notes
- 

EOF
    
    print_phase_message "SUCCESS" "TDD session initialized in $progress_file"
}

# Mark phase as complete
mark_phase_complete() {
    local phase="$1"
    local progress_file
    progress_file=$(get_progress_file)
    
    if ! has_active_tdd_session; then
        print_phase_message "ERROR" "No active TDD session found"
        return 1
    fi
    
    # Update phase status
    if grep -q "- $phase: ❌" "$progress_file"; then
        sed -i "s/- $phase: ❌/- $phase: ✅/" "$progress_file"
        print_phase_message "$phase" "Phase $phase marked complete"
        
        # Update current status
        local next_phase
        next_phase=$(get_next_phase "$phase")
        if [[ "$next_phase" != "COMPLETE" ]]; then
            update_current_status "$next_phase"
        else
            update_current_status "COMPLETE"
        fi
    else
        print_phase_message "WARNING" "Phase $phase already complete or not found"
    fi
}

# Get next phase in sequence
get_next_phase() {
    local current_phase="$1"
    local phases
    readarray -t phases < <(get_tdd_phases)
    
    for i in "${!phases[@]}"; do
        if [[ "${phases[$i]}" == "$current_phase" ]]; then
            local next_index=$((i + 1))
            if [[ $next_index -lt ${#phases[@]} ]]; then
                echo "${phases[$next_index]}"
                return
            fi
        fi
    done
    
    echo "COMPLETE"
}

# Update current status in progress file
update_current_status() {
    local new_phase="$1"
    local progress_file
    progress_file=$(get_progress_file)
    
    if [[ ! -f "$progress_file" ]]; then
        return 1
    fi
    
    # Get phase description
    local phase_desc
    case "$new_phase" in
        "RED") phase_desc="Write failing test" ;;
        "GREEN") phase_desc="Write minimal code to pass" ;;
        "REFACTOR") phase_desc="Improve code while keeping tests green" ;;
        "COVER") phase_desc="Add more test cases for coverage" ;;
        "COMMIT") phase_desc="Commit when cycle complete" ;;
        "COMPLETE") phase_desc="TDD cycle complete - ready for next feature" ;;
        *) phase_desc="Unknown phase" ;;
    esac
    
    # Update status section
    sed -i "/^\*\*Phase\*\*:/c\\**Phase**: $new_phase ($phase_desc)" "$progress_file"
}

# Get current feature name from progress file
get_current_feature() {
    local progress_file
    progress_file=$(get_progress_file)
    
    if [[ -f "$progress_file" ]]; then
        grep "# TDD Feature:" "$progress_file" | sed 's/# TDD Feature: //' | head -1
    else
        echo ""
    fi
}

# Add note to progress file
add_progress_note() {
    local note="$1"
    local progress_file
    progress_file=$(get_progress_file)
    
    if [[ ! -f "$progress_file" ]]; then
        return 1
    fi
    
    # Add timestamped note
    local timestamp
    timestamp=$(date "+%H:%M:%S")
    echo "- [$timestamp] $note" >> "$progress_file"
}

# Show current TDD status
show_tdd_status() {
    local current_phase
    local feature_name
    
    current_phase=$(detect_current_phase)
    feature_name=$(get_current_feature)
    
    if [[ "$current_phase" == "NONE" ]]; then
        print_phase_message "INFO" "No active TDD session"
        print_colored "$YELLOW" "Use: ./tdd/scripts/tdd-cycle.sh init <feature-name>"
        return
    fi
    
    print_tdd_status "$current_phase" "$feature_name"
    
    # Show recent notes
    local progress_file
    progress_file=$(get_progress_file)
    if [[ -f "$progress_file" ]]; then
        local notes
        notes=$(grep "^- \[" "$progress_file" | tail -3)
        if [[ -n "$notes" ]]; then
            print_section "Recent Notes" "$CYAN"
            echo "$notes"
        fi
    fi
}

# Clean up completed session
cleanup_session() {
    local progress_file
    progress_file=$(get_progress_file)
    
    if [[ -f "$progress_file" ]]; then
        local backup_file="${progress_file}.$(date +%Y%m%d_%H%M%S).bak"
        mv "$progress_file" "$backup_file"
        print_phase_message "SUCCESS" "Session archived to $backup_file"
    fi
}

# Export functions for use by other scripts
export -f get_progress_file
export -f get_tdd_phases
export -f has_active_tdd_session
export -f detect_current_phase
export -f init_tdd_session
export -f mark_phase_complete
export -f get_next_phase
export -f update_current_status
export -f get_current_feature
export -f add_progress_note
export -f show_tdd_status
export -f cleanup_session