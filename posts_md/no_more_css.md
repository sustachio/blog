Never Write a Line of CSS Again
Project
4/20/23
Any time I have to do a frontent (website) project I always end up spending too much time writing CSS, which can often lead to me giving up on it. To solve this, I created [random-css](https://github.com/sustachio/random-css), a tool which writes quality css for you.

You can give it any HTML and it will spit out some css for you giving styles to all of your tags, classes, and ids. 

For example I could give it:

    <h1 id="title">Hello</h1>
    <p class="paragraph">World</p>

And I could get:

    p {
        background-color: teal;
        float: right;
    }

    h1 {
        border: thin double gray;
        border: thin double yellow;
    }

    #title {
        color: white;
        border: thin dotted silver;
        border: medium dotted lime;
    }

    .paragraph {
        float: left;
        border: thick double teal;
        display: block;
    }

Want to try it out? I built it into this website! Just add `?random_css=1` to the end of any url to get a page that a computer designed.

Here are some links to a few pages with random css:

- <a href="{{ url_for('home') }}">Home</a>
- <a href="{{ url_for('findme') }}">Find Me</a> (this is my favorite for the random css)
- <a href="{{ url_for('post', post_id='never-write-a-line-of-css-again') }}">This Post</a>

If you want to try it yourself (or modify it), I wrote instructions on how to use it on it's [github](https://github.com/sustachio/random-css).
