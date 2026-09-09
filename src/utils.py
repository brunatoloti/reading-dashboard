import requests


class ReadingDashboardUtilities:
    def __init__(self, data):
        self.data = data
        self.book_name = None
        self.publisher = None
        self.pages_quantity = None
        self.author_name = None
        
    def search_open_library(self):
        isbn = self.data['isbn']
        req_book = requests.get(f'https://openlibrary.org/isbn/{isbn}.json')
        if req_book.status_code == 200:
            req_book = req_book.json()
            try:
                self.book_name = req_book['title']
            except:
                pass
            try:
                self.publisher = req_book['publishers']
            except:
                pass
            try:
                self.pages_quantity = req_book['number_of_pages']
            except:
                pass
        req_author1 = requests.get(f'https://openlibrary.org/search.json?isbn={isbn}')
        if req_author1.status_code == 200:
            author_id = req_author1.json()['docs'][0]['author_key'][0]
            print(author_id)
            req_author2 = requests.get(f'https://openlibrary.org/author/{author_id}.json')
            if req_author2.status_code == 200:
                try:
                    self.author_name = req_author2.json()['personal_name']
                except:
                    try:
                        self.author_name = req_author2.json()['name']
                    except:
                        pass
        return {'book_name': self.book_name,
                'author_name': self.author_name,
                'pages_quantity': self.pages_quantity,
                'publisher': self.publisher}