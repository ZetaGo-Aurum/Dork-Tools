# Dork-Tools
Advanced Dork Tool

# Quick Installation Guide for Advanced Dorking Tool

This guide provides simple and easy steps to install the **Advanced Dorking Tool** on **Termux**, **Ubuntu**, and **Debian**.

## Prerequisites

Before starting the installation, ensure that you have the following installed on your system:

- **Python 3.6 or higher**
- **Git**
- **pip** (Python package installer)

## Installation on Termux

### Step 1: Update and Upgrade Termux Packages

```bash
pkg update && pkg upgrade -y
```

### Step 2: Install Required Packages

```bash
pkg install python git -y
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/ZetaGo-Aurum/Dork-Tools.git
```

### Step 4: Navigate to the Project Directory

```bash
cd DorkTools
```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Tool

```bash
python DorkTool.py
```


## Installation on Ubuntu/debian

### Step 1: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Required Dependencies

```bash
sudo apt install python3 python3-pip git -y
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/ZetaGo-Aurum/Dork-Tools.git
```

### Step 4: Navigate to the Project Directory

```bash
cd DorkTools
```

### Step 5: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 6: Run the Tool
```bash
python3 DorkTool.py
```


## Additional Tips

- **Permissions**: Ensure that you have the necessary permissions to execute the script. You can make the script executable using:
  
  ```bash
    chmod +x DorkTool.py
  ```
  
- **Virtual Environment**: It's recommended to use a virtual environment to manage dependencies:

  ```bash
    python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- **Help Menu**: After running the tool, navigate through the menu to explore various scanning options and configurations.
  
## Troubleshooting

- **Missing Dependencies**: If you encounter errors related to missing packages, ensure all dependencies listed in `requirements.txt` are installed correctly.
  
- **Permission Denied**: If you receive permission denied errors, try running the script with elevated privileges:

  ```bash
    sudo python3 DorkTool.py
  ```

- **Network Issues**: Ensure you have a stable internet connection as the tool relies on internet access to perform searches.
  
  
## Conclusion

Follow the above steps to quickly install and run the **Advanced Dorking Tool** on Termux, Ubuntu, and Debian. For further assistance, refer to the [GitHub Repository](https://github.com/ZetaGo-Aurum?tab=repositories).
