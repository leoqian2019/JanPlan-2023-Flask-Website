from website import create_app
import requests
from flask import Flask, render_template

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error-404.html'), 404


def find_book_title_with_isbn(isbn):
    """
    :param isbn: the 10 or 13 digit isbn of the given book
    :return: the book title given by google api after query using the isbn
    """

    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if response.status_code == 200:
        response = response.json()
        if "items" in response:
            book = response["items"][0]
            book_title = book['volumeInfo']['title']
            return book_title

    return None


def convert_group_num_to_text(group_num):
    if group_num == str(1):
        return "for donation"
    elif group_num == str(2):
        return "for exchange"
    else:
        return "for needed"


# Add the function by name to the jinja environment.
app.jinja_env.globals.update(find_book_title_with_isbn=find_book_title_with_isbn)
app.jinja_env.globals.update(convert_group_num=convert_group_num_to_text)

if __name__ == '__main__':
    app.run(debug=True)
