The Textbook company Springer Link has a lot of free textbooks to download on their website.
During the COVID-19 Pandemic, they made a lot more of them free [here](https://link.springer.com/search?package=mat-covid19_textbooks&facet-language=%22En%22&facet-content-type=%22Book%22). Because I am a book hoarder,
I wanted to download all of the books available while they are still there, even though I
have no intention of reading them all (and may not even read any). To aid in this quest
this script. On  the Springer results page, there is a button on the top right with a down arrow that allows you to download the search results as a csv. The information therein contains enough information to reconstruct the download link for each book.

And that is what this script does. To use, run `python3 dl.py <csv file 1> ... <csv file n>`
For each CSV file, it creates a directory of the same name as the csv (sans the extension) and puts all the files inside. Depending on internet connection, it can work really well. For the link above, it downloaded 406 pdfs (8.71 GB) in < 6 minutes. Also in this repo are some csvs. This might not work in the future if Springer changes stuff.