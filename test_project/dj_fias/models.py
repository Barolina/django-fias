from django.db import models

# Create your models here.

# Create your models here.

from fias.fields import AddressField, ChainedAreaField
from fias.models import AddrObj, FIASAddress, FIASAddressWithArea, FIASHouse
#

class Item(models.Model):
    title = models.CharField('title', max_length=100)
    location = AddressField()


class ItemWithArea(models.Model):
    title = models.CharField('title', max_length=100)

    location = AddressField()

    area = ChainedAreaField(AddrObj, address_field='location', related_name='+')
