#### DLCXSS

#### Deep Link Community XSS Scanner

Our XSS vulnerability scanner is a comprehensive scanning tool designed to identify reflected XSS vulnerabilities in web applications. It offers advanced features to enhance your web security testing process:

- **Crawling Capabilities**: Utilizes Selenium bot to mimic real human interactions to find deep links inside a web application, ensuring thorough exploration of the web application.
- **Reporting Capabilities**: Generates detailed reports in a Word file format, including all findings and screenshots.
- **WAF Testing Capabilities**: Supports detection of Web Application Firewalls (WAF) and uses specialized payloads to test their effectiveness.
- **Community Feature**: Allows users to contribute and share payloads with the community, fostering collaboration and improving overall effectiveness.

### Installation Guide
Below are the instructions for installing both Geckodriver for crawling capabilities and the application itself:
#### Prerequisites

- Python 3.x
- Selenium

#### Installing Geckodriver

##### Windows

1. Download the latest version of Geckodriver from the [Geckodriver releases page](https://github.com/mozilla/geckodriver/releases).
2. Extract the downloaded file.
3. Add the extracted `geckodriver.exe` to your system PATH:
    - Right-click on 'This PC' or 'Computer' on the desktop or in File Explorer.
    - Click 'Properties'.
    - Click 'Advanced system settings'.
    - Click 'Environment Variables'.
    - In the 'System variables' section, find the `Path` variable and select it.
    - Click 'Edit'.
    - Click 'New' and add the path to the directory where `geckodriver.exe` is located.
    - Click 'OK' to close all dialogs.

##### Kali Linux

1. Open a terminal.
2. Download Geckodriver:

    ```sh
    wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
    ```

3. Extract the downloaded file:

    ```sh
    tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
    ```

4. Move Geckodriver to `/usr/local/bin`:

    ```sh
    sudo mv geckodriver /usr/local/bin/
    ```

5. Ensure Geckodriver is executable:

    ```sh
    sudo chmod +x /usr/local/bin/geckodriver
    ```

### Installing the Python Application

1. **Clone the Repository**:
    - Open a terminal or Git Bash.
    - Clone the repository to your local machine:

    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. **Navigate to the Project Directory**:
    - Change directory to the cloned repository:

    ```sh
    cd yourrepository
    ```

3. **Create a Virtual Environment**:
    - Create a virtual environment to manage dependencies:

    ```sh
    python -m venv .venv
    ```

4. **Activate the Virtual Environment**:

    - On Windows:

    ```sh
    .venv\Scripts\activate
    ```

    - On Linux/Mac:

    ```sh
    source .venv/bin/activate
    ```

5. **Install the Dependencies**:
    - Install the required packages listed in `requirements.txt`:

    ```sh
    pip install -r requirements.txt
    ```


### Summary

By following these steps, you will have Geckodriver installed and your Python application set up with all the necessary dependencies on both Windows and Kali Linux. This setup ensures that DLCXSS scanner can do its job to the fullest.
