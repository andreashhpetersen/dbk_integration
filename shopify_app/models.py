import shopify
from django.db import models


class DbkOrder(models.Model):
    # Id of the Shopify Order
    order_id = models.BigIntegerField()
    order_number = models.IntegerField()

    # Dates and times
    created_at = models.DateTimeField()
    processed_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)

    # Track and trace number
    tnt_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "#" + str(self.order_number)

    def get_shop_instance(self):
        """
        Get the Order object from Shopify
        """
        return shopify.Order.find(self.order_id)
