import logging
from typing import List, Set

from ror.RORResult import RORResult
from argument_parser import parse_program_arguments
from ProgramParameters import ProgramParameters

from ror.Dataset import RORDataset
from ror.ror_solver import solve_model
from ror.data_loader import DatasetReaderException, read_dataset_from_txt


def load_ror_dataset(filename: str) -> RORDataset:
    try:
        loader_result = read_dataset_from_txt(filename)
        # ignore parameters from file
        return loader_result.dataset
    except DatasetReaderException as e:
        logging.error(f'Failed to read problem file from {filename}, cause: {e}')
        raise e

def solve_problem(program_parameters: ProgramParameters) -> RORResult:
    dataset = load_ror_dataset(program_parameters.filename)
    result: RORResult = None
    try:
        result: RORResult = solve_model(
            dataset,
            program_parameters.ror_parameters,
            save_all_data=True
        )
        logging.info(f'Final rank is: {result.final_rank.rank_to_string()}')
        logging.info(f'Saved output to {result.output_dir}')
        return result
    except Exception as e:
        msg = f'Failed to solve problem, cause: {e}'
        logging.error(msg)
        raise e

def main():
    program_parameters: ProgramParameters = parse_program_arguments()
    solve_problem(program_parameters)


if __name__ == '__main__':
    main()
