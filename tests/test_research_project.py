""" Tests related to the ResearchProject class """

from gene.research import ResearchProject
from gene.research import ResearchTask


def test_gedcom_is_none_by_default():
    """ Gedcom is None by default """
    project = ResearchProject("")
    assert project.gedcom == "none"


def test_has_gedcom_is_false_for_none():
    """ If there is no associated gedcom, has_gedcom should return false """
    project = ResearchProject("")
    project.gedcom = "none"

    assert project.has_gedcom() is False


def test_filename_is_set():
    """ filename is set to parameter """
    filename = "foo/bar.test"
    project = ResearchProject(filename)

    assert project.filename == filename


def test_plans_is_set():
    """ The plans field is available """
    project = ResearchProject("")

    assert project.plans == []


def test_project_conversion_matches():
    """ Check that to/from conversion matches """
    project_data = {}
    project_data["gedcom"] = "foo"
    project_data["version"] = "1.0"
    project_data["plans"] = []

    project = ResearchProject("")
    project.from_py(project_data)
    assert project_data == project.to_py()


def test_unset_task_fields_are_defaulted():
    """ Check that when converting a task, any fields not set in py are defaulted """
    # Given
    task = ResearchTask()
    task_data = {}

    # When
    task.from_py(task_data)

    # Then
    assert task.title != ""
    assert task.status != ""
