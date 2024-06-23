from django.db import models
import uuid
# Is model ko apne entire project ma use kare ga .... isi lya hum ise product app k models file ma import ker ly aga.


# Django ma jab bhi hum koi model ki class bnate hai tu wo ose data(sql) consider kerta hai.
# Tu isi lya hum is ma k under 'meta' name ki key dalte hai jis se django is class consider kera ga.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

# this tell django to don't create database table.
    class Meta:
        abstract = True
