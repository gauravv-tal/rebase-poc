import os
import subprocess
import sys
from datetime import datetime

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip()

def get_merge_base(branch1, branch2):
    """Get the merge base of two branches."""
    command = f"git merge-base {branch1} {branch2}"
    merge_base, error = run_command(command)
    if error:
        print(f"Error finding merge base: {error}")
        return None
    return merge_base

def get_git_log(branch, merge_base):
    """Get the git log for a branch against the merge base."""
    command = f"git log  --pretty=format:'%h %ad %s' --date=unix  {merge_base}..{branch}"
    log_output, error = run_command(command)
    if error:
        print(f"Error getting log for {branch}: {error}")
        return []
    
    # Parse the log output
    logs = []
    for line in log_output.splitlines():
        parts = line.split(' ', 2)
        if len(parts) >= 3:
            commit_hash = parts[0]
            commit_date = parts[1]   # Combine date and time
            commit_message = parts[2]
            logs.append((commit_hash, commit_date, commit_message))
    
    return logs

def main():
    # Input directory and branches
    directory_path = sys.argv[1]
    branch1 = sys.argv[2]
    branch2 = sys.argv[3]

    #python getGitlogs.py <directory> <downstream_branch1> <upstream_branch2>

    # Change working directory to the specified path
    os.chdir(directory_path)

    # Get the merge base
    merge_base = get_merge_base(branch1, branch2)
    
    if not merge_base:
        return

    # Get logs for both branches
    logs_branch1 = get_git_log(branch1, merge_base)
    logs_branch2 = get_git_log(branch2, merge_base)

    # Combine and sort logs by date
    all_logs = logs_branch1 + logs_branch2
    all_logs_sorted = sorted(all_logs, key=lambda x: x[1])  # Sort by Unix timestamp

    # Print sorted logs
    print("\nOrdered Git Logs:")
    for log in all_logs_sorted:
        print(f"{log[1]} - {log[0]} - {log[2]}")
        command = f"git cherry-pick {log[0]}"
        merge_base, error = run_command(command)
        if error:
            print(f"Error git cherry-pick {log[0]}")
        return None
        

if __name__ == "__main__":
    main()
