from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Member)
admin.site.register(Coach)
admin.site.register(Admin)

admin.site.register(Event)
admin.site.register(Date)
admin.site.register(Ticket)
admin.site.register(EventTicket)

admin.site.register(Program)
admin.site.register(MemberProgram)

admin.site.register(Court)
admin.site.register(CourtReservation)
