// Test to demonstrate enhanced directory listing with file sizes and subdirectories
#include "Svc/FileManager/test/ut/FileManagerTester.hpp"
#include <iostream>

using namespace Svc;

int main() {
    std::cout << "Testing Enhanced Directory Listing\n";
    std::cout << "==================================\n";
    
    // Create test harness
    FileManagerTester tester;
    
    // Create test directory structure
    system("rm -rf test_enhanced_dir");
    system("mkdir -p test_enhanced_dir/subdir");
    system("echo 'file1 content here' > test_enhanced_dir/file1.txt");
    system("echo 'file2 longer content here' > test_enhanced_dir/file2.txt");  
    system("echo 'sub1 content' > test_enhanced_dir/subdir/sub1.txt");
    system("echo 'sub2 content' > test_enhanced_dir/subdir/sub2.txt");
    
    std::cout << "\nCreated test structure:\n";
    system("find test_enhanced_dir -type f -exec ls -la {} \\;");
    std::cout << "\n";
    
    // Call ListDirectory on our test directory
    std::cout << "Calling FileManager ListDirectory...\n";
    Fw::CmdStringArg dirName("test_enhanced_dir");
    tester.sendCmd_ListDirectory(0, 0, dirName);
    
    // Dispatch events
    tester.dispatchAll();
    
    // Check event counts
    std::cout << "\nEvent Counts:\n";
    std::cout << "- ListDirectoryStarted: " << tester.eventHistory_ListDirectoryStarted->size() << "\n";
    std::cout << "- DirectoryListing: " << tester.eventHistory_DirectoryListing->size() << "\n"; 
    std::cout << "- DirectoryListingSubdir: " << tester.eventHistory_DirectoryListingSubdir->size() << "\n";
    std::cout << "- ListDirectorySucceeded: " << tester.eventHistory_ListDirectorySucceeded->size() << "\n";
    
    // Print file events (if any)
    if (tester.eventHistory_DirectoryListing->size() > 0) {
        std::cout << "\nFile Events:\n";
        for (size_t i = 0; i < tester.eventHistory_DirectoryListing->size(); i++) {
            const auto& event = tester.eventHistory_DirectoryListing->at(i);
            std::cout << "  File: " << event.fileName.toChar() 
                     << " (Size: " << event.fileSize << " bytes)\n";
        }
    }
    
    // Print subdirectory events (if any)  
    if (tester.eventHistory_DirectoryListingSubdir->size() > 0) {
        std::cout << "\nSubdirectory Events:\n";
        for (size_t i = 0; i < tester.eventHistory_DirectoryListingSubdir->size(); i++) {
            const auto& event = tester.eventHistory_DirectoryListingSubdir->at(i);
            std::cout << "  Subdir: " << event.fileName.toChar() 
                     << " (Contains: " << event.fileCount << " files)\n";
        }
    }
    
    // Clean up
    system("rm -rf test_enhanced_dir");
    
    std::cout << "\nTest completed!\n";
    return 0;
}
