import pandas as pd
import pytest
from PandasToPydantic.test.testData.libraryTypes import Book, Author, Library
from PandasToPydantic.test.config import LIBRARY_DATA_PATH
from PandasToPydantic.src.dataframeSerializer import (
    expandAnnotation,
    getBaseFields,
    getListFields,
    serializeDataframe,
)

data = pd.read_csv(LIBRARY_DATA_PATH)

targetLibrary1 = {
    "LibraryID": 1,
    "LibraryName": "City Central Library",
    "Location": "Cityville",
    "EstablishedYear": 1950,
    "BookCollectionSize": 50000,
    "AuthorList": [
        {
            "AuthorID": 1,
            "AuthorName": "J.K. Rowling",
            "AuthorBirthdate": "1965-07-31",
            "BookList": [
                {
                    "BookID": 1,
                    "Title": "Harry Potter and the Philosopher's Stone",
                    "Genre": "Fantasy",
                    "PublishedYear": 1997,
                    "AvailableCopies": 5,
                }
            ],
        },
        {
            "AuthorID": 6,
            "AuthorName": "J.R.R. Tolkien",
            "AuthorBirthdate": "1892-01-03",
            "BookList": [
                {
                    "BookID": 11,
                    "Title": "The Hobbit",
                    "Genre": "Fantasy",
                    "PublishedYear": 1937,
                    "AvailableCopies": 2,
                }
            ],
        },
        {
            "AuthorID": 5,
            "AuthorName": "Mark Twain",
            "AuthorBirthdate": "1835-11-30",
            "BookList": [
                {
                    "BookID": 10,
                    "Title": "The Adventures of Tom Sawyer",
                    "Genre": "Adventure",
                    "PublishedYear": 1876,
                    "AvailableCopies": 2,
                }
            ],
        },
    ],
}


class Test_serialzeDataframe:
    def test_library1(self):
        libraryList = serializeDataframe(data, expandAnnotation(Library))
        library1 = libraryList[0]

        assert library1 == targetLibrary1
