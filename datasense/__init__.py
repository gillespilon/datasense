'''
datasense

Statistical and graphical functions for:
- Analytics
- Analysing process variation
- Data science
- Supervised machine learning
- Six Sigma methodology

Why this?
- Functions to support process control charts.
- Functions to support measurement system analysis.
- Functions to simplify statistics, graphs, etc.
- Develop a free open-source package.
- Equivalent Python functions that are available in R and SAS.
- Other packages have limited process control analysis features.
- Other packages are abandoned or inadequately supported.
'''


from .stats import *
from .control_charts import *
from .msa import *
from .munging import *
from .graphs import *
from .html import *
from .pyxl import *
