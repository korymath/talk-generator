from flask import Flask
from flask_sslify import SSLify
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


# App config.
DEBUG = True
app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    talk_topic = TextField('Topic: ', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print('Errors: {}'.format(form.errors))

    if request.method == 'POST':
        talk_topic = request.form['talk_topic']
        print('Input talk topic: {}'.format(talk_topic))

        if form.validate():
            # Save the comment here.
            flash('Generating a talk on: ' + talk_topic)
        else:
            flash('All the form fields are required. ')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()