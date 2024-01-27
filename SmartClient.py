# Shidhi Mohammad Bin Arif
# V00911512

import re
import sys
import ssl
import socket

class SmartClient:
    REDIRECT_STATUS_CODES = [301, 302, 307]
    
    def __init__(self, url):
        self.url = url
        self.domain, self.path = self.parseUrl(url)

    def parseUrl(self, url):
        if url.startswith("http://"):
            url = url[len("http://"):]
        elif url.startswith("https://"):
            url = url[len("https://"):]
        parts = url.split("/", 1)
        domain = parts[0]
        path = '/' + parts[1] if len(parts) > 1 else '/'
        return domain, path

    def retrieveWebContent(self, domain=None, path=None, redirect_count=0):
        # if domain and path are None, it means it's the first call, so use self.domain and self.path
        if domain is None and path is None:
            domain, path = self.domain, self.path

        if redirect_count > 10:
            print("Too many redirects.")
            return None
        
        context = ssl.create_default_context()
        try:
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as conn:
                    request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\n\r\n"
                    conn.send(request.encode('utf-8'))

                    response = ""
                    while '\r\n\r\n' not in response:
                        chunk = conn.recv(1024).decode('utf-8', 'ignore')
                        if not chunk:
                            break
                        response += chunk

                status_match = re.search(r'\s(\d{3})\s', response)
                if not status_match:
                    print("Invalid response received")
                    print("Response Received:", response)
                    return None

                status_code = int(status_match.group(1))
                if status_code not in self.REDIRECT_STATUS_CODES:
                    return response

                location_match = re.search(r'location: (.+)', response, re.IGNORECASE)
                if location_match:
                    new_url = location_match.group(1).strip()
                    new_domain, new_path = self.parseUrl(new_url)
                    return self.retrieveWebContent(new_domain, new_path, redirect_count + 1)
                else:
                    print("Location header not found for redirect.")
                    return None
        except socket.gaierror:
            print("Website does not exist.")
            return None
        except Exception as e:
            print(f"Connection error {domain}: {e}")
            return None
        
    def supportsHttp2(self):
        context = ssl.create_default_context()
        context.set_alpn_protocols(['h2', 'http/1.1'])
        try:
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.domain)
            conn.connect((self.domain, 443))
            return conn.selected_alpn_protocol() == 'h2'
        except Exception as e:
            print(f"Error connecting to {self.domain}: {e}")

    def printCookies(self, response):
        cookies = re.findall(r'Set-Cookie: (.*?)(?:\r\n|$)', response, re.IGNORECASE)
        print("2. List of Cookies:")
        if not cookies:
            print("No cookies found.")
            return
        for cookie in cookies:
            name = re.match(r'^([^=]*)', cookie).group(0)
            domain = re.search(r'domain=([^;]*)', cookie, re.IGNORECASE)
            expires = re.search(r'expires=([^;]*)', cookie, re.IGNORECASE)
            cookieDomain = domain and f", domain name: {domain.group(1)}" or ''
            expiresStr = expires and f", expires time: {expires.group(1)}" or ''
            print(f"cookie name: {name}{expiresStr}{cookieDomain}")

    def isPasswordProtected(self, response):
        statusCodes = re.findall(r'HTTP/1\.1 (4\d{2})', response)
        return any(400 <= int(code) < 500 for code in statusCodes)

    def run(self):
        print("website: " + self.url)
        if not self.domain:
            print("Please enter URL properly.")
            return
        response = self.retrieveWebContent()
        if response:
            print(f"1. Supports http2: {'yes' if self.supportsHttp2() else 'no'}")
            self.printCookies(response)
            print(f"3. Password-protected: {'yes' if self.isPasswordProtected(response) else 'no'}")
        else:
            print("Failed to get a response.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 SmartClient <url>")
        sys.exit(1)
    client = SmartClient(sys.argv[1])
    client.run()