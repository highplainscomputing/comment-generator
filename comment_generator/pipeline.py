"""Defines end-to-end pipeline that performs Classification, Named-Entity Recognition on raw text and Generate Comments.

1. Put file with models class implementation into `models` module.
2. Import models class in `models/__init__.py` file.
"""
from typing import Dict, Any

from comment_generator import logger
from comment_generator import models


class Pipeline(models.BaseModel):
    def __init__(self, post_classifier: models.TextClassifier, ner_extractor: models.NER,
                 comment_generator: models.CommentGenerator):
        """Performs Text Classification ,named entity recognition and Generate Comment for the given text.

        Supported types of categories for can be defined at config.yaml.
        Pipeline performs the following steps:
        ```
        Classify the given text.

        Perform NER using Spacy.

        Generate Comment for Given Text.
        ```

        Args:
            post_classifier: `TextClassifier` instance.
            ner_extractor: `NER` instance.
            comment_generator: 'CommentGenerator' instance.
        """
        self.post_classifier = post_classifier
        self.ner_extractor = ner_extractor
        self.comment_generator_model = comment_generator

    @staticmethod
    def from_config(config: Dict[str, Any]) -> 'Pipeline':
        """Instantiates Pipeline object from config file."""
        pipeline = dict()
        pipeline['text_classifier'] = models.TextClassifier.from_config(config)
        pipeline['text_ner'] = models.NER.from_config(config)
        pipeline['comment_generator'] = models.CommentGenerator.from_config(config)

        logger.info('Pipeline has been configured with the following modules:')
        for name, module in pipeline.items():
            logger.info(f'  {name.replace("_", " ").title()}: {module}')

        return Pipeline(post_classifier=pipeline['text_classifier'],
                        ner_extractor=pipeline['text_ner'],
                        comment_generator=pipeline['comment_generator'])

    def apply(self, post: str) -> Dict[str, Any]:
        """Runs end-to-end NER pipeline for the given text.

        Args:
            post: Social Media Post to process.

        Returns:
            Dictionary with Category, extracted named-entities and generated comment. Output example:
            {
            'entities': [
                {'name': ['Sherlock', 'Holmes'], 'address': ['221B Baker Street']},
                {'name': ['Elon Musk']}
            ],

            'category': 'Politics',
            'comment: 'Imran khan is great leader.'
            }
        """

        category = self.post_classifier.apply(sequence_to_classify=post)
        ner = self.ner_extractor.apply(sequence_for_ner=post)  # we apply ner on the same text input
        generated_comment = self.comment_generator_model.apply(sequence_for_text_generation=post)

        result = {
            'entities': ner,
            'comment': generated_comment,
            'category': category
        }
        return result
