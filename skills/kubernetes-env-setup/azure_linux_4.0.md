Yes, Azure Linux 4.0 has been released, but it is currently in Public Preview. Microsoft officially launched the public preview on June 2, 2026, shifting it from an internal-only tool to a full general-purpose commercial distribution. [1, 2, 3, 4] 
Because it is in preview, Microsoft notes that it is currently intended for evaluation and testing purposes rather than critical production environments. [2] 
## Key Specifications & Features
Azure Linux 4.0 represents a major architectural shift and modernization for Microsoft's in-house distribution: [2, 5] 

* 
* Fedora-Based Upstream: It is now a Fedora-derived, RPM-based distribution, making it highly familiar to users of Red Hat, CentOS, or Rocky Linux.
* Upgraded Kernel: It ships with the newer Linux 6.18 LTS kernel.
* New Package Manager: It uses DNF5, a C++ rewrite of the DNF package manager that is significantly faster and lighter.
* Target Workloads: It is built strictly for cloud, server, and container workloads; there is no desktop GUI version.
* Enhanced Security: Includes OpenSSL 3.5 with native post-quantum cryptography support. [1, 6, 7, 8, 9] 
* 

## Current Availability
You can access and test Azure Linux 4.0 across several environments: [4, 10] 

* 
* Azure Marketplace: Deployable on any Azure Virtual Machine (VM) or VM Scale Set.
* Azure Container Linux (ACL): Available as an immutable, container-optimized base image variant.
* Local Testing: For the first time, Microsoft is providing downloadable ISO images directly on the [Azure Linux GitHub Repository](https://github.com/microsoft/azurelinux) so developers can boot and test it locally inside a local VM without needing an Azure account.
* WSL Support: Integration for the Windows Subsystem for Linux is scheduled to become available shortly. [1, 11, 12, 13] 
* 

---

You can download the latest installer files for Azure Linux 4.0 directly from the official [microsoft/azurelinux GitHub Repository](https://github.com/microsoft/azurelinux). [1, 2] 
Note: Microsoft does not list these ISOs under the standard "Releases" tab. Instead, they are embedded directly as short aka.ms download links within the Using Azure Linux section on the repository's main page. [3, 4, 5, 6] 
## 1. Download Links
Choose the ISO installer link matching your VM architecture: [1, 2] 

* 
* Azure Linux 4.0 ISO Installer (x86_64) (For Intel/AMD virtual machines)
* Azure Linux 4.0 ISO Installer (ARM64) (For Apple Silicon, Ampere, or ARM64 virtual environments) [1, 2, 7] 
* 

------------------------------
## 2. How to Install Azure Linux 4.0 in a Local VM
Azure Linux 4.0 images are currently in Public Preview and are not Secure Boot signed. They utilize a text-based Anaconda installer. [3, 8] 
Follow these steps to deploy it in common hypervisors like Hyper-V, Proxmox, VirtualBox, or QEMU/KVM. [6, 8] 
## Step 1: Configure the VM Hardware [6] 

   1. Create a New VM: Define your VM as a Generation 2 machine (or select UEFI firmware instead of legacy BIOS).
   2. Disable Secure Boot: Ensure Secure Boot is turned off in your VM settings so the un-signed preview ISO can boot.
   3. Disable Dynamic Memory: Set a fixed RAM allocation (minimum 2 GB is recommended).
   4. Attach the ISO: Add the downloaded Azure Linux 4.0 ISO file to the VM’s virtual CD-ROM drive and set it as the first boot device. [6, 8, 9, 10, 11] 

## Step 2: Boot and Start the Installer [6] 

   1. Turn on the VM. It will boot into a minimal command-line shell environment.
   2. Launch the guided interactive installer by typing the following command and pressing Enter:
   
   install-azl
   
   [6] 

## Step 3: Run Through the Anaconda Prompt Configuration
The installer will prompt you to complete the basic configuration sections via text-based inputs: [6, 8] 

* 
* Disk Partitioning: Choose between a standard automatic installation or an encrypted disk setup using LUKS.
* User Creation: Create your administrator user account and define a strong root password.
* Resolve Warnings: Ensure all critical configuration points marked with an exclamation point [!] are filled out or resolved, otherwise the installation will not proceed. [6, 9, 12, 13] 
* 

## Step 4: Finalize and Reboot

   1. Once you complete the prompts, the text installer will copy the base packages onto your virtual hard drive.
   2. When the success prompt appears, press Enter to reboot the machine.
   3. Unmount the ISO image from the virtual drive so the system boots into your local hard drive installation.
   4. Sign in with your newly provisioned credentials. You will be greeted by a fast, minimal server-style CLI. [9, 14, 15, 16, 17] 

---

To run Azure Linux 4.0 natively using Windows Subsystem for Linux (WSL) containers, you must use Microsoft's newly introduced native container runtime feature (wslc), which is currently in public preview. [1, 2] 
Because wslc runs lightweight, native OCI containers on Windows without needing a heavy Hyper-V environment or Docker Desktop, it serves as the ideal framework for running the containerized version of Azure Linux 4.0. [1, 3, 4, 5, 6] 
------------------------------
## Step 1: Install the WSL Pre-Release Client
The container engine API (wslc) is bundled exclusively in the pre-release channels of WSL. [1, 2] 

   1. Open PowerShell as an Administrator.
   2. Force-update your WSL installation to the latest unstable preview build by running:
   
   wsl.exe --update --pre-release
   
   3. Restart WSL to apply changes:
   
   wsl.exe --shutdown
   
   [1, 3, 7, 8] 

------------------------------
## Step 2: Grab the Azure Linux 4.0 Container Core Link
Instead of downloading a massive ISO file, you will use Microsoft's official container registry image target. The container image path for the public preview is:
mcr.microsoft.com/azurelinux-beta/base/core:4.0 [9] 
------------------------------
## Step 3: Run Azure Linux 4.0 via WSL Container (wslc)
Once your preview client is updated, use the wslc engine to pull and boot into the environment immediately: [1] 

   1. Run the container command directly inside PowerShell to fetch the repository layer and execute an interactive Bash terminal:
   
   wsl.exe --container run -it mcr.microsoft.com/azurelinux-beta/base/core:4.0 /bin/bash
   
   2. You will be placed immediately inside the command line of Azure Linux 4.0. [10] 

------------------------------
## Step 4: Verify the Environment
Once inside the running shell, you can verify that you are truly executing the new Fedora-derived infrastructure and kernel configuration: [11, 12] 

* 
* Check the System Version:

cat /etc/os-release

(This will print NAME="Azure Linux" and VERSION="4.0").
* Test the New C++ Package Manager:

dnf5 update

(This validates the presence of the rewritten, hyper-fast dnf5 tool instead of standard tdnf or old python-based packages). [11, 13, 14] 
* 

---

To use the native WSL Containers engine (wslc), you must configure a clean installation of Windows to fetch the pre-release update channels. [1] 
Because wslc mirrors industry-standard OCI container commands, configuring directories and running Azure Linux 4.0 follows a syntax that is highly familiar to Docker users. [2, 3] 
------------------------------
## Part 1: Install WSL Container Capability on a Fresh Windows OS
Follow these steps on a brand-new install of Windows 10 (Build 19041+) or Windows 11: [4] 
## Step 1: Install the Base WSL Engine

   1. Right-click the Start Menu and select Terminal (Admin) or PowerShell (Admin).
   2. Run the deployment command to install virtual machine components and the base kernel:
   
   wsl --install
   
   3. Restart your computer when prompted to initialize the system architecture.
   (Note: If a default Linux setup window pops up after the reboot, you can fill it out or close it. We will be using the separate wslc engine). [4, 5, 6, 7, 8] 

## Step 2: Upgrade to the Container Pre-Release Preview
The wslc command-line utility is bundled inside the public preview channel. [9, 10] 

   1. Re-open PowerShell as an Administrator.
   2. Upgrade your WSL package version into the pre-release ring:
   
   wsl --update --pre-release
   
   3. Terminate running background instances to refresh the subsystem:
   
   wsl --shutdown
   
   [1, 5, 11, 12] 

## Step 3: Confirm Installation
Verify that the native Windows container runtime tool is installed and active: [11] 

wslc --version

(This will return a version output like WSLC 2.9.x or higher, indicating readiness). [3, 11] 
------------------------------
## Part 2: Map a Windows Folder into an Azure Linux 4.0 Container
Windows file sharing inside wslc utilizes a high-performance virtiofs backend filesystem that maps folders quickly. [6, 13] 
To share files between host and guest environments, use the standard volume binding flag (-v) followed by your Windows host path and your internal container destination path. [2, 14] 
## Option A: Run via PowerShell [15] 
When using a native Windows terminal, pass the absolute path exactly as it is formatted in Windows (e.g., C:\YourFolder):

wslc run -it -v "C:\Users\Public\Documents:/mnt/windows_data" ://microsoft.com /bin/bash

## Option B: Run from inside a standard WSL Distro (like Ubuntu) [16] 
If you prefer running commands from inside an existing WSL Linux distribution terminal, your local storage drives reside under /mnt/. Format your command like this: [17] 

wslc run -it -v /mnt/c/Users/Public/Documents:/mnt/windows_data ://microsoft.com /bin/bash

------------------------------
## Part 3: Verify the File Link
Once your container initializes and drops you into the Azure Linux shell prompt, run these steps to test the link:

   1. Move inside the target destination folder you created:
   
   cd /mnt/windows_data
   
   2. Display the folder contents:
   
   ls -la
   
   (You will immediately see all your existing local Windows documents).
   3. Create a test file inside the container:
   
   echo "Hello from Azure Linux 4.0" > container_test.txt
   
   4. Minimize your terminal window and open Windows File Explorer. Navigate to your C:\Users\Public\Documents folder on the host computer. The text file will be visible and fully editable from Windows. [18] 

---

Here is your meticulously researched step-by-step guide to installing the native Microsoft Coreutils for Windows, and configuring Claude Code and Codex CLI to utilize a Bash shell paired with these utilities. [1, 2, 3] 
------------------------------
## Part 1: Meticulous Step-by-Step Guide to Installing Windows Coreutils
Microsoft provides a native, high-performance port of Unix Coreutils written in Rust, eliminating the heavy overhead of Virtual Machines or WSL translation layers. [4, 5] 
## Step 1: System Requirements & Preparation

* 
* Operating System: Windows 11 (build 22H2 or newer recommended).
* Host Terminal: Ensure you have [Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/) installed for the best multi-shell execution behavior.
* Administrative Access: You must run the installer terminal with Elevated Privileges (Run as Administrator). [4, 6, 7, 8] 
* 

## Step 2: Install via WinGet (Method A - Recommended)
The fastest, most secure method utilizes the Windows Package Manager. [2] 

   1. Open Windows Terminal using PowerShell or CMD as an Administrator.
   2. Run the [WinGet Command](https://learn.microsoft.com/en-us/windows/package-manager/winget/):
   
   winget install Microsoft.Coreutils
   
   3. Accept the source agreements when prompted by typing Y. [2, 4, 7, 9, 10] 

## Step 3: Install via GitHub Prebuilt Binaries (Method B - Alternate)
If your corporate network blocks WinGet, use the official repository assets: [11] 

   1. Go to the official [Microsoft uutils-coreutils GitHub Releases page](https://github.com/microsoft/uutils-coreutils).
   2. Download the latest .msi or .exe installer architecture bundle (x64 or ARM64).
   3. Execute the file and complete the step-by-step installation wizard. [7, 12, 13] 

## Step 4: Add Utilities to Windows System Environment Variables
If the installer didn't automatically bind the environment paths, add them manually: [9] 

   1. Press Win + R, type sysdm.cpl, and hit Enter.
   2. Click the Advanced tab $\rightarrow$ Environment Variables.
   3. Under System variables, select Path and click Edit.
   4. Click New and append the default installation directory:
   
   C:\Program Files\coreutils\bin
   
   5. Click OK to save and apply. Close and reopen all active terminal windows. [9, 14, 15, 16] 

## Step 5: Verify the Coreutils Installation
Open a clean prompt and test standard GNU Linux commands natively: [14] 

touch verification_file.txt
uptime
ls -la

Note: In PowerShell, native aliases (like ls or cat) point to PowerShell cmdlets. Running ls.exe explicitly calls the newly installed Windows Coreutils version. [2, 14] 
------------------------------
## Part 2: Researching Bash & Coreutils Integration for AI Coding CLIs
Both Claude Code and Codex CLI operate under a dynamic agentic model where they programmatically invoke localized system shells to execute structural tool workflows (reading directories, searching text, or editing code files). [15, 17, 18] 
## 1. Claude Code Bash & Coreutils Configuration
By default, Claude Code natively attempts to run commands through the PowerShell tool layer when a Windows host environment is detected. However, it contains an explicit architectural fallback to map onto a Bash ecosystem if requested. [3, 19] 
## Step-by-Step Setup:
To force Claude Code to handle tasks natively through standard Unix formatting using Windows Coreutils, configure its local environment variables: [3] 

   1. Install Git for Windows: This is required because it yields the underlying /bin/bash.exe execution environment that acts as the shell runner. [3, 20] 
   2. Explicitly Route paths in Settings: Modify the global configuration parameters in Claude Code's config files:
   * Locate or create the configuration file at ~/.claude/settings.json (or your customized .claude/settings.json project workspace root).
      * Inject the absolute path pointing directly to your local Bash executable, forcing it to utilize the newly added Windows Coreutils paths:
      
      {
        "env": {
          "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
        }
      }
      
      [3, 21] 
   3. Alternatively, use Runtime Variable Injection: You can execute your prompt session by routing the command directly through PowerShell syntax or setting system-wide profiles:
   
   $env:CLAUDE_CODE_SHELL="C:\Program Files\Git\bin\bash.exe"
   claude
   
   [22] 

Now, when Claude processes terminal commands through its agent workflows, it pipes them through Git Bash. Because C:\Program Files\coreutils\bin is mapped directly inside your system PATH, your underlying Bash shell safely maps commands like cat, grep, and find natively over Windows file blocks without any translation issues. [2, 3, 9, 14, 19] 
------------------------------
## 2. Codex CLI Bash & Coreutils Configuration
The standalone Codex CLI (developed by OpenAI) functions primarily as a lightweight global system agent. While it natively supports direct script piping (codex exec), it relies entirely on the parent environment block to determine which system shell intercepts raw text. [1, 17, 23, 24, 25] 
## Step-by-Step Setup:

   1. Initialize the Session inside Git Bash: Instead of opening Codex from an elevated PowerShell or Windows CMD prompt, explicitly trigger your workspace directly inside a Git Bash terminal shell instance. [1, 20, 26] 
   2. Expose Coreutils directly to the Bash Profile: To ensure that the Windows Coreutils binary directory takes priority over any native or overlapping Git Bash internal utilities, insert the path explicitly into your Bash runtime config:
   * Open or create a ~/.bashrc or ~/.bash_profile file.
      * Add the core directory to the front of your path statement:
      
      export PATH="/c/Program Files/coreutils/bin:$PATH"
      
      * Save and execute source ~/.bashrc. [27] 
   3. Execute Codex: Launch the command line interface framework from inside your project folder:
   
   codex .
   
   [17] 

When you instruct Codex to build files, search strings, or run automated workflows via codex exec, the operations execution block safely invokes your configured Windows Coreutils stack seamlessly. [17] 
------------------------------
## Summary Matrix: Native Shell Comparison

| Configuration Metric | Claude Code Setup | Codex CLI Setup |
|---|---|---|
| Primary Execution Path | Controlled via settings.json environmental keys. | Driven by the parent shell context launching the tool. |
| Shell Routing Variable | CLAUDE_CODE_GIT_BASH_PATH | Managed through local custom system $PATH exports. |
| Fallback Behavior | Reverts back to standard Windows PowerShell. | Throws execution syntax or missing executable flags. |

---

This meticulously researched guide provides the architectural planning and exact configuration steps required to force OpenCode, Kilo Code, and Pi agent to execute commands inside a native Bash environment on Windows, natively backed by Microsoft's high-performance Windows Coreutils. [1, 2, 3, 4, 5] 
------------------------------
## Part 1: Strategic Pre-Requisites (The Foundation)
AI coding agents are highly efficient at writing Bash syntax, but natively stumble when dealing with PowerShell variations on Windows. By coupling Git Bash (the shell container) with Microsoft Coreutils (the native Windows binaries), we provide the agents with an optimal, high-speed execution environment. [2, 4, 6, 7] 
Before configuring the individual CLIs, ensure these dependencies are globally exposed:

   1. Install Native Windows Coreutils:
   
   winget install Microsoft.Coreutils
   
   This creates high-performance native ports of commands like cat, grep, and ls located at C:\Program Files\coreutils\bin.
   2. Install Git Bash: Download from git-scm.com to provide the underlying /bin/bash.exe runtime wrapper. [4, 7] 

------------------------------
## Part 2: CLI-Specific Integration & Routing Plans

   ┌────────────────────────────────────────┐
   │         Windows Host Environment       │
   └───────────────────┬────────────────────┘
                       │ Spawns
                       ▼
   ┌────────────────────────────────────────┐
   │    AI Agent CLI (OpenCode / Pi / Kilo) │
   └───────────────────┬────────────────────┘
                       │ Overrides Shell Path
                       ▼
   ┌────────────────────────────────────────┐
   │      Git Bash Runner (bash.exe)        │
   └───────────────────┬────────────────────┘
                       │ Prioritizes
                       ▼
   ┌────────────────────────────────────────┐
   │ Windows Coreutils (C:\Program Files...)│
   └────────────────────────────────────────┘

## 1. OpenCode CLI Configuration
OpenCode is a Go-based terminal agent. By default, it detects your SHELL environment variable or throws execution commands directly at Windows PowerShell. It provides an explicit configuration schema to swap out the underlying process engine. [2, 8] 
## Step-by-Step Configuration:

   1. Open or create the global configuration file for OpenCode. This is typically located at:
   
   %USERPROFILE%\.config\opencode\config.json
   
   [9, 10] 
   2. Inject the custom shell object. Note the escaped double-backslashes required for Windows directory paths:
   
   {
     "shell": {
       "path": "C:\\Program Files\\Git\\bin\\bash.exe",
       "args": ["-l", "-c"]
     }
   }
   
   [1, 8] 
   3. Open Git Bash on your computer and append the Windows Coreutils path to your active profile (~/.bashrc) so that OpenCode prioritizes Microsoft’s native utilities over standard Git binaries:
   
   export PATH="/c/Program Files/coreutils/bin:$PATH"
   
   4. Start your session by running opencode. When OpenCode automatically creates a terminal process tool to audit, find, or create code, it will pass strings directly through your optimized native Coreutils layer. [3, 4, 8] 

------------------------------
## 2. Pi Agent CLI Configuration
The Pi Coding Agent (@mariozechner/pi-coding-agent) explicitly mandates a Bash shell runtime layer on Windows and natively checks fixed locations upon startup. [1, 7] 
## Step-by-Step Configuration:

   1. Locate or create the initialization settings file for Pi:
   
   %USERPROFILE%\.pi\agent\settings.json
   
   2. Force-feed the shellPath variable directly into the JSON configuration:
   
   {
     "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe"
   }
   
   3. Expose the environment variable at execution time. Open an administrative PowerShell prompt and launch Pi with injected path priorities:
   
   $env:PATH = "C:\Program Files\coreutils\bin;" + $env:PATH
   pi
   
   4. Verify execution within Pi’s interface by running a shell pass-through command using the ! prefix:
   
   !which grep
   
   Expected Output: /c/Program Files/coreutils/bin/grep.exe [1, 7, 8, 11, 12] 

------------------------------
## 3. Kilo Code CLI Configuration
Kilo Code CLI (@kilocode/cli) spawns and orchestrates command execution independently through an encapsulated bash tool structure. [13, 14] 
## Step-by-Step Configuration:
Kilo Code defaults to using system-wide execution parameters or its internal TUI configs. [15] 

   1. Open your global or project-local configuration script:
   
   %USERPROFILE%\.config\kilo\tui.jsonc
   
   [15] 
   2. Look for or add the terminal shell properties layout:
   
   {
     "terminal": {
       "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe",
       "env": {
         "PATH": "C:\\Program Files\\coreutils\\bin;%PATH%"
       }
     }
   }
   
   3. Alternatively, if running Kilo Code inside VS Code via the Kilo CLI Launcher extension, ensure your VS Code Integrated Terminal default profile is explicitly set to Git Bash. [14] 
   4. Run kilo in your project folder. When the agent drops into automated execution cycles (e.g., Orchestrator or Code modes), the underlying commands natively route through the Windows Coreutils tool pipelines. [4, 13, 16, 17, 18] 

------------------------------
## Integration Architecture Overview

| AI Agent CLI | Configuration File Location | Path Routing Parameter |
|---|---|---|
| OpenCode | ~/.config/opencode/config.json | "shell": { "path": "..." } |
| Pi Agent | ~/.pi/agent/settings.json | "shellPath": "..." |
| Kilo Code | ~/.config/kilo/tui.jsonc | "terminal": { "shellPath": "..." } |
