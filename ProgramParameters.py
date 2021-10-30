from ror.RORParameters import RORParameters


class ProgramParameters:
    def __init__(self, ror_parameters: RORParameters) -> None:
        self.__ror_parameters: RORParameters = ror_parameters

    @property
    def ror_parameters(self) -> RORParameters:
        return self.__ror_parameters
