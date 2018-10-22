from django.db import models
import datetime


class User(models.Model):
    fullName = models.TextField()
    email = models.TextField()
    password = models.TextField()
    status = models.IntegerField(default=1)
    verificationCode = models.TextField()
    isVerified = models.BooleanField(default=False)
    
    def _asdict(self):
        return self.__dict__
        
    def __str__(self):
        return self.fullName

class QrScanData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qrCode = models.TextField()
    scannedAt = models.DateField(("Date"), default=datetime.date.today)
    status = models.IntegerField(default=1)
