from enum import Enum

from typed_argument_parser import TypedArgumentParser


class SupportedSource(Enum):
    NEW_YORK_TIMES = 'new_york_times'
    FILMSTADEN = 'filmstaden'

    def __str__(self) -> str:
        return self.value


class MovieListRetrieverArgumentParser(TypedArgumentParser):

    class Namespace:
        source: SupportedSource

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(
                    description='Retrieve movie lists.'
                ) | kwargs
            )
        )

        self.add_argument(
            'source',
            help='The source from which to retrieve movies.',
            type=SupportedSource,
            choices=list(SupportedSource)
        )
