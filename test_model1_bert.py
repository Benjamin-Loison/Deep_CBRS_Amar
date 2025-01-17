import pandas as pd
import numpy as np
import tensorflow as tf
from utilities.utils import (
    read_bert_embeddings,
    read_ratings,
    matching_bert_emb_id,
    top_scores,
)

user_embeddings, item_embeddings = read_bert_embeddings(
    "embeddings/UserProfiles_lastLayer.json", "embeddings/ITEM_embeddingslastlayer.json"
)
user, item, rating = read_ratings("datasets/dbbook/test2id.tsv")
X, y, dim_embeddings = matching_bert_emb_id(
    user, item, rating, user_embeddings, item_embeddings
)

model = tf.keras.models.load_model("results/model.h5")
score = model.predict([X[:, 0], X[:, 1]])

print("Computing predictions...")
score = score.reshape(1, -1)[0, :]
predictions = pd.DataFrame()
predictions["users"] = np.array(user) + 1
predictions["items"] = np.array(item) + 1
predictions["scores"] = score

predictions = predictions.sort_values(by=["users", "scores"], ascending=[True, False])

top_5_scores = top_scores(predictions, 5)
top_5_scores.to_csv(
    "predictions/top_5/predictions_1.tsv", sep="\t", header=False, index=False
)
print("Writing top 5 scores succeeed")

top_10_scores = top_scores(predictions, 10)
top_10_scores.to_csv(
    "predictions/top_10/predictions_1.tsv", sep="\t", header=False, index=False
)
print("Writing top 10 scores succeeed")


"""
# evaluate loaded model on test data
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy',tf.keras.metrics.Precision(),tf.keras.metrics.Recall()])
score = model.evaluate([X[:,0],X[:,1]], y, verbose=0)
print("%s: %.2f%%" % ('accuracy', score[1]*100))
print("%s: %.2f%%" % ('precision', score[2]*100))
print("%s: %.2f%%" % ('recall', score[3]*100))
f1_val = 2*(score[2]*score[3])/(score[2]+score[3])
print("%s: %.2f%%" % ('f1_score', f1_val*100))
"""
