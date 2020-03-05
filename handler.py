import json
import logging
import s3util
import util

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
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
    sb.add_request_handler(CancelOrStopIntentHandler())

    sb.add_exception_handler(AllExceptionHandler())

    handler = sb.lambda_handler()

    return handler(event, context)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to Farsi dictionary, ask any word I will happy to answer"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("launch", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        logger.info('CancelOrStopIntentHandler')

        handler_input.response_builder.speak("Bye").set_card(
            SimpleCard("Hello World", "Bye"))
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        logger.info('AllExceptionHandler')
        logger.info('locale')
        locale = handler_input.request_envelope.request.locale
        logger.info(locale)

        speech_text = "Internal Error"

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class QuestionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("question")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Tell us about Lexis Noah's philosophy

        logger.info('request')
        logger.info(handler_input.request_envelope)

        logger.info('question')

        slots = handler_input.request_envelope.request.intent.slots
        logger.info('slots')
        logger.info(slots)

        word_slot = slots['word']
        logger.info('slot')
        logger.info(word_slot)

        logger.info('value')
        word = word_slot.value
        logger.info(word)

        words = ["able", "ability", "absence", "absolute", "abroad", "abortion"]
        if word in words:
            logger.info('signed_url')
            signed_url = s3util.create_presigned_url("farsi-dic", "%s.%s" % (word, "mp3"))
            logger.info(signed_url)
            return util.play(url=signed_url, offset=0, text=word,
                             card_data=None, response_builder=handler_input.response_builder)

        speech_text = "I don't know the word %s" % word
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("aaa", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response