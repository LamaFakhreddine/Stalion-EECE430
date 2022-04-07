from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(EventTicket)
admin.site.register(Program)
admin.site.register(Date)
