from django.db import models

# class Contact(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField()
#     phone = models.CharField(max_length=30)
#     desc = models.TextField()


class Mappings (models.Model):
    OM = models.CharField(max_length=30)
    MDM = models.CharField(max_length=30)
    OCEP =models.CharField(max_length=30)
    OCED =models.CharField(max_length=30)
    


class MDM (models.Model):
    First_name1 =models.CharField(max_length=30)
    Last_name1 =models.CharField(max_length=30)
    Country1 =models.CharField(max_length=30)
    ID1 = models.IntegerField()
    Address1 =models.CharField(max_length=100)
    Entity_type1=models.CharField(max_length=30)
    Speciality1 =models.CharField(max_length=30)

class OCEP(models.Model):
    First_name4 = models.CharField(max_length=30)
    Last_name4 = models.CharField(max_length=30)
    Country4 = models.CharField(max_length=30)
    OCEP_ID4 = models.IntegerField()
    Address4 = models.CharField(max_length=100)
    Entity_type4 = models.CharField(max_length=30)
    Speciality4 =models.CharField(max_length=30)

class OCED (models.Model):
    First_name2 =models.CharField(max_length=30)
    Last_name2 =models.CharField(max_length=30)
    Country2 =models.CharField(max_length=30)
    OCED_ID2 = models.IntegerField()
    Address2 =models.CharField(max_length=30)
    Entity_type2 =models.CharField(max_length=30)
    Speciality2 =models.CharField(max_length=30)

class OM (models.Model):
    First_name3 =models.CharField(max_length=30)
    Last_name3 =models.CharField(max_length=30)
    Country3 =models.CharField(max_length=30)
    OM_ID3 = models.IntegerField()
    Entity_type3 =models.CharField(max_length=30)
    Territory3 =models.CharField(max_length=30)


