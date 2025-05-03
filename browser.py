import tkinter
import sys
from url import DEFAULT_URL, URL, extract_scheme, load, show

WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width= WIDTH,
            height = HEIGHT
        )
        self.canvas.pack()
        
    def load(self, url):
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text = "Hi!")
        

# if __name__ == "__main__":
#     Browser().load("test")
#     tkinter.mainloop()
if __name__ == "__main__":
    
    view_source = False
    
    if len(sys.argv) == 1:
        scheme, url = extract_scheme(DEFAULT_URL)
    else:
        scheme, url = extract_scheme(sys.argv[1])
        if scheme == "view-source":
            scheme, url = extract_scheme(url)
            print(scheme, url)
            view_source = True
            
    body = load(URL(url, scheme))
    if not view_source:
        parsed_html = show(body)
        print(parsed_html)
    else:
        print(body)