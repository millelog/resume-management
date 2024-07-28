#!/usr/bin/env python3
# scripts/generate_cover_letter.py

import os
import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import yaml
from datetime import datetime

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.models.cover_letter import CoverLetter

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_most_recent_yaml(directory):
    yaml_files = list(Path(directory).glob('*.yaml'))
    if not yaml_files:
        raise FileNotFoundError(f"No YAML files found in {directory}")
    return max(yaml_files, key=os.path.getmtime)

def main():
    parser = argparse.ArgumentParser(description="Generate a cover letter from YAML data.")
    parser.add_argument("input", nargs='?', help="Path to the input YAML file (optional)")
    parser.add_argument("-o", "--output", help="Path to the output HTML file")
    parser.add_argument("-t", "--template", default="templates/cover_letter_template.html", 
                        help="Path to the HTML template file")
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

    # Set default output path if not provided
    if args.output is None:
        input_path = Path(args.input)
        args.output = f"output/{input_path.stem}_cover_letter.html"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    try:
        # Load the cover letter data from YAML
        yaml_data = load_yaml(args.input)
        cover_letter = CoverLetter(**yaml_data)
        
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(os.path.dirname(args.template)))
        template = env.get_template(os.path.basename(args.template))
        
        # Render the HTML
        html_content = template.render(content=cover_letter.content)
        
        # Write the HTML to file
        with open(args.output, 'w') as f:
            f.write(html_content)
        
        print(f"Cover letter generated successfully: {args.output}")
    except Exception as e:
        print(f"Error generating cover letter: {e}")

if __name__ == "__main__":
    main()