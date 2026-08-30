from flask import Flask, render_template
import markdown
import frontmatter
import os
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/blog")
def blog():
    posts = []

    for filename in os.listdir("posts"):
        if filename.endswith(".md"):
            post = frontmatter.load(f"posts/{filename}")
            slug = filename.removesuffix(".md")

            posts.append({
                "title": post["title"],
                "date": post["date"],
                "description": post["description"],
                "slug": slug
            })

    return render_template("blog.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog/<slug>")
def post(slug):
    path = f"posts/{slug}.md"

    post = frontmatter.load(path)

    content = markdown.markdown(post.content)

    return render_template(
        "post.html",
        content=content,
        title=post["title"],
        date=post["date"],
        description=post["description"]
    )
    return render_template("post.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)