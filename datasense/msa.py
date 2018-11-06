'''
Honest MSA reports on pandas DataFrames
'''

# TODO: Measurement system analysis (MSA) using control charts.
# TODO: MSA range chart.
# TODO: MSA average chart.
# TODO: MSA parallelism chart.
# TODO: MSA main effects chart (ANOME).
# TODO: MSA mean ranges chart (ANOMR).
# TODO: MSA test-retest error.
# TODO: MSA probable error.
# TODO: MSA intraclass correlation coefficient with operator bias.
# TODO: MSA intraclass correlation coefficient without operator bias.

import pandas as pd


class MSA:
    '''
    TODO
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        '''
        :param df: Must be a dataframe with an index set, and 2+ numeric columns
        '''
        do_the_calculations()

    def _subcalc0(self):
        pass

    # […]

    def report(self):
        '''
        TODO
        '''
        return [
            self.range_chart(),
            self.average_chart(),
            self.parallelism_plot(),

            self.emp_results(),
            self.classification(),
            self.effective_resolution(),
            self.variance_components(),
            self.emp_gauge_rr_results(),

            self.analysis_of_main_effects(),
            self.analysis_of_mean_ranges()
        ]

    # Charts

    def range_chart(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def average_chart(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def parallelism_plot(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def analysis_of_main_effects(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def analysis_of_mean_ranges(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    # Tables

    def emp_results(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def classification(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def effective_resolution(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def variance_components(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def emp_gauge_rr_results(self):
        '''
        TODO
        '''
        raise NotImplementedError()

    def interpret(self):
        '''
        Overall interpretation
        '''
        raise NotImplementedError()

    def interpret_tables(self):
        '''
        General interpretation of tables
        '''
        raise NotImplementedError()

    # Chart interpretations

    def range_in_control(self) -> bool:
        '''
        TODO
        '''
        raise NotImplementedError()

    def range_out_of_control_reason(self) -> str:
        '''
        TODO
        '''
        raise NotImplementedError()

    def average_in_control(self) -> bool:
        '''
        TODO
        '''
        raise NotImplementedError()

    def average_out_of_control_reason(self) -> str:
        '''
        TODO
        '''
        raise NotImplementedError()

    def main_effects_in_control(self) -> bool:
        '''
        TODO
        '''
        raise NotImplementedError()

    def main_effects_out_of_control_reason(self) -> str:
        '''
        TODO
        '''
        raise NotImplementedError()

    def mean_ranges_in_control(self) -> bool:
        '''
        TODO
        '''
        raise NotImplementedError()

    def mean_ranges_out_of_control_reason(self) -> str:
        '''
        TODO
        '''
        raise NotImplementedError()

    # Table interpretations

    # TODO: Probable error vs resolution
    # TODO: Inter-class correlation class
    # TODO: Variance components
    # TODO: Gauge R&R


if __name__ == '__main__':
    from argparse import ArgumentParser

    argument_parser = ArgumentParser(description=__doc__)
    argument_parser.add_argument('csv', type=pd.read_csv,
                                 help='Path to CSV file')

    args = argument_parser.parse_args()
    msa = MSA(args.csv)
    msa.report()
