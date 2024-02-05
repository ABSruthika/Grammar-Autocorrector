from flask import Flask, render_template, request, jsonify
from spellchecker import SpellChecker

app = Flask(__name__)
spell = SpellChecker()

# Function to perform autocorrection
def perform_autocorrection(input_text):
    dict_of_autocorrect_words = {}
    for word in spell.unknown(input_text.split()):
        correction = spell.correction(word)
        dict_of_autocorrect_words[word] = correction

    autocorrected_words = [dict_of_autocorrect_words.get(word, word) for word in input_text.split()]
    autocorrected_words = [word for word in autocorrected_words if word is not None]
    autocorrected_text = ' '.join(autocorrected_words)
    return autocorrected_text

# Route for autocorrect suggestions
@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    input_text = request.form['text']
    autocorrected_text = perform_autocorrection(input_text)
    return jsonify({'autocorrected_text': autocorrected_text})

# Route for autocorrect suggestions and translation
@app.route('/autocorrect_translate', methods=['POST'])
def autocorrect_translate():
    input_text = request.form['text']
    autocorrected_text = perform_autocorrection(input_text)

    # # Translate the autocorrected text from Tamil to English
    # translator = Translator(to_lang="en", from_lang="ta")
    # translated_text = translator.translate(autocorrected_text)

    return jsonify({'autocorrected_text': autocorrected_text})

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
