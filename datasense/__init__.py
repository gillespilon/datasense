'''
datasense

Statistical and graphical functions for:
- Analysing process variation
- Supervised machine learning
- Six Sigma methodology
- Regular expressions
- Excel file edits
- Data science
- Analytics

Why this?
- Equivalent Python functions that are available in R, SAS, JMP, Minitab
- Other packages have limited process control analysis features.
- Other packages are abandoned or inadequately supported.
- Functions to support measurement system analysis.
- Functions to simplify statistics, graphs, etc.
- Functions to support process control charts.
- Functions to support SQL functionality.
- Develop a free open-source package.
'''


from .control_charts import *
from .munging import *
from .graphs import *
from .sequel import *
from .stats import *
from .html import *
from .pyxl import *
from .msa import *
from .rgx import *
