from django.dispatch import Signal 

actvation_token_reset = Signal(providing_args=["token"])