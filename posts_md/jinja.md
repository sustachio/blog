Jinja is Awesome
Post
4/14/23
{%raw%}
While making the server for this blog using Flask (a python library for web servers), I discovered the wonders of the Jinja templating engine.

## What it is

In an HTML file (or any other type of file) you can type Jinja code, which will be converted or rendered back into normal HTML through a python script. The code has many features like loops, variables, if statements, and filters (which are very similar to functions).

You can find Jinja's documentation [here](https://jinja.palletsprojects.com/en/3.1.x/templates/)

Jinja tries to make its syntax similar to python, which makes templates very readable. In your template (HTML where you type the code), you can put Jinja statements in between {% and %}, and expressions in between {{ and }}.

For example, if I wanted to make a `<ul>` with names from a list I could write:

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

This may not seem too useful, as it would just give the same output every time. This is where Jinja becomes very powerful. When you are rendering the code with your python script, you can pass parameters into it from the script.

This is great because it allows you to generate lots of similar files that are all based on your template. It can also allow for values that can change every time you, for example, load a webpage without any client-side rendering. This means no extra API calls or javascript.

## How I use it

I use Jinja in my blog to render the posts on the homepage and in the left sidebar. To create the left side bar I have this `<ul>` in my template:

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

(`reverse` is a filter that will reverse the order of posts and `url_for` will generate the url for the post) And this code in the python script:

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

If you've ever made a website you might be thinking "Why not do this with Javascript?" When you do it this way, and render the entire page on the server, you avoid making extra API calls to fetch things like the posts. This can save time and make the page load faster. Also in my opinion it is easier to make and edit the templates than to make a whole javascript script to do it.

It makes a near direct link between the server code and the HTML, which makes it extremely easy to change values server side while simultaneously changing them on the resulting page.

## Conclusion

Jinja is a great tool for rendering pages on the server, but can also be used for many other things. It results in fast, easily editable pages, and a connection between the code/database and HTML that is delivered to a user.

This post was just meant to be an extremely simple introduction to what Jinja is, but there is so much more to it. If you would like to learn more, there are hundreds of resources online. I would recommend learning it alongside Flask, as it has Jinja built-in.
{%endraw%}