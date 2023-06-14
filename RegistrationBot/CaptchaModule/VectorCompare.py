import math

class VectorCompare:

      @staticmethod
      def magnitude(concordance) -> float:
        """
        :return: length of the vector
        """
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

      @staticmethod
      def relation(concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
          if word in concordance2:
            topvalue += count * concordance2[word]
        return topvalue / (VectorCompare.magnitude(concordance1) * VectorCompare.magnitude(concordance2))
