#!/usr/bin/env python3
"""
Test script to demonstrate enhanced directory listing with the Ref deployment.
This shows the actual events being generated with file sizes and subdirectory counts.
"""

import os
import time
import subprocess
import tempfile
from pathlib import Path

def create_test_structure():
    """Create a test directory structure to demonstrate the enhanced listing"""
    test_dir = tempfile.mkdtemp(prefix="fprime_test_")
    
    # Create some files with different sizes
    with open(f"{test_dir}/small_file.txt", "w") as f:
        f.write("Small content")  # 13 bytes
    
    with open(f"{test_dir}/medium_file.txt", "w") as f:
        f.write("This is a medium-sized file with more content than the small one.")  # 67 bytes
    
    with open(f"{test_dir}/large_file.txt", "w") as f:
        content = "This is a large file! " * 100  # 2300 bytes
        f.write(content)
    
    # Create a subdirectory with some files
    subdir = f"{test_dir}/subdir"
    os.makedirs(subdir)
    
    with open(f"{subdir}/sub1.txt", "w") as f:
        f.write("Subdirectory file 1")
    
    with open(f"{subdir}/sub2.txt", "w") as f:
        f.write("Subdirectory file 2") 
    
    with open(f"{subdir}/sub3.txt", "w") as f:
        f.write("Subdirectory file 3")
    
    # Create an empty subdirectory
    empty_subdir = f"{test_dir}/empty_subdir"
    os.makedirs(empty_subdir)
    
    return test_dir

def show_directory_structure(test_dir):
    """Show the created directory structure"""
    print(f"\nTest directory structure created at: {test_dir}")
    print("=" * 60)
    
    # Show file sizes
    print("Files with sizes:")
    for item in sorted(os.listdir(test_dir)):
        path = os.path.join(test_dir, item)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            print(f"  📄 {item:<20} - {size:>6} bytes")
        elif os.path.isdir(path):
            file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            print(f"  📁 {item:<20} - {file_count:>6} files")
    
    # Show subdirectory contents
    subdir_path = os.path.join(test_dir, "subdir")
    if os.path.exists(subdir_path):
        print(f"\nContents of subdir/:")
        for item in sorted(os.listdir(subdir_path)):
            path = os.path.join(subdir_path, item)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                print(f"  📄 {item:<20} - {size:>6} bytes")

def main():
    print("F' Enhanced Directory Listing Demonstration")
    print("=" * 50)
    
    # Create test structure
    test_dir = create_test_structure()
    
    try:
        # Show what we created
        show_directory_structure(test_dir)
        
        print(f"\n" + "=" * 60)
        print("🚀 Expected Enhanced Events from FileManager:")
        print("=" * 60)
        
        print("\nFor 'ListDirectory' command on this directory, you should see:")
        print("1. ListDirectoryStarted event")
        
        print("2. Individual entry events:")
        # Count files and subdirs
        files = []
        subdirs = []
        for item in os.listdir(test_dir):
            path = os.path.join(test_dir, item)
            if os.path.isfile(path):
                files.append((item, os.path.getsize(path)))
            elif os.path.isdir(path):
                file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
                subdirs.append((item, file_count))
        
        for filename, size in sorted(files):
            print(f"   • DirectoryListing: {filename} (Size: {size} bytes)")
        
        for dirname, count in sorted(subdirs):
            print(f"   • DirectoryListingSubdir: {dirname} (Contains: {count} files)")
        
        print("3. ListDirectorySucceeded event")
        
        print(f"\n" + "=" * 60)
        print("💡 To see these events in action:")
        print("=" * 60)
        print("1. Run the F' GDS:")
        print(f"   cd {os.path.dirname(os.path.abspath(__file__))}/Ref")
        print("   fprime-gds")
        
        print("\n2. In the GDS Command tab, send:")
        print(f"   fileManager.ListDirectory(\"{test_dir}\")")
        
        print("\n3. Check the Events tab to see:")
        print("   - File entries with actual byte sizes")
        print("   - Subdirectory entries with file counts")
        print("   - Separate event types for files vs directories")
        
        print(f"\n📁 Test directory path: {test_dir}")
        print("📝 Remember to clean up the test directory when done!")
        
    except Exception as e:
        print(f"Error: {e}")
        # Clean up on error
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
