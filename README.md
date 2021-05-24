# users-search
Run the steps inside virtual environment.

python3.9 -m venv env

source env/bin/activate

pip install -r requirements.txt

export API_TOKEN=<github_personal_token_of_user>

python3.9 main.py

From POSTMAN hit the URL
http://127.0.0.1:8080/users/?name=user1,user2&include=commit_latest
