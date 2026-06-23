import os
import hashlib

# Directories and files that MUST be ignored for the app to survive
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache'}
IGNORE_FILES = {'__init__.py', '.gitkeep', '.env.example', '.env'}

def get_file_hash(filepath):
    """Returns the MD5 hash of a file to check for exact duplicates."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception:
        return None

def clean_and_audit(root_dir="."):
    print("🧹 Starting Project Audit & Cleanup...\n")
    
    empty_files = []
    empty_dirs = []
    file_hashes = {}
    duplicates = []

    # Walk the directory tree bottom-up to handle nested empty folders
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Skip protected directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        # 1. Audit Files
        for filename in filenames:
            if filename in IGNORE_FILES:
                continue
                
            filepath = os.path.join(dirpath, filename)
            
            # Check for empty files
            if os.path.getsize(filepath) == 0:
                empty_files.append(filepath)
                continue
            
            # Check for duplicates
            file_hash = get_file_hash(filepath)
            if file_hash:
                if file_hash in file_hashes:
                    duplicates.append((filepath, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = filepath

        # 2. Audit Directories
        if not os.listdir(dirpath) and os.path.basename(dirpath) not in IGNORE_DIRS:
            empty_dirs.append(dirpath)

    # --- REPORTING ---
    if empty_dirs:
        print(f"📁 Found {len(empty_dirs)} Empty Directories:")
        for d in empty_dirs:
            print(f"  - {d}")
            # Uncomment the next line to auto-delete empty folders
            # os.rmdir(d) 
            
    if empty_files:
        print(f"\n📄 Found {len(empty_files)} Empty Files (Safe to delete):")
        for f in empty_files:
            print(f"  - {f}")
            # Uncomment the next line to auto-delete empty files
            # os.remove(f)

    if duplicates:
        print(f"\n👯 Found {len(duplicates)} Exact Duplicate Files:")
        for dup, original in duplicates:
            print(f"  - {dup} (Duplicate of {original})")

    if not empty_dirs and not empty_files and not duplicates:
        print("✅ Repository is clean! No empty files, folders, or duplicates found.")

if __name__ == "__main__":
    clean_and_audit()