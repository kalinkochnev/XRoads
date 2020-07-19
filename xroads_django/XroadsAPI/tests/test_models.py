from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.test import TestCase
from parameterized import parameterized
from XroadsAPI.models import Profile


class TestProfileModel(TestCase):
    def setUp(self):
        self.email = "kalin.kochnev@gmail.com"
        self.password = "2323hj23hk2h"
        self.first_name = "kalin"
        self.last_name = "kochnev"
        self.phone_number_str = '518-888-1542'
        self.phone_number_int = 5188881542
        self.is_anon = True

    @parameterized.expand([
        # phone number, expected value
        ['518-888-1542', "5188881542"],
        ['(518) 888-1542', "5188881542"],
        ['518 888 1542', "5188881542"],
        ['5 1 8 8 8 8 1 5 4 2', "5188881542"]
    ])
    def test_parse_phone_valid_len(self, input_phone, expected):
        self.assertEqual(Profile.parse_phone(input_phone), expected)

    @parameterized.expand(['518-888-154211111', '123-4567', '12345678'])
    def test_parse_phone_invalid_len(self, input_phone):
        with self.assertRaises(FieldError) as context:
            Profile.parse_phone(input_phone)

    def test_creation_optional(self):
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name)
        self.assertIsNone(prof.phone_num)
        self.assertFalse(prof.is_anon)

        user_obj = prof.user
        self.assertEqual(user_obj.first_name, self.first_name)
        self.assertEqual(user_obj.last_name, self.last_name)
        self.assertEqual(user_obj.email, self.email)

    def test_creation_all_params(self):
        prof: Profile = Profile.create_profile(email=self.email, password=self.password, first=self.first_name,
                                               last=self.last_name, phone=self.phone_number_str, is_anon=self.is_anon)
        self.assertEqual(prof.phone_num, self.phone_number_int)
        self.assertEqual(prof.is_anon, self.is_anon)


if __name__ == '__main__':
    unittest.main()
