Jinja is Awesome
Post
2023-4-14
{%raw%}
While making the server for this blog using Flask (a Python library for web servers), I learned about the Jinja templating engine and how powerful it is.

## What it is

In any file, you can type Jinja code, and pass the file through a Python script for the code to be run/rendered and turned into normal text. These files are called templates as they can be used to generate other similar files. The templating code has many features like loops, variables, if statements, and filters (which are very similar to functions).

You can find Jinja's documentation [here](https://jinja.palletsprojects.com/en/3.1.x/templates/)

Jinja tries to make its syntax similar to Python, which makes templates very readable. In your template, you can put Jinja statements in between {% and %}, and expressions in between {{ and }}.

For example, if I was working on a website and wanted to make a list of people's names:

    <ul>
    {% for item in ["Bob", "Jane", "Bill"] %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
    
Which, when rendered by a script, would become:

    <ul>
        <li>Bob</li>
        <li>Jane</li>
        <li>Bill</li>
    </ul>

This may not seem too useful, as it would just give the same output every time. To make it useful, Jinja allows you to pass in values to the template when you render it which makes it very useful.

This is great because it allows you to generate lots of files that are all based on your template. For example, if a company wants to store readable records of their employees, they could use Jinja to generate simple paragraphs about each employee:

    Name: {{employee.name}}
        Years worked: {{employee.years_worked}}
        Work done:    {{employee.work_done}}

This template could be rendered from a complicated JSON file:

    from jinja2 import Template
    from json import loads
    
    # create the template
    template = Template(
        """Name: {{employee.name}}
            Years worked: {{employee.years_worked}}
            Work done:    {{employee.work_done}}"""
        )

    # get the data to be rendered
    with open("company.json", "r") as f:
        employees = loads(f.read())["employees"]

    # render the template for each employee
    records = []
    for employee in employees:
        records.append(
            template.render(employee=employee)
        )

    # display the result
    print("\n".join(records))

Which would make the nice and readable result:

    Name: John
            Years worked: 7
            Work done:    A lot
    Name: Bill
            Years worked: 5
            Work done:    A bit
    Name: Steve
            Years worked: 1
            Work done:    Not much

## How I use it

On the left sidebar of my site, there is a list of posts that is rendered with Jinja. To create this list I have a `ul` in my HTML template which will be populated with links to each post passed in by a posts variable:

__templates/index.html__

    All Posts:
    <ul>
        {% for post in posts|reverse %}
            <li>
                <a href="{{ url_for('post', post_id=post.id) }}">
                {{ post.title }}
                </a>
            </li>
        {% endfor %}
    </ul>

(`reverse` is a filter that will reverse the order of posts and `url_for` will generate the url for the post) 
This code in the Python script is used to render the file:

__main.py__

    @app.route('/')
    def home():
        return render_template("index.html", posts=get_posts())

This will result in a nice list of the posts from newest to oldest:
![List of all posts]({%endraw%}{{ url_for('static', filename='all_posts_list.png') }}{%raw%} "List of all posts")

Or this HTML:

    <ul>
        <li><a href="/post/1">Jinja is Awesome</a></li>           
        <li><a href="/post/0">A Blog Post About This Blog</a></li>
    </ul>

And all I had to do in the template was design how each item should look and pass it a generated list of posts.

## Why it's great (for websites)

When you generate most of the page on the server you can avoid using Javascript to make extra API calls to figure out what to put on the page. This will result in faster pages and can reduce the likelihood of bugs happening while the user is browsing the site. It also results in easy to edit scripts as templates have very little logic compared to fetching data from the server, making new elements, and putting them in the right place that you might have to do with extra Javascript.

## Conclusion

Jinja is a great tool for server-side rendering, but can also be used for many other things. It results in fast, easily editable pages, and a connection between the backend code and the generated HTML.

This post was just meant to be a simple introduction to what Jinja is, but there is much more to it. If you would like to learn more I would recommend learning it alongside Flask, as it has Jinja built-in.
{%endraw%}
