import spacy
import contextualSpellCheck
from spacytextblob.spacytextblob import SpacyTextBlob
import numpy as np

def get_prediction(message, encoding_model, clf_model):
    print(f"{message}")

    # Loading spacy model
    nlp = spacy.load("en_core_web_sm")
    # Adding packages to pipeline
    contextualSpellCheck.add_to_pipe(nlp)
    nlp.add_pipe('spacytextblob')

    # Spell checking and getting sentiment for the message
    doc = nlp(message)
    spellchecked_quote = doc.text
    sentiment = [doc._.blob.polarity, doc._.blob.subjectivity]

    # Getting embeddings
    embeddings = encoding_model.encode(spellchecked_quote)

    # Combing embeddings into a numpy array with message sentiment
    sentence = np.append(embeddings, sentiment)
    sentence = np.array(sentence)

    # Checking if the array is 2-dimensional
    if sentence.ndim == 1:
        sentence = np.expand_dims(sentence, axis=0)

    # Running data through the model
    pred_probs = clf_model.predict(sentence)

    # Getting data from the model
    speakers = ["ben", "ayden", "vince", "max"]
    predicted_index = pred_probs.argmax()
    predicted_speaker = speakers[predicted_index]
    prediction = predicted_speaker

    print(f"Quote: '{message}'")
    print(f"Predicted speaker: {predicted_speaker}, Probabilities: {dict(zip(speakers, pred_probs))}\n")\

    return prediction