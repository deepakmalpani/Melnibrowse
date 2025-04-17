import socket
import sys
import ssl

class URL:
    def __init__(self, url):
        
        self.scheme, url = url.split("://", 1) # split the scheme from the rest of the URL
        assert self.scheme in ["http", "https"] # the browser only supports http
        
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443   # Encryptyed HTTP connections usually use port 443 instead of port 80

        if "/" not in url:
            url = url + "/" # add a trailing slash if there is no path
        
        self.host, url = url.split("/", 1) # split the host from the rest of the URL
        
        if ":" in self.host:
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
    body = url.request()
    show(body)

if __name__ == "__main__":
    load(URL(sys.argv[1]))
        