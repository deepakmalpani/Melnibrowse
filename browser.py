import socket
import sys

class URL:
    def __init__(self, url): 
        self.scheme, url = url.split("://", 1) # split the scheme from the rest of the URL
        assert self.scheme == "http" # the browser only supports http

        if "/" not in url:
            url = url + "/" # add a trailing slash if there is no path
        
        self.host, url = url.split("/", 1) # split the host from the rest of the URL
        self.path = "/" + url

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
            )
    
        s.connect((self.host, 80))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
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
        