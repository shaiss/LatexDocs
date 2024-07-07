import zipfile
import os
import tempfile
from bs4 import BeautifulSoup
import html2text
import subprocess
import shutil

def extract_html_from_zip(zip_path, output_dir, base_name):
    print(f"Extracting HTML from {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        html_files = [f for f in zip_ref.namelist() if f.endswith('.html')]
        if not html_files:
            raise ValueError("No HTML file found in the zip archive")
        
        print(f"Found HTML file: {html_files[0]}")
        with zip_ref.open(html_files[0]) as html_file:
            content = html_file.read().decode('utf-8', errors='replace')
            print(f"HTML content length: {len(content)} characters")
            
            # Save HTML content to a file
            html_output_path = os.path.join(output_dir, f'{base_name}.html')
            with open(html_output_path, 'w', encoding='utf-8') as html_output_file:
                html_output_file.write(content)
            print(f"Saved extracted HTML to: {html_output_path}")
            
            return content

def html_to_markdown(html_content, output_dir, base_name):
    print("Converting HTML to Markdown")
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_tables = False
    h.body_width = 0  # Don't wrap lines
    markdown_content = h.handle(html_content)
    print(f"Markdown content length: {len(markdown_content)} characters")
    
    # Save Markdown content to a file
    md_output_path = os.path.join(output_dir, f'{base_name}.md')
    with open(md_output_path, 'w', encoding='utf-8') as md_output_file:
        md_output_file.write(markdown_content)
    print(f"Saved Markdown to: {md_output_path}")
    
    return markdown_content

def markdown_to_latex(markdown_content, output_dir, base_name):
    print("Converting Markdown to LaTeX")
    md_file_path = os.path.join(output_dir, f'{base_name}_input.md')
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)
    
    print(f"Temporary Markdown file: {md_file_path}")
    tex_file_path = os.path.join(output_dir, f'{base_name}.tex')
    
    try:
        print(f"Running pandoc: {md_file_path} -> {tex_file_path}")
        result = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'latex', '--standalone', '-o', tex_file_path, md_file_path], 
                                check=True, capture_output=True, text=True)
        print(f"Pandoc stdout: {result.stdout}")
        print(f"Pandoc stderr: {result.stderr}")
        
        with open(tex_file_path, 'r', encoding='utf-8') as tex_file:
            latex_content = tex_file.read()
        print(f"LaTeX content length: {len(latex_content)} characters")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")
        print(f"Pandoc stdout: {e.stdout}")
        print(f"Pandoc stderr: {e.stderr}")
        raise
    
    return latex_content

def latex_to_pdf(latex_content, output_dir, base_name):
    print("Converting LaTeX to PDF")
    tex_file_path = os.path.join(output_dir, f'{base_name}.tex')
    
    with open(tex_file_path, 'w', encoding='utf-8') as tex_file:
        tex_file.write(latex_content)
    
    # Specify the full path to pdflatex here
    pdflatex_path = r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"  # Adjust this path as needed
    
    try:
        print(f"Running pdflatex on {tex_file_path}")
        result = subprocess.run([pdflatex_path, '-interaction=nonstopmode', '-output-directory', output_dir, tex_file_path],
                                check=True, capture_output=True, text=True)
        print(f"pdflatex stdout: {result.stdout}")
        print(f"pdflatex stderr: {result.stderr}")
        
        pdf_path = os.path.join(output_dir, f'{base_name}.pdf')
        if os.path.exists(pdf_path):
            print(f"PDF generated successfully: {pdf_path}")
            return pdf_path
        else:
            raise FileNotFoundError(f"PDF file not found at expected location: {pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running pdflatex: {e}")
        print(f"pdflatex stdout: {e.stdout}")
        print(f"pdflatex stderr: {e.stderr}")
        raise

def process_zip_file(zip_path, output_dir):
    base_name = os.path.splitext(os.path.basename(zip_path))[0]
    try:
        html_content = extract_html_from_zip(zip_path, output_dir, base_name)
        markdown_content = html_to_markdown(html_content, output_dir, base_name)
        latex_content = markdown_to_latex(markdown_content, output_dir, base_name)
        pdf_path = latex_to_pdf(latex_content, output_dir, base_name)
        print("Conversion completed successfully")
        print(f"LaTeX file: {os.path.join(output_dir, f'{base_name}.tex')}")
        print(f"PDF file: {pdf_path}")
    except Exception as e:
        print(f"An error occurred while processing {zip_path}: {e}")
        import traceback
        traceback.print_exc()

def move_debug_files(output_dir, base_name):
    debug_dir = os.path.join(output_dir, 'debug')
    os.makedirs(debug_dir, exist_ok=True)
    
    debug_files = [f'{base_name}.html', f'{base_name}.md', f'{base_name}_input.md']
    for file in debug_files:
        src = os.path.join(output_dir, file)
        dst = os.path.join(debug_dir, file)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved {file} to debug folder")

# Main execution
input_folder = 'input'
output_base = 'output'

# Create input folder if it doesn't exist
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
    print(f"Created input folder: {input_folder}")
    print("Please place your zip files in this folder and run the script again.")
else:
    # Process each zip file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.zip'):
            zip_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(output_base, base_name)
            os.makedirs(output_dir, exist_ok=True)
            
            print(f"Processing {filename}")
            process_zip_file(zip_path, output_dir)
            move_debug_files(output_dir, base_name)
            print(f"Finished processing {filename}")
            print("-" * 50)

    print("All zip files processed.")