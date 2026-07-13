import glob
import re

html_files = glob.glob('c:/Users/anand/Downloads/Expo_website/*.html')

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace styles.css?v=X or styles.css with styles.css?v=7
    content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=7', content)
    content = re.sub(r'styles\.css"', 'styles.css?v=7"', content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
