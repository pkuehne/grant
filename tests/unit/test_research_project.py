""" Tests related to the ResearchProject class """

from grant.research import ResearchProject
from grant.research import ResearchPlan


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


def test_add_plan_creates_and_returns():
    """ add_plan() should return the newly created plan """
    # Given
    project = ResearchProject("")

    # When
    retval = project.add_plan()

    # Then
    assert len(project.plans) == 1
    assert retval is not None


def test_delete_plan_does_nothing_if_no_plans():
    """ delete_plan() does nothing if there are no plans """
    # Given
    project = ResearchProject("")

    # When
    project.delete_plan(1)

    # Then
    assert len(project.plans) == 0


def test_delete_plan_deletes_the_specified_plan():
    """ delete_plan() does nothing if there are no plans """
    # Given
    project = ResearchProject("")
    plan_one = ResearchPlan()
    plan_two = ResearchPlan()
    plan_three = ResearchPlan()

    project.plans.append(plan_one)
    project.plans.append(plan_two)
    project.plans.append(plan_three)

    # When
    project.delete_plan(1)

    # Then
    assert len(project.plans) == 2
    assert project.plans[0] == plan_one
    assert project.plans[1] == plan_three


def test_delete_plan_does_nothing_if_index_out_of_bounds():
    """ delete_plan() does nothing if the index is too large """
    # Given
    project = ResearchProject("")
    plan_one = ResearchPlan()
    plan_two = ResearchPlan()
    plan_three = ResearchPlan()

    project.plans.append(plan_one)
    project.plans.append(plan_two)
    project.plans.append(plan_three)

    # When
    project.delete_plan(5)

    # Then
    assert len(project.plans) == 3
