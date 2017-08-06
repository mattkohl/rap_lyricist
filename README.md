# Rap Lyricist

Rap Lyricist was an experiment to crowd-source evaluation of a Markov language model.

The model was seeded with extracts from [The Right Rhymes](https://www.therightrhymes.com) and loaded into a MongoDB collection, which was leveraged by a Flask app with some basic JavaScript in the front end.  

Whenever a new user would come to the site, the model would generate a new lyric and give the user an opportunity to feedback.

![screen shot](/app/static/img/rap_lyricist_screen_shot_1.png)

That feedback was then applied to the lyric's entry in the database, and used to update a chart in the UI:

![screen shot](/app/static/img/rap_lyricist_screen_shot_2.png)

If the feedback was `GOOD`, the app would publish the lyric on Twitter as [@rap_lyricist](https://twitter.com/rap_lyricist).