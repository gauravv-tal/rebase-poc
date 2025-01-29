import os
import openai
from pathlib import Path

# Set your OpenAI API key
openai.api_key = "token"

def get_java_files(directory):
    """Recursively finds all Java files in the given directory."""
    return [file for file in Path(directory).rglob("*.java")]

def read_file(file_path):
    """Reads the content of a file."""
    print(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def resolve_conflicts(java_code):
    """Sends Java code to OpenAI and asks it to resolve conflicts."""
    prompt = f"""
    The following Java code contains conflicts. Please resolve them:
    ```java
    {java_code}
    ```
    Provide only the fixed code without any explanations.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Java expert who resolves code conflicts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

def write_file(file_path, content):
    """Writes content back to the file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main(directory):
    java_files = get_java_files(directory)
    conflict_count = {}
    
    for file in java_files:
        original_content = read_file(file)
        resolved_content = resolve_conflicts(original_content)
        write_file(file, resolved_content)
        
        # Counting changes
        conflicts_resolved = original_content.count("<<<<<<<")  # Common conflict markers
        conflict_count[file.name] = conflicts_resolved
    
    # Display the summary
    print("Conflicts Resolved:")
    for filename, count in conflict_count.items():
        print(f"{filename}: {count} conflicts resolved")

if __name__ == "__main__":
    input_directory = "C:/code/hadoop-3.1.1/hadoop/"
    main(input_directory)
