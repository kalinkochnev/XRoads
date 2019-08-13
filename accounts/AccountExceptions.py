

# when the tags are out of range of the possible ones
class OutOfBounds(BaseException):
    pass


# when all the tags for a given alias are taken
class NoAvailableTags(BaseException):
    pass


# when a given tag number is taken
class TagTaken(BaseException):
    pass
