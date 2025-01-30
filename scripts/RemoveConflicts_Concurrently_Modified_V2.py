import os
import openai
from pathlib import Path
import concurrent.futures

# Set your OpenAI API key
openai.api_key = "sk-**"

def get_java_files(directory):
    """Recursively finds all files in the given directory that contain conflicts."""
    conflicted_files = []
    for file in Path(directory).rglob("*.*"):
        content = read_file(file)
        if is_conflicted(content):
            conflicted_files.append(file)
    return conflicted_files

def read_file(file_path):
    """Reads the content of a file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def is_conflicted(java_code):
    """Checks if the file contains conflict markers."""
    return "<<<<<<<" in java_code or "=======" in java_code or ">>>>>>>" in java_code

def resolve_conflicts(code):
    """Sends code to OpenAI and asks it to resolve conflicts."""
    prompt = f"""
    The following code contains conflicts. Please resolve them:
    {code}
    Provide only the fixed code without any explanations.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an expert who resolves code conflicts."},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def write_file(file_path, content):
    """Writes content back to the file.""" 
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def process_file(file):
    """Processes a single file: reads, resolves conflicts, and writes back."""
    original_content = read_file(file)
    
    if is_conflicted(original_content):
        resolved_content = resolve_conflicts(original_content)
        write_file(file, resolved_content)
        
        # Counting changes
        conflicts_resolved = original_content.count("<<<<<<<")  # Common conflict markers
        return file.name, conflicts_resolved
    return file.name, 0

def process_batch(files):
    """Processes a batch of files concurrently."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(process_file, file): file for file in files}
        for future in concurrent.futures.as_completed(future_to_file):
            file_name, conflicts_resolved = future.result()
            results[file_name] = conflicts_resolved
    return results

def main(directory):
    java_files = get_java_files(directory)
    conflict_count = {}
    batch_size = 10
    
    for i in range(0, len(java_files), batch_size):
        batch = java_files[i:i + batch_size]
        batch_results = process_batch(batch)
        conflict_count.update(batch_results)
    
    # Display the summary
    print("Conflicts Resolved:")
    for filename, count in conflict_count.items():
        print(f"{filename}: {count} conflicts resolved")
if __name__ == "__main__":
    input_directory = "C:/POC/Self_POC/conflictsTest/conflicting-files"
    #output_dir = "C:/POC/Self_POC/conflictsTest/resolved-conflicting-files"
    main(input_directory)
