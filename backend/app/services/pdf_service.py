import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Set up Jinja2 to look in the templates folder
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def generate_pdf_from_data(data: dict, output_filename: str = "tailored_resume.pdf") -> str:
    """
    Renders an HTML template with data and converts it to a PDF.
    Returns the file path of the generated PDF.
    """
    template = env.get_template('resume_template.html')
    
    # Render the HTML with the dictionary data
    rendered_html = template.render(
        name=data.get("name", "Name"),
        email=data.get("email", "Email"),
        phone=data.get("phone", ""),
        portfolio_url=data.get("portfolio_url", ""),
        summary=data.get("summary", ""),
        skills=data.get("skills", ""),
        experience_html=data.get("experience_html", "")
    )
    
    # Ensure a directory exists to save the generated PDFs
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Generate the PDF
    HTML(string=rendered_html).write_pdf(output_path)
    
    return output_path