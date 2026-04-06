name: Update Publications
import bibtexparser

def generate_html():
    with open('papers.bib') as bibtex_file:
        db = bibtexparser.load(bibtex_file)
    
    html_output = ""
    for entry in db.entries:
        # Create a list item with categories for filtering
        cat = entry.get('keywords', 'general').lower()
        year = entry.get('year', 'Unknown')
        
        html_output += f'<li class="paper" data-category="{cat}" data-year="{year}">\n'
        html_output += f'  <strong>{entry.get("title")}</strong><br>\n'
        html_output += f'  {entry.get("author")} ({year})<br>\n'
        html_output += f'  <em>{entry.get("journal", entry.get("booktitle", ""))}</em>\n'
        html_output += '</li>\n'
    
    # Inject into index.html
    with open('test.html', 'r') as f:
        content = f.read()
    
    start_tag = ""
    end_tag = ""
    
    new_content = content.split(start_tag)[0] + start_tag + "\n" + html_output + end_tag + content.split(end_tag)[1]
    
    with open('test.html', 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    generate_html()

