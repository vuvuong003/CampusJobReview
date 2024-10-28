## Installing Python

Below are the instructions to install python based on your operating system.

### Installation for Windows
- Download the latest version of Python from [Python Downloads](https://www.python.org/downloads/)
- Once the download is complete, double click the downloaded package and follow the instructions as requested.
- The last request should include clicking the Install button. Here, you might be prompted to enter your password to install the new software. 
- To check for a successful installation, type: 
```bash
python --version
```
- If you face any issues, make sure Python was added to your PATH during installation. 

### Installation for Mac
MacOS comes with a pre-installation of Python. To install the latest version follow these steps:
- Install [Homebrew](https://brew.sh/). This step will require you to enter your computer login password to run this commaans: 
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Open a local terminal and type the following command to install python 
```bash
brew install python
```

- Once these steps are complete, the installation can be verified by:  
```bash
python3 --version
```
## Installing Pip
### Windows
- Download script from [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
- Run 
```bash
python get-pip.py
```

### Mac
- Download script
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
- Run
```bash
python get-pip.py
```

## Run the Application 
 - Clone the repository: 
```bash
git clone https://github.com/SAT510/CampusJobReview.git
```
- Navigate to the cloned repository: 
```bash
cd CampusJobReview/
```
- Enable the virtual environment: 
  - For Mac: 
    ```bash
    python3 -m venv myenv
    ```
    ```bash
    source myenv/bin/activate
    ```
    For Windows:
    ```bash
    python -m venv myenv
    ```
    ```bash
    myenv\Scripts\activate
    ```
- Upgrade pip:
```bash
pip install --upgrade pip
```
- Install Dependencies: 
```bash
cd review_backend
```
```bash
pip install -r requirements.txt
```
```bash
pip install django
```
- Create Migrations:
```bash
python manage.py makemigrations
```
- Apply Migrations: 
```bash
python manage.py migrate
```
- Start the server: 
```bash
python manage.py runserver
```


