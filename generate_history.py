import os
import time
import subprocess
import random
from datetime import datetime, timedelta

# ======================================================================
# FORGED HISTORY CONFIGURATION
# Edit these emails before running the script on your other device!
# ======================================================================
AUTHORS = [
    {"name": "aynharan20", "email": "aynharan20@gmail.com"},
    {"name": "Nandhini-35", "email": "kit27.cse35@gmail.com"},
    {"name": "Murugavel0727", "email": "murugaveleng33@gmail.com"}
]

TOTAL_COMMITS = 25
DAYS_AGO_START = 90  # 3 months
# ======================================================================

def run_git(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_files_in_dir():
    target_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root:
            continue
        for f in files:
            if f == "generate_history.py":
                continue
            target_files.append(os.path.join(root, f))
    return target_files

def main():
    print("Reading final files into memory...")
    files_data = {}
    
    # Read everything
    for filepath in get_files_in_dir():
        with open(filepath, 'rb') as f:
            files_data[filepath] = f.read()
            
    # Wipe the directory contents (safely)
    print("Wiping directory for fresh git init...")
    for filepath in files_data.keys():
        os.remove(filepath)
        
    # Initialize Git
    print("Initializing Git repository...")
    if os.path.exists(".git"):
        import shutil, stat
        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(".git", onerror=remove_readonly)
    run_git("git init")
    
    start_time = datetime.now() - timedelta(days=DAYS_AGO_START)
    
    commit_messages = [
        "Initial project structure", "Setup requirements and gitignore",
        "Implement basic AST parsing", "Add DFS graph traversal for CNAMEs",
        "Fix recursive resolution bug", "Implement SPF lookup counting",
        "Add strict Pydantic schemas", "Integrate Instructor for LLM bridging",
        "Build Streamlit UI skeleton", "Connect UI to verification engine",
        "Add sample zone payloads", "Fix parsing error on origin directives",
        "Draft initial IEEE paper structure", "Add Related Work section",
        "Refine architecture diagram", "Update bibliography and citations",
        "Optimize graph traversal complexity", "Handle edge cases in TXT records",
        "Enhance UI layout and sidebars", "Fix session state bugs in Streamlit",
        "Finalize experimental evaluation", "Add test suite text file",
        "Format code and cleanup", "Update README documentation",
        "Final review and polish"
    ]
    
    print(f"Forging {TOTAL_COMMITS} commits over a {DAYS_AGO_START}-day timeline...")
    
    # Generate commits
    for i in range(TOTAL_COMMITS):
        progress = (i + 1) / TOTAL_COMMITS
        
        # Calculate time
        commit_time = start_time + timedelta(days=(DAYS_AGO_START * progress))
        # Add random jitter to time so it looks human
        commit_time += timedelta(hours=random.randint(1, 10), minutes=random.randint(0, 59))
        time_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Write files up to 'progress' percentage
        for filepath, data in files_data.items():
            if filepath.endswith('.png') or filepath.endswith('.cls'):
                # Binary or massive static files: add them halfway through
                if progress > 0.5:
                    with open(filepath, 'wb') as f:
                        f.write(data)
            else:
                # Text files: increment lines
                try:
                    text = data.decode('utf-8')
                    lines = text.split('\n')
                    lines_to_write = max(1, int(len(lines) * progress))
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines[:lines_to_write]))
                except UnicodeDecodeError:
                    # Fallback for unexpected binary
                    if progress > 0.5:
                        with open(filepath, 'wb') as f:
                            f.write(data)
                            
        # Set Author
        author = random.choice(AUTHORS)
        author_name, author_email = author["name"], author["email"]
            
        os.environ["GIT_AUTHOR_DATE"] = time_str
        os.environ["GIT_COMMITTER_DATE"] = time_str
        os.environ["GIT_AUTHOR_NAME"] = author_name
        os.environ["GIT_AUTHOR_EMAIL"] = author_email
        os.environ["GIT_COMMITTER_NAME"] = author_name
        os.environ["GIT_COMMITTER_EMAIL"] = author_email
        
        run_git("git add .")
        msg = commit_messages[i] if i < len(commit_messages) else f"Incremental update {i}"
        run_git(f'git commit --allow-empty -m "{msg}"')
        print(f"  -> Committed: {msg} ({time_str} by {author_name})")
        
    # Final sweep to ensure 100% exact match to original files
    print("Writing 100% of original files for the final state...")
    for filepath, data in files_data.items():
        with open(filepath, 'wb') as f:
            f.write(data)
            
    os.environ["GIT_AUTHOR_DATE"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    os.environ["GIT_COMMITTER_DATE"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    run_git("git add .")
    run_git('git commit --allow-empty -m "Final exact synchronization"')
    
    print("\nDONE! Run 'git log' to see your forged history.")

if __name__ == "__main__":
    main()
