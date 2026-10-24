# NoSQL Contact Book

A beginner-friendly Python command-line app that demonstrates **CRUD operations with MongoDB**.

## Features

- Add contacts (name, email, city)
- View all contacts in alphabetical order
- Search contacts by name (case-insensitive)
- Update a contact's name or city
- Delete contacts by email
- Avoid duplicate emails in the CLI

## Tech Stack

- Python 3.10+
- MongoDB (local server or MongoDB Atlas)
- PyMongo
- python-dotenv

## Getting Started

1. Clone the repository and open it in a terminal.
2. Make sure you have a MongoDB server running locally, or create a MongoDB Atlas cluster.
3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set `MONGODB_URI` to your MongoDB connection string. For local MongoDB, the default URI works.
5. Start the app:

   ```bash
   python app.py
   ```

## Example Menu

```text
=== Contact Book ===
1. Add contact
2. View contacts
3. Search by name
4. Update contact
5. Delete contact
0. Exit
```

## MongoDB Data Example

```json
{
  "name": "Sara",
  "email": "sara@example.com",
  "city": "Oulu"
}
```

The app uses database `contact_book` and collection `contacts`. MongoDB automatically creates them when the first document is inserted.

## Learning Goals

| Operation | MongoDB Method |
| --- | --- |
| Create | `insert_one()` |
| Read | `find()` / `find_one()` |
| Update | `update_one()` |
| Delete | `delete_one()` |

## Security

Do not commit `.env` or any database credentials. The `.gitignore` file excludes `.env`.

## Limitations

This is a learning project, not a production-ready contact manager. Duplicate email checking is performed in application code rather than enforced by a unique database index; concurrent writes could still create duplicates. Input validation is intentionally minimal.

## License

MIT
