from django.db import models


class ContactMessage(models.Model):
    class Meta:
        ordering = ['timestamp']

    name = models.CharField(max_length=100, verbose_name='Your name')
    email = models.EmailField(blank=True, verbose_name='Your email')
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=10000, verbose_name='Your message')
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}from {}".format('' if self.read else 'UNREAD ', self.name)