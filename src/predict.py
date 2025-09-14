import numpy as np

def get_prediction(message, encoding_model, clf_model):
    print(f"{message}")

    test_embeddings = encoding_model.encode(message)

    if test_embeddings.ndim == 1:
        test_embeddings = np.expand_dims(test_embeddings, axis=0)

    pred_probs = clf_model.predict(test_embeddings)

    speakers = ["ben", "ayden", "vince", "max"]
    predicted_index = pred_probs.argmax()
    predicted_speaker = speakers[predicted_index]
    prediction = predicted_speaker

    print(f"Quote: '{message}'")
    print(f"Predicted speaker: {predicted_speaker}, Probabilities: {dict(zip(speakers, pred_probs))}\n")\

    return prediction