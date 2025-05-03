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
        
    def load(self, parsed_html):
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text = "Hi!")
        
        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in parsed_html:
            self.canvas.create_text(cursor_x, cursor_y, text = c)
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

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
            view_source = True
            
    body = load(URL(url, scheme))
    
    if not view_source:
        parsed_html = show(body)
        Browser().load(parsed_html)
        tkinter.mainloop()
        print(parsed_html)
    else:
        print(body)