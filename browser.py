import tkinter
import sys
from url import DEFAULT_URL, URL, extract_scheme, load, show

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.height = HEIGHT
        self.width = WIDTH
        self.canvas = tkinter.Canvas(
            self.window,
            width= self.width,
            height = self.height,
            highlightthickness = 0
        )       
        self.canvas.pack(fill = tkinter.BOTH, expand= True)
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.handle_mwheel)
        self.canvas.bind("<Configure>", self.handle_resize)
        self.HSTEP = 13
        self.VSTEP = 18
        self.parsed_html = None
        
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
        
    def scrollup(self, e):
        if self.scroll - SCROLL_STEP > 0 :
            self.scroll -= SCROLL_STEP
            self.draw()
            
    def handle_mwheel(self, e):
        if self.scroll - e.delta > 0: 
            self.scroll += -1 * e.delta
            self.draw()
            
    def handle_resize(self, e):
        self.canvas.config(width= e.width, height= e.height)
        self.height = e.height
        self.width = e.width
        self.load(self.parsed_html)
        
    def layout(self, parsed_html):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        display_list = []
        for c in parsed_html:
            if c == '\n':
                cursor_y += self.VSTEP
            else:
                display_list.append((cursor_x, cursor_y, c))
                cursor_x += self.HSTEP
            if cursor_x >= self.width - self.HSTEP:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP
        
        return display_list
    
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.height:
                continue
            if y + self.VSTEP < self.scroll : 
                continue
            self.canvas.create_text(x, y - self.scroll, text = c)
            
    def load(self, parsed_html):
        self.parsed_html = parsed_html
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