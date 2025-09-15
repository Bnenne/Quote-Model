import spacy
import contextualSpellCheck
from spacytextblob.spacytextblob import SpacyTextBlob
import numpy as np

def get_prediction(message, encoding_model, clf_model):
    print(f"{message}")

    nlp = spacy.load("en_core_web_sm")
    contextualSpellCheck.add_to_pipe(nlp)
    nlp.add_pipe('spacytextblob')

    doc = nlp(message)
    spellchecked_quote = doc.text
    sentiment = [doc._.blob.polarity, doc._.blob.subjectivity]

    test_embeddings = encoding_model.encode(spellchecked_quote)

    sentence = np.append(test_embeddings, sentiment)

    sentence = np.array(sentence)

    if sentence.ndim == 1:
        sentence = np.expand_dims(sentence, axis=0)

    pred_probs = clf_model.predict(sentence)

    speakers = ["ben", "ayden", "vince", "max"]
    predicted_index = pred_probs.argmax()
    predicted_speaker = speakers[predicted_index]
    prediction = predicted_speaker

    print(f"Quote: '{message}'")
    print(f"Predicted speaker: {predicted_speaker}, Probabilities: {dict(zip(speakers, pred_probs))}\n")\

    return prediction