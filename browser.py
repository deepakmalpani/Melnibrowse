import tkinter
import sys
from url import DEFAULT_URL, URL, extract_scheme, load, show

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width= WIDTH,
            height = HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.HSTEP = 13
        self.VSTEP = 18
        
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
        
    def layout(self, parsed_html):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        display_list = []
        for c in parsed_html:
            if c == '\n':
                cursor_y += self.VSTEP
            else:
                display_list.append((cursor_x, cursor_y, c))
                cursor_x += self.HSTEP
            if cursor_x >= WIDTH - self.HSTEP:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP
        
        return display_list
    
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + self.VSTEP < self.scroll : 
                continue
            self.canvas.create_text(x, y - self.scroll, text = c)
            
    def load(self, parsed_html):
        self.display_list = self.layout(parsed_html)
        self.draw()

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