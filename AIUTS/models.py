from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accountId = models.CharField(primary_key=True,max_length=255,)
    accountAmount = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.user}"

    '''
    everytime the user is create, it will add to a users group directly
    '''
    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, **kwargs):
        if created:
            print(User.username)
            # UserAccount.objects.create(user=instance)
            print('User create')
            instance.groups.add(Group.objects.get(name='users'))
            print('User add to group')
            

    # post_save.connect(create_account, sender=User)


class UserTransaction(models.Model):
    STATUS = (('Pending', 'Pending'),('Approve', 'Approve'))
    transactionId = models.AutoField(primary_key=True)
    transactionTime = models.DateTimeField(auto_now_add=True)
    transactionSender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="Sender")
    transactionReceiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="Receiver")
    transactionAmount = models.IntegerField(default=0)
    transactionMessage = models.CharField(max_length=100, null=True)
    transactionStatus =  models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])
    
    def __str__ (self):
        return "{}".format(self.transactionTime)

    def save(self, *args, **kwargs):
        if self.transactionStatus == 'Approve':
            print("Approve")

            self.transactionSender.accountAmount -= self.transactionAmount
            self.transactionSender.save()
            self.transactionReceiver.accountAmount += self.transactionAmount
            self.transactionReceiver.save()

            super(UserTransaction, self).save(*args, **kwargs)

        if self.transactionStatus == 'Pending':
            print("pending")
            super(UserTransaction, self).save(*args, **kwargs)

class DepositRequest(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Approve', 'Approve')
		)
    DepositRequestID = models.AutoField(primary_key=True)
    RequestTime = models.DateTimeField(auto_now_add=True)
    RequestReceiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="RequestReceiver")
    RequestAmount = models.IntegerField(default=100)
    RequestStatus =  models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])

    def __str__(self):
        return f"{self.RequestReceiver}"

    def save(self, *args, **kwargs):
        if self.RequestStatus == 'Approve':
            self.RequestReceiver.accountAmount += self.RequestAmount
            self.RequestReceiver.save()

            super(DepositRequest, self).save(*args, **kwargs)
        if self.RequestStatus == 'Pending':
            super(DepositRequest, self).save(*args, **kwargs)



        
   
