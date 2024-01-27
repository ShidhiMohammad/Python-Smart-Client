# SmartClient README

## Overview
The `SmartClient` class is a Python-based utility designed to interact with web servers. It can parse URLs, establish secure connections, handle redirects, check for HTTP/2 support, print cookies from the server's response, and determine whether the server’s response indicates password protection.

## Usage
### Command-Line Execution

python3 SmartClient.py <url>

## Class Methods

`__init__(self, url: str)`
Initializes the SmartClient object with the provided URL.

`parseUrl(self, url: str) -> tuple`
Parses the given URL and returns the domain and path.

`retrieveWebContent(self, domain: str=None, path: str=None, redirect_count: int=0) -> str`
Retrieves web content from the server. Handles redirects recursively and returns the response as a string.

`supportsHttp2(self) -> bool`
Checks if the server supports HTTP/2 and returns a boolean value.

`printCookies(self, response: str)`
Prints the cookies found in the server's response.

`isPasswordProtected(self, response: str) -> bool`
Checks if the server's response is password-protected and returns a boolean value.

`run(self)`
Executes the client, prints the results, and handles errors.
