"""
HTML and report functions
"""

from typing import IO, List, NoReturn
from datetime import datetime
from inspect import signature
from pathlib import Path
import webbrowser
import sys

from dirsync import sync


def html_header(
    *,
    header_title: str = 'Report',
    header_id: str = 'report'
) -> NoReturn:
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
    >>> ds.html_header(
    >>>     header_title=header_title,
    >>>     header_id=header_id
    >>> )
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


def html_footer() -> NoReturn:
    """
    Create an html footer.

    Example
    -------
    >>> ds.html_footer()
    """
    print('</body>')
    print('</html>')


def page_break() -> NoReturn:
    """
    Create an html page break.

    Example
    -------
    >>> ds.page_break()
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
        >>>
        >>> output_url = 'my_html_file.html'
        >>> original_stdout = ds.html_begin(output_url=output_url)

    Example 2
        >>> header_title = 'My Report'
        >>> header_id = 'my-report'
        >>> original_stdout = ds.html_begin(
        >>>     output_url=output_url,
        >>>     header_title=header_title,
        >>>     header_id=header_id
        >>> )
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
) -> NoReturn:
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
        >>>
        >>> output_url = 'my_html_file.html'
        >>> # see original_stdout example in def html_begin()
        >>> ds.html_end(
        >>>     original_stdout=original_stdout,
        >>>     output_url=output_url
        >>> )
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
) -> NoReturn:
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
    >>> graph_file = 'my_graph_file.svg'
    >>> fig.savefig(graph_file)
    >>> ds.html_figure(file_name=graph_file)

    Example 2
    >>> ds.html_figure(
    >>>     file_name=graph_file,
    >>>     caption='my graph file caption'
    >>> )
    """
    if caption is None:
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
    read_file_names: List[str] = None,
    save_file_names: List[str] = None,
    targets: List[str] = None,
    features: List[str] = None,
    number_knots: List[int] = None
) -> NoReturn:
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
    read_file_names : List[str] = None
        The list of file names read.
    save_file_names : List[str] = None
        The list of file names saved.
    targets : List[str] = None
        The list of target variables.
    features : List[str] = None
        Thje list of feature variables.
    number_knots : List[str] = None
        The number of spline knots.

    Example
    -------
    >>> ds.report_summary(
    >>>     start_time=start_time,
    >>>     stop_time=stop_time
    >>> )
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
) -> NoReturn:
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
    >>> ds.script_summary(script_path=Path(__file__))

    Example 2
    ---------
    >>> ds.script_summary(
    >>>     script_path=Path(__file__),
    >>>     action="started at"
    >>> )

    Example 3
    ---------
    >>> ds.script_summary(
    >>>     script_path=Path(__file__),
    >>>     action="finished at"
    >>> )
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
) -> NoReturn:
    """
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
    >>> local_docs = 'string_to_directory'
    >>> sharepoint_docs = 'string_to_mapped_drive_of_sharepoint'
    >>> ds.sync_directories(
    >>>     sourcedir=local_docs,
    >>>     targetdir=sharepoint_docs,
    >>>     action='sync',
    >>>     twoway=False,
    >>>     purge=False,
    >>>     verbose=True
    >>> )
    """
    sync(
        sourcedir=sourcedir,
        targetdir=targetdir,
        action=action,
        twoway=twoway,
        purge=purge,
        verbose=verbose
    )


def explore_functions(function: str) -> NoReturn:
    """
    Explore functions using inspect.signature.

    Parameters
    ----------
    function : str
        Name of function to explore.

    Examples
    --------
    Example 1
    >>> from sklearn.compose import make_column_transformer
    >>> function_to_explore = make_column_transformer
    >>> ds.explore_functions(function=function_to_explore)

    Example 2
    >>> from sklearn.compose import make_column_transformer
    >>> from sklearn.pipeline import make_pipeline
    >>> functions = [function_name_syntax, function_name]
    >>> for function in functions:
    >>>     ds.explore_functions(function=function)
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