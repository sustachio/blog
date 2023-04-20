from random import randint, choice
from bs4 import BeautifulSoup

def get_identifiers(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")
    if not body:
        body = soup
    
    classes = set([
            class_ 
            for element in body.find_all(class_=True)
            for class_ in element["class"]
    ])

    ids = set([
            element["id"] 
            for element in body.find_all(id=True)
    ])

    tags = set([
            element.name 
            for element in body.find_all()
    ])

    return ((["body"] if soup.find("body") else []) +
            list(tags) +
            ["#"+id for id in ids] + 
            ["."+class_ for class_ in classes]
            )
    

PROPRETIES_RANGE = (2,4)

COLOR = ["black", "silver", "gray", "white", "maroon", "red", "purple", "fuchsia", "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua"]

properties = [
    {
        "name": "background-color",
        "arguments": [COLOR,]
    },
    {
        "name": "color",
        "arguments": [COLOR,]
    },
    # {
    #     "name": "float",
    #     "arguments": [["left", "right"]]
    # },
    {
        "name": "border",
        "arguments": [
            ["thin", "medium", "thick"],
            ["dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset"],
            COLOR
        ]
    },
    {
        "name": "display",
        "arguments": [["inline", "block", "inline-block", "table", "flex"]]
    }
]

def generate_css(html):
    identifiers = get_identifiers(html)
    
    result = ""

    # each rule
    for identifier in identifiers:
        result += identifier+" {\n"

        # each proprety
        for _ in range(randint(*PROPRETIES_RANGE)):
            proprety = choice(properties)

            #name: choice(argument) choice(argument);
            result += "\t{}: {};\n" \
                .format(
                    proprety["name"], 
                    " ".join([choice(argument) for argument in proprety["arguments"]])
                )

        result += "}\n\n"

    return result