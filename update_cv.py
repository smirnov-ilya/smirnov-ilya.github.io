import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

def clean_latex(text):
    if not text:
        return ""
    return LatexNodes2Text().latex_to_text(text)

def format_bibtex_authors(author_string, use_oxford_comma=True):
    # 1. Split and reformat individual names
    authors = author_string.split(' and ')
    formatted_list = []

    for author in authors:
        author = author.strip()
        if ',' in author:
            parts = author.split(',')
            formatted_list.append(f"{parts[1].strip()} {parts[0].strip()}")
        else:
            formatted_list.append(author)

    # 2. Join names based on the count
    n = len(formatted_list)
    
    if n == 0:
        return ""
    if n == 1:
        return formatted_list[0]
    if n == 2:
        return f"{formatted_list[0]} and {formatted_list[1]}"
    
    # For 3 or more authors
    if use_oxford_comma:
        # Result: "Name1, Name2, and Name3"
        return ", ".join(formatted_list[:-1]) + f", and {formatted_list[-1]}"
    else:
        # Result: "Name1, Name2 and Name3"
        return ", ".join(formatted_list[:-1]) + f" and {formatted_list[-1]}"


def generate_html():
    # 1. Load the BibTeX file
    try:
        with open('papers.bib', encoding='utf-8') as bibfile:
            db = bibtexparser.load(bibfile)
    except FileNotFoundError:
        print("Error: papers.bib not found.")
        return
    try:
        with open('preprints.bib', encoding='utf-8') as bibfile:
            prepdb = bibtexparser.load(bibfile)
    except FileNotFoundError:
        print("Error: preprints.bib not found.")
        return

    # Sort entries by year (newest first)
    papers = sorted(db.entries, key=lambda x: x.get('year', '0'), reverse=True)
    preprints = sorted(prepdb.entries, key=lambda x: x.get('year', '0'), reverse=True)

    html_output = ""
    second_html_output = ""
    for entry in papers:
        # Basic metadata
        title = clean_latex(entry.get('title', 'No Title'))
        author = format_bibtex_authors(clean_latex(entry.get('author', 'Unknown Author')))
        year = clean_latex(entry.get('year', 'N/A'))
        journal = clean_latex(entry.get('journal', entry.get('booktitle', '')))
        
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
        series = entry.get('series', '')
        
        source = f"<em>{journal}</em>"
        if vol:
            if series: source += f", volume {vol} of {series}"
            else: source += f", {vol}"
        if num: source += f"({num})"
        if pages: source += f", pp. {pages}"
        if pages: source += f", {year}"

        # Category for filtering
        category = entry.get('keywords', 'general').lower()
        
        # Construct the HTML list item
        item = f'<li class="paper-item" data-category="{category}" data-year="{year}">\n'
        item += f'  <div class="title-row"><strong>{title_html}</strong></div>\n'
        item += f'  <b>{author}</b>. {source}.\n'
                    
        item += '</li>\n'
        html_output += item
    
    for entry in preprints:
        # Basic metadata
        title = clean_latex(entry.get('title', 'No Title'))
        author = format_bibtex_authors(clean_latex(entry.get('author', 'Unknown Author')))
        
        
        # Link Logic
        arxiv_id = entry.get('eprint', '')
        url = entry.get('url', '')
        link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else url
        
        if link:
            title_html = f'<a href="{link}" target="_blank" class="paper-title">{title}</a>'
        else:
            title_html = title

        # Category for filtering
        category = entry.get('keywords', 'general').lower()
        
        # Construct the HTML list item
        item = f'<li class="paper-item" data-category="{category}" data-year="{year}">\n'
        item += f'  <div class="title-row"><strong>{title_html}</strong></div>\n'
        item += f'  <b>{author}</b>.\n'
                    
        item += '</li>\n'
        second_html_output += item

    # 2. Inject into cv.html
    with open('cv.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<!-- Paste publications here -->'
    end_tag = '<!-- End of publications here -->'
    
    if start_tag in content and end_tag in content:
        parts_before = content.split(start_tag)
        # Fix: correctly isolate the part after the start
        parts_after = parts_before[1].split(end_tag, 1) 
        
        changed_content = parts_before[0] + start_tag + "\n" + html_output + end_tag + parts_after[1]
        
        with open('cv.html', 'w', encoding='utf-8') as f:
            f.write(changed_content)
        print(f"Successfully processed {len(papers)} papers.")
    else:
        print("Error: Could not find <!-- Paste publications here --> in cv.html")

    start_tag = '<!-- Start of preprints -->'
    end_tag = '<!-- End of preprints -->'
    
    if start_tag in content and end_tag in content:
        parts_before = changed_content.split(start_tag)
        # Fix: correctly isolate the part after the first occurrence of </ul>
        parts_after = parts_before[1].split(end_tag, 1) 
        
        final_content = parts_before[0] + start_tag + "\n" + second_html_output + end_tag + parts_after[1]
        
        with open('cv.html', 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Successfully processed {len(preprints)} preprints.")
    else:
        print("Error: Could not find <!-- Paste publications here --> in cv.html")


if __name__ == "__main__":
    generate_html()
