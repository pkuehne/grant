""" Tests related to the ResearchProject class """

from gene.research import ResearchProject


def test_gedcom_is_none_by_default():
    """ Gedcom is None by default """
    project = ResearchProject("")
    assert project.gedcom == "none"


def test_has_gedcom_is_false_for_none():
    """ If there is no associated gedcom, has_gedcom should return false """
    project = ResearchProject("")
    project.gedcom = "none"

    assert project.has_gedcom() is False


def test_conversion_matches():
    """ Check that to/from conversion matches """
    project_data = {}
    project_data["gedcom"] = "foo"
    project_data["version"] = "1.0"
    project_data["plans"] = []

    project = ResearchProject("")
    project.from_py(project_data)
    assert project_data == project.to_py()
