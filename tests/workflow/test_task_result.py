""" Workflow test for Research Results """

def test_research_result(window_driver, tmpdir):
    """
    Test Schedule:
    * Create Main Window
    * Create new project
    * Add a Plan
    * Add two tasks
    * Make task 1 nil result
    * Make task 2 success result
    """

    # Setup
    filename = tmpdir.join("new_project.gra").ensure()

    # Create new project
    window_driver.create_new_project(filename)

    # Add a plan
    window_driver.add_plan()

    # Add a task
    window_driver.select_plan(0)
    window_driver.add_task(0)
    window_driver.select_task(0, 0)

    # Make result nil
    window_driver.press_button_in_result_widget("result_nil")
    assert window_driver.project().plans[0].tasks[0].result.is_nil()

    # Add a second task
    window_driver.select_plan(0)
    window_driver.add_task(0)
    window_driver.select_task(0, 1)

    # Make result success
    window_driver.press_button_in_result_widget("result_success")
    assert not window_driver.project().plans[0].tasks[1].result.is_nil()
