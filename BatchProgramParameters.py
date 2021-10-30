class BatchProgramParameters:
    def __init__(self, config_file: str):
        self.__config_file: str = config_file
    
    @property
    def config_file(self) -> str:
        return self.__config_file