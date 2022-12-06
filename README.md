
# Web Crawler by Łukasz Ziemacki
mail: lukasz.ziemacki@gmail.com

## Set up
Approach is to create and activate python virtual environment, install packages listed inside requirements.txt file using pip and run crawlers.py from console using desired arguments.

### Set up virtual environment
Create env:
```
\web-crawler> python -m venv venv
\web-crawler> venv/Scripts/activate
```
### Install packages:
```
(venv) \web-crawler> pip install -r requirements.txt 
```

## Running script:
General scheme: `python crawlers.py <crawler/print-tree> --page <URL> --format <csv/json> --output <path_to_file>`

Example:
```
(venv) \web-crawler> python crawlers.py crawl --page https://crawler-test.com/ --format json --output C:\Results
```

### Site Crawler
`crawl --page <URL> --format <csv/json> --output <path_to_file(default is main script location)>`  
Results are saved in CSV or JSON file format where in CSV each row, in JSON each object, is representing one page with the following columns/keys:
- url
- page title
- number of internal links
- number of external links
- number of times url was referenced by other pages


### Tree Crawler
`print-tree --page <URL>`
Prints the structure of the page as a tree in the following format:
```
Main page (5)
  subpage1 (2)
    subpage1_1 (0)
    subpage1_2 (0)
  subpage2 (1)
    subpage2_1 (0)
```
The `subpage` represents actual urls to pages and the numbers in parentheses represent the number of internal pages at the current level.

## Tests:
```
\web-crawler> python -m unittest
```

