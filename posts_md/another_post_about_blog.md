Another Blog Post About This Blog (updates!)
Post
2025-6-27
Despite not posting here too much, I have had a lot of fun adding little things to the blog over time, so I wanted to document some of them here. This post will continue to be updated if I add new things.

## Fun pages

 - <https://sethmueller.page/spm> - Strokes per minute counter for telling the rate a rowing boat is stroking. This was written during a weekend long regatta. (Only page on this site that uses javascript!)
 - <https://sethmueller.page/?random_css> - Randomizes the css every time you reload, `?random_css` can be added to any page. ([Post](https://sethmueller.page/post/never-write-a-line-of-css-again))
 - <https://sethmueller.page/?doughnut> - Puts all text into doughnuts, `?doughnut` can be added to any page. 
 - <https://sethmueller.page/?doughnut&random_css> - Combination of the last two ¯\\_(ツ)_/¯

## Comments

One of my favorite things I've added is comments. I was actually also working on adding an ability to reply to others' comments but it has been stalled for a few months now. Every time a comment is posted I get a notification from a Discord bot that is running on the same Raspberry Pi hosting this blog. It gives me the option to remove the comment if it is from a bot (there are more of these than you'd think). I also have some very basic moderation commands built into the bot being list (lists all comments), delete \[id] (hides comment), and undelete \[id] (unhides comment). Each comment's id can be accessed from the HTML id on the element so they are easy to find.

All of the comments are stored in an sqlite database.

Below are some images demonstrating the new comments and discord bot (these are from the development bot which is identical but for the development server):

<div class="picture-grid">
    <div>
        <img src="{{ url_for('static', filename='another_post_about_blog/messages.jpg') }}" />
        <i>Messages received upon comment</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='another_post_about_blog/comments.png') }}" />
        <i>Comment section</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='another_post_about_blog/commands.jpg') }}" />
        <i>Commands for the discord bot</i>
    </div>
</div>

## Holidays

The site was stuck saying Happy Holidays! with some color additions for a few months, but I felt bad about simply removing it, so I added holiday homepages to the site which will be rendered on the holidays. Right now there is only Christmas, Halloween, Fourth of July, New Years, and Valentine's Day. The text in "Welcome to my blog!" alternates in color which is just done by having each letter in a `span` and then separate colors for each even and odd element in CSS (different colors depending on the class, normally `holiday-none` which has no CSS defined for it).

<img src="{{ url_for('static', filename='another_post_about_blog/holidays.png') }}" alt="Five holiday texts" />
<i>Flavor headers for holidays</i>

## Other new things

Visitor counter! This has been around a while but was not included in the original post. This doesn't actually count individual visitors but instead page visits. It simply displays images of each digit individually, I have an image for each number 0-9.

New pages:

 - [Find Me page](https://sethmueller.page/findme) - Contacts
 - [Portfolio page](https://sethmueller.page/portfolio) - This is very outdated and in dire need of a do-over
 - [Projects page](https://sethmueller.page/projects) - Just the normal home page but only filters to projects
