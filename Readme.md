venv/Scripts/activate
## bash
    source venv/Scripts/activate

pip install -r requirements.txt



flask db init
flask db migrate -m "users table"
flask db upgrade
flask run ou python run.py


