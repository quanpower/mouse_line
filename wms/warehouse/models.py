from django.db import models

class ListModel(models.Model):
    warehouse_name = models.CharField(max_length=255, verbose_name="Warehouse Name")
    warehouse_city = models.CharField(max_length=255, verbose_name="Warehouse Name")
    warehouse_address = models.CharField(max_length=255, verbose_name="Warehouse Address")
    warehouse_contact = models.IntegerField(default=0, verbose_name="Warehouse Contact")
    warehouse_manager = models.CharField(max_length=255, verbose_name="Warehouse Manager")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'warehouse'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['warehouse_name']

    def __str__(self):
        return self.pk
