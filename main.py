import db.db as db
from ui import ui

db.check_or_create_user_db()
ui.initializeGui()