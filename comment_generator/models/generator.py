import random

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import Dict, Any

from comment_generator.models.base import BaseModel


class CommentGenerator(BaseModel):
    def __init__(self, model_name: str, max_sequence_length: int,
                 repetition_penalty: float,
                 number_of_beams: int, number_of_sequences: int, length_penalty: int):
        """Performs deep-learning-based text generation on Text Input.

        Based on: https://huggingface.co/transformers/

        Args:
            model_name: Path to the pre-trained bert models.
            max_sequence_length: maximum length of input text.
            repetition_penalty: Float parameter for Randomness in Generated Text.
            number_of_sequences: Number of sequences to return by generator.
            number_of_beams: for decoding strategy

        """
        self._repetition_penalty = repetition_penalty
        self._generator = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._length_penalty = length_penalty
        self._max_sequence_length = max_sequence_length
        self._number_of_beams = number_of_beams
        self._number_of_sequences = number_of_sequences

    @staticmethod
    def from_config(config: Dict[str, Any]) -> 'CommentGenerator':
        """Creates CommentGenerator instance from a given config.

        Args
            config: Dictionary that contains `comment_generator` project config.
                Expected fields:
                    args: Arguments for current CommentGenerator constructor.

        Returns:
            CommentGenerator instance.

        Raises:
            KeyError: In case of missing config fields.
            TypeError: In case of missing or wrong keyword arguments defined in `args`.
        """
        if 'comment_generator' not in config:
            raise KeyError(f'Expects to have `comment_generator` in config dictionary.')

        args = config['comment_generator'].get('args', {})
        try:
            return CommentGenerator(**args)
        except TypeError as e:
            raise TypeError(f'{e}. Check `args` fields defined in config with the actual keyword args'
                            f'required in {CommentGenerator.__name__} `__init__` method.')

    def apply(self, sequence_for_text_generation: str) -> str:
        """Performs Classification on text input.

        Args:
            sequence_for_text_generation: Input Text for inference.

        Returns:
            Generated Sequence
        """
        input_ids = self._tokenizer.encode("summarize: " + sequence_for_text_generation, return_tensors="pt",
                                           add_special_tokens=True)
        generated_ids = self._generator.generate(input_ids=input_ids, num_beams=self._number_of_beams,
                                                 max_length=self._max_sequence_length,
                                                 repetition_penalty=self._repetition_penalty,
                                                 length_penalty=self._length_penalty, early_stopping=True,
                                                 num_return_sequences=self._number_of_sequences)

        tgt_text = [self._tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True)
                    for g in generated_ids]

        return random.choice(tgt_text)
