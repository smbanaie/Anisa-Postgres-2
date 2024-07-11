-- init.sql
CREATE EXTENSION vector;

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    vector_description vector,  -- Assuming 'pv_vector' is your vector data type
    promised_ce INT,
    stock_level INT,
    category VARCHAR(255),
    title VARCHAR(255),
    brand VARCHAR(255),
    description TEXT
);

-- Insert ten sample products
INSERT INTO product (vector_description, promised_ce, stock_level, category, title, brand, description)
VALUES 
    ('{1.2, 3.4, 5.6}', 24, 100, 'Electronics', 'Laptop', 'BrandX', 'Powerful laptop for gaming and productivity.'),
    ('{0.8, 2.6, 4.9}', 12, 50, 'Clothing', 'T-shirt', 'FashionCo', 'Comfortable cotton t-shirt for everyday wear.'),
    ('{2.1, 4.3, 6.5}', 36, 80, 'Home & Kitchen', 'Coffee Maker', 'KitchenMaster', 'Automatic coffee maker for brewing fresh coffee.'),
    ('{1.5, 3.8, 7.2}', 48, 120, 'Electronics', 'Smartphone', 'TechGiant', 'Latest smartphone with high-resolution display and powerful processor.'),
    ('{0.9, 2.4, 5.7}', 18, 60, 'Clothing', 'Jeans', 'DenimCo', 'Classic denim jeans with a comfortable fit.'),
    ('{2.3, 4.6, 8.9}', 64, 150, 'Home & Kitchen', 'Blender', 'KitchenMaster', 'Powerful blender for making smoothies and sauces.'),
    ('{1.8, 3.1, 6.4}', 30, 70, 'Electronics', 'Tablet', 'TechGiant', 'Versatile tablet for work and entertainment.'),
    ('{0.7, 2.9, 4.2}', 10, 40, 'Clothing', 'Sweater', 'FashionCo', 'Cozy sweater for chilly days.'),
    ('{2.5, 4.8, 7.1}', 42, 90, 'Home & Kitchen', 'Rice Cooker', 'KitchenMaster', 'Automatic rice cooker for perfectly cooked rice every time.'),
    ('{1.3, 3.6, 5.9}', 28, 80, 'Electronics', 'Smart Watch', 'TechGiant', 'Smart watch with fitness tracking and notification features.');

