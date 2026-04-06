import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

def clean_latex(text):
    if not text:
        return ""
    # Converts {St\"{u}ckard} to Stückard and removes extra braces
    return LatexNodes2Text().latex_to_text(text)

def generate_html():
    # 1. Load the BibTeX file
    try:
        with open('papers.bib', encoding='utf-8') as bibfile:
            db = bibtexparser.load(bibfile)
    except FileNotFoundError:
        print("Error: papers.bib not found.")
        return

    html_output = ""
    # Sort entries by year descending if possible
    entries = sorted(db.entries, key=lambda x: x.get('year', '0'), reverse=True)

for entry in db.entries:
        # Core Data
        title = clean_latex(entry.get('title', 'No Title'))
        author = clean_latex(entry.get('author', 'Unknown Author'))
        year = clean_latex(entry.get('year', 'N/A'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', '')))
        abstract = clean_latex(entry.get('abstract', '')) # Get the abstract
        
        # Link Logic
        arxiv_id = entry.get('eprint', '')
        url = entry.get('url', '')
        link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else url
        
        title_html = f'<a href="{link}" target="_blank" class="paper-title">{title}</a>' if link else title

        # Bibliographic Details
        vol = entry.get('volume', '')
        num = entry.get('number', '')
        pages = entry.get('pages', '').replace('--', '-')
        
        source = f"<em>{journal}</em>"
        if vol: source += f", {vol}"
        if num: source += f"({num})"
        if pages: source += f", pp. {pages}"

        # Category logic
        category = entry.get('keywords', 'general').lower()
        
        # Generate HTML Block
        item = f'<li class="paper-item" data-category="{category}" data-year="{year}" style="margin-bottom: 25px; list-style: none;">\n'
        item += f'  <div class="title-row"><strong>{title_html}</strong></div>\n'
        item += f'  <div class="author-row" style="color: #555;">{author} ({year})</div>\n'
        item += f'  <div class="source-row">{source}.</div>\n'
        
        # Add Abstract if it exists
        if abstract:
            item += f'  <details class="abstract-section">\n'
            item += f'    <summary>Abstract</summary>\n'
            item += f'    <div class="abstract-text">{abstract}</div>\n'
            item += f'  </details>\n'
            
        item += '</li>\n'
        html_output += item

    # 2. Inject into test.html
    with open('test.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<ul id="publications-list">'
    end_tag = '</ul>'
    
    if start_tag in content and end_tag in content:
        parts = content.split(start_tag)
        pre_list = parts[0]
        post_list = parts[1].split(end_tag)[1]
        
        new_content = pre_list + start_tag + "\n" + html_output + end_tag + post_list
        
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Success: Processed {len(entries)} papers.")
    else:
        print("Error: Could not find <ul id='publications-list'> in test.html")

if __name__ == "__main__":
    generate_html()