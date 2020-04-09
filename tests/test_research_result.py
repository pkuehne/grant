""" Tests for the ResearchResult class """

from grant.research import ResearchResult


def test_date_is_defaulted():
    """ A date should be set when the object is constructed """
    # Given
    result = ResearchResult(False)

    # Then
    assert result.date is not None


def test_false_result_is_nil():
    """ Passing success as false, sets result to be nil """
    # Given
    result = ResearchResult(False)

    # When
    retval = result.is_nil()

    # Then
    assert retval is True


def test_true_result_is_not_nil():
    """ Passing success as false, sets result to be nil """
    # Given
    result = ResearchResult(True)

    # When
    retval = result.is_nil()

    # Then
    assert retval is False


def test_string_representation_includes_nil_for_nil_result():
    """ If a result is nil, it should include nil in the string """
    # Given
    result = ResearchResult(False)

    # When
    string = str(result)

    # Then
    assert "nil" in string


def test_string_representation_does_not_include_nil_for_success_result():
    """ If a result is not nil, it should not include nil in the string """
    # Given
    result = ResearchResult(True)

    # When
    string = str(result)

    # Then
    assert "nil" not in string


def test_string_representation_includes_summary_for_nil_results():
    """ If a result is nil, it should include the summary in the string """
    # Given
    result = ResearchResult(True)
    result.summary = "Summary"

    # When
    string = str(result)

    # Then
    assert result.summary in string


def test_string_representation_includes_summary_for_success_results():
    """ If a result is not nil, it should include the summary in the string """
    # Given
    result = ResearchResult(True)
    result.summary = "Summary"

    # When
    string = str(result)

    # Then
    assert result.summary in string
