"""
HTML and report functions
"""

from datetime import datetime
from inspect import signature
from pathlib import Path
from typing import IO
import webbrowser
import sys

from dirsync import sync


def html_header(
    *,
    header_title: str = 'Report',
    header_id: str = 'report'
) -> None:
    """
    Create an html header.

    Parameters
    ----------
    header_title : str = 'Report'
        The header title.
    header_id : str = 'report'
        The header ID.

    Example
    -------
    >>> import datasense as ds
    >>> ds.html_header(
    ...     header_title="header title",
    ...     header_id="header-id"
    ... ) # doctest: +NORMALIZE_WHITESPACE
    <!DOCTYPE html>
    <html lang="" xml:lang="" xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0, user-scalable=yes"\
            name="viewport"/>
    <style>@import url("support.css");</style>
    <title>header title</title>
    </head>
    <body>
    <h1 class="title" id="header-id">header title</h1>
    """
    print('<!DOCTYPE html>')
    print('<html lang="" xml:lang="" xmlns="http://www.w3.org/1999/xhtml">')
    print('<head>')
    print('<meta charset="utf-8"/>')
    print(
        '<meta content="width=device-width, initial-scale=1.0, '
        'user-scalable=yes" name="viewport"/>'
    )
    print('<style>@import url("support.css");</style>')
    print(f'<title>{header_title}</title>')
    print('</head>')
    print('<body>')
    print(
        f'<h1 class="title"'
        f' id="{header_id}">'
        f'{header_title}</h1>'
    )


def html_footer() -> None:
    """
    Create an html footer.

    Example
    -------
    >>> import datasense as ds
    >>> ds.html_footer() # doctest: +NORMALIZE_WHITESPACE
    </body>
    </html>
    """
    print('</body>')
    print('</html>')


def page_break() -> None:
    """
    Create an html page break.

    Example
    -------
    >>> import datasense as ds
    >>> ds.page_break() # doctest: +NORMALIZE_WHITESPACE
    </pre>
    <p style="page-break-after:always"></p>
    <p style="page-break-before:always"></p>
    <pre style="white-space: pre-wrap;">
    """
    print('</pre>')
    print('<p style="page-break-after:always"></p>')
    print('<p style="page-break-before:always"></p>')
    print('<pre style="white-space: pre-wrap;">')


