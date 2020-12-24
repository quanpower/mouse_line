from django.db import models

class ListModel(models.Model):
    driver_name = models.CharField(max_length=255, verbose_name="Driver Name")
    license_plate = models.CharField(max_length=255, verbose_name="License Plate")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'driver'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['driver_name']

    def __str__(self):
        return self.pk
