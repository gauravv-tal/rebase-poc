import os
import openai
from pathlib import Path

# Set your OpenAI API key
openai.api_key = "sk-**"

def get_java_files(directory):
    """Recursively finds all files in the given directory."""
    return [file for file in Path(directory).rglob("*.*")]

def read_file(file_path):
    """Reads the content of a file."""
    print(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def resolve_conflicts(code):
    """Sends code to OpenAI and asks it to resolve conflicts."""
    prompt = f"""
    The following code contains conflicts. Please resolve them:
    {code}
    Provide only the fixed code without any explanations.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert who resolves code conflicts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

def write_file(output_dir, input_file_path, content):
    """Writes content back to the file."""
    #filename = os.path.basename(file_path)
    filename = Path(input_file_path).name
    output_file_path = os.path.join(output_dir, filename) 
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main(directory, output_dir):
    java_files = get_java_files(directory)
    
    conflict_count = {}
    
    for file in java_files:
        #print('file----------------->',file)
        original_content = read_file(file)
        print('original_content----------------->',original_content)
        resolved_content = resolve_conflicts(original_content)
        print('resolved_content----------------->',resolved_content)
        write_file(output_dir, file, resolved_content)
        
        # Counting changes
        conflicts_resolved = original_content.count("<<<<<<<")  # Common conflict markers
        conflict_count[file.name] = conflicts_resolved
    
    # Display the summary
    print("Conflicts Resolved:")
    for filename, count in conflict_count.items():
        print(f"{filename}: {count} conflicts resolved")

if __name__ == "__main__":
    #input_directory = "C:/code/hadoop-3.1.1/hadoop/"
    input_directory = "C:/POC/Self_POC/conflictsTest/conflicting-files"
    output_dir = "C:/POC/Self_POC/conflictsTest/resolved-conflicting-files"
    main(input_directory, output_dir)
