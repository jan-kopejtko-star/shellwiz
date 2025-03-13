from app import app, db

if __name__ == "__main__":
    with app.app_context():
        try:
            # Connect to the database
            with db.engine.connect() as connection:
                connection.execute(db.text('DROP TABLE IF EXISTS alembic_version'))
                print("Migration tracking table dropped successfully")
        except Exception as e:
            print(f"Error: {e}")