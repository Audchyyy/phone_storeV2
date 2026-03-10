from phone_store import create_app
from phone_store.extensions import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
