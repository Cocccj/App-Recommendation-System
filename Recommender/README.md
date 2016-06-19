# Application Recommendation
Recommend top 5 apps for each app with Cosine Similarity and Collaborative Filtering.

Compute the cosine similarity between each app and each user(app download history).
Then compute the similarity between two apps by aggregating the cosine similarity values of app1 and all the users who downloaded both app1 and app2.

For each app, output the top 5 similar apps, and store the results in mongoDB.
