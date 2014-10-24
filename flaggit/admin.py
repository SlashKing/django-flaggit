from django.contrib import admin
from django.core.urlresolvers import reverse

from flaggit.models import Flag, Reason, FlagInstance, CONTENT_APPROVED, \
    CONTENT_REJECTED
from datetime import datetime


class FlagAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('status', 'link', 'created',
        'reviewer', 'reviewed', 'num_flags')

    actions = ['approve', 'reject']
    actions_on_bottom = True

    def num_flags(self, obj):
        return obj.flags.all().count()

    def link(self, obj):
        """give an amdin link"""
        try:
#             import pdb;pdb.set_trace()
            link = u'<a href="%s">%s</a>' % (reverse("admin:%s_%s_change" % (obj.content_object._meta.app_label,
                                                                             obj.content_object._meta.object_name.lower()),
                                                     args=(obj.content_object.id,)),
                                             obj.content_object)
            return link
        except TypeError:
            return
    link.allow_tags = True

    def approve(self, request, queryset):
        for obj in queryset:
            obj.status = CONTENT_APPROVED
            obj.reviewer = request.user
            obj.reviewed = datetime.now()
            obj.save()
    approve.short_description = "Approve content on selected flags. (Save content)"

    def reject(self, request, queryset):
        for obj in queryset:
            obj.status = CONTENT_REJECTED
            obj.save()
    reject.short_description = "Reject content on selected flags. (Delete content)"

    def get_actions(self, request):
        actions = super(FlagAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Flag, FlagAdmin)
admin.site.register(FlagInstance)
admin.site.register(Reason)
