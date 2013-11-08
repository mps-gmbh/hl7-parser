import doctest
import hl7parser.hl7


def additional_tests():
    return doctest.DocTestSuite(hl7parser.hl7)
