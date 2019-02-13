from django.db import models

class Company(models.Model):
    """ Any company or legal entity """
    # FIELDS
    legal_name = models.CharField(max_length=50, null=True)
    short_name = models.CharField(max_length=20, db_index=True)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    # TO STRING METHOD
    def __str__(self):
        return self.short_name

class Device(models.Model):
    """ Major PV power system device or component """
    # FIELDS
    manufacturer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='devices')
    model_name = models.CharField(max_length=50)

    # META CLASS
    class Meta:
        abstract = True
        ordering = ['manufacturer', 'model_name']
    
    # TO STRING METHOD
    def __str__(self):
        return '%s %s' % (self.manufacturer, self.model_name)

class PvCellTechnology(models.Model):
    """ Photovoltaic cell technology type """
    # CHOICES
    MONO_SILICON = 'Mono_Si'
    POLY_SILICON = 'Poly_Si'
    MONO_PERC = 'Mono_PERC'
    POLY_PERC = 'Poly_PERC'
    CADMIUM_TELURIDE = 'CdTe'
    CELL_TYPE_CHOICES = (
        (MONO_SILICON, 'Mono-crystaline silicon'),
        (POLY_SILICON, 'Poly-crystaline silicon'),
        (MONO_PERC, 'Mono-crystaline silicon with PERC'),
        (POLY_PERC, 'Poly-crystaline silicon with PERC'),
        (CADMIUM_TELURIDE, 'Cadmium Teluride thin film')
    )

    # FIELDS
    name = models.CharField(max_length=50, choices=CELL_TYPE_CHOICES)
    description = models.TextField('description of cell technology', blank=True, null=True)

class PvModule(Device):
    """ A photovoltaic panel """
    # FIELDS
    length = models.DecimalField('length of longest module dimension in mm', max_digits=6, decimal_places=2, null=True)
    width = models.DecimalField('length of 2nd longest module dimension in mm', max_digits=6, decimal_places=2, null=True)
    thickness = models.DecimalField('thickness of module in mm', max_digits=6, decimal_places=3, null=True)
    weight = models.DecimalField('weight in kg', max_digits=6, decimal_places=3, null=True)

    is_bifacial = models.BooleanField(null=True)
    cell_type = models.ForeignKey(PvCellTechnology, on_delete=models.PROTECT, related_name='pvmodules', blank=True, null=True)
    cell_count = models.PositiveSmallIntegerField('number of solar cells per module', null=True)
    p_max = models.DecimalField('rated max power bin in W', max_digits=6, decimal_places=2, null=True)
    v_sys_max = models.DecimalField('max system dc voltage', max_digits=6, decimal_places=2, null=True)
    
class PvModuleDatasheet(models.Model):
    """ Datasheet specifications for pv modules """
    # FIELDS
    pvmodule = models.ForeignKey(PvModule, on_delete=models.CASCADE, related_name='datasheets')
    p_max_stc = models.DecimalField('max power output at stc in W', max_digits=6, decimal_places=2, null=True)
    eff_stc = models.DecimalField('module efficiency at stc in percent', max_digits=6, decimal_places=2, null=True)
    v_mp_stc = models.DecimalField('voltage at p_max_stc', max_digits=6, decimal_places=2, null=True)
    i_mp_stc = models.DecimalField('current at p_max_stc', max_digits=6, decimal_places=2, null=True)
    v_oc_stc = models.DecimalField('open circuit voltage at stc', max_digits=6, decimal_places=2, null=True)
    i_sc_stc = models.DecimalField('short circuit at stc', max_digits=6, decimal_places=2, null=True)
    temp_co_p_max = models.DecimalField('temperature coefficient of power', max_digits=6, decimal_places=2, null=True)
    temp_co_v_oc = models.DecimalField('temperature coefficient of open circuit voltage', max_digits=6, decimal_places=2, null=True)
    temp_co_i_sc = models.DecimalField('temperature coefficient of short circuit current', max_digits=6, decimal_places=2, null=True)

    date_late_updated = models.DateField()
    # Add FileField later

# class PvModuleModelParams(models.Model):
    # Add modeling parameters
    # Need to add software/model type?

# class PvModuleWarranty(model.Model):
    # Add attributes related to module warranties