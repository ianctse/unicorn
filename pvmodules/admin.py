from django.contrib import admin

from .models import Company, Manufacturer, Certification, MfgActivity, PvModule, PvModuleDatasheet

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'parent_company', 'hq_country', 'mfg_capacity_yr', 'display_mfgactivity')

class CertificationAdmin(admin.ModelAdmin):
    list_display = ('body', 'standard', 'version')

class PvModuleAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'p_max', 'cell_count', 'cell_type', 'cell_tech', 'is_bifacial')
    list_filter = ('cell_type',)

    fieldsets = (
        (None, {
            'fields': ('manufacturer', 'model_name', 'p_max','v_sys_max', 'is_bifacial', 'has_frame', 'has_arcoat')
        }),
        ('Cell', {
            'fields': ('cell_count', 'cell_type', 'cell_tech', 'doping_type')
        }),
        ('Misc.', {
            'fields': ('certification', 'comments')
        })
    )
class PvModuleDatasheetAdmin(admin.ModelAdmin):
    list_display = ('pvmodule', 'p_max_stc', 'year_published')
    fieldsets = (
        ('Standard Testing Conditions (25C, 1kW/m^2)', {
            'fields': ('p_max_stc', 'eff_stc', 'v_mp_stc', 'i_mp_stc', 'v_oc_stc', 'i_sc_stc')
        }),
        ('Temperature Coefficients', {
            'fields': ('temp_co_p_max', 'temp_co_v_oc', 'temp_co_i_sc')
        }),
        ('Physical', {
            'fields': ('length', 'width', 'thickness', 'weight')
        })
    )

admin.site.register(Company)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(MfgActivity)
admin.site.register(PvModule, PvModuleAdmin)
admin.site.register(PvModuleDatasheet, PvModuleDatasheetAdmin)