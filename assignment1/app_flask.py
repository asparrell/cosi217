"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template

import spacy_process

app = Flask(__name__)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        method = request.form["parse-type"]
        doc = spacy_process.SpacyDocument(text)
        if method == "ner":
            title = "SpaCy Entity Parsing"
            foreword = "Processing results:"
            markup = doc.get_entities_with_markup()
            markup_paragraphed = ''
            for line in markup.split('\n'):
                if line.strip() == '':
                    markup_paragraphed += '<p/>\n'
                else:
                    markup_paragraphed += line
        else:
            title = "SpaCy Dependency Parsing"
            foreword = "<p>Original text:</p><p><i>" + text + "</i></p><p>Processing results:</p>"
            markup = doc.get_dependencies()
            markup_paragraphed = "<table><tr><th>Word</th><th style='color:#6b6bc7'>Relation</th><th>Head</th></tr>"
            for dependency in markup:
                dep_str = "<tr><td>" + dependency[0] + "</td><td style='color:#6b6bc7'>" + dependency[1] + "</td><td>" + dependency[2] + "</td></tr>"
                markup_paragraphed += dep_str
            markup_paragraphed += "</table>"
        return render_template('result.html', markup=markup_paragraphed, foreword=foreword, title=title)


if __name__ == '__main__':
    app.run(debug=True)
