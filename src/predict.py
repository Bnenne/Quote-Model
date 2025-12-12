from textblob import TextBlob
import numpy as np

def get_prediction(message, encoding_model, clf_model):
    print(f"{message}")

    # Spell checking + sentiment via TextBlob
    blob = TextBlob(message)
    spellchecked_quote = str(blob.correct())  # corrected text
    sentiment = [blob.sentiment.polarity, blob.sentiment.subjectivity]

    # Embeddings
    embeddings = encoding_model.encode(spellchecked_quote)

    # Combine embeddings + sentiment
    sentence = np.append(embeddings, sentiment)
    sentence = np.array(sentence)

    if sentence.ndim == 1:
        sentence = np.expand_dims(sentence, axis=0)

    pred_probs = clf_model.predict(sentence)

    speakers = ["ben", "ayden", "vince", "max"]
    predicted_index = pred_probs.argmax()
    predicted_speaker = speakers[predicted_index]

    print(
        f"Quote: '{message}'\n"
        f"Spellchecked: '{spellchecked_quote}'\n"
        f"Predicted speaker: {predicted_speaker}, "
        f"Probabilities: {dict(zip(speakers, pred_probs[0]))}\n"
    )

    return predicted_speaker
