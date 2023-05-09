# blog

This is the repo for my blog site. Now self-hosted at: [https://sethmueller.page](https://sethmueller.page)!

You can find all of the posts in `posts_md/`

## Want to use this for your own blog?

I would not recomend trying to use this as a lot of the features are specific to my blog but if you want to here's how:

You have to create the database by making the `database.db` file and running `make_tables` with the `db` object created in `main.py`

To make a new post you add a file in `posts_md` using this layout:

```
title
type
date
contents (markdown)
```