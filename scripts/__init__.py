"""Development scripts package."""

# Import all functions to make them available via scripts:function_name
from scripts.__main__ import (  # noqa: F401
    clean,
    format_code,
    lint,
    test,
    test_cov,
)


