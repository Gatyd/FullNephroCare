from django.contrib import admin
from .models import AlerteCritere, Notification, ReglageNotification

@admin.register(AlerteCritere)
class AlerteCritereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_alerte', 'actif', 'createur') #, 'priorite'
    list_filter = ('type_alerte', 'actif') #, 'priorite'
    search_fields = ('nom', 'description')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_notification', 'patient', 'destinataire', 'date_creation')#, 'lue'
    list_filter = ('type_notification', 'destinataire')#, 'lue'
    search_fields = ('titre', 'message', 'patient__nom')
    date_hierarchy = 'date_creation'

@admin.register(ReglageNotification)
class ReglageNotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'recevoir_alertes', 'email_actif')#, 'recevoir_rappels', 'priorite_minimum'
    list_filter = ('recevoir_alertes', 'email_actif')#, 'recevoir_rappels'
    search_fields = ('utilisateur__username', 'utilisateur__email')