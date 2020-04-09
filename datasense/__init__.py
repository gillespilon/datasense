'''
datasense

Statistical and graphical functions for:

- Analytics
- Analysing process variation
- Data science
- Six Sigma methodology

Why this?

- Wanted functions to support process control charts.
- Wanted functions to support measurement system analysis.
- Develop a package that is open-source for those unable to buy software.
- Wanted Python functions that are available in R and SAS.
- Other packages have limited features for process control analysis.
- Other packages are abandoned or inadequately supported.

'''

from .stats import *
from .control_charts import *
from .msa import *
from .munging import *
from .graphs import *
