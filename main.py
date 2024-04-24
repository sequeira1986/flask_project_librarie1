import psycopg2
from flask import Flask, jsonify, request

conn = psycopg2.connect(
    dbname='brgeicfqg8kyazonirom',
    user='ulwgoripw8ejfilgoi5u',
    password='yIus83C46Zx1VgDBZ5UjzY04BQrST3',
    host='brgeicfqg8kyazonirom-postgresql.services.clever-cloud.com',
    port=50013
)

cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR
); 

 """)

cur.execute("""INSERT INTO  person (id, name, age, gender) VALUES
(1, 'Allan', 37, 'm'),
(2, 'Jose',37, 'm'),
(3, 'Veronika',40, 'f'),
(4, 'Stefan', 43, 'm'),
(5, 'Pedro', 57, 'm'),
(6, 'Macho', 17, 'm'),
(7, 'Pepe', 47, 'm');
 """)
cur.execute("""SELECT * FROM  person WHERE name = 'Jose'; """)
print(cur.fetchone())

cur.execute("""SELECT * FROM  person WHERE age > 50; """)
for row in cur.fetchall():
    print(row)

sql = cur.mogrify("""SELECT * FROM person WHERE starts_with(name, %s) AND age < %s;""", ("J", 50))
print(sql)
cur.execute(sql)
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()

books = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
    {'id': 3, 'title': 'El Quijote', 'author': 'Cervantes '},
    {'id': 4, 'title': 'Juan charrasquiado', 'author': 'Pedro infante'},
    {'id': 5, 'title': 'Lo fatal', 'author': 'Ruben Dario'},
    {'id': 6, 'title': 'El rey', 'author': 'Pepe Agilar'}
]

app = Flask(__name__)


@app.route('/')
def home():
    return 'Nasa kniznica'


@app.route('/knihy/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404


@app.route('/knihy/', methods=['POST'])
def add_book():
    if request.json and 'title' in request.json and 'author' in request.json:
        new_book = {
            'id': books[-1]['id'] + 1,
            'title': request.json['title'],
            'author': request.json['author']
        }
        books.append(new_book)
        return jsonify(new_book), 201
    else:
        return jsonify({"error": "Missing required fields in request body"}), 400


@app.route('/knihy/<int:id>', methods=['PUT'])
def update_book(id):  # Renamed variable for consistency
    for i, book in enumerate(books):
        if book['id'] == id:
            if request.json:
                books[i]['title'] = request.json.get('title', book['title'])
                books[i]['author'] = request.json.get('author', book['author'])
                return jsonify(books[i]), 200
            else:
                return jsonify({"error": "Empty request body"}), 400
    return jsonify({"error": "Book not found"}), 404


@app.route('/knihy/<int:id>', methods=['PATCH'])
def update_book_partial(id):  # Renamed variable for consistency
    for i, book in enumerate(books):
        if book['id'] == id:
            if request.json:
                for key, value in request.json.items():
                    book[key] = value
                return jsonify(books), 200
            else:
                return jsonify({"error": "Empty request body"}), 400
    return jsonify({"error": "Book not found"}), 404


@app.route('/knihy/<int:id>', methods=['DELETE'])
def delete_book(id):
    for i, book in enumerate(books):
        if book['id'] == id:
            del books[i]  # Remove the book from the list using delete
            return jsonify()
        return jsonify({"message": "Book deleted successfully"}), 200
    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run()
