
-- Create a new database (This command needs to be run in the PostgreSQL environment)
-- CREATE DATABASE sql_practice;

-- Connect to the database (This command is for psql command line tool)
-- \c sql_practice

-- Create 'distribution_companies' table
CREATE TABLE distribution_companies (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL
);

-- Create 'movies' table
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    movie_title VARCHAR(255) NOT NULL,
    imdb_rating DECIMAL(2,1),
    year_released INT,
    budget DECIMAL(10,2),
    box_office DECIMAL(10,2),
    distribution_company_id INT,
    language VARCHAR(255),
    FOREIGN KEY (distribution_company_id) REFERENCES distribution_companies (id)
);

-- Insert data into 'distribution_companies'
INSERT INTO distribution_companies (company_name) VALUES
('Columbia Pictures'),
('Paramount Pictures'),
('Warner Bros. Pictures'),
('United Artists'),
('Universal Pictures'),
('New Line Cinema'),
('Miramax Films'),
('Produzioni Europee Associate'),
('Buena Vista'),
('StudioCanal');

-- Insert data into 'movies'
INSERT INTO movies (movie_title, imdb_rating, year_released, budget, box_office, distribution_company_id, language) VALUES
('The Shawshank Redemption', 9.2, 1994, 25.00, 73.30, 1, 'English'),
('The Godfather', 9.2, 1972, 7.20, 291.00, 2, 'English'),
('The Dark Knight', 9.0, 2008, 185.00, 1006.00, 3, 'English'),
('The Godfather Part II', 9.0, 1974, 13.00, 93.00, 2, 'English, Sicilian'),
('12 Angry Men', 9.0, 1957, 0.34, 2.00, 4, 'English'),
('Schindler\'s List', 8.9, 1993, 22.00, 322.20, 5, 'English, German, Yiddish'),
('The Lord of the Rings: The Return of the King', 8.9, 2003, 94.00, 1146.00, 6, 'English'),
('Pulp Fiction', 8.8, 1994, 8.50, 213.90, 7, 'English'),
('The Lord of the Rings: The Fellowship of the Ring', 8.8, 2001, 93.00, 898.20, 6, 'English'),
('The Good, the Bad and the Ugly', 8.8, 1966, 1.20, 38.90, 8, 'English, Italian, Spanish');
