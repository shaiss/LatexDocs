# HTML to LaTeX to PDF Converter

This Python script automates the process of converting HTML files (contained within zip archives) to LaTeX and then to PDF. It's designed to handle multiple zip files, creating separate output folders for each conversion.

## Features

- Extracts HTML from zip files
- Converts HTML to Markdown
- Converts Markdown to LaTeX
- Generates PDF from LaTeX
- Handles multiple zip files in batch
- Creates organized output structure
- Moves intermediate files to a debug folder

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- pip (Python package installer)

You will also need the following external tools:

- [Pandoc](https://pandoc.org/installing.html)
- A LaTeX distribution (e.g., [MiKTeX](https://miktex.org/download) for Windows or [TeX Live](https://www.tug.org/texlive/) for Linux/macOS)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/html-to-latex-pdf-converter.git
   cd html-to-latex-pdf-converter
   ```

2. Install the required Python packages:
   ```
   pip install beautifulsoup4 html2text
   ```

3. Ensure Pandoc and LaTeX are installed and accessible from the command line.

## Usage

1. Place your zip files containing HTML documents in the `input` folder.

2. Run the script:
   ```
   python html_to_latex_converter.py
   ```

3. Check the `output` folder for the results. Each zip file will have its own subfolder containing:
   - A LaTeX file (.tex)
   - A PDF file (.pdf)
   - A debug folder with intermediate files (.html, .md)

## Configuration

You may need to adjust the path to `pdflatex` in the `latex_to_pdf` function if it's not in your system's PATH.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pandoc](https://pandoc.org/) for Markdown to LaTeX conversion
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [html2text](https://github.com/Alir3z4/html2text/) for HTML to Markdown conversion