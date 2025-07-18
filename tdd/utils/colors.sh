#!/bin/bash
# Color and Output Utilities
# Provides consistent color output and emoji support

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/platform-detector.sh"

# Initialize colors based on configuration
init_colors() {
    local colors_enabled
    colors_enabled=$(get_config_value ".tdd.colors.enabled" "true")
    
    if [[ "$colors_enabled" == "true" && -t 1 ]]; then
        # Colors enabled and outputting to terminal
        export RED=$(get_config_value ".tdd.colors.red" '\033[0;31m')
        export GREEN=$(get_config_value ".tdd.colors.green" '\033[0;32m')
        export YELLOW=$(get_config_value ".tdd.colors.yellow" '\033[1;33m')
        export BLUE=$(get_config_value ".tdd.colors.blue" '\033[0;34m')
        export CYAN=$(get_config_value ".tdd.colors.cyan" '\033[0;36m')
        export NC=$(get_config_value ".tdd.colors.reset" '\033[0m')
    else
        # Colors disabled or not a terminal
        export RED=""
        export GREEN=""
        export YELLOW=""
        export BLUE=""
        export CYAN=""
        export NC=""
    fi
}

# Initialize emojis based on configuration
init_emojis() {
    local emojis_enabled
    emojis_enabled=$(get_config_value ".tdd.emojis.enabled" "true")
    
    if [[ "$emojis_enabled" == "true" ]]; then
        export EMOJI_RED=$(get_config_value ".tdd.emojis.red" "🔴")
        export EMOJI_GREEN=$(get_config_value ".tdd.emojis.green" "🟢")
        export EMOJI_REFACTOR=$(get_config_value ".tdd.emojis.refactor" "🔧")
        export EMOJI_COVER=$(get_config_value ".tdd.emojis.cover" "📊")
        export EMOJI_COMMIT=$(get_config_value ".tdd.emojis.commit" "✅")
        export EMOJI_THINKING=$(get_config_value ".tdd.emojis.thinking" "🤔")
        export EMOJI_RUNNING=$(get_config_value ".tdd.emojis.running" "🏃")
        export EMOJI_SUCCESS=$(get_config_value ".tdd.emojis.success" "🎉")
    else
        export EMOJI_RED=""
        export EMOJI_GREEN=""
        export EMOJI_REFACTOR=""
        export EMOJI_COVER=""
        export EMOJI_COMMIT=""
        export EMOJI_THINKING=""
        export EMOJI_RUNNING=""
        export EMOJI_SUCCESS=""
    fi
}

# Print colored message
print_colored() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

# Print phase-specific message
print_phase_message() {
    local phase="$1"
    local message="$2"
    
    case "$phase" in
        "RED")
            print_colored "$RED" "${EMOJI_RED} $message"
            ;;
        "GREEN")
            print_colored "$GREEN" "${EMOJI_GREEN} $message"
            ;;
        "REFACTOR")
            print_colored "$YELLOW" "${EMOJI_REFACTOR} $message"
            ;;
        "COVER")
            print_colored "$BLUE" "${EMOJI_COVER} $message"
            ;;
        "COMMIT")
            print_colored "$CYAN" "${EMOJI_COMMIT} $message"
            ;;
        "INFO")
            print_colored "$BLUE" "${EMOJI_THINKING} $message"
            ;;
        "SUCCESS")
            print_colored "$GREEN" "${EMOJI_SUCCESS} $message"
            ;;
        "ERROR")
            print_colored "$RED" "❌ $message"
            ;;
        "WARNING")
            print_colored "$YELLOW" "⚠️  $message"
            ;;
        *)
            echo "$message"
            ;;
    esac
}

# Print section header
print_section() {
    local title="$1"
    local color="${2:-$BLUE}"
    echo
    print_colored "$color" "═══ $title ═══"
    echo
}

# Print progress indicator
print_progress() {
    local current="$1"
    local total="$2"
    local description="$3"
    
    local percentage=$((current * 100 / total))
    local filled=$((current * 20 / total))
    local empty=$((20 - filled))
    
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="█"; done
    for ((i=0; i<empty; i++)); do bar+="░"; done
    
    print_colored "$BLUE" "[$bar] $percentage% - $description"
}

# Print command being executed
print_command() {
    local cmd="$1"
    print_colored "$CYAN" "${EMOJI_RUNNING} Executing: $cmd"
}

# Print TDD phase status
print_tdd_status() {
    local current_phase="$1"
    local feature_name="$2"
    
    print_section "TDD Status" "$BLUE"
    print_colored "$CYAN" "Feature: $feature_name"
    print_colored "$CYAN" "Current Phase: $current_phase"
    
    # Show phase checklist
    local phases=("RED" "GREEN" "REFACTOR" "COVER" "COMMIT")
    for phase in "${phases[@]}"; do
        if [[ "$phase" == "$current_phase" ]]; then
            print_colored "$YELLOW" "▶ $phase (current)"
        else
            print_colored "$GREEN" "✓ $phase"
        fi
    done
    echo
}

# Initialize colors and emojis when sourced
init_colors
init_emojis

# Export functions for use by other scripts
export -f init_colors
export -f init_emojis
export -f print_colored
export -f print_phase_message
export -f print_section
export -f print_progress
export -f print_command
export -f print_tdd_status