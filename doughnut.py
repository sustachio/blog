#######################################################
# https://github.com/sustachio/doughnut-text-formater #
#######################################################

from math import sqrt, pi, ceil
from re import sub
from html.parser import HTMLParser

CHARECTER_WIDTH_TO_HEIGHT_RAIO = 2
HOLE_TO_FULL_RATIO = 2.64
PI = pi

# given an area find width and height of doughnut and doughnut hole
def calculate_sizes(area, extra_size):
    # https://www.desmos.com/calculator/8zn0ov3d73
    x_1 = sqrt(area/(PI*CHARECTER_WIDTH_TO_HEIGHT_RAIO*(HOLE_TO_FULL_RATIO**2-1)))+extra_size
    y_1 = x_1*CHARECTER_WIDTH_TO_HEIGHT_RAIO

    x_2 = x_1*HOLE_TO_FULL_RATIO
    y_2 = y_1*HOLE_TO_FULL_RATIO
    
    # find innaccuarcy:
    #new_area = PI*x_2*y_2 - PI*x_1*y_1
    #print("Found circle with innacuracy of:", new_area-area)
    
    # I got the x and y mixed up
    return(y_1, x_1, y_2, x_2)


def generate_doughnut(text, extra_size=0):
    # remove whitespaces (except for space)
    text = sub("[^\\S ]+", "", text)
    
    x_1, y_1, x_2, y_2 = calculate_sizes(len(text), extra_size)

    # dont run on an empty doughnut
    if x_2<=0 or y_2<=0 or x_1<=0 or y_1<=0: return ""

    char_on = 0
    result = ""
    
    for y in range(ceil(2*y_2)+1):
        y = y-(y_2) # center on (0,0)
        for x in range(ceil(2*x_2)+1):
            x = x-(x_2)  # center on (0,0)        
            
            # in doughnut, not in hole
            if ((x**2)/((x_2)**2) + (y**2)/((y_2)**2) <= 1) and not \
               ((x**2)/((x_1)**2) + (y**2)/((y_1)**2) <= 1) and \
               char_on<len(text):
                result += text[char_on]
                char_on += 1
            else:
                result += " "

        
        result += "\n"

    # increase the size of the doughnut until it has all charecters
    if (len(text)-char_on > 0):
        return generate_doughnut(text, extra_size+.01)

    return result

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)

        self.parsed = []

    # create html from self.parsed
    def regenerate_html(self):
        result = ""
        for item in self.parsed:
            if item[0] == "start_tag":
                result += f"<{item[1]} {' '.join([attr[0]+'='+attr[1] for attr in item[2] if attr[1]])}>"
            elif item[0] == "end_tag":
                result += f"</{item[1]}>"
            elif item[0] == "data":
                result += generate_doughnut(item[1].strip())
            elif item[0] == "ref":
                result += item[1]
        return result
    
    def handle_starttag(self, tag, attrs):
        self.parsed.append(("start_tag", tag, attrs))

    def handle_endtag(self, tag):
        self.parsed.append(("end_tag", tag))

    def handle_data(self, data):
        self.parsed.append(("data", data))

    def handle_entityref(self, name):
        self.parsed.append(("ref", "&"+name+";"))

    def handle_charref(self, name):
        self.parsed.append(("ref", self.handle_entityref("&#"+name+";")))

def generate_html(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.regenerate_html()