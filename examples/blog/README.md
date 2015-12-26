
Instructions
============

- Install virtualenv and python requirements
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Make sure that `source venv/bin/activate` is run before any python commands to ensure this environment is used.

- Manually create postgres database "main_dev" with user "main", password "main"

- Use the following commands to create the sql migration and update the database
```
python manage_db.py db init
python manage_db.py db migrate
python manage_db.py db upgrade
```

- Confirm databases user and comment are present

- Run the app in dev mode with:
```
python run.py dev
```

- To test the application, in a separate terminal window run:
```
python test.py
```
