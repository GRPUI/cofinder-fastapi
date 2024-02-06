CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY ,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY ,
    name TEXT NOT NULL,
    category INT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    FOREIGN KEY (category) REFERENCES categories(id)
);
CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY ,
    product INT NOT NULL,
    price INT NOT NULL,
    source TEXT NOT NULL,
    link TEXT NOT NULL,
    date timestamp NOT NULL,
    FOREIGN KEY (product) REFERENCES products(id)
);
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY ,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY ,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role INT NOT NULL,
    token TEXT NOT NULL,
    FOREIGN KEY (role) REFERENCES roles(id)
);
CREATE TABLE IF NOT EXISTS user_products (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    review TEXT NOT NULL,
    date timestamp NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
