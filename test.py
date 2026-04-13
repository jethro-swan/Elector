#!/home/john/Sync/Elector/venv/bin/python3
#!/home/elector/ELECTOR/venv/bin/python3

from app.core.login import member_exists
from app.core.login import register_authenticated_login
from app.core.login import deregister_authenticated_login
from app.core.login import check_authenticated_login

test_user = "john.waters@cooptel.net"

def show_login_status(test_user):
    if check_authenticated_login(test_user):
        print("Test member is logged in")
    else:
        print("Test member is not logged in")


if member_exists(test_user):
    print("Test member exists")
else:
    print("Test member does not exist")

show_login_status(test_user)

if register_authenticated_login(test_user):
    print(test_user + " has been logged in")
else:
    print(test_user + " has not been logged in")

show_login_status(test_user)

if deregister_authenticated_login(test_user):
    print(test_user + " has been logged out")
else:
    print(test_user + " has not been logged out")

show_login_status(test_user)
