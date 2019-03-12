from flask import Flask, jsonify, request, Response 
import json
from settings import *

app = Flask(__name__)

books = [
    {   'name': 'A',
        'price': 7.99,
        'isbn': 978999400165

    },
    {   'name': 'B',
        'price': 6.99,
        'isbn': 9792371000193

    },
    {   
        'name': 'C',
        'price': 7.99,
        'isbn': 9800394800165

    },
    {   'name': 'D',
        'price': 6.99,
        'isbn': 9812371000193

    },    
    {   'name': 'E',
        'price': 7.19,
        'isbn': 1234567890132
    },
    {   'name': 'F',
        'price': 2.99,
        'isbn': 9876653400165

    },
    {   'name': 'G',
        'price': 6.99,
        'isbn': 9792371000193

    },
    {   
        'name': 'H',
        'price': 7.99,
        'isbn': 9800394807776
    },
    {   'name': 'I',
        'price': 6.99,
        'isbn': 9810192374001

    },    
    {   'name': 'J',
        'price': 17.19,
        'isbn': 1917003390132

    },       
    {   'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165

    },
        {'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]

DEFAULT_PAGE_LIMIT = 3

# GET /books/page/<int:page_number>
# /books/page/1?limit=100
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    startIndex = page_number*LIMIT-LIMIT
    endIndex = page_number*LIMIT
    print(startIndex)
    print(endIndex)
    return jsonify({'books': books[startIndex:endIndex]})

# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route ('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    print(type(isbn))
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


# POST Method

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']           
        }
        books.insert(0, new_book)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response



def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book ["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
        }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

app.run(port=5000)


# @app.route('/books/<int:isbn>', methods=['PUT'])
# def replace_book(isbn):
#     request_data = request.get_json()
#     new_book = {
#         'name': request_data['name'],
#         'price': request_data['price'],
#         'isbn': isbn
#     }
#     i = 0
#     for book in books:
#         currentIsbn = book["isbn"]
#         if currentIsbn == isbn:
#             books[i] = new_book
#         i += 1
#     response = Response("", status=204)
#     return response

# def validBookObject(bookObject):
#     if ("name" in bookObject 
#             and "price" in bookObject 
#                 and "isbn" in bookObject):
#         return True
#     else:
#         return False
