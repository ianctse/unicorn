from django.db import models
from django_countries.fields import CountryField

class Company(models.Model):
    """ Any company or legal entity """
    # FIELDS
    legal_name = models.CharField('legal name', max_length=50, null=True)
    short_name = models.CharField('short name', max_length=20, unique=True)
    hq_city = models.CharField('headquarter city', max_length=50, null=True)
    hq_country = CountryField('headquarter country', null=True)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    # META CLASS
    class Meta:
        ordering = ['short_name']

    # METHODS
    def __str__(self):
        return self.short_name

class Certification(models.Model):
    """ Certification standards """
    # FIELDS
    body = models.ForeignKey('Company', on_delete=models.PROTECT, verbose_name='certification body', null=True)
    standard = models.CharField('standard id', max_length=20)
    version = models.CharField('version/year', max_length=20, blank=True, null=True)
    comments = models.TextField('comments', blank=True, null=True)

    # META CLASS
    class Meta:
        ordering = ['body', 'standard', '-version']

    # METHODS
    def __str__(self):
        return '%s %s' % (self.body, self.standard)



class MfgActivity(models.Model):
    """ Manufacturing activites """
    # FIELDS
    name = models.CharField('description', max_length=144, unique=True)
    comments = models.TextField('comments', blank=True, null=True)

    # META CLASS
    class Meta:
        ordering = ['name']

    # METHODS
    def __str__(self):
        return self.name

class Manufacturer(Company):
    """ A company that manufactures devices """
    # FIELDS
    mfg_experience = models.CharField('manufacturing experience', max_length=280, null=True)
    mfg_capacity_yr = models.DecimalField('manufacturing capacity [GW/yr]', max_digits=6, decimal_places=3, blank=True, null=True)
    mfg_country = CountryField('manufacturing location(s)', multiple=True)
    mfg_activity = models.ManyToManyField('MfgActivity', verbose_name='manufacturing activity(s)', related_name='manufacturers')
    comments = models.TextField('comments', blank=True, null=True)

    # METHODS
    def display_mfgcountry(self):
        return ', '.join(country for country in self.mfg_country.all()[:3])
    
    def display_mfgactivity(self):
        return ', '.join(activity.name for activity in self.mfg_activity.all()[:3])
    
    display_mfgcountry.short_description = 'Hello World.'
    display_mfgactivity.short_description = 'Mfg Activity'

class Device(models.Model):
    """ Major PV power system device or component """
    # FIELDS
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='devices')
    model_name = models.CharField('model name', max_length=50)

    # META CLASS
    class Meta:
        abstract = True
        ordering = ['manufacturer', 'model_name']
    
    # METHODS
    def __str__(self):
        return '%s %s' % (self.manufacturer, self.model_name)

class PvModule(Device):
    """ A photovoltaic panel """
    # CHOICES - these can all be classes of their own
    CELL_TYPE_CHOICES = (
        (None, 'unknown'),
        ('monosi', 'Mono-Si'),
        ('polysi', 'Poly-Si'),
        ('cdte', 'CdTe'),
        ('cigs', 'CIGS/CIS')
    )
    DOPING_TYPE_CHOICES = (
        (None, 'unknown'),
        ('p', 'p-type'),
        ('n', 'n-type'),
        ('na', 'N/A')
    )
    CELL_TECH_CHOICES = (
        (None, 'unknown'),
        ('perc', 'PERC/PERL'),
        ('pert', 'PERT'),
        ('backcontact', 'Back contact'),
        ('hit', 'HJ/HIT'),
        ('ibc', 'IBC'),
        ('hjibc', 'HJ-IBC')
    )

    # FIELDS
    p_max = models.DecimalField('rated max power [W]', max_digits=6, decimal_places=2, null=True)
    v_sys_max = models.DecimalField('max system voltage [Vdc]', max_digits=6, decimal_places=2, null=True)
    cell_count = models.PositiveSmallIntegerField('number of cells', null=True)
    cell_type = models.CharField('cell type', max_length=20, choices=CELL_TYPE_CHOICES, blank=True)
    doping_type = models.CharField('doping type', max_length=20, choices=DOPING_TYPE_CHOICES, blank=True)
    cell_tech = models.CharField('cell technology', max_length=20, choices=CELL_TECH_CHOICES, blank=True)

    is_bifacial = models.BooleanField('is bifacial', null=True)
    has_frame = models.BooleanField('has frame', null=True)
    has_arcoat = models.BooleanField('has AR coating', null=True)

    certification = models.ManyToManyField('Certification', verbose_name='certification(s)', related_name='pvmodules', blank=True, null=True)    
    
    comments = models.TextField('comments', blank=True, null=True)

    # METHODS
    def display_certifications(self):
        return ', '.join(cert.body + ' ' + cert.standard for cert in self.certification.all()[:3])
    
    display_certifications.short_description = 'Certifications'
    
class PvModuleDatasheet(models.Model):
    """ Datasheet specifications for pv modules """
    # FIELDS
    pvmodule = models.ForeignKey(PvModule, on_delete=models.CASCADE, related_name='datasheets')
    year_published = models.SmallIntegerField('year published', blank=True, null=True)

    p_max_stc = models.DecimalField('max power @STC [W]', max_digits=6, decimal_places=2, null=True)
    eff_stc = models.DecimalField('efficiency @STC [%]', max_digits=6, decimal_places=2, null=True)
    v_mp_stc = models.DecimalField('voltage @STC [Vdc]', max_digits=6, decimal_places=2, null=True)
    i_mp_stc = models.DecimalField('current @STC [A]', max_digits=6, decimal_places=2, null=True)
    v_oc_stc = models.DecimalField('open-circuit voltage @STC [Vdc]', max_digits=6, decimal_places=2, null=True)
    i_sc_stc = models.DecimalField('short-circuit current @STC [A]', max_digits=6, decimal_places=2, null=True)
    temp_co_p_max = models.DecimalField('temperature coefficient of power', max_digits=6, decimal_places=2, null=True)
    temp_co_v_oc = models.DecimalField('temperature coefficient of V_oc', max_digits=6, decimal_places=2, null=True)
    temp_co_i_sc = models.DecimalField('temperature coefficient of I_sc', max_digits=6, decimal_places=2, null=True)

    length = models.DecimalField('length [mm]', max_digits=6, decimal_places=2, null=True)
    width = models.DecimalField('width [mm]', max_digits=6, decimal_places=2, null=True)
    thickness = models.DecimalField('thickness [mm]', max_digits=6, decimal_places=3, null=True)
    weight = models.DecimalField('weight [kg]', max_digits=6, decimal_places=3, null=True)

    # META CLASS
    class Meta:
        ordering = ['pvmodule','-p_max_stc']
    
    # METHODS
    def __str__(self):
        return 'datasheet for %s' % (self.pvmodule)
    # Add FileField later

# class PvModuleModelParams(models.Model):
    # Add modeling parameters
    # Need to add software/model type?

# class PvModuleWarranty(model.Model):
    # Add attributes related to module warranties