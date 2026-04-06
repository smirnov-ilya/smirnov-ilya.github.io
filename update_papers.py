import bibtexparser

def generate_html():
    # 1. Load the BibTeX file
    with open('papers.bib') as bibfile:
        db = bibtexparser.load(bibfile)
    
    # 2. Build the HTML string
    html_output = ""
    for entry in db.entries:
        title = entry.get('title', 'No Title')
        author = entry.get('author', 'Unknown Author')
        year = entry.get('year', 'N/A')
        journal = entry.get('journal', entry.get('booktitle', ''))
        # Get category from keywords, default to 'general'
        category = entry.get('keywords', 'general').lower()
        
        # Build the HTML for one paper
        item = '<li class="paper" data-category="' + category + '" data-year="' + year + '">\n'
        item += '  <strong>' + title + '</strong><br>\n'
        item += '  ' + author + ' (' + year + ')<br>\n'
        item += '  <em>' + journal + '</em>\n'
        item += '</li>\n'
        html_output += item

    # 3. Read your index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 4. Find the tags and swap the middle
    start_tag = ""
    end_tag = ""
    
    if start_tag in content and end_tag in content:
        parts_before = content.split(start_tag)
        parts_after = parts_before[1].split(end_tag)
        
        final_content = parts_before[0] + start_tag + "\n" + html_output + end_tag + parts_after[1]
        
        # 5. Save the updated file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_content)
        print("Success: Papers injected into index.html")
    else:
        print("Error: Could not find the START or END comments in index.html")

if __name__ == "__main__":
    generate_html()