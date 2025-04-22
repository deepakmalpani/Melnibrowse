import socket
import sys
import ssl

DEFAULT_URL = 'file://C:/Users/deepa/Desktop/test.txt'

class URL:
    def __init__(self, url):
        self.file_path = None
        self.inline_html = None
        
        if "://" in url:
            self.scheme, url = url.split("://", 1) # split the scheme from the rest of the URL
        elif ":" in url:
            self.scheme, url = url.split(":", 1) # split the scheme when the url doesn't contain :// for eg: data:text/html
        
        assert self.scheme in ["http", "https","file","data"] # the browser now supports http, https, file, data
        
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443   # Encryptyed HTTP connections usually use port 443 instead of port 80
        elif self.scheme == "file":
            self.file_path = url # extract the filepath in case of file scheme
        elif self.scheme == "data":
            if "," in url:
                document_type, self.inline_html = url.split(",", 1)
                print(document_type)   
                
        if "/" not in url:
            url = url + "/" # add a trailing slash if there is no path
        
        self.host, url = url.split("/", 1) # split the host from the rest of the URL
        
        if not self.file_path and ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        
        self.path = "/" + url
        
        self.request_headers = {
            "Host" : self.host,
            "Connection" : "close",
            "User-Agent" : "melnibrowse"
        }
    
    def add_headers(self,request, request_headers):
        for key, value in request_headers.items():
            request += "{}: {}\r\n".format(key, value)
        return request
    
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
            )
        
        s.connect((self.host, self.port))
        
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname= self.host)

        request = "GET {} HTTP/1.1\r\n".format(self.path) # we can now use http/1.1 instead of 1.0
        request = self.add_headers(request, self.request_headers)
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding = "utf8", newline="\r\n") #returns file like object containing every byte received from server and decodes it using utf8

        statusline = response.readline()  # first line in response is a status line
        version, status, explanation = statusline.split(" ",2) 

        response_headers = {}
        while True:
            line = response.readline() # after the status line, comes the headers
            if line == "\r\n":
                break
            header, value = line.split(":",1)
            response_headers[header.casefold()] = value.strip() # convert header key to lower case and strip whitespace from key

            assert "transfer-encoding" not in response_headers # these headers tell us, that the data is being sent in an unusual way, so making sure they are not present
            assert "content-encoding" not in response_headers

            content = response.read() # the usual way is to get the sent data, then, is everything after the headers
            s.close()
            
            return content
    
    def open_file(self):
        if self.file_path :
            with open(self.file_path, 'r') as file:
                content = file.read()
                print(content)
        
def show( body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    if url.scheme == "file":
        url.open_file()
        return
    
    if url.scheme == "data":
        show(url.inline_html)
        return
    
    body = url.request()
    show(body)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        load(URL(DEFAULT_URL))
    else:
        load(URL(sys.argv[1]))