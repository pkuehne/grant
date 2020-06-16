""" Tests for the TaskMatcher class """

import pytest
from grant.models.task_matcher import TaskMatcher
from grant.research import ResearchTask
from grant.research import ResearchResult
from grant.research import ResearchPlan


def test_default_matches_all():
    """ A new TaskMatcher should match all Tasks """
    # Given
    task = ResearchTask()
    matcher = TaskMatcher()

    # When
    result = matcher.match(task)

    # Then
    assert result is True


def test_validate_argument():
    """ A None type argument should not match """
    # Given
    matcher = TaskMatcher()

    # When
    result = matcher.match(None)

    # Then
    assert result is False


def test_text_filter_successful_match():
    """ The text_filter should match tasks containing the text """
    # Given
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.text_filter("foo")

    # When
    task.source = "A foo bar"
    match = matcher.match(task)

    # Then
    assert match is True


def test_text_filter_failed_match():
    """ The text_filter should not match tasks not containing the text """
    # Given
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.text_filter("foo")

    # When
    task.source = "A baz bar"
    match = matcher.match(task)

    # Then
    assert match is False


def test_text_filter_emits_signal(qtbot):
    """ Check that setting the text filter emits the filters_changed signal """
    # Given
    matcher = TaskMatcher()

    # When
    with qtbot.waitSignals([matcher.filters_updated]):
        matcher.text_filter("Foo")


def test_result_filter_emits_signal(qtbot):
    """ Check that setting the result filter emits the filters_changed signal """
    # Given
    matcher = TaskMatcher()

    # When
    with qtbot.waitSignals([matcher.filters_updated]):
        matcher.result_filter("Foo")


def test_empty_result_filter_matches_all_results():
    """ An empty result filter will match all possible result types """
    # Given
    nil_result = ResearchResult(False)
    success_result = ResearchResult(True)
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("")

    # When
    task.result = None
    assert matcher.match(task) is True

    task.result = nil_result
    assert matcher.match(task) is True

    task.result = success_result
    assert matcher.match(task) is True


def test_open_result_filter_matches_open_results():
    """ An open result filter will match open result types """
    # Given
    nil_result = ResearchResult(False)
    success_result = ResearchResult(True)
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("open")

    # When
    task.result = None
    assert matcher.match(task) is True

    task.result = nil_result
    assert matcher.match(task) is False

    task.result = success_result
    assert matcher.match(task) is False


def test_nil_result_filter_matches_nil_results():
    """ A nil result filter will match nil result types """
    # Given
    nil_result = ResearchResult(False)
    success_result = ResearchResult(True)
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("nil")

    # When
    task.result = None
    assert matcher.match(task) is False

    task.result = nil_result
    assert matcher.match(task) is True

    task.result = success_result
    assert matcher.match(task) is False


def test_success_result_filter_matches_success_results():
    """ A success result filter will match success result types """
    # Given
    nil_result = ResearchResult(False)
    success_result = ResearchResult(True)
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("success")

    # When
    task.result = None
    assert matcher.match(task) is False

    task.result = nil_result
    assert matcher.match(task) is False

    task.result = success_result
    assert matcher.match(task) is True


@pytest.mark.parametrize(
    "result, value",
    [(None, False), (ResearchResult(False), False), (ResearchResult(True), False)],
)
def test_unknown_result_filter_matches_no_results(result, value):
    """ An unknown result filter will match no result types """
    # Given
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("foo")

    # When
    task.result = result
    assert matcher.match(task) is value


@pytest.mark.parametrize(
    "source, result, value",
    [("foo", None, True), ("foo", ResearchResult(False), False), ("bar", None, False)],
)
def test_filters_are_anded(source, result, value):
    """ Test that filters are 'and'ed together """
    # Given
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.result_filter("open")
    matcher.text_filter("foo")

    # When
    task.source = source
    task.result = result

    # Then
    assert matcher.match(task) is value


@pytest.mark.parametrize(
    "ancestor, value", [("Henry", True), ("David", False), ("", False), (None, True)]
)
def test_ancestor_matches_plan(ancestor, value):
    """ When the plan is passed and ancestor filter set, it should be applied """
    # Given
    task = ResearchTask()
    plan = ResearchPlan()
    matcher = TaskMatcher()
    matcher.ancestor_filter("Henry")

    # When
    plan.ancestor = ancestor

    # Then
    assert matcher.match(task, plan) is value


def test_ancestor_filter_has_no_effect_if_no_plan_passed():
    """ When no plan is passed to the match function, the ancestor filter should have no effect """

    # Given
    task = ResearchTask()
    matcher = TaskMatcher()
    matcher.ancestor_filter("Henry")

    # When
    assert matcher.match(task, None) is True
