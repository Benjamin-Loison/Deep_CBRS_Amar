import pandas as pd
import numpy as np
import tensorflow as tf
from utilities.utils import (
    read_ratings,
    read_graph_embeddings,
    read_bert_embedding,
    top_scores,
    matching_Bert_Graph,
)

graph_embeddings = read_graph_embeddings("embeddings/TRANSDembedding_768.json")
user_bert_embeddings = read_bert_embedding(
    "embeddings/elmo_user_embeddings_nostopw_1024.json"
)
item_bert_embeddings = read_bert_embedding(
    "embeddings/elmo_embeddings_nostopw_1024.json"
)

user, item, rating = read_ratings("datasets/movielens/test2id.tsv")
X_graph, X_bert, dim_graph, dim_bert, y = matching_Bert_Graph(
    user, item, rating, graph_embeddings, user_bert_embeddings, item_bert_embeddings
)

model = tf.keras.models.load_model("results/model.h5")
score = model.predict([X_graph[:, 0], X_graph[:, 1], X_bert[:, 0], X_bert[:, 1]])

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
