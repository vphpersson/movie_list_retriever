from typed_argument_parser import TypedArgumentParser

from movie_list_retriever import SupportedSource


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
