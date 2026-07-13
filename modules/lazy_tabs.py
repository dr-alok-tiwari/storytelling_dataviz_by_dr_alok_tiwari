"""Enable lazy execution for legacy ``st.tabs`` page functions.

The original course pages were written before Streamlit supported stateful tabs.
By default, Streamlit executes every tab body on every rerun, even when only one
tab is visible. This adapter transforms those existing functions at import time
so hidden tab bodies are skipped without rewriting the teaching content.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Callable, Iterable
from typing import Any, TypeVar, cast


FunctionT = TypeVar("FunctionT", bound=Callable[..., Any])


def _is_tabs_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "st"
        and node.func.attr == "tabs"
    )


def _target_names(target: ast.AST) -> set[str]:
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        return {
            element.id
            for element in target.elts
            if isinstance(element, ast.Name)
        }
    return set()


def enable_lazy_tabs(function: FunctionT, *, key: str | None = None) -> FunctionT:
    """Return a function whose hidden ``st.tabs`` bodies are not executed.

    If the function does not contain a top-level ``st.tabs`` assignment, it is
    returned unchanged. When source inspection is unavailable, the safe fallback
    is also to return the original function.
    """

    try:
        source = textwrap.dedent(inspect.getsource(function))
    except (OSError, TypeError):
        return function

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return function

    definition = next(
        (node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))),
        None,
    )
    if definition is None:
        return function

    transformed = False
    tab_names: set[str] = set()
    new_body: list[ast.stmt] = []

    for statement in definition.body:
        if isinstance(statement, ast.Assign) and _is_tabs_call(statement.value):
            call = cast(ast.Call, statement.value)
            existing_keywords = {keyword.arg for keyword in call.keywords}
            if "on_change" not in existing_keywords:
                call.keywords.append(ast.keyword(arg="on_change", value=ast.Constant("rerun")))
            if "key" not in existing_keywords:
                tab_key = key or (
                    f"lazy_tabs_{function.__module__.replace('.', '_')}_{function.__name__}"
                )
                call.keywords.append(ast.keyword(arg="key", value=ast.Constant(tab_key)))

            for target in statement.targets:
                tab_names.update(_target_names(target))
            transformed = bool(tab_names)
            new_body.append(statement)
            continue

        if tab_names and isinstance(statement, ast.With) and len(statement.items) == 1:
            context = statement.items[0].context_expr
            if isinstance(context, ast.Name) and context.id in tab_names:
                new_body.append(
                    ast.If(
                        test=ast.Attribute(
                            value=ast.Name(id=context.id, ctx=ast.Load()),
                            attr="open",
                            ctx=ast.Load(),
                        ),
                        body=[statement],
                        orelse=[],
                    )
                )
                continue

        new_body.append(statement)

    if not transformed:
        return function

    definition.body = new_body
    ast.fix_missing_locations(tree)
    namespace: dict[str, Any] = {}
    filename = inspect.getsourcefile(function) or "<lazy-tabs>"
    exec(compile(tree, filename, "exec"), function.__globals__, namespace)
    transformed_function = namespace[function.__name__]

    transformed_function.__defaults__ = function.__defaults__
    transformed_function.__kwdefaults__ = function.__kwdefaults__
    transformed_function.__annotations__ = function.__annotations__
    transformed_function.__dict__.update(function.__dict__)
    transformed_function.__doc__ = function.__doc__
    transformed_function.__module__ = function.__module__
    transformed_function.__qualname__ = function.__qualname__

    return cast(FunctionT, transformed_function)


def enable_lazy_tabs_for(functions: Iterable[FunctionT]) -> tuple[FunctionT, ...]:
    """Apply :func:`enable_lazy_tabs` to an iterable of page functions."""

    return tuple(enable_lazy_tabs(function) for function in functions)
