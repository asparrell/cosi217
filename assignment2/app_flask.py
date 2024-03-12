"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template

import spacy_process
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entities.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(80), unique=False, nullable=False)
    term = db.Column(db.String(80), unique=False, nullable=False)
    head = db.Column(db.String(80), unique=False, nullable=False)
    type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "Relation from %r to %r of type %r" % (self.head, self.term, self.type)

# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        method = request.form["result-type"]
        doc = spacy_process.SpacyDocument(text)
        deps = doc.get_dependencies()
        entities = doc.get_entities()
        markup = doc.get_entities_with_markup()
        dependencies = {}
        for dependency in deps:
            dependencies[dependency[0]] = {"relation": dependency[1], "head": dependency[2]}
        for entity in entities:
            name = entity[3]
            for word in name.split():
                relation = Relation(entity=name, term=word, head=dependencies[word]["head"],
                                    type=dependencies[word]["relation"])
                db.session.add(relation)


        if method == "result":
            title = "Entities and Dependencies"
            foreword = "<p>Original text:</p><p><i>" + text + "</i></p><p>Processing results:</p>"
            markup_paragraphed = '<p><b>Entities:</b><p>'
            for line in markup.split('\n'):
                if line.strip() == '':
                    markup_paragraphed += '</p>\n'
                else:
                    markup_paragraphed += line
            markup_paragraphed += "<br><br><p><b>Entity relations:</b></p><table><tr><th>Word</th><th style='color:#6b6bc7'>Relation</th><th>Head</th></tr>"
            for rel in db.session.execute(db.select(Relation)).scalars():
                dep_str = "<tr><td>" + rel.term + "</td><td style='color:#6b6bc7'>" + rel.type + "</td><td>" + rel.head + "</td></tr>"
                markup_paragraphed += dep_str
            markup_paragraphed += "</table>"


        else:
            title = "Database View"
            foreword = "Entities and their heads data:"
            markup_paragraphed = "<table><tr><th>Entity</th><th style='color:#6b6bc7'>Term</th><th>Relation</th><th style='color:#6b6bc7'>Head</th></tr>"
            for rel in db.session.execute(db.select(Relation)).scalars():
                dep_str = ("<tr><td>" + rel.entity + "</td><td style='color:#6b6bc7'>" + rel.term +
                           "</td><td>" + rel.type + "</td><td style='color:#6b6bc7'>" + rel.head +
                           "</td></tr>")
                markup_paragraphed += dep_str
            markup_paragraphed += "</table>"
        return render_template('result.html', markup=markup_paragraphed, foreword=foreword, title=title)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
