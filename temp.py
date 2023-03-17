from typing import TypedDict

class Movie(TypedDict):
    title: str
    url: str


d: Movie = {'title': 'Fight club'}
print(d)