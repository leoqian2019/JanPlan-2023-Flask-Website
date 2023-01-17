from website import create_app
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error-404.html'), 404


def find_book_title_with_isbn(isbn):
    cookies = {
        'PHPSESSID': '1sri7noa3r4t8mdvtrp9nf3cdd',
        '_ga': 'GA1.2.129701461.1673921088',
        '_gid': 'GA1.2.1721929122.1673921088',
        '_gat': '1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=1sri7noa3r4t8mdvtrp9nf3cdd; _ga=GA1.2.129701461.1673921088; _gid=GA1.2.1721929122.1673921088; _gat=1',
        'Referer': 'https://isbnsearch.org/search?s=1285741552222',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    response = requests.get(f'https://isbnsearch.org/isbn/{isbn}', cookies=cookies, headers=headers)
    if response.status_code == 200:
        response = response.text
        soup = BeautifulSoup(response, "html.parser")

        book_title = soup.find('h1')

        if book_title:
            book_title = book_title.get_text()
            return book_title

    return None


# Add the function by name to the jinja environment.
app.jinja_env.globals.update(find_book_title_with_isbn=find_book_title_with_isbn)

if __name__ == '__main__':
    app.run(debug=True)
