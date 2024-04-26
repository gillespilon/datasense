'''
datasense library of modules

Tools for statistical, graphical, and predictive analysis:

- Supervised machine learning
- Six Sigma methodology
- Regular expressions
- Process capability
- Process variation
- Excel file edits
- Taguchi Methods
- Data Science
- Automation
- Analytics

Why this?

- Equivalent Python functions that are available in R, SAS, JMP, Minitab
- Other packages have limited process control analysis features.
- Other packages are abandoned or inadequately supported.
- Functions to support measurement system analysis.
- Functions to simplify statistics, graphs, etc.
- Functions to support process control charts.
- Functions to support SQL functionality.
- Develop a free open source package.
'''


from .stats import *
from .control_charts import *
from .msa import *
from .munging import *
from .graphs import *
from .html_ds import *
from .pyxl import *
from .sequel import *
from .rgx import *
from .automation import *
from .taguchi import *
from .process_capability import *
