""" Tests for the ResearchResult class """

from grant.research import ResearchResult


def test_default_result_is_nil():
    """ Check that when converting a task, any fields not set in py are defaulted """
    # Given
    result = ResearchResult()

    # When
    retval = result.is_nil()

    # Then
    assert retval is True
