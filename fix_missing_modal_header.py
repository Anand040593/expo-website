import glob
import re

html_files = glob.glob('c:/Users/anand/Downloads/Expo_website/*.html')

for fpath in html_files:
    if fpath.endswith('admin.html') or fpath.endswith('admin-login.html'):
        continue
        
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if modal-item-name exists
    if 'id="modal-item-name"' not in content:
        # Find <div class="modal-body">
        idx = content.find('<div class="modal-body">')
        if idx != -1:
            insertion_idx = idx + len('<div class="modal-body">')
            insertion = '\n                <p id="modal-item-name" class="modal-item">Item Name</p>\n                <h2 id="modal-amount" class="modal-price">₹10</h2>'
            content = content[:insertion_idx] + insertion + content[insertion_idx:]
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {fpath}")
        else:
            print(f"Could not find modal-body in {fpath}")
    else:
        print(f"Already has modal-item-name: {fpath}")
