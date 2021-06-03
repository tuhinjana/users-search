# users-search
`Objective of this project`
This project works as rest-api server which accept HTTP GET request with list of user names
and search those usernames in github and get public repo of those users, last commit details of those repos.

Run the steps inside virtual environment.

python3.9 -m venv env

source env/bin/activate

pip install -r requirements.txt

export API_TOKEN=<github_personal_token_of_user>

python3.9 main.py

From POSTMAN hit the URL
http://127.0.0.1:8080/users/?name=abc_xyz,user2&include=commit_latest

Response will be as below:--
=======
```[
    {
        "user_id": 11111,
        "login_name": "abc_xyz",
        "resource_uri": "https://api.github.com/users/abc_xyz",
        "repo_list": [
            {
                "id": 2222222,
                "name": "scrapy-web-site-data",
                "url": "https://api.github.com/repos/abc_xyz/scrapy-web-site-data",
                "created_at": "2021-04-06T09:44:10Z",
                "updated_at": "2021-04-06T09:46:29Z",
                "commit_latest": {
                    "sha": "fd71c820e648367a4b032a53fd71bf4ecfb85911",
                    "commit": {
                        "author": {
                            "name": "Abc",
                            "email": "abc.def@gmail.com",
                            "date": "2021-04-06T10:03:04+00:00"
                        }
                    },
                    "html_url": "https://github.com/abc_xyz/scrapy-web-site-data/commit/fd71c820e648367a4b032a53fd71bf4ecfb85911"
                }
            },
        ]
    }
    ]
```
PS: if any user is not found in github , user will be skipped and logger will
add warning a message for this.
