from typing import Dict, Any
import numpy as np
from transformers import pipeline

from comment_generator.models.base import BaseModel


class TextClassifier(BaseModel):
    def __init__(self, model_name: str, task: str, categories: Dict[str, str]):
        """Performs deep-learning-based Zero Shot Classification on Text Input.

        Based on: https://huggingface.co/transformers/

        Args:
            model_name: Path to the pre-trained bert models.
            categories: Possible classes to be predicted by models.
            task: Type of NLP task to be initialized.

        """
        self._category_map = categories
        self._classifier = pipeline(task, model=model_name)

    @staticmethod
    def from_config(config: Dict[str, Any]) -> 'TextClassifier':
        """Creates TextClassifier instance from a given config.

        Args
            config: Dictionary that contains `comment_generator` project config.
                Expected fields:
                    args: Arguments for current TextClassifier constructor.

        Returns:
            TextClassifier instance.

        Raises:
            KeyError: In case of missing config fields.
            TypeError: In case of missing or wrong keyword arguments defined in `args`.
        """
        if 'text_classifier' not in config:
            raise KeyError(f'Expects to have `text_classifier` in config dictionary.')

        args = config['text_classifier'].get('args', {})
        try:
            return TextClassifier(**args)
        except TypeError as e:
            raise TypeError(f'{e}. Check `args` fields defined in config with the actual keyword args'
                            f'required in {TextClassifier.__name__} `__init__` method.')

    def apply(self, sequence_to_classify: str) -> str:
        """Performs Classification on text input.

        Args:
            sequence_to_classify: Input Text for inference.

        Returns:
            category with highest probability.
        """

        output = self._classifier(sequence_to_classify, self._category_map)
        output = output['labels'][np.argmax(output['scores'])]
        return output
