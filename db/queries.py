

CREATE_TABLE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    size TEXT,
    price TEXT,
    product_id TEXT,
    photo TEXT
);
"""

INSERT_PRODUCT = """
INSERT INTO products (name, category, size, price, product_id, photo)
VALUES (?, ?, ?, ?, ?, ?);
"""