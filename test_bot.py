import unittest
from unittest.mock import patch
import logging
import bot

logger = logging.getLogger('unittests')
logger.setLevel(logging.DEBUG)

# These are used to mock lastline.txt
line_to_tweet = 285
line_char = 0


def mock_open_sideeffect(file, mode='r', *args, **kwargs):
    """
    Sideeffect of calling open in main file, uses args to serve either the data.txt as is
    or mocked last_line.txt
    :param file: (str)filename
    :param mode: [(str)mode]
    :param args:
    :return: fileobject

    """

    logger.info("opened " + str(file))
    if file == "data.txt":
        return open("data.txt")
    elif file == 'last_line.txt':
        content = str(line_to_tweet) + '\n' + str(line_char)
    else:
        raise FileNotFoundError(file)
    file_object = unittest.mock.mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object


class TestBot(unittest.TestCase):
    """
    Mock twitter API and file opening to test bot without affecting its state

    """

    @patch('bot.tweepy.API')
    @patch('bot.open', new=mock_open_sideeffect)
    def test_run(self, mocked_api):
        bot.run()
        # Call list has all status updates, this is only to verify what the bot tweets
        # Always better to use direct assertion in tests!
        call_list = mocked_api.return_value.update_status.call_args_list
        for call in call_list:
            args, kwargs = call
            logger.debug(kwargs['status'])

            # Sample assertion
            self.assertIsInstance(kwargs['status'], str)


if __name__ == '__main__':
    unittest.main()
