from flask import Flask, jsonify, request, Response 
from BookModel import *
from settings import *
import json

# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

@app.route ('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

def validBookObject(bookObject):
    if ("name" in bookObject 
            and "price" in bookObject 
                and "isbn" in bookObject):
        return True
    else:
        return False

# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
        "error": "Inalid book object passed in request",
        "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
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

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

def valid_patch_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
 
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
        
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
        
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response

    invalidBookObjectErrorMsg = {
        "error": "Book with ISBN number provided not found, so unable to delete",
        }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

app.run(port=5000)

# ~~PAGINATION~~
# DEFAULT_PAGE_LIMIT = 3
# @app.route('/books/page/<int:page_number>')
# def get_paginated_books(page_number):
#     print(type(request.args.get('limit')))
#     LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
#     startIndex = page_number*LIMIT-LIMIT
#     endIndex = page_number*LIMIT
#     print(startIndex)
#     print(endIndex)
#     return jsonify({'books': books[startIndex:endIndex]})
