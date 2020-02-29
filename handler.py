import json
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def hello(event, context):

    logger.info('event')
    logger.info(event)
    logger.info('context')
    logger.info(context)

    sb.add_request_handler(LaunchRequestHandler())
    sb.add_request_handler(QuestionIntentHandler())

    handler = sb.lambda_handler()

    return handler(event, context)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to the Lexis Noah AI company, ask me any question, and I will happy to answer"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("launch", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response




class QuestionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("question")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Tell us about Lexis Noah's philosophy
        speech_text = "I don't know the answer"

        logger.info('request')
        logger.info(handler_input.request_envelope)

        logger.info('question')

        slots = handler_input.request_envelope.request.intent.slots
        logger.info('slots')
        logger.info(slots)

        key = slots['key']
        logger.info(key)

        if key.id == 'philosophy':
            speech_text = "Lexis Noah's philosophy is to unlock the infinite possibilities of one billion people."

        if key.id == 'company':
            speech_text = "Lexis Noah Co., Ltd. is headquartered in Nihonbashi Ningyocho, Chuo-ku, Tokyo, and has three core businesses: seminar business, edtech business, and education business."

        if key.id == 'representative':
            speech_text = "Lexis Noah's representative director is Seiji Kano."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("aaa", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response