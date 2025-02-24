class Paper:
    def __init__(self, t, l, a, y, i, v):
        self.pdf = None
        self.title = t
        self.link = l
        self.abstract = a
        self.year = y
        self.issue = i
        self.volume = v
        self.colleges = []

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def setAbstract(self, a):
        self.abstract = a

    def getAbstract(self):
        return self.abstract

    def getYear(self):
        return self.year

    def getIssue(self):
        return self.issue

    def getVolume(self):
        return self.volume

    def getColleges(self):
        return self.colleges

    def appendColleges(self, a):
        self.colleges.append(a)

    def setPDF(self, a):
        self.pdf = a

    def getPDF(self):
        return self.pdf

    def __str__(self):
        return str(self.title) + ", " + str(self.link) + ", " + str(self.abstract[:20]) + "..."
