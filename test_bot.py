import unittest
from unittest.mock import patch
import logging
import bot

logger = logging.getLogger('unittests')
logger.setLevel(logging.DEBUG)

# These are used to mock lastline.txt
def gen_mock_fopen(line_to_tweet, line_char):
    """
    Sideeffect generator that sets the expected
    last_line.txt data.
    :param line_to_tweet: (int) represents row in data.txt
    :param line_char: (int) represents coloum in data.txt
    :return: function
    """
    def mock_fopen(file, mode='r', *args, **kwargs):
        """
        Sideeffect for calling open in main file,
        uses args to serve either the data.txt as is
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

    return mock_fopen

class TestBot(unittest.TestCase):
    """
    Mock twitter API and file opening to test bot without affecting its state

    """

    @patch('bot.tweepy.API')
    @patch('bot.open', new=gen_mock_fopen(45,0))
    def test_basic(self, mocked_api):
        bot.run()

        # Get the args list from update_status
        call_list = mocked_api.return_value.update_status.call_args_list

        # len should be 1
        self.assertEqual(len(call_list), 1)

        # check the status
        args, kwargs = call_list[0]
        logger.debug(kwargs['status'])
        expected = 'The Chairman\nThe next message is from the Embassy of the Republic of China - New Delhi.'
        self.assertEqual(kwargs['status'], expected)

    @patch('bot.tweepy.API')
    @patch('bot.open', new=gen_mock_fopen(1908,2729))
    def test_multiline(self, mocked_api):
        bot.run()

        # Get the args list from update_status
        call_list = mocked_api.return_value.update_status.call_args_list

        # len should be 2
        self.assertEqual(len(call_list), 2)

        # check the first status 
        args, kwargs = call_list[0]
        logger.debug(kwargs['status'])
        expected = 'Of course, if the idea of some people is to ignore those limitations altogether and convert this Constituent Assembly into a force for gaining political power, irrespective of the limitations of this Paper, to seize power and thereby create'
        self.assertEqual(kwargs['status'], expected)

        # check the second status
        args, kwargs = call_list[1]
        logger.debug(kwargs['status'])
        expected = ' a revolution in the country, that is outside the present plan, and I have nothing to say about it.'
        self.assertEqual(kwargs['status'], expected)


    @patch('bot.tweepy.API')
    @patch('bot.open', new=gen_mock_fopen(285, 0))
    def test_multiline_split(self, mocked_api):
        bot.run()

        # Get the args list from update_status
        call_list = mocked_api.return_value.update_status.call_args_list

        # len should be 2
        self.assertEqual(len(call_list), 2)

        # check the first status
        args, kwargs = call_list[0]
        logger.debug(kwargs['status'])
        expected = '(6)Where at any ballot any of three or more candidates obtain an equal number of votes and one of them has to be excluded from the election under rule (4) the determination as between the candidates whose votes are equal of the candidate'
        self.assertEqual(kwargs['status'], expected)

        # check the second status
        args, kwargs = call_list[1]
        logger.debug(kwargs['status'])
        expected = 'who is to be excluded shall be by the drawing of lots\".'
        self.assertEqual(kwargs['status'], expected)


if __name__ == '__main__':
    unittest.main()
