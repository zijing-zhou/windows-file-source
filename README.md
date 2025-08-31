# windows-file-source
Perform a comprehensive analysis of all files within the Windows installation media, including tracking their version details and modification history. Investigate each file’s intended function and its corresponding installation path post-deployment. Additionally, examine how these files change across different Windows updates or patches.

[![Logical Architecture Diagram](https://github.com/zijing-zhou/windows-file-source/blob/main/document/Logical%20Architecture%20Diagram/Logical%20Architecture%20Diagram.png)](https://github.com)

1. The final version is expected to fully automate the entire process — from providing only an ISO download link, to downloading, extracting, computing installation file hashes, creating a virtual machine, retrieving system files, computing system file hashes, and performing comparative analysis.

2. Considering that different installation options may result in variations in system files, in addition to the ISO download link, it is also necessary to provide a list of system components to be installed, and possibly configuration information.

3. After installing the operating system, the virtual machine needs to attempt deploying different system patches and record the changes in system files before and after the patch deployment.

4. The expected final output information includes:

    - Which system files originate from the installation media

    - Which system files are generated during the installation process

    - Which files change across different Windows versions

    - Which files change after selecting different system components

    - Which files change after deploying system patches
      
5. Expected Verification Technologies‌:

    - Which files change after deploying system patches
    - Windows Automated Installation Technology‌

    - Virtualization File Analysis‌
    
    - Common Package File Formats in Windows Installation Process
