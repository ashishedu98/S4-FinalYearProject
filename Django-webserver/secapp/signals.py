from django.dispatch import Signal

image_signal = Signal(providing_args=["newface","hasreceived"])