from comment_generator.utils.parse_config import parse_config
from comment_generator.models.classifier import TextClassifier
from comment_generator.models.ner import NER
from comment_generator.models.generator import CommentGenerator


def test_parse_config():
    cfg = parse_config('config.yaml')
    assert isinstance(cfg, dict)
    assert len(cfg) > 0


def test_text_classifier_from_config():
    cfg = parse_config('config.yaml')
    text_classifier = TextClassifier.from_config(cfg)
    assert isinstance(text_classifier, TextClassifier)


def test_ner_from_config():
    cfg = parse_config('config.yaml')
    ner_instance = NER.from_config(cfg)
    assert isinstance(ner_instance, NER)


def test_generator_from_config():
    cfg = parse_config('config.yaml')
    comment_generator = CommentGenerator.from_config(cfg)
    assert isinstance(comment_generator, CommentGenerator)
