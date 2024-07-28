#!/usr/bin/env python3
# scripts/generate_cover_letter.py

import os
import sys
import argparse
import webbrowser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import yaml
from datetime import datetime

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.models.cover_letter import CoverLetter, JobSpecificInfo
from src.models.resume import PersonalInfo

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().splitlines()
            return yaml.safe_load('\n'.join(content))
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            print(f"Error position: line {mark.line + 1}, column {mark.column + 1}")
            print(f"Problematic line: {content[mark.line]}")
        return None

def get_most_recent_yaml(directory):
    yaml_files = list(Path(directory).glob('*.yaml'))
    if not yaml_files:
        raise FileNotFoundError(f"No YAML files found in {directory}")
    return max(yaml_files, key=os.path.getmtime)

def main():
    parser = argparse.ArgumentParser(description="Generate a cover letter from YAML data and open in browser.")
    parser.add_argument("input", nargs='?', help="Path to the input YAML file (optional)")
    parser.add_argument("-o", "--output", help="Path to the output HTML file")
    parser.add_argument("-t", "--template", default="templates/cover_letter_template.html", 
                        help="Path to the HTML template file")
    parser.add_argument("-m", "--main", default="data/resumes/main.yaml",
                        help="Path to the main resume YAML file")
    args = parser.parse_args()

    # If no input file is specified, use the most recent YAML file
    if args.input is None:
        letters_dir = os.path.join(project_root, 'data', 'cover_letters')
        args.input = get_most_recent_yaml(letters_dir)
        print(f"Using most recent cover letter: {args.input}")

    # Ensure the input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    # Ensure the main resume file exists
    if not os.path.isfile(args.main):
        print(f"Error: main resume file '{args.main}' does not exist.")
        return

    # Set default output path if not provided
    if args.output is None:
        input_path = Path(args.input)
        args.output = f"output/{input_path.stem}_cover_letter.html"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    try:
        # Load the cover letter data from YAML
        cover_letter_data = load_yaml(args.input)
        cover_letter = CoverLetter(**cover_letter_data)
        
        # Load the personal info from the main resume YAML
        main_data = load_yaml(args.main)
        if main_data and 'personal_info' in main_data:
            personal_info = PersonalInfo(**main_data['personal_info'])
        else:
            print(f"Error: Could not find 'personal_info' in {args.main}")
            return
        
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(os.path.dirname(args.template)))
        template = env.get_template(os.path.basename(args.template))
        
        # Render the HTML
        html_content = template.render(
            content=cover_letter.content,
            personal_info=personal_info,
            job_specific_info=cover_letter.job_specific_info
        )
        
        # Write the HTML to file
        with open(args.output, 'w') as f:
            f.write(html_content)
        
        print(f"Cover letter generated successfully: {args.output}")
        
        # Open the generated HTML file in the default browser
        webbrowser.open('file://' + os.path.realpath(args.output))
        print("Cover letter opened in your default web browser.")
    except Exception as e:
        print(f"Error generating cover letter: {e}")

if __name__ == "__main__":
    main()