albums={
        574107989528:'spotify:album:7ycBtnsMtyVbbwTfJwRjSP', 
        300621870712:'spotify:album:6rsQnwaoJHxXJRCDBPkBRw',
        711696889559:'spotify:album:3kEtdS2pH6hKcMU9Wioob1',
        505538524678:'spotify:album:0D9034elnnZF9AOWeVT6vN',
        712233825974:'spotify:album:4QElAwQufg6wCeyvpafqwA',
        93758600709:'spotify:album:6HXJjUKTpltXMGgVidh1bB',
        231919105544:'spotify:album:1UcS2nqUhxrZjrBZ3tHk2N',
        712418571960:'spotify:album:19bQiwEKhXUBJWY6oV3KZk',
        918862149344:'spotify:album:2VuZJsJBPLwg9BeQFQle8G',
        25039189524:'spotify:album:2k8KgmDp9oHrmu0MIj4XDE',
        644017731235:'spotify:album:7dAm8ShwJLFm9SaJ6Yc58O'
        }

def get_album(id):
    if id not in albums:
        return False
    else:
        return albums[id]