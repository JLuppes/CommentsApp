from flask import Flask, render_template, request, redirect, url_for, flash
import html  # Python's built-in HTML escaping
import bleach  # Library for advanced sanitization

app = Flask(__name__)
app.secret_key = 'devkey'

# Store comments in memory (for demo purposes)
comments = []
comments_advanced = []


def sanitize_comment(text):
    """Allow only safe HTML tags"""
    # Define which HTML tags are allowed
    allowed_tags = ['p', 'br', 'strong', 'em',
                    'ul', 'ol', 'li', 'b', 'i', 'h1']

    # Clean the input - remove any tags not in our allowed list
    clean_text = bleach.clean(text, tags=allowed_tags, strip=True)
    return clean_text


@app.route('/comments')
def show_comments():
    """Display all comments"""
    return render_template('comments.html', comments=comments)


@app.route('/add', methods=['POST'])
def add_comment():
    """Add a new comment - THIS IS VULNERABLE!"""
    comment_text = request.form.get('comment_text', '').strip()
    if comment_text:
        # UNSAFE: Store raw user input without any sanitization
        comments.append(comment_text)
        flash('Comment added successfully!')
    else:
        flash('Please enter a comment.')
    return redirect(url_for('show_comments'))


@app.route('/')
def show_comments_advanced():
    return render_template('comments_advanced.html', comments=comments_advanced)


@app.route('/add_advanced', methods=['POST'])
def add_comment_advanced():
    comment_text = request.form.get('comment_text', '').strip()

    if comment_text:
        # SAFE: Sanitize before storing
        clean_comment = sanitize_comment(comment_text)
        comments_advanced.append(clean_comment)
        flash('Comment added with safe HTML!')
    else:
        flash('Please enter a comment.')
    return redirect(url_for('show_comments_advanced'))


if __name__ == '__main__':
    app.run(debug=True)