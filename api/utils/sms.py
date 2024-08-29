from abc import ABC, abstractmethod


class SMSProvider(ABC):
    @abstractmethod
    def send_sms(self, message, phone_number):
        """
        Sends an SMS message.
        """
        pass

    @property
    @abstractmethod
    def price(self):
        """
        Returns the price of the SMS service.
        """
        pass


class VodafoneSMSProvider(SMSProvider):
    def send_sms(self, message, phone_number):
        print(f"Sending SMS to {phone_number}: {message}")
        print("Vodafone")

    @property
    def price(self):
        return 0.02


class OrangeSMSProvider(SMSProvider):
    def send_sms(self, message, phone_number):
        print(f"Sending SMS to {phone_number}: {message}")
        print("Orange")

    @property
    def price(self):
        return 0.03


class SMSProviderUtils:
    @staticmethod
    def get_cheapest_sms_provider(*providers):
        """
        Return the cheapest SMS provider.
        """
        return min(providers, key=lambda provider: provider.price)
