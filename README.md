# RobertVmAPI
Python API created using FASTAPI and Azure CLI , with the end-goal to facilitate the easier provisioning and deprovisioning of vms within Azure.


## POST example
```json
{
  "order":
  {
    "vm_name": "plm",
    "resource_group": "plm",
    "location": "plm",
    "user_id": 1,
    "recipient_id": 2
  }
}
```

```python
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         first_name TEXT NOT NULL,
#         last_name TEXT NOT NULL
#     );
#     ''')
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS orders (
#         id INTEGER PRIMARY KEY,
#         vm_name TEXT NOT NULL,
#         rg_name TEXT NOT NULL,
#         location TEXT NOT NULL,
#         user_id INTEGER,
#         recipient_id INTEGER,
#         status TEXT NOT NULL,
#         FOREIGN KEY (user_id) REFERENCES users(id),
#         FOREIGN KEY (recipient_id) REFERENCES users(id)
#     );
# ''')
```