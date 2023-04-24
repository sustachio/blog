Never Write a Line of CSS Again
Project
4/24/23
Any time I have to do a project involving making a website, I always end up spending too much time writing CSS, which often leads to me giving up on it or just making bad choices. To solve this, I created [random-css](https://github.com/sustachio/random-css), a tool which writes quality CSS for you.

You can give it any HTML and it will spit out some css making styles for all of your tags, classes, and ids. If you dislike the styles it gives you, all you need to to is run it again and get a complety new page.

For example I could give it:

    <h1 id="title">Hello</h1>
    <p class="paragraph">World</p>

And I might get back:

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

You can easily customize what propreties it can or can't make by changing the `propreties` variable in the source code.

Want to try it out? I built it right into this website! Just add `?random_css=1` to the end of any url on this site to get a computer-designed webpage. Here's links to some pages with random css applied: (make sure to reload a few times and see how different each one is)

- <a href="{{ url_for('home', random_css=1) }}">Home</a>
- <a href="{{ url_for('find_me', random_css=1) }}">Find Me</a>
- <a href="{{ url_for('post', post_id='never-write-a-line-of-css-again', random_css=1) }}">This Post</a>

If you want to try it on your own code (or modify it), I wrote instructions on how to use it on its [github](https://github.com/sustachio/random-css).