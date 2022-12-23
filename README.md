# PhoneBook API

## Introduction
1.	FastAPI is and API framework by python that make API design easy to use and development. In short it is a Swiss army knife for API development.
2.	We require below files for keeping the code more organize and easy to understand the purpose:
    -   main.py
    -   database.py
    -   schemas.py
    -   models.py
    -   tests
        -   test_main.py
    -   requirements.txt
3.	main.py is the main execution file where all the http methods are implemented, and all dependency are called.
4.	database.py is where our SQLite configuration is present for DB creation and local session creation.
5.	schemas.py contains the schemas for table that is what field should be present in the DB table.
6.	models.py defines the request pattern allowed once the server receives the request. For every request I have used different model request and if request doesn’t follow then it would be invalid requests.
7.	Tests folder contains the automated test cases required. Inside this folder there is test_main.py which has all the test cases and using pytest all are automated.
8.	requirements.txt contains all the dependencies.

## Design of Regex
Used re python module for regex pattern matching. I have used blacklist approach (but whitelisting approach far better approach as per security requirements). Below are the regexs:
1.	name:
    -   .\*[\\\*;].\*: match “*;” and all the words before it and after it using “.*”
        -   Matched: select * from users;
    -   .\*[<><\/>].\*: match the open brackets and closed brackets having “/”.
        -   Matched: <Script>alert(“XSS”)</Script>
    -   .\*[\d].\* : match digits and everything before and after.
        -   Matched: L33t Hacker
    -   .\*[’]{2}.\*: matches “ ’ ” two times (together) and allowing everything before and after.
        -   Matched: Ron O’’Henry
    -   .\*[’].\*[-].\*[-].\*: matches “ ‘ ” and two “ - ” and allowing everything.
        -   Matched: Ron O’Henry-Smith-Barnes
    -   .\*[a-zA-Z][ ].\*[a-zA-Z].\*[a-zA-Z][ ].\*: matches spaces and allowing everything.
        -   Matched: Brad Everett Samuel Smith

2.	phoneNumber:
    -   .\*[a-zA-Z].+ : matches words and + to make sure to match the at least one word.
        -   Matched: Nr 102-123-1234
    -   .\*[/].\*: matches the / in the number.
        -   Matched:  1/703/123/1234
    -   [0-9]{10} : matches all the numbers with length 10.
        -   Matched: 7031111234
    -   [0-9]{3} : matches all the number with length 3.
        -   Matched: 123
    -   ^[\+][0-9]{4,}.\* : matches the number with min length of 4 and start should have +.
        -   Matched: +1234 (201) 123-1234
    -   ^\(001\).\* : matches at the start (001) of the number string and after that allow any number.
        -   Matched: (001) 123-1234
    -   ^[\+][0][1].\* : matches +01 at the start of the number string.
        -   Matched: +01 (703) 123-1234
    -   .+[a-z].+ : matches the word at least one.
        -   Matched: (703) 123-1234 ext 204

## Assumptions
1.	For .\*[\d].\* assuming name doesn’t have any word.
2.	.\*[’]{2}.\* assuming there will be only two ‘ ‘ but there could be more.
3.	[0-9]{10} assuming phone number should not be larger than 10 digit but for example +16823138425 which is valid and it is 10 digit. Also, I can match the + and matches infinite number but this could lead to buffer overflow issue if the api designed using c or c++.
4.	^[\+][0-9]{4,}.\* assuming this pattern will always come first.
5.	^\(001\).\* assuming this pattern is important or clue that this is the problem.

## Pros

At least whatever pattern mentioned my regex can match and we can block it.

## Cons

I have used blacklist approach where we block the invalid request but if there more pattern then we must find and then pattern. Better approach is whitelist where only allow valid request and block everything. This will solve finding different invalid requests.



