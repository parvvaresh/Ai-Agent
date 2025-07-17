-- Create the database and use it
CREATE DATABASE IF NOT EXISTS shop_db;
USE shop_db;

-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(500),
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    brand VARCHAR(100),
    price FLOAT NOT NULL,
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address VARCHAR(500),
    status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    payment_method VARCHAR(100),
    total_amount FLOAT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB;

-- Create the order_items (junction) table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    discount_percent INT DEFAULT 0,
    total_price FLOAT GENERATED ALWAYS AS (price * quantity * (1 - discount_percent / 100.0)) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB;

-- Generate 1000 customers
DELIMITER $$

CREATE PROCEDURE insert_customers()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 1000 DO
    INSERT INTO customers (name, email, phone, address, city, country)
    VALUES (
      CONCAT('Customer_', i),
      CONCAT('customer', i, '@example.com'),
      CONCAT('0912', LPAD(FLOOR(RAND() * 10000000), 7, '0')),
      CONCAT('Address_', i),
      CONCAT('City_', FLOOR(1 + (RAND() * 50))),
      'Iran'
    );
    SET i = i + 1;
  END WHILE;
END $$

DELIMITER ;

CALL insert_customers();
DROP PROCEDURE insert_customers;

-- Generate 1000 products
DELIMITER $$

CREATE PROCEDURE insert_products()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 1000 DO
    INSERT INTO products (name, description, category, brand, price, stock)
    VALUES (
      CONCAT('Product_', i),
      CONCAT('Description for product ', i),
      CONCAT('Category_', FLOOR(1 + (RAND() * 20))),
      CONCAT('Brand_', FLOOR(1 + (RAND() * 10))),
      ROUND(100000 + (RAND() * 10000000), -3),
      FLOOR(RAND() * 100)
    );
    SET i = i + 1;
  END WHILE;
END $$

DELIMITER ;

CALL insert_products();
DROP PROCEDURE insert_products;

-- Generate 1000 orders
DELIMITER $$

CREATE PROCEDURE insert_orders()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 1000 DO
    INSERT INTO orders (customer_id, shipping_address, status, payment_method, total_amount)
    VALUES (
      FLOOR(1 + (RAND() * 1000)),
      CONCAT('Shipping Address_', i),
      ELT(FLOOR(1 + (RAND() * 4)), 'Pending', 'Shipped', 'Delivered', 'Cancelled'),
      ELT(FLOOR(1 + (RAND() * 3)), 'Credit Card', 'Cash', 'PayPal'),
      ROUND(50000 + (RAND() * 10000000), -2)
    );
    SET i = i + 1;
  END WHILE;
END $$

DELIMITER ;

CALL insert_orders();
DROP PROCEDURE insert_orders;

-- Generate 1000 order_items
DELIMITER $$

CREATE PROCEDURE insert_order_items()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 1000 DO
    INSERT INTO order_items (order_id, product_id, quantity, price, discount_percent)
    VALUES (
      FLOOR(1 + (RAND() * 1000)),
      FLOOR(1 + (RAND() * 1000)),
      FLOOR(1 + (RAND() * 5)),
      ROUND(100000 + (RAND() * 10000000), -2),
      FLOOR(RAND() * 20)
    );
    SET i = i + 1;
  END WHILE;
END $$

DELIMITER ;

CALL insert_order_items();
DROP PROCEDURE insert_order_items;

-- Done: You now have 1000 rows in each table
