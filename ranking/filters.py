def does_title_exist(rankingObject):
    title = rankingObject.title
    author = rankingObject.author

    if Ranking.objects.filter(author=author, title=title):
        raise Exception("Ranking with this title already exists!")


