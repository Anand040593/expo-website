import glob
import re

html_files = glob.glob('c:/Users/anand/Downloads/Expo_website/*.html')

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'script\.js\?v=\d+', 'script.js?v=8', content)
    content = re.sub(r'script\.js"', 'script.js?v=8"', content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
