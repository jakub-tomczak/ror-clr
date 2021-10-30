from ror.RORParameters import DataValidationException, RORParameters
from ror.loader_utils import RORParameter
from ProgramParameters import ProgramParameters
import argparse
import logging


def parse_program_arguments() -> ProgramParameters:
    parser = argparse.ArgumentParser(
        prog='ROR-distance solver CLI',
        description='ROR-distance solver is available as python module at https://github.com/jakub-tomczak/ror'
    )
    # default values available at:
    # https://github.com/jakub-tomczak/ror/blob/067882816bce37bc223e652044404bf051e625d9/ror/RORParameters.py#L49
    parser.add_argument('--eps', metavar='epsilion value', type=float, required=False,
        help='epsilion value, must be a float, greater or equal 0.0')
    parser.add_argument('--initial_alpha', metavar='initial alpha', type=float, required=False,
        help='Alpha value used for solving first model, must be in range <0.0, 1.0>')
    parser.add_argument('--alpha_values', nargs='+', required=False,
        help='alpha values that should be used, provide it as float values separated by comma. '+\
            'Each alpha value must be in range <0.0, 1.0>')
    parser.add_argument('--alpha_weights', nargs='+', required=False,
        help='alpha weights that should be used, provide it as float values separated by comma. '+\
            "Each alpha weight must be greater or equal 0.0")
    parser.add_argument('--precision', metavar='display precision', type=int, required=False,
        help='Float point values precision used when displaying results,'+\
            'doesn\'t influence calculations precision. Precision must be an int number in range <0, 10>.')
    parser.add_argument('--result_aggregator', metavar='result aggregator', type=str, required=False,
        help='Name of the result aggregator to be used, available values:'+\
            '{"DefaultResultAggregator", "WeightedResultAggregator",'+\
            ' "BordaResultAggregator", "CopelandResultAggregator"}')
    parser.add_argument('--tie_resolver', metavar='result aggregator', type=str, required=False,
        help='Name of the tie resolver to be used, available values:'+\
            '{"NoResolver", "BordaTieResolver", "CopelandTieResolver"}')
    parser.add_argument('--alpha_values_number', metavar='Numbr of alpha values', type=int, required=False,
        help='Number of alpha values to be used. This argument is only used with the following aggregators:'+\
            '{"BordaResultAggregator", "CopelandResultAggregator"}.'+\
            'Number of alpha values must be an int value in range <3, 15>.')
    parser.add_argument('file', metavar='file', type=str,
        help='Text file with problem definition.')

    args = parser.parse_args()
    print(args)
    filename = ''
    ror_parameters = RORParameters()
    for argument, argument_value in args._get_kwargs():
        if argument == 'file':
            filename = argument_value
            logging.info(f'Setting filename to {filename}')
        else:
            if argument_value is not None:
                argument = argument.upper()
                logging.info(f'Trying to add ROR-distance method parameter: {argument} with value: {argument_value}')
                try:
                    ror_parameters.add_parameter(RORParameter[argument], argument_value)
                except DataValidationException as e:
                    logging.error(f'Failed to set parameter {argument}, cause: {e}')
                    # pass exception further to stop processing
                    raise e
    parameters = ProgramParameters(ror_parameters, filename)
    return parameters
