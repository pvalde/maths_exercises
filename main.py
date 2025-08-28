import db
import platformFuns

db.check_or_create_user_db()
print(platformFuns.get_list_of_users())