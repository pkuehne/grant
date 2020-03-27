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


def test_string_representation_includes_nil_for_nil_result():
    """ If a result is nil, it should include nil in the string """
    # Given
    result = ResearchResult()

    # When
    string = str(result)

    # Then
    assert "nil" in string


def test_string_representation_does_not_include_nil_for_success_result():
    """ If a result is not nil, it should not include nil in the string """
    # Given
    result = ResearchResult()
    result.nil = False

    # When
    string = str(result)

    # Then
    assert "nil" not in string


def test_string_representation_includes_summary_for_nil_results():
    """ If a result is nil, it should include the summary in the string """
    # Given
    result = ResearchResult()
    result.summary = "Summary"

    # When
    string = str(result)

    # Then
    assert result.summary in string


def test_string_representation_includes_summary_for_success_results():
    """ If a result is not nil, it should include the summary in the string """
    # Given
    result = ResearchResult()
    result.nil = False
    result.summary = "Summary"

    # When
    string = str(result)

    # Then
    assert result.summary in string
