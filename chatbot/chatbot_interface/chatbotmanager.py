import logging
import sys
import os

from chatbot import chatbot


# chatbotPath = "/".join(settings.BASE_DIR.split('/')[:-1])
chatbotPath = ""
sys.path.append(chatbotPath)

logger = logging.getLogger(__name__)


class ChatbotManager():
    """ Manage a single instance of the chatbot shared over the website
    """
    name = 'chatbot_interface'
    verbose_name = 'Chatbot Interface'

    bot = None

    def __init__(self):
        """ Called by web server only once during startup
        """
        ChatbotManager.initBot()

    @staticmethod
    def initBot():
        """ Instantiate the chatbot for later use
        Should be called only once
        """
        if not ChatbotManager.bot:
            logger.info('Initializing bot...')
            ChatbotManager.bot = chatbot.Chatbot()
            ChatbotManager.bot.main(['--modelTag', 'server', '--rootDir', chatbotPath])
        else:
            logger.info('Bot already initialized.')

    @staticmethod
    def callBot(sentence):
        """ Use the previously instantiated bot to predict a response to the given sentence
        Args:
            sentence (str): the question to answer
        Return:
            str: the answer
        """
        if ChatbotManager.bot:
            return ChatbotManager.bot.daemonPredict(sentence)
        else:
            logger.error('Error: Bot not initialized!')
