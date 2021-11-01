import json
from typing import List

from ror.RORParameters import RORParameters
from ror.loader_utils import RORParameter
from BatchProgramParameters import BatchProgramParameters

from ProgramParameters import ProgramParameters
from argument_parser import parse_batch_program_arguments
from solve_problem import solve_problem
import logging
from tqdm import tqdm
import os
import time


def program_parameters_from_values(
    filename: str,
    eps: float,
    aggregator: str,
    tie_resolver: str,
    weights: List[float],
    alpha_values: List[float] = None,
    alpha_values_number: List[float] = None,
):
    ror_parameters: RORParameters = RORParameters()
    ror_parameters.add_parameter(RORParameter.EPS, eps)
    ror_parameters.add_parameter(RORParameter.RESULTS_AGGREGATOR, aggregator)
    ror_parameters.add_parameter(RORParameter.TIE_RESOLVER, tie_resolver)
    ror_parameters.add_parameter(RORParameter.ALPHA_WEIGHTS, weights)
    if alpha_values is not None:
        ror_parameters.add_parameter(RORParameter.ALPHA_VALUES, alpha_values)
    if alpha_values_number is not None:
        ror_parameters.add_parameter(
            RORParameter.NUMBER_OF_ALPHA_VALUES, alpha_values_number)
    return ProgramParameters(ror_parameters, filename)


def create_configs(data) -> List[ProgramParameters]:
    program_parameters_list: List[ProgramParameters] = []
    if 'problem_files' not in data or type(data['problem_files']) is not list:
        raise Exception(
            'problem_files key must be provided as a list in config file')
    if len(data['problem_files']) < 1:
        raise Exception('There must be at least one file with problem')
    files: List[str] = data['problem_files']
    eps_values: List[float] = []
    if 'eps_values' in data:
        assert type(data['eps_values']
                    ) is list, 'Epsilon values must be provided as a list'
        eps_values = data['eps_values']
    if len(eps_values) < 1:
        # add default value - so we can enter inner loops
        eps_values.append(
            RORParameters.get_default_parameter_value(RORParameter.EPS))
    aggregators: List[str] = []
    if 'aggregators' in data:
        assert type(data['aggregators']
                    ) is list, 'Aggregators must be provided as a list'
        aggregators = data['aggregators']
    if len(aggregators) < 1:
        aggregators.append(RORParameters.get_default_parameter_value(
            RORParameter.RESULTS_AGGREGATOR))
    tie_resolvers: List[str] = []
    if 'tie_resolvers' in data:
        assert type(data['tie_resolvers']
                    ) is list, 'Tie resolvers must be provided as a list'
        tie_resolvers = data['tie_resolvers']
    if len(tie_resolvers) < 1:
        tie_resolvers.append(
            RORParameters.get_default_parameter_value(RORParameter.TIE_RESOLVER))
    alpha_weights: List[List[float]] = []
    if 'alpha_weights_lists' in data:
        assert type(data['alpha_weights_lists']
                    ) is list, 'Alpha values weights must be provided as a list'
        alpha_weights = data['alpha_weights_lists']
    if len(alpha_weights) < 1:
        alpha_weights.append(RORParameters.get_default_parameter_value(
            RORParameter.ALPHA_WEIGHTS))
    alpha_values_number_list: List[float] = []
    if 'alpha_values_number' in data:
        assert type(data['alpha_values_number']
                    ) is list, 'Alpha values number must be provided as a list'
        alpha_values_number_list = data['alpha_values_number']
    if len(alpha_values_number_list) < 1:
        alpha_values_number_list.append(
            RORParameters.get_default_parameter_value(RORParameter.NUMBER_OF_ALPHA_VALUES))
    alpha_values_list: List[List[float]] = []
    if 'alpha_values_lists' in data:
        assert type(data['alpha_values_lists']
                    ) is list, 'Alpha values must be provided as a list'
        alpha_values_list = data['alpha_values_lists']
    if len(alpha_values_list) < 1:
        alpha_values_list.append(
            RORParameters.get_default_parameter_value(RORParameter.ALPHA_VALUES))

    for file in files:
        for eps in eps_values:
            for aggregator in aggregators:
                for tie_resolver in tie_resolvers:
                    if aggregator in ['BordaResultAggregator', 'CopelandResultAggregator'] and tie_resolver != 'NoResolver':
                        # tie resolver is only used
                        continue
                    for weights in alpha_weights:
                        for alpha_values_number in alpha_values_number_list:
                            if aggregator not in ['BordaResultAggregator', 'CopelandResultAggregator']:
                                # number of alpha values is only used in Borda and Copeland aggregators
                                continue
                            program_parameters_list.append(program_parameters_from_values(
                                file,
                                eps,
                                aggregator,
                                tie_resolver,
                                weights,
                                alpha_values_number=alpha_values_number
                            ))
                        for alpha_values in alpha_values_list:
                            if aggregator not in ['DefaultResultAggregator', 'WeightedResultAggregator']:
                                # number of alpha values is only used in Borda and Copeland aggregators
                                continue
                            program_parameters_list.append(program_parameters_from_values(
                                file,
                                eps,
                                aggregator,
                                tie_resolver,
                                weights,
                                alpha_values=alpha_values
                            ))
    return program_parameters_list


def read_batch_runner_config(params: BatchProgramParameters) -> List[ProgramParameters]:
    if not os.path.exists(params.config_file):
        logging.error(f'Config file {params.config_file} not found.')
        exit(1)
    logging.info(f'Trying to read config from file {params.config_file}')
    with open(params.config_file) as config:
        try:
            config_data = json.load(config)
            return create_configs(config_data)
        except Exception as e:
            logging.error('Failed to read data from config file.')
            raise e


def main():
    batch_parameters = parse_batch_program_arguments()
    launch_parameters: List[ProgramParameters] = read_batch_runner_config(
        batch_parameters)
    success = 0
    all_combinations = len(launch_parameters)
    logging.info(f'Generated {all_combinations} launch configs')

    for launch_parameter in tqdm(launch_parameters):
        logging.info(
            f'Trying to solve problem {launch_parameter.filename} with parameters {launch_parameter}')
        try:
            solve_problem(launch_parameter)
            success += 1
            # wait so output dir is changed
            time.sleep(1)
        except:
            logging.error('Failed to solve problem')

    logging.info(
        f'Tried to solve problem using {all_combinations} parameter configurations.')
    logging.info(f'Ran successfully: {success}')
    logging.info(f'Ran failed: {all_combinations - success}')
    logging.info(f'Success rate: {success/all_combinations}')


if __name__ == '__main__':
    main()
