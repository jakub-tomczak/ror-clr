from ror.RORParameters import RORParameters


class ProgramParameters:
    def __init__(self, ror_parameters: RORParameters, filename: str) -> None:
        self.__ror_parameters: RORParameters = ror_parameters
        self.__filename: str = filename

    @property
    def ror_parameters(self) -> RORParameters:
        return self.__ror_parameters

    @property
    def filename(self) -> str:
        return self.__filename

    def __repr__(self) -> str:
        return f'<ProgramParameters:\nfilename: {self.__filename},\nror parameters: {self.__ror_parameters}>'

    def __eq__(self, o: object) -> bool:
        if type(o) is ProgramParameters:
            return o.filename == self.filename and o.ror_parameters == self.ror_parameters
        return False
    
    def __hash__(self) -> int:
        return self.ror_parameters.__hash__() * 13 + self.__filename.__hash__()*19
