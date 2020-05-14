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


def test_from_py_does_nothing_if_none_passed():
    """ If None is passed to the from_py function, nothing should happen """
    # Given
    result = ResearchResult(True)

    # When
    result.from_py(None)

    assert result is not None


def test_to_py_encodes_data_fields():
    """ to_py should encode the class in a python data structure """
    # Given
    result = ResearchResult(True)
    result.summary = "SUMMARY"
    result.document = "DOCUMENT"

    # When
    data = result.to_py()

    # Then
    assert data["date"] is not None
    assert data["summary"] == result.summary
    assert data["document"] == result.document
    assert data["nil"] == result.is_nil()
    assert len(data.keys()) == 4  # To verify nothing else was added
