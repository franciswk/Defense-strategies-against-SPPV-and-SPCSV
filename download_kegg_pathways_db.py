"""
Parses a saved KEGG PATHWAY HTML page to extract category, sub-category,
pathway ID, and pathway name, saving the results to kegg_pathways.csv.

Note: kegg_pathways_db.csv used in kegg_paths_plot.py is prepared in Excel
from kegg_pathways.csv.

Input: KEGG PATHWAY Database.html
Output: kegg_pathways.csv
Dependencies: bs4, pandas

Data: Available on request.
Citation: https://doi.org/10.1002/csc2.21392
"""


from bs4 import BeautifulSoup
import pandas as pd

# Load the HTML file
with open('C:/Users/hp/Documents/Python_R_data_analysis_0724/KEGG PATHWAY Database.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract category, sub-category, pathway name, and ID
data = []

# Function to extract pathway information from <dl> tags
def extract_pathways(dl_elements, category_name, subcategory_name):
    for dl in dl_elements:
        for dt in dl.find_all('dt'):
            id_code = dt.text.strip()
            # Ensure ID is preserved exactly as it is
            if id_code and len(id_code) >= 5:
                # Find the <a> tag within the <dd> tag
                dd_tag = dt.find_next_sibling('dd')
                if dd_tag:
                    a_tag = dd_tag.find('a')
                    if a_tag:
                        pathway_name = a_tag.text.strip()  # Extract pathway name from the <a> tag
                        data.append({
                            'Category': category_name,
                            'Sub-category': subcategory_name,
                            'Pathway ID': f'>{id_code} <',  # Format ID with '>' and '<'
                            'Pathway Name': pathway_name
                        })
                        print(f'Extracted: Category={category_name}, Sub-category={subcategory_name}, Pathway Name={pathway_name}, ID={id_code}')  # Debugging output

# Process <h4> tags for main categories
categories = soup.find_all('h4')

for category in categories:
    # Extract category name
    category_number = category.text.strip().split(' ', 1)[0]
    category_name = category.text.strip().split(' ', 1)[-1].strip()

    # Process subcategories within this category
    subcategories = category.find_next_sibling('div', class_='list')
    if subcategories:
        for b_tag in subcategories.find_all('b'):
            # Extract subcategory name
            subcategory_number = b_tag.text.strip().split(' ', 1)[0]
            subcategory_name = b_tag.text.strip().split(' ', 1)[-1].strip()
            subcategory_dl = b_tag.find_next_sibling('div', class_='list')
            if subcategory_dl:
                extract_pathways(subcategory_dl.find_all('dl'), category_name, subcategory_name)

# Additional processing for sections with <b> tags followed by <dl> elements
additional_sections = soup.find_all('b')

for b_tag in additional_sections:
    # Extract subcategory name
    subcategory_number = b_tag.text.strip().split(' ', 1)[0]
    subcategory_name = b_tag.text.strip().split(' ', 1)[-1].strip()
    subcategory_dl = b_tag.find_next_sibling('div', class_='list')
    if subcategory_dl:
        # Use 'N/A' for category when processing these sections
        extract_pathways(subcategory_dl.find_all('dl'), 'N/A', subcategory_name)

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV file
df.to_csv('kegg_pathways.csv', index=False)

print("Data saved to 'kegg_pathways.csv'")
