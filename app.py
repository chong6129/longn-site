from abc import ABC, abstractmethod
from flask import Flask, render_template
import markdown
import frontmatter
import os

app = Flask(__name__)


class posts(ABC):
    @abstractmethod
    def get_posts(self):
        """Return a list of post metadata dictionaries."""
        raise NotImplementedError

    @abstractmethod
    def get_post(self, slug):
        """Return a single post dictionary with content rendered to HTML."""
        raise NotImplementedError


class MarkdownPosts(posts):
    def __init__(self, directory="posts"):
        self.directory = directory

    def get_posts(self):
        posts = []

        for filename in sorted(os.listdir(self.directory)):
            if filename.endswith(".md"):
                path = os.path.join(self.directory, filename)
                post = frontmatter.load(path)
                slug = filename.removesuffix(".md")

                posts.append({
                    "title": post["title"],
                    "date": post["date"],
                    "description": post["description"],
                    "slug": slug,
                })

        posts.sort(key=lambda post: post["date"], reverse=True)
        return posts

    def get_post(self, slug):
        path = os.path.join(self.directory, f"{slug}.md")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Post not found: {slug}")

        post = frontmatter.load(path)
        return {
            "title": post["title"],
            "date": post["date"],
            "description": post["description"],
            "content": markdown.markdown(post.content),
            "slug": slug,
        }


post_store = MarkdownPosts()

def get_posts():
    return post_store.get_posts()

@app.route("/")
def home():
    posts = get_posts()

    return render_template("index.html", posts=posts)

@app.route("/blog")
def blog():
    posts = get_posts()

    return render_template("blog.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog/<slug>")
def post(slug):
    post = post_store.get_post(slug)

    return render_template(
        "post.html",
        content=post["content"],
        title=post["title"],
        date=post["date"],
        description=post["description"]
    )

@app.route("/archive")
def archive():
    posts = get_posts()
  
    return render_template("archive.html", posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

