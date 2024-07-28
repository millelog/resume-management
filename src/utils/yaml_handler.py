# src/utils/yaml_handler.py

import yaml
from pathlib import Path
from typing import Dict, Any

from src.models.resume import Resume

def read_yaml(file_path: str) -> Dict[str, Any]:
    """
    Read a YAML file and return its contents as a dictionary.

    Args:
    file_path (str): Path to the YAML file

    Returns:
    Dict[str, Any]: Contents of the YAML file as a dictionary
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist")

    with path.open('r') as file:
        try:
            data = yaml.safe_load(file)
            print("YAML data loaded successfully:")
            return data
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

def load_resume(file_path: str) -> Resume:
    """
    Load resume data from a YAML file and return a Resume object.

    Args:
    file_path (str): Path to the YAML file containing resume data

    Returns:
    Resume: A Resume object populated with data from the YAML file
    """
    yaml_data = read_yaml(file_path)
    try:
        resume = Resume(**yaml_data)
        print("Resume object created successfully")
        return resume
    except ValueError as e:
        print(f"Error creating Resume object: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        resume = load_resume("data/resumes/logan_miller_resume.yaml")
        print(f"Successfully loaded resume for {resume.personal_info.name}")
        print(f"Summary: {resume.summary[:50]}...")  # Print first 50 characters of summary
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")