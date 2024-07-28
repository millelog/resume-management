# src/generators/resume_generator.py

import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
from src.models.resume import Resume
from src.utils.date_formatter import format_date
from src.utils.add_tracking import add_tracking_filter

class ResumeGenerator:
    def __init__(self, template_path: str):
        self.template_dir = os.path.dirname(template_path)
        self.template_file = os.path.basename(template_path)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.env.filters['format_date'] = format_date
        self.env.filters['add_tracking'] = add_tracking_filter
        self.template = self.env.get_template(self.template_file)

    def generate_html(self, resume: Resume) -> str:
        """
        Generate HTML from the resume data and template.

        Args:
        resume (Resume): A Resume object containing the resume data

        Returns:
        str: Generated HTML
        """
        resume_dict = resume.dict()
        return self.template.render(resume_dict)

    def generate_and_open(self, resume: Resume, output_path: str):
        """
        Generate an HTML file from the resume data and open it in the default browser.

        Args:
        resume (Resume): A Resume object containing the resume data
        output_path (str): Path where the HTML file should be saved

        Raises:
        Exception: If HTML generation or file opening fails
        """
        html_content = self.generate_html(resume)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML file generated successfully: {output_path}")
            
            # Open the HTML file in the default browser
            webbrowser.open('file://' + os.path.realpath(output_path))
        except Exception as e:
            print(f"Error generating or opening HTML: {e}")
            raise

if __name__ == "__main__":
    # Example usage
    from src.utils.yaml_handler import load_resume
    
    try:
        resume = load_resume("data/resumes/logan_miller_resume.yaml")
        generator = ResumeGenerator("templates/resume_template.html")
        generator.generate_and_open(resume, "output/logan_miller_resume.html")
    except Exception as e:
        print(f"Error: {e}")