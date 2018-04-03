from flask import Flask, render_template, flash, session, redirect, url_for
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField


DEBUG = True
SECRET_KEY = 'secret'

# keys for localhost. Change as appropriate.

app = Flask(__name__)
app.config.from_object(__name__)


class CommentForm(FlaskForm):

    comment = TextAreaField("Comment", validators=[DataRequired()])


@app.route("/")
def testform(form=None):
    if form is None:
        form = CommentForm()
    comments = session.get("comments", [])
    return render_template("testform.html",
                           comments=comments,
                           form=form)


@app.route("/add/", methods=("POST"))
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comments = session.pop('comments', [])
        comments.append(form.comment.data)
        session['comments'] = comments
        flash("You have added a new comment")
        return redirect(url_for("testform"))
    return testform(form)


if __name__ == "__main__":
    app.run()
