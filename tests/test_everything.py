import unittest
from io import StringIO
import sys
from unittest.mock import patch, mock_open
import src.login_signup.bankLoginService as bls 
from src.login_signup.bankSignUpService import *
from src.transact.transact_impl import *
from functions import *

class TestEverything(unittest.TestCase):

    # --- Consolidation Functions Tests ---
    def test_fibonacci(self):
        # Test small cases and a longer sequence
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual([fibonacci(n) for n in range(15)],
                         [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377])
        self.assertEqual([fibonacci(n) for n in range(30)][-1], 514229)

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        # Check negative input returns empty string (or your error code)
        self.assertEqual(factorial(-1), "")

    def test_find_max_and_odd_numbers(self):
        self.assertEqual(find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(find_odd_numbers([1, 9, 11, 16, 20]), (1, 9, 11))
        self.assertEqual(find_number_of_even_numbers([1, 2, 3, 4, 5]), 2)

    def test_matrix_multiply(self):
        matrix_a = [[1, 2, 3],
                    [4, 5, 6]]
        matrix_b = [[7, 8],
                    [9, 10],
                    [11, 12]]
        self.assertEqual(matrix_multiply(matrix_a, matrix_b), [[58, 64], [139, 154]])
        # Test invalid dimensions raise ValueError
        matrix_b_bad = [[7, 8, 9],
                        [10, 11, 12]]
        with self.assertRaises(ValueError):
            matrix_multiply(matrix_a, matrix_b_bad)

    def test_generate_squared_dict(self):
        self.assertEqual(generate_squared_dict(5), {1: 1, 2: 4, 3: 9, 4: 16, 5: 25})
        self.assertEqual(generate_squared_dict(0), {})
        self.assertEqual(generate_squared_dict(-3), {-3: 9, -2: 4, -1: 1})

    def test_binary_conversion(self):
        self.assertEqual(binary_conversion("0"), "0")
        self.assertEqual(binary_conversion("10101"), "21")
        self.assertEqual(binary_conversion("000110"), "6")
        self.assertEqual(binary_conversion("111001"), "57")
        self.assertEqual(binary_conversion("onezero"), "Error: Not a binary number.")

    def test_pascals_triangle(self):
        self.assertEqual(pascals_triangle(0), [1])
        self.assertEqual(pascals_triangle(1), [1, 1])
        self.assertEqual(pascals_triangle(5), [1, 5, 10, 10, 5, 1])

    def test_palindrome_words(self):
        self.assertTrue(is_palindrome_iterative("radar"))
        self.assertTrue(is_palindrome_iterative("Level"))
        self.assertTrue(is_palindrome_iterative("NoOn"))
        self.assertFalse(is_palindrome_iterative("hello"))
        self.assertFalse(is_palindrome_iterative("world"))

    def test_punnett_square(self):
        # Basic test: heterozygous for two traits
        result = punnett_square("Aa", "Bb")
        expected = [["AB", "Ab"], ["aB", "ab"]]
        self.assertEqual(result, expected)

    def test_dna_protein(self):
        # Valid: length divisible by 3, starts with ATG and has a stop codon at end
        self.assertTrue(dna_protein("ATGCGATACTGA"))
        # Invalid: length not divisible by 3
        self.assertFalse(dna_protein("ATGCGATAGA"))
        # Invalid: no start codon
        self.assertFalse(dna_protein("CGATACTGA"))
        # Invalid: no stop codon
        self.assertFalse(dna_protein("ATGCGATACT"))
        # Too short to be valid
        self.assertFalse(dna_protein("ATG"))

    def test_text_processing(self):
        # Test converting sentence to list of words
        sentence = ("There is only one to fear and his name is Death,"
                    " and there is only one thing we say to Death: 'Not today!")
        words = convert_to_word_list(sentence)
        self.assertEqual(words, ['there', 'is', 'only', 'one', 'to', 'fear', 'and',
                                 'his', 'name', 'is', 'death', 'and', 'there', 'is',
                                 'only', 'one', 'thing', 'we', 'say', 'to', 'death', 
                                 'not', 'today'])
        # Test letters count map (at least a few letters exist)
        count_map = letters_count_map("Hello World!")
        self.assertTrue(count_map['h'] > 0)
        self.assertTrue(count_map['w'] > 0)

    def test_text_to_morse(self):
        self.assertEqual(text_to_morse("Hello World 123"),
                         ".... . .-.. .-.. ---   .-- --- .-. .-.. -..   .---- ..--- ...--")
        self.assertEqual(text_to_morse(",:?!'"),
                         "--..-- ---... ..--.. -.-.-- .----.")

    # --- Data Structures Functions Tests ---
    def test_list_statistics(self):
        stats = return_list_stats([1, 2, 3, 4, 5])
        self.assertEqual(stats["min"], 1)
        self.assertEqual(stats["max"], 5)
        self.assertAlmostEqual(stats["average"], 3.0)
        self.assertEqual(stats["even_numbers"], (2, 4))
        self.assertEqual(stats["odd_numbers"], (1, 3, 5))
        self.assertEqual(stats["number_of_even_numbers"], 2)
        self.assertEqual(stats["number_of_odd_numbers"], 3)
        self.assertEqual(stats["unique_numbers"], {1, 2, 3, 4, 5})

    def test_process_characters(self):
        input_list = ['a', '1', 'B', '2', '@', 'z']
        alphabets, numbers = process_characters(input_list)
        self.assertEqual(alphabets, ['a', 'B', 'z'])
        self.assertEqual(numbers, [1, 2])

    # --- Transaction (CSV) Tests ---
    def test_get_user_data_found(self):
        sample_csv = (
            "username,password,cheque_account_balance,savings_account_balance,investment_account_balance\n"
            "johndoe,pass123,1500,3000,5000\n"
            "janedoe,pass456,2000,4000,6000\n"
        )
        with patch('builtins.open', mock_open(read_data=sample_csv)):
            user = get_user_data("johndoe")
            self.assertIsNotNone(user)
            self.assertEqual(user["username"], "johndoe")
            self.assertEqual(user["cheque_account_balance"], "1500")
    
    def test_get_user_data_not_found(self):
        sample_csv = (
            "username,password,cheque_account_balance,savings_account_balance,investment_account_balance\n"
            "johndoe,pass123,1500,3000,5000\n"
        )
        with patch('builtins.open', mock_open(read_data=sample_csv)):
            self.assertIsNone(get_user_data("nonexistent"))
    
    def test_get_user_data_file_error(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            self.assertIsNone(get_user_data("johndoe"))

    # --- Login Tests ---
    def test_login_function(self):
        sample_login_data = "username,password\njohndoe,secure123\njanedoe,abc123\n"
        with patch('builtins.open', mock_open(read_data=sample_login_data)):
            result, _ = bls.login("johndoe", "secure123")
            self.assertTrue(result)
            result, _ = bls.login("johndoe", "wrongpassword")
            self.assertFalse(result)
            result, _ = bls.login("nonexistent", "nopass")
            self.assertFalse(result)

    def test_login_empty_fields(self):
        sample_login_data = "username,password\njohndoe,secure123\n"
        with patch('builtins.open', mock_open(read_data=sample_login_data)):
            result, _ = bls.login("", "secure123")
            self.assertFalse(result)
            result, _ = bls.login("johndoe", "")
            self.assertFalse(result)

    # --- Sign-Up Tests ---
    def test_sign_up_success(self):
        with patch('src.login_signup.bankSignUpService.user_exists', return_value=False), \
             patch('src.login_signup.bankSignUpService.write_user_data') as write_data_mock, \
             patch('builtins.input', side_effect=['newuser', 'newpass', 'newpass']), \
             patch('builtins.print') as print_mock:
            result = sign_up()
            self.assertTrue(result)
            write_data_mock.assert_called_once_with('newuser', 'newpass')
            print_mock.assert_called_with("Registration successful. You can now log in.")

    def test_sign_up_existing(self):
        with patch('src.login_signup.bankSignUpService.user_exists', return_value=True), \
             patch('builtins.input', return_value='existinguser'), \
             patch('builtins.print') as print_mock:
            result = sign_up()
            self.assertFalse(result)
            print_mock.assert_called_with("This username already exists. Please choose a different one.")

    def test_sign_up_password_mismatch(self):
        with patch('src.login_signup.bankSignUpService.user_exists', return_value=False), \
             patch('src.login_signup.bankSignUpService.write_user_data') as write_data_mock, \
             patch('builtins.input', side_effect=['newuser', 'pass1', 'pass2']), \
             patch('builtins.print') as print_mock:
            with self.assertRaises(StopIteration):
                sign_up()
            write_data_mock.assert_not_called()
            print_mock.assert_called_with("Passwords do not match. Please try again.")

    # --- Patterns Tests ---
    def test_patterns_get_shape_and_height(self):
        # Test get_shape (simulate user input)
        with patch("sys.stdin", StringIO("Square\n")), \
             patch("sys.stdout", new_callable=StringIO):
            self.assertEqual(patterns.get_shape(), "square")
        with patch("sys.stdin", StringIO("7\n")), \
             patch("sys.stdout", new_callable=StringIO):
            height = patterns.get_height()
            self.assertIsInstance(height, int)
    
    def test_draw_square(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_square(4)
            expected = "****\n****\n****\n****\n"
            self.assertEqual(fake_out.getvalue(), expected)

    def test_draw_triangle_reversed(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_triangle_reversed(3)
            expected = "1 1 1 \n2 2 \n3 \n"
            self.assertEqual(fake_out.getvalue(), expected)

    def test_draw_triangle(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_triangle(3)
            expected = "1 \n1 2 \n1 2 3 \n"
            self.assertEqual(fake_out.getvalue(), expected)

    def test_draw_triangle_multiplication(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_triangle_multiplication(5)
            expected = ("1 \n2 4 \n3 6 9 \n4 8 12 16 \n5 10 15 20 25 \n")
            self.assertEqual(fake_out.getvalue(), expected)

    def test_draw_pyramid(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_pyramid(3)
            expected = "  *\n ***\n*****\n"
            self.assertEqual(fake_out.getvalue(), expected)

    def test_draw_triangle_prime(self):
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            patterns.draw_triangle_prime(5)
            expected = ("2 \n3 5 \n7 11 13 \n17 19 23 29 \n31 37 41 43 47 \n")
            self.assertEqual(fake_out.getvalue(), expected)

    def test_tower_of_hanoi(self):
        result = patterns.tower_of_hanoi(3, 'A', 'B', 'C')
        expected = [('A', 'C'), ('A', 'B'), ('C', 'B'),
                    ('A', 'C'), ('B', 'A'), ('B', 'C'),
                    ('A', 'C')]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
