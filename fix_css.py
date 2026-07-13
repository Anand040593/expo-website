import re

with open(r'c:\Users\anand\Downloads\Expo_website\styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

missing_css = """
.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}

.modal-content {
    background: linear-gradient(135deg, rgba(20, 25, 45, 0.9), rgba(10, 15, 30, 0.95));
    border: 1px solid var(--glass-highlight);
    padding: 40px;
    border-radius: 30px;
    width: 90%;
    max-width: 450px;
    position: relative;
    transform: translateY(40px) scale(0.95);
    transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    box-shadow: 0 30px 60px rgba(0,0,0,0.6), 0 0 30px rgba(255, 107, 0, 0.1);
    max-height: 90vh;
    overflow-y: auto;
}

.modal-overlay.active .modal-content {
    transform: translateY(0) scale(1);
}

/* Custom Scrollbar for Modal to match theme */
.modal-content::-webkit-scrollbar {
    width: 6px;
}
.modal-content::-webkit-scrollbar-track {
    background: transparent;
}
.modal-content::-webkit-scrollbar-thumb {
    background: var(--glass-border);
    border-radius: 10px;
}
.modal-content::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

"""

# find .modal-header and insert before it
idx = content.find('.modal-header {')
if idx != -1:
    content = content[:idx] + missing_css + content[idx:]
    with open(r'c:\Users\anand\Downloads\Expo_website\styles.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed CSS")