def html_begin(
    *,
    output_url: str = 'html_report.html',
    header_title: str = 'Report',
    header_id: str = 'report',
) -> IO[str]:
    """
    Open a file to write html and set an hmtl header.

    Parameters
    ----------
    output_url : str = 'html_report.html'
        The file name for the html output.
    header_title : str = 'Report'
        The file title.
    header_id : str = 'report'
        The id for the header_title.

    Returns
    -------
    original_stdout : IO[str]
        A file object for the output of print().

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> output_url = '../tests/my_html_file.html'
    >>> original_stdout = ds.html_begin(output_url=output_url)

    Example 2
    ---------
    >>> header_title = 'My Report'
    >>> header_id = 'my-report'
    >>> original_stdout = ds.html_begin(
    ...     output_url=output_url,
    ...     header_title=header_title,
    ...     header_id=header_id
    ... )
     """
    original_stdout = sys.stdout
    sys.stdout = open(
        file=output_url,
        mode='w'
    )
    html_header(
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    return original_stdout


def html_end(
    *,
    original_stdout: IO[str],
    output_url: str
) -> None:
    """
    Create an html footer, close an html file, and open an html file in
    a new tab in a web browser.

    Parameters
    ----------
    original_stdout : IO[str]
        The original stdout.
    output_url : str
        The file name for the html output.

    Example
    -------
    >>> import datasense as ds
    >>> output_url = '../tests/my_html_file.html'
    >>> # see original_stdout example in def html_begin()
    >>> original_stdout = ds.html_begin(
    ...     output_url="output_url.html",
    ...     header_title="header_title",
    ...     header_id="header-id"
    ... )
    >>> ds.html_end(
    ...     original_stdout=original_stdout,
    ...     output_url="output_url.html"
    ... )
    """
    print('</pre>')
    html_footer()
    sys.stdout.close()
    sys.stdout = original_stdout
    webbrowser.open_new_tab(
        url=output_url
    )


def html_figure(
    *,
    file_name: Path | str,
    caption: str = None
) -> None:
    """
    Print an html tag for a figure.

    Parameters
    ----------
    file_name : str
        The file name of the image.
    caption : str = None
        The figure caption.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> import matplotlib.pyplot as plt
    >>> graph_file = 'my_graph_file.svg'
    >>> figsize = (8, 6)
    >>> fig = plt.figure(figsize=figsize)
    >>> fig.savefig(graph_file)
    >>> ds.html_figure(file_name=graph_file)
    </pre><figure><img src="my_graph_file.svg" alt="my_graph_file.svg"/>\
<figcaption>my_graph_file.svg</figcaption>\
</figure><pre style="white-space: pre-wrap;">

    Example 2
    ---------
    >>> import datasense as ds
    >>> ds.html_figure(
    ...     file_name=graph_file,
    ...     caption='../tests/my graph file caption'
    ... )
    </pre><figure><img src="my_graph_file.svg" alt="my_graph_file.svg"/>\
<figcaption>../tests/my graph file caption</figcaption>\
</figure><pre style="white-space: pre-wrap;">
    """
    if not caption:
        caption = ""
    else:
        caption = file_name
    print(
        '</pre>'
        '<figure>'
        f'<img src="{file_name}" '
        f'alt="{file_name}"/>'
        f'<figcaption>{caption}</figcaption>'
        '</figure>'
        '<pre style="white-space: pre-wrap;">'
    )


def report_summary(
    *,
    start_time: float,
    stop_time: float,
    print_heading: bool = True,
    read_file_names: list[str] = None,
    save_file_names: list[str] = None,
    targets: list[str] = None,
    features: list[str] = None,
    number_knots: list[int] = None
) -> None:
    """
    Create a report summary.

    Parameters
    ----------
    start_time : float
        The start time.
    stop_time : float
        The stop time.
    print_heading : bool = True
        The boolean to print the heading for the report summary.
    read_file_names : list[str] = None
        The list of file names read.
    save_file_names : list[str] = None
        The list of file names saved.
    targets : list[str] = None
        The list of target variables.
    features : list[str] = None
        Thje list of feature variables.
    number_knots : list[str] = None
        The number of spline knots.

    Example
    -------
    >>> import datasense as ds
    >>> import time
    >>> start_time = time.perf_counter()
    >>> stop_time = time.perf_counter()
    >>> ds.report_summary(
    ...     start_time=start_time,
    ...     stop_time=stop_time
    ... )
    </pre>
    <h1>Report summary</h1>
    <pre style="white-space: pre-wrap;">
    Execution time : 0.000 s
    """
    elapsed_time = stop_time - start_time
    if print_heading:
        print('</pre>')
        print('<h1>Report summary</h1>')
        print('<pre style="white-space: pre-wrap;">')
    print(f'Execution time : {elapsed_time:.3f} s')
    if read_file_names:
        print(f'Files read     : {read_file_names}')
    if save_file_names:
        print(f'Files saved    : {save_file_names}')
    if targets:
        print(f'Targets        : {targets}')
    if features:
        print(f'Features       : {features}')
    if number_knots:
        print(f'Number of knots: {number_knots}')


def script_summary(
    *,
    script_path: Path,
    action: str = "run"
) -> None:
    """
    Print script name and time of execution.

    Parameters
    ----------
    script_path : Path
        The path of the script file.
    action : str = "run"
        An action message: run, started at, finished at, etc.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> ds.script_summary(script_path=Path(__file__)) # doctest: +SKIP

    Example 2
    ---------
    >>> import datasense as ds
    >>> ds.script_summary(
    ...     script_path=Path(__file__),
    ...     action="started at"
    ... ) # doctest: +SKIP

    Example 3
    ---------
    >>> import datasense as ds
    >>> ds.script_summary(
    ...     script_path=Path(__file__),
    ...     action="finished at"
    ... ) # doctest: +SKIP
    """
    print(
        "Script",
        Path(Path().resolve(), script_path),
        f"{action} "
        f"{(datetime.now()):%Y-%m-%d %H:%M:%S}."
    )
    print()


def sync_directories(
    *,
    sourcedir: str,
    targetdir: str,
    action: str = 'sync',
    twoway: bool = False,
    purge: bool = False,
    verbose: bool = True
) -> None:
    """
    Synchronize two directories.

    Parameters
    ----------
    sourcedir : str
        The source directory for syncing.
    targetdir : str
        The target directory for syncing.
    action : str = 'sync'
        The syncing action. Options: diff, sync, update.
    twoway : bool = False
        Update files from sourcedir to targetdir (False) or both (True).
    purge : bool = False
        Delete files from targetdir.
    verbose : bool = True
        Provide verbose output.

    Example
    -------
    >>> import datasense as ds
    >>> local_docs = 'string_to_directory'
    >>> sharepoint_docs = 'string_to_mapped_drive_of_sharepoint'
    >>> ds.sync_directories(
    ...     sourcedir="../tests/sourcedir",
    ...     targetdir="../tests/targetdir",
    ...     action='sync',
    ...     twoway=False,
    ...     purge=False,
    ...     verbose=True
    ... ) # doctest: +SKIP
    """
    sync(
        sourcedir=sourcedir,
        targetdir=targetdir,
        action=action,
        twoway=twoway,
        purge=purge,
        verbose=verbose
    )


def explore_functions(function: str) -> None:
    """
    Explore functions using inspect.signature.

    Parameters
    ----------
    function : str
        Name of function to explore.

    Examples
    --------
    Example 1
    ---------
    >>> import datasense as ds
    >>> from sklearn.compose import make_column_transformer
    >>> function_to_explore = make_column_transformer
    >>> ds.explore_functions(function=function_to_explore) # doctest: +SKIP

    Example 2
    ---------
    >>> from sklearn.compose import make_column_transformer
    >>> from sklearn.pipeline import make_pipeline
    >>> functions = ["function_name_syntax", "function_name"]
    >>> for function in functions:
    ...     ds.explore_functions(function=function) # doctest: +SKIP
    """
    print()
    print("function name:")
    print("--------------")
    print(function.__name__)
    print()
    print("function signature:")
    print("-------------------")
    print(signature(function))
    print()
    for param in signature(function).parameters.values():
        print(param, param.kind.description)
    print()
    print(help(function))
    print()


__all__ = (
    'explore_functions',
    'sync_directories',
    'report_summary',
    'script_summary',
    'html_figure',
    'html_footer',
    'html_header',
    'html_begin',
    'page_break',
    'html_end',
)
