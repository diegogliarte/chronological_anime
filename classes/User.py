class User():
    def __init__(self, input):
        self.url = None
        self.name = None
        self.days = None
        self.mean_score = None
        self.animes = {"Watching" : [], "Completed" : [], "On-Hold" : [], "Droppped" : [], "Plan to Watch" : []}
        self.favorites = {"Anime" : [], "Characters" : [], "People" : []}
        self.gender = None
        self.birthday = None
        self.location = None
        self.joined = None
        self.forum_posts = None
        self.reviews = None
        self.recommendations = None
        self.blog_posts = None
        self.clubs = None
        self.friends = []

        self.set_parameters(input)

    def set_parameters(self, input):
        pass


