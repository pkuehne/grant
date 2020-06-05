""" Workflow test for the gedcom linking functionality """


def test_gedcom_ancestor_completion(window_driver, qtbot, tmpdir):
    """
    Test Schedule:
    * Create Main Window
    * Create new project
    * Link gedcom file
    * Add a plan
    * Autocomplete ancestor
    * Unlink gedcom file
    * Try autocomplete again
    """

    # Setup
    project_file = tmpdir.join("new_project.gra").ensure()
    gedcom_file = "./tests/workflow/test.ged"

    # Begin

    # Create new project
    window_driver.create_new_project(project_file)

    # Link gedcom file
    window_driver.link_gedcom(gedcom_file)

    # Add a plan
    window_driver.add_plan()

    # Type into Ancestor field
    ancestor_edit = window_driver.window.main_screen.screens["plan"].ancestor
    ancestor_edit.clear()

    qtbot.keyClicks(ancestor_edit, "A")
    assert ancestor_edit.completer().completionCount() == 2
    qtbot.keyClicks(ancestor_edit, "da")
    assert ancestor_edit.completer().completionCount() == 1

    # Unlink the gedcom
    window_driver.unlink_gedcom()

    # Type into ancestor field again
    ancestor_edit.clear()
    qtbot.keyClicks(ancestor_edit, "A")
    assert ancestor_edit.completer().completionCount() == 0
    qtbot.keyClicks(ancestor_edit, "da")
    assert ancestor_edit.completer().completionCount() == 0
