import math

class Helper(object):

    @classmethod
    def cosine_similarity(cls, list1, list2):
        match_count = cls.__count_match(list1, list2)
        return float(match_count) / math.sqrt(len(list1) * len(list2))

    @classmethod
    def __count_match(cls, list1, list2):
        count = 0
        for elem in list1:
            if elem in list2:
                count += 1
        return count

