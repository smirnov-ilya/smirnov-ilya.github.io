import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

def clean_latex(text):
    if not text:
        return ""
    return LatexNodes2Text().latex_to_text(text)

def generate_html():
    # 1. Load the BibTeX file
    try:
        with open('papers.bib', encoding='utf-8') as bibfile:
            db = bibtexparser.load(bibfile)
    except FileNotFoundError:
        print("Error: papers.bib not found.")
        return

    # Sort entries by year (newest first)
    entries = sorted(db.entries, key=lambda x: x.get('year', '0'), reverse=True)

    html_output = ""
    for entry in entries:
        # Basic metadata
        title = clean_latex(entry.get('title', 'No Title'))
        author = clean_latex(entry.get('author', 'Unknown Author'))
        year = clean_latex(entry.get('year', 'N/A'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', '')))
        abstract = clean_latex(entry.get('abstract', ''))
        
        # Link Logic
        arxiv_id = entry.get('eprint', '')
        url = entry.get('url', '')
        link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else url
        
        if link:
            title_html = f'<a href="{link}" target="_blank" class="paper-title">{title}</a>'
        else:
            title_html = title

        # Bibliographic Details
        vol = entry.get('volume', '')
        num = entry.get('number', '')
        pages = entry.get('pages', '').replace('--', '-')
        
        source = f"<em>{journal}</em>"
        if vol: source += f", {vol}"
        if num: source += f"({num})"
        if pages: source += f", pp. {pages}"
        if pages: source += f", {year}"

        # Category for filtering
        category = entry.get('keywords', 'general').lower()
        
        # Construct the HTML list item
        item = f'<li class="paper-item" data-category="{category}" data-year="{year}">\n'
        item += f'  <div class="title-row"><strong>{title_html}</strong></div>\n'
        item += f'  <div class="author-row"><b>{author}</b></div>, '
        item += f'  <div class="source-row">{source}.</div>\n'
                    
        item += '</li>\n'
        html_output += item

    # 2. Inject into cv.html
    with open('cv.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<!-- Paste publications here -->'
    end_tag = '<!-- End of publications here -->'
    
    if start_tag in content and end_tag in content:
        parts_before = content.split(start_tag)
        # Fix: correctly isolate the part after the first occurrence of </ul>
        parts_after = parts_before[1].split(end_tag, 1) 
        
        final_content = parts_before[0] + start_tag + "\n" + html_output + end_tag + parts_after[1]
        
        with open('cv.html', 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Successfully processed {len(entries)} papers.")
    else:
        print("Error: Could not find <!-- Paste publications here --> in cv.html")

if __name__ == "__main__":
    generate_html()
