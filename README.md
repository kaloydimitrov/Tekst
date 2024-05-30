# Virtual Environment
py -m venv .venv<br />
.venv\Scripts\activate.bat

# Install Requirements
pip install -r requirements.txt
<br />_***you can let PyCharm do it instead**_

# Database Setup
name - **tekst_db**
<br />python manage.py makemigrations
<br />python manage.py migrate
