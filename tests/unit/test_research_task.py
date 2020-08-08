""" Tests for the ResearchTask class """

from grant.research import ResearchTask


def test_unset_fields_are_defaulted():
    """ Check that when converting a task, any fields not set in py are defaulted """
    # Given
    task = ResearchTask()
    task_data = {}

    # When
    task.from_py(task_data)

    # Then
    assert task.source == ""
    assert task.description == ""


def test_default_task_is_open():
    """ Check that by default there is no result for a task """
    # Given
    task = ResearchTask()

    # When
    result = task.is_open()

    # Then
    assert result is True


def test_string_repr_includes_description():
    """ The str() representation should include the description """
    # Given
    task = ResearchTask()
    task.description = "DESCRIPTION"

    # When
    string = str(task)

    # Then
    assert task.description in string


def test_to_py_sets_fields():
    """ The to_py() function should create a python data structure of the class fields """
    # Given
    task = ResearchTask()
    task.source = "SOURCE"
    task.source_link = 123
    task.description = "DESCRIPTION"

    # When
    data = task.to_py()

    # Then
    assert data["description"] == task.description
    assert data["source"] == task.source
    assert data["source_link"] == task.source_link
    assert data["result"] == task.result
    assert len(data.keys()) == 4  # To verify nothing else was added
