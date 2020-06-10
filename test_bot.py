import unittest
from unittest.mock import patch
import bot

# These are used to mock lastline.txt
line_to_tweet = 8
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

    print("opened " + str(file))
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
    @patch('bot.tweepy')
    @patch('bot.open', new=mock_open_sideeffect)
    def test_run(self, mock_open):
        bot.run()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
