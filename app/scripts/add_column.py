from database.sqllite_engine import engine
from sqlalchemy import text

def run():
    with engine.connect() as conn:
        conn.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN must_change_password BOOLEAN DEFAULT 0"
            )
        )
        conn.commit()

    print("Column added successfully")

if __name__ == "__main__":
    run()
