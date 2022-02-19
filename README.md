# xpense-api
API for the xpense react application. View the API documentation : https://infinite-taiga-28404.herokuapp.com/redoc

## Project Setup
**Create Database in PostgreSQL**
<pre>
psql
CREATE DATABASE xpense_db;
</pre>

**Create .env file in the root of the project**
<pre>
touch .env
</pre>

**Add the following lines to the file**
<pre>
FLASK_APP=run.py
DATABASE_URL=postgresql://username:password@localhost:5432/xpense_db
JWT_SECRET_KEY='secret key'
JWT_ERROR_MESSAGE_KEY=message
</pre>

**Generate JWT_SECRET_KEY (Optional)**
<pre>
# Run in python shell
import secrets
secrets.token_hex()
</pre>

**Install project requirements**
<pre>
pip install -r requirements.txt
</pre>

**Perform Migrations**
<pre>
source env/bin/activate
flask db migrate
flask db upgrade
</pre>

**Run the code**
<pre>
flask run
</pre>
