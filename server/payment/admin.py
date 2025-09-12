from django.contrib import admin

from server.payment.models import Payment, Collect

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin class for Payment model."""

    list_display = ('id', 'amount', 'comment', 'user__username')
    search_fields = ('user__username',)
    list_filter = ('user__username',)
    list_display_links = ('user__username',)


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title', 
        'description', 
        'user__username',
        'current_amount',
        'target_amount',
        'donators_count',
    )
    search_fields = ('user__username',)
    list_filter = ('title', 'target_amount')
    list_display_links = ('user__username',)
