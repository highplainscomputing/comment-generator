import spacy

from typing import Dict, Any
from collections import defaultdict
from comment_generator.models.base import BaseModel


class NER(BaseModel):
    def __init__(self, model_name: str, entity_map: Dict[str, str]):
        """Performs deep-learning-based Named-Entity Recognition on Text Input.

        Based on: https://huggingface.co/transformers/

        Args:
            model_name: Path to the pre-trained bert models.
            entity_map: Possible classes to be predicted by models.

        """
        self._entity_map = entity_map
        self._ner = spacy.load(model_name)  # Load English tokenizer, tagger, parser and NER

    @staticmethod
    def from_config(config: Dict[str, Any]) -> 'NER':
        """Creates NER instance from a given config.

        Args
            config: Dictionary that contains `comment_generator` project config.
                Expected fields:
                    args: Arguments for current NER constructor.

        Returns:
            NER instance.

        Raises:
            KeyError: In case of missing config fields.
            TypeError: In case of missing or wrong keyword arguments defined in `args`.
        """
        if 'text_ner' not in config:
            raise KeyError(f'Expects to have `text_ner` in config dictionary.')

        args = config['text_ner'].get('args', {})
        try:
            return NER(**args)
        except TypeError as e:
            raise TypeError(f'{e}. Check `args` fields defined in config with the actual keyword args'
                            f'required in {NER.__name__} `__init__` method.')

    def apply(self, sequence_for_ner: str) -> defaultdict:
        """Performs Named-Entity Recognition on text input.

        Args:
            sequence_for_ner: Input Text for Extracting Named Entities.

        Returns:
            List of extracted named entities.
        """

        output = self._ner(sequence_for_ner)
        named_entities = defaultdict(list)
        for entity in output.ents:
            if entity.label_ in self._entity_map:
                named_entities[entity.label_].append(entity.text)
        return named_entities
