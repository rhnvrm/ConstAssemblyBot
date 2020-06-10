import unittest
from unittest.mock import patch
import bot


def mock_open_sideeffect(*args):
    filename = args[0]
    print("opened " + str(filename))
    if filename == "data.txt":
        return open("data.txt")
    elif filename == 'last_line.txt':
        content = "0\n0"
    else:
        raise FileNotFoundError(filename)
    file_object = unittest.mock.mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object


class TestBot(unittest.TestCase):
    @patch('bot.create_api')
    @patch('bot.open', new=mock_open_sideeffect)
    def test_run(self, mock_open):
        bot.run()
        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()
