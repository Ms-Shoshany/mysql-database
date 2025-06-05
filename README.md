


A lightweight and dynamic wrapper around `mysql.connector` to simplify MySQL database interactions with schema-driven table creation, automatic connection handling, and Python object mapping.

---
pip install mysql-database
---

## 📁 Project Structure

Your project must include a `schemas/` folder (or custom path) containing JSON schema files for each database.

Example:

```
schemas/
└── mydatabase.json
```
in this case the database name will be 'mydatabase'

Each file should follow this format:

```json
{
  "users": {
    "name": "VARCHAR(255)",
    "email": "VARCHAR(255)",
    "active": "BOOLEAN"
  },
  
  "products": {
    "title": "VARCHAR(255)",
    "price": "FLOAT",
    "users_id": "INT"
  }
}
```
to use FOREIGN KEY create an INT column <foreign_table>_id:
    for example in the schema above
        users_id will be assosiated with the table users
---

## 🚀 Usage Example

```python
from easy_mysql import Database, DatabaseCreds

# Define credentials
creds = DatabaseCreds(
    host="localhost",
    user="root",
    password="yourpassword",
    port=3306
)

# Initialize database (auto-creates DB and tables if they don't exist)
db = Database(name="mydatabase", creds=creds)

# Add object
user_id = db.add_object("users", {
    "name": "Alice",
    "email": "alice@example.com",
    "active": True
})

# Get list of user objects
users = db.get_list_of_objects("users")

# Get user by ID
user = db.get_object_by_id("users", user_id)

# Update user
db.update_object("users", user_id, {"active": False})

# Delete user
db.delete_object("users", user_id)
```

---

## 🔍 Advanced Usage

### Get filtered list of objects:

```python
db.get_filtered_list_of_objects(
    object_type="users",
    filter="alice",
    include_columns=["name", "email"]
    as_dict=True
)
```

---

## 📄 License

MIT License. See `LICENSE` file for details.

```

---

Let me know if you'd like to add badges (PyPI version, license, etc.) to the top of the README.
```
