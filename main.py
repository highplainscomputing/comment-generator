#!/usr/bin/env python
"""Code for running pipeline locally, can be used for debugging and testing."""

import argparse
import logging
import pprint

from comment_generator import logger
from comment_generator.utils.parse_config import parse_config
from comment_generator.pipeline import Pipeline
from comment_generator.utils.db_utils import initialize_mongodb_instance, insert_record


def parse_args():
    parser = argparse.ArgumentParser(description='Pipeline for Text Classification , NER and Comment Generation')
    parser.add_argument('--config', help='Path to pipeline config', default='config.yaml')
    parser.add_argument('--input_text', help='Text Input to Process', default='')
    return parser.parse_args()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    args = parse_args()
    cfg = parse_config(config_path=args.config)
    pipeline = Pipeline.from_config(config=cfg)
    mongo_client, mongo_db, collection_name = initialize_mongodb_instance(config=cfg)
    text_input = ''
    social_media_post = """Labour plans maternity pay rise
        Maternity pay for new mothers is to rise by £1,400 as part of new proposals announced by the Trade and Industry 
        Secretary Patricia Hewitt. It would mean paid leave would be increased to nine months by 2007, Ms Hewitt told 
        GMTV's Sunday programme.Other plans include letting maternity pay be given to fathers and extending rights to 
        parents of older children.The Tories dismissed the maternity pay plan as "desperate",while the Liberal Democrats
        said it was misdirected.Ms Hewitt said: "We have already doubled the length of maternity pay, it was 13 weeks
        when we were elected,we have already taken it up to 26 weeks. "We are going to extend the pay to nine months by
        2007 and the aim is to get it right up to the full 12 months by the end of the next Parliament." She said new
        mothers were already entitled to 12 months leave, but that many women could not take it as only six of those
        months were paid. "We have made a firm commitment. We will definitely extend the maternity pay, from the six
        months where it now is to nine months, that's the extra £1,400." She said ministers would consult on other
        proposals that could see fathers being allowed to take some of their partner's maternity pay or leave period,
        or extending the rights of flexible working to carers or parents of older children. The Shadow Secretary of
        State for the Family, Theresa May, said: "These plans were announced by Gordon Brown in his pre-budget review in
        December and Tony Blair is now recycling it in his desperate bid to win back women voters."
        She said the Conservatives would announce their proposals closer to the General Election. Liberal Democrat
        spokeswoman for women Sandra Gidley said: "While mothers would welcome any extra maternity pay the Liberal
        Democrats feel this money is being misdirected." She said her party would boost maternity pay in the first six
        months to allow more women to stay at home in that time.Ms Hewitt also stressed the plans would be paid for
        by taxpayers, not employers. But David Frost, director general of the British Chambers of Commerce, warned that
        many small firms could be "crippled" by the move. "While the majority of any salary costs may be covered by the
        government's statutory pay, recruitment costs, advertising costs, retraining costs and the strain on the company
        will not be," he said. Further details of the government's plans will be outlined on Monday. New mothers are 
        currently entitled to 90% of average earnings for the first six weeks after giving birth, followed by £102.80
        a week until the baby is six months old.
        """
    if args.input_text == '':
        text_input = social_media_post
    result = pipeline.apply(post=text_input)
    task_id = insert_record(output_json=result, mongo_client=mongo_db, collection_name=collection_name)
    info = pprint.pformat(result, indent=4)
    logger.info(info)
    logger.info(task_id)
