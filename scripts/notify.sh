#!/bin/bash

# notify.sh - Cross-platform notification and file viewer script for Claude Code
# Usage: 
#   ./scripts/notify.sh "Your message here" [title]          # Send notification
#   ./scripts/notify.sh --md-view /path/to/file.md           # Open markdown file in browser as HTML
#   ./scripts/notify.sh --html-view /path/to/file.html       # Open HTML file in browser
#   ./scripts/notify.sh --mermaid-view /path/to/file.mmd     # Open Mermaid diagram in browser

set -e

# Check if this is a file viewer request
if [[ "$1" == "--md-view" || "$1" == "--html-view" || "$1" == "--mermaid-view" ]]; then
    if [[ -z "$2" ]]; then
        echo "Usage: $0 --md-view /path/to/file.md"
        echo "       $0 --html-view /path/to/file.html"
        echo "       $0 --mermaid-view /path/to/file.mmd"
        exit 1
    fi
    
    INPUT_FILE="$2"
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "Error: File '$INPUT_FILE' not found"
        exit 1
    fi
    
    # Determine the file to open in browser
    if [[ "$1" == "--html-view" ]]; then
        # HTML file - open directly
        HTML_FILE="$INPUT_FILE"
        echo "Opening HTML file '$INPUT_FILE' in browser"
    elif [[ "$1" == "--mermaid-view" ]]; then
        # Mermaid file - convert to HTML with Mermaid.js
        convert_mermaid_to_html() {
            local mermaid_file="$1"
            local html_file="/tmp/$(basename "$mermaid_file" .mmd).html"
            
            cat > "$html_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$(basename "$mermaid_file")</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #fff;
        }
        .mermaid {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <h1>$(basename "$mermaid_file")</h1>
    <div class="mermaid">
$(cat "$mermaid_file")
    </div>
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: { useMaxWidth: true, htmlLabels: true }
        });
    </script>
</body>
</html>
EOF
            
            echo "$html_file"
        }
        
        HTML_FILE=$(convert_mermaid_to_html "$INPUT_FILE")
        echo "Converting Mermaid diagram '$INPUT_FILE' to HTML"
    else
        # Markdown file - convert to HTML first
        convert_md_to_html() {
            local md_file="$1"
            local html_file="/tmp/$(basename "$md_file" .md).html"
            
            # Check if pandoc is available
            if command -v pandoc > /dev/null 2>&1; then
                # Create HTML with pandoc and add Mermaid support
                pandoc "$md_file" -o "$html_file" --standalone \
                    --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css \
                    --include-in-header=<(cat << 'HEADER'
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>.mermaid { background: #fff; border-radius: 4px; margin: 20px 0; }</style>
HEADER
) \
                    --include-after-body=<(cat << 'FOOTER'
<script>
mermaid.initialize({ startOnLoad: true, theme: 'default', flowchart: { useMaxWidth: true, htmlLabels: true } });
// Convert mermaid code blocks to mermaid divs
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('pre code.language-mermaid, pre code.mermaid').forEach(function(block) {
        const mermaidDiv = document.createElement('div');
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = block.textContent;
        block.parentNode.parentNode.replaceChild(mermaidDiv, block.parentNode);
    });
    mermaid.run();
});
</script>
FOOTER
)
            else
                # Fallback: Use marked.js for client-side markdown conversion with Mermaid support
                cat > "$html_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$(basename "$md_file")</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        .markdown-body { box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 45px; }
        .mermaid { background: #fff; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body class="markdown-body">
    <div id="content"></div>
    <script>
        // Initialize Mermaid
        mermaid.initialize({ 
            startOnLoad: false,
            theme: 'default',
            flowchart: { useMaxWidth: true, htmlLabels: true }
        });
        
        const markdown = \`$(cat "$md_file" | sed 's/`/\\`/g; s/\$/\\$/g')\`;
        
        // Parse markdown with marked
        let html = marked.parse(markdown);
        
        // Replace mermaid code blocks with mermaid divs
        html = html.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, 
            '<div class="mermaid">\$1</div>');
        
        // Also handle plain mermaid blocks without language specification
        html = html.replace(/<pre><code>mermaid\n([\s\S]*?)<\/code><\/pre>/g, 
            '<div class="mermaid">\$1</div>');
        
        document.getElementById('content').innerHTML = html;
        
        // Render Mermaid diagrams
        mermaid.run();
    </script>
</body>
</html>
EOF
            fi
            
            echo "$html_file"
        }
        
        HTML_FILE=$(convert_md_to_html "$INPUT_FILE")
        echo "Converting markdown file '$INPUT_FILE' to HTML"
    fi
    
    # Open in browser based on platform
    if [[ -n "$WSL_DISTRO_NAME" || -n "$WSLENV" ]]; then
        # WSL - convert Linux path to Windows path and use Windows browser
        WIN_PATH=$(wslpath -w "$HTML_FILE")
        powershell.exe -Command "Start-Process '$WIN_PATH'"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open "$HTML_FILE" 2>/dev/null || firefox "$HTML_FILE" 2>/dev/null || chromium "$HTML_FILE" 2>/dev/null
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$HTML_FILE"
    else
        echo "Platform not supported for browser opening. HTML file created at: $HTML_FILE"
    fi
    
    echo "Markdown file '$MD_FILE' opened in browser as HTML"
    exit 0
fi

MESSAGE="${1:-Claude has something to tell you!}"
TITLE="${2:-Claude Notification}"

# Function to send notification on WSL/Windows
send_windows_notification() {
    powershell.exe -Command "
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show('$MESSAGE', '$TITLE', 'OK', 'Information')
    " > /dev/null
}

# Function to send notification on Linux with notify-send
send_linux_notification() {
    if command -v notify-send > /dev/null 2>&1; then
        notify-send "$TITLE" "$MESSAGE"
    else
        echo "notify-send not found. Install with: sudo apt-get install libnotify-bin"
        return 1
    fi
}

# Function to send notification on macOS
send_macos_notification() {
    if command -v osascript > /dev/null 2>&1; then
        osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\""
    else
        echo "osascript not found (macOS required)"
        return 1
    fi
}

# Detect platform and send appropriate notification
if [[ -n "$WSL_DISTRO_NAME" || -n "$WSLENV" ]]; then
    # WSL environment
    echo "Sending Windows notification..."
    send_windows_notification
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Sending Linux notification..."
    send_linux_notification
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Sending macOS notification..."
    send_macos_notification
else
    # Fallback - just echo and beep
    echo "Platform not detected. Falling back to terminal notification."
    echo "🔔 $TITLE: $MESSAGE"
    echo -e "\a"  # Terminal bell
fi

echo "Notification sent: $MESSAGE"