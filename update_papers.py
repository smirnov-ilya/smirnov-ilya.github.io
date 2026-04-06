import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

def clean_latex(text):
    if not text:
        return ""
    # Converts LaTeX accents/braces to UTF-8 (e.g., {St\"{u}ckard} -> Stückard)
    return LatexNodes2Text().latex_to_text(text)

def generate_html():
    # 1. Load the BibTeX file
    with open('papers.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)
    
    # 2. Build the HTML string
    html_output = ""
    for entry in db.entries:
        # Basic Fields
        title = clean_latex(entry.get('title', 'No Title'))
        author = clean_latex(entry.get('author', 'Unknown Author'))
        year = clean_latex(entry.get('year', 'N/A'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', '')))
        
        # Link Logic (Checks eprint/arxiv first, then general URL)
        arxiv_id = entry.get('eprint', '')
        general_url = entry.get('url', '')
        link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else general_url
        
        if link:
            title_html = f'<a href="{link}" target="_blank" class="paper-title">{title}</a>'
        else:
            title_html = title

        # Bibliographic Details (Vol, No, Pages)
        vol = entry.get('volume', '')
        num = entry.get('number', '')
        pages = entry.get('pages', '').replace('--', '-')
        
        source = f"<em>{journal}</em>"
        if vol: source += f", {vol}"
        if num: source += f"({num})"
        if pages: source += f", pp. {pages}"

        # Category for filtering (from keywords)
        category = entry.get('keywords', 'general').lower()
        
        # Build the HTML Item
        item = f'<li class="paper-item" data-category="{category}" data-year="{year}">\n'
        item += f'  <span class="title-row">{title_html}</span><br>\n'
        item += f'  <span class="author-row">{author} ({year})</span><br>\n'
        item += f'  <span class="source-row">{source}.</span>\n'
        item += '</li>\n'
        html_output += item

    # 3. Inject into index.html
    with open('test.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<ul id="publications-list">'
    end_tag = '</ul>'
    
    if start_tag in content and end_tag in content:
        parts_before = content.split(start_tag)
        parts_after = parts_before[1].split(end_tag)
        final_content = parts_before[0] + start_tag + "\n" + html_output + end_tag + parts_after[1]
        
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Success: Processed {len(db.entries)} papers.")
    else:
        print("Error: Could not find the <ul> tags in test.html")

if __name__ == "__main__":
    generate_html()
