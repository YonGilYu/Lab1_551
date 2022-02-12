import os

import db

# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


def main():
    books_list = db.session.execute(
        "SELECT isbn, title, author, year FROM books_list"
    ).fetchall()
    for books_lists in books_list:
        print(f"{books_lists.isbn} to {books_lists.title}, {books_lists.author}")


if __name__ == "__main__":
    main()
