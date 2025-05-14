from django.test import TestCase
from django.urls import reverse

from users.urls import UrlNames


class CreateUserTest(TestCase):
    def test_success(self):
        payload = self.generate_valid_payload()
        url = reverse(UrlNames.CREATE_AND_FIND_ALL_USERS)
        response = self.client.post(url, payload)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertEqual(data['data']['first_name'], payload['first_name'])
        self.assertEqual(data['data']['last_name'], payload['last_name'])
        self.assertEqual(data['data']['email'], payload['email'].lower())

    def generate_valid_payload(self):
        return {
            "first_name": "John",
            "last_name": "Due",
            "email": "johndue@email.com",
            "password": "123",
            "password_confirmation": "123"
        }

    def test_bad_request_out_range_payload(self):
        test_cases = self.__generate_out_range_payload()

        for (attribute, value, expected_error) in test_cases:
            payload = self.generate_valid_payload()
            payload[attribute] = value
            url = reverse(UrlNames.CREATE_AND_FIND_ALL_USERS)
            response = self.client.post(url, payload)
            data = response.json()
            self.assertIsNotNone(data, f'deveria ter o erro {expected_error}')
            self.assertEqual(
                data['details'],
                expected_error,
                f'{attribute} {value} deveria ter o erro {expected_error}'
            )

    def test_bad_request_none_payloads(self):
        test_cases = self.__generate_none_payloads()

        for (attribute, expected_error) in test_cases:
            payload = self.generate_valid_payload()
            payload.pop(attribute)
            url = reverse(UrlNames.CREATE_AND_FIND_ALL_USERS)
            response = self.client.post(url, payload)
            data = response.json()
            self.assertIsNotNone(data, f'deveria ter o erro {expected_error}')
            self.assertEqual(
                data['details'],
                expected_error,
                f'{attribute} deveria ter o erro {expected_error}'
            )

    def __generate_none_payloads(self):
        return [
            # empty cases
            ("first_name", {'first_name': ['This field is required.']}),
            ("last_name", {'last_name': ['This field is required.']}),
            ("email", {'email': ['This field is required.']}),
            ("password", {'password': ['This field is required.']}),
            ("password_confirmation", {'password_confirmation': ['This field is required.']}),
        ]

    def __generate_out_range_payload(self):
        return [
            # empty cases
            ("first_name", '', {'first_name': ['This field may not be blank.']}),
            ("last_name", '', {'last_name': ['This field may not be blank.']}),
            ("email", '', {'email': ['This field may not be blank.']}),
            ("password", '', {'password': ['This field may not be blank.']}),
            ("password_confirmation", '', {'password_confirmation': ['This field may not be blank.']}),

            # bigger cases
            ("first_name", 'a' * 101, {'first_name': ['Ensure this field has no more than 100 characters.']}),
            ("last_name", 'a' * 101, {'last_name': ['Ensure this field has no more than 100 characters.']}),
            ("email", 'a' * 101,
             {'email': ['Ensure this field has no more than 100 characters.', 'Enter a valid email address.']}),
            ("password", 'a' * 101, {'password': ['Ensure this field has no more than 100 characters.']}),
            ("password_confirmation", 'a' * 101,
             {'password_confirmation': ['Ensure this field has no more than 100 characters.']}),
        ]
