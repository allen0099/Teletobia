from sqlalchemy import text
from sqlalchemy.orm import Session

from database import db, Database

if __name__ == "__main__":
    """This is example of Engine for raw connection to database."""
    if True:
        with db.ENGINE.connect() as conn:
            # As we did not call Connection.commit(), so this block will automatically ROLLBACK,
            # And the data is not committed.
            result = conn.execute(text("SELECT 'hello world'"))
            print(result.all())

        with db.ENGINE.connect() as conn:
            # With this, we can actually commit the data into database.
            # We called Connection.commit() to commit the data as we need.
            conn.execute(text("CREATE TABLE some_table (x int, y int)"))
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
            )
            conn.commit()

        with db.ENGINE.begin() as conn:
            # This is a transaction block form, it will automatically ROLLBACK if any exception raised.
            # And if there is no exception, it will automatically COMMIT.
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
            )

    """This is a Session usage example, which use a context manager to automatically commit or rollback."""
    if True:
        stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(
            y=6
        )
        # verbose version of what a context manager will do
        with Session(db.ENGINE) as sess:
            sess.begin()
            try:
                sess.execute(stmt)
            except:
                sess.rollback()
                raise
            else:
                sess.commit()

        # create session and add objects
        with Session(db.ENGINE) as sess:
            with sess.begin():
                sess.execute(stmt)
            # inner context calls session.commit(), if there were no exceptions
        # outer context calls session.close()

        # create session and add objects
        with Session(db.ENGINE) as sess, sess.begin():
            sess.execute(stmt)
        # inner context calls session.commit(), if there were no exceptions
        # outer context calls session.close()

        """The code blocks above are all equivalent."""

    """Using sessionmaker to make a new session in need."""
    if True:
        # Construct a Session() and include begin()/commit()/rollback() at once
        with Database.sess.begin() as sess:
            sess.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
            )
            sess.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 2, "y": 2}, {"x": 3, "y": 7}],
            )
        # commits the transaction, closes the session

    """Scoped session can use without context manager and can used in anywhere, when finished, call remove() to remove it."""
    if True:
        db.session.execute(text("SELECT 'Goodbye World'"))

        # Remove the scoped session from the registry.
        db.session.remove()
