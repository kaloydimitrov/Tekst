# Virtual Environment
`py -m venv .venv`<br />
`.venv\Scripts\activate.bat`

# Install Requirements
`pip install -r requirements.txt`

# Database Setup
name - **tekst_db**
<br />`python manage.py makemigrations`
<br />`python manage.py migrate`
<br />`python manage.py createsuperuser`

# Create .env file
EMAIL_HOST_USER=<br />
EMAIL_HOST_PASSWORD=

# Run project
`python manage.py runserver`

# PyCharm
Configure Inspections: `Ctrl` `Alt` `Shift` `H`<br />
Reformat file: `Ctrl` `Alt` `L`
