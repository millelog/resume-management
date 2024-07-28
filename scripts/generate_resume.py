#!/usr/bin/env python3
# scripts/generate_resume.py

import os
import sys
import argparse
from pathlib import Path

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.utils.yaml_handler import load_resume
from src.generators.resume_generator import ResumeGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate an HTML resume from YAML data and open in browser.")
    parser.add_argument("input", help="Path to the input YAML file")
    parser.add_argument("-o", "--output", help="Path to the output HTML file")
    parser.add_argument("-t", "--template", default="templates/resume_template.html", 
                        help="Path to the HTML template file")
    args = parser.parse_args()

    # Ensure the input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    # Set default output path if not provided
    if args.output is None:
        input_path = Path(args.input)
        args.output = f"output/{input_path.stem}_resume.html"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    try:
        # Load the resume data from YAML
        resume = load_resume(args.input)
        
        # Initialize the Resume generator with the specified template
        generator = ResumeGenerator(args.template)
        
        # Generate the HTML and open in browser
        generator.generate_and_open(resume, args.output)
        
        print(f"HTML resume generated and opened in browser. File saved as: {args.output}")
        print("You can use your browser's print function to save as PDF if desired.")
    except Exception as e:
        print(f"Error generating HTML resume: {e}")

if __name__ == "__main__":
    main()