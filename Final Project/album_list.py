albums={
        161738241634:'spotify:album:79dL7FLiJFOO0EoehUHQBv',
        229940573836:'spotify:album:3xybjP7r2VsWzwvDQipdM0',
        505251739193:'spotify:album:2S8AWAM0nxyFy66YnUfIs3',
        93371020870:'spotify:album:3RQQmkQEvNCY4prGKE6oc5',
        437941417587:'spotify:album:19bQiwEKhXUBJWY6oV3KZk',
        25658111517:'spotify:album:7ycBtnsMtyVbbwTfJwRjSP',
        780582565605:'spotify:album:6HXJjUKTpltXMGgVidh1bB',
        93438129722:'spotify:album:2VuZJsJBPLwg9BeQFQle8G',
        711443724015:'spotify:album:5uRdvUR7xCnHmUW8n64n9y',
        436649702944:'spotify:album:0zicd2mBV8HTzSubByj4vP',
        986120369808:'spotify:album:0ndGMh4twJNzPpr5XtHTR2',
        1054456854087:'spotify:album:7dAm8ShwJLFm9SaJ6Yc58O',
        986492286585:'spotify:album:0bUTHlWbkSQysoM3VsWldT',
        93055202956:'spotify:album:4VFG1DOuTeDMBjBLZT7hCK',
        230930298563:'spotify:album:6x9s2ObPdpATZgrwxsk9c0',
        986576107107:'spotify:album:0D9034elnnZF9AOWeVT6vN',
        24822134519:'spotify:album:6rsQnwaoJHxXJRCDBPkBRw',
        917873342037:'spotify:album:20r762YmB5HeofjMCiPMLv',
        230930167493:'spotify:album:6s84u2TUpR3wdUv4NgKA2j',
        505506084595:'spotify:album:2VBcztE58pBKjIDS5oEgFh'
        }

def get_album(id):
    if id not in albums:
        return False
    else:
        return albums[id]