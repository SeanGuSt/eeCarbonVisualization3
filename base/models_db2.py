# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaseDataset(models.Model):
    name = models.CharField(unique=True, max_length=255)
    hastime = models.BooleanField(db_column='hasTime')  # Field name made lowercase.
    hassoil = models.BooleanField(db_column='hasSoil')  # Field name made lowercase.
    file = models.CharField(max_length=255)
    delimiter = models.CharField(max_length=1)
    source = models.ForeignKey('BaseSource', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_dataset'


class BaseSite(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    county = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    bdc = models.TextField(db_column='BDc')  # Field name made lowercase.
    socc = models.TextField(db_column='SOCc')  # Field name made lowercase.
    source = models.ForeignKey('BaseSource', models.DO_NOTHING)
    field_order = models.IntegerField(db_column='_order')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'base_site'
        unique_together = (('name', 'source'),)


class BaseSource(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'base_source'


class BaseStandard(models.Model):
    name = models.CharField(unique=True, max_length=255)
    summary = models.BooleanField()
    issoil = models.BooleanField(db_column='isSoil')  # Field name made lowercase.
    istime = models.BooleanField(db_column='isTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'base_standard'


class BaseSynonym(models.Model):
    standard = models.ForeignKey(BaseStandard, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'base_synonym'


class BaseSynonymDataset(models.Model):
    synonym = models.ForeignKey(BaseSynonym, models.DO_NOTHING)
    dataset = models.ForeignKey(BaseDataset, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'base_synonym_dataset'
        unique_together = (('synonym', 'dataset'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LabAnalysisProcedure(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    apid = models.TextField()  # This field type is a guess.
    procedure_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    requested_anal_name = models.TextField(blank=True, null=True)
    proced_name = models.TextField(blank=True, null=True)
    proced_abbrev = models.TextField(blank=True, null=True)
    proced_desc = models.TextField(blank=True, null=True)
    ssir_5_page = models.TextField(db_column='SSIR_5_Page', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pdf_pg = models.TextField(db_column='PDF_pg', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    links_to_ssir_42_v_5 = models.TextField(db_column='Links_to_SSIR_42_V_5', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_analysis_procedure'


class LabAnalyte(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    analyte_key = models.TextField()  # This field type is a guess.
    analyte_type = models.TextField()
    analyte_name = models.TextField()
    column_name = models.TextField(blank=True, null=True)
    analyte_abbrev = models.TextField()
    analyte_code = models.TextField(blank=True, null=True)
    analyte_data_type = models.TextField()
    analyte_format = models.TextField()
    uom_abbrev = models.TextField(blank=True, null=True)
    analyte_source_type = models.TextField()
    analyte_agg_method = models.TextField(blank=True, null=True)
    analyte_algorithm = models.TextField(blank=True, null=True)
    analyte_desc = models.TextField(blank=True, null=True)
    analyte_size_frac_base = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_analyte'


class LabArea(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    area_key = models.TextField()  # This field type is a guess.
    area_type = models.TextField()
    area_sub_type = models.TextField(blank=True, null=True)
    parent_area_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    parent_org_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    area_code = models.TextField(blank=True, null=True)
    area_name = models.TextField()
    area_abbrev = models.TextField(blank=True, null=True)
    area_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_area'


class LabCalculationsIncludingEstimatesAndDefaultValues(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField()
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    bulk_density_3rd_bar_for_calc = models.TextField()  # This field type is a guess.
    bulk_density_3rd_bar_source = models.TextField()
    particle_density_for_calc = models.TextField()  # This field type is a guess.
    particle_density_calc_source = models.TextField()
    bulk_density_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_oven_dry_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_saturated_whole_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_lt_2_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_usda_sand_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    vol_pct_usda_silt_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_usda_clay_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    pct_pores_drained_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    pct_pores_filled_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_gt_2_mm_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_2_75_mm_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_2_20_mm_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_sand_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_silt_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_tot_clay_clay_free_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_vcs_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_cs_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_ms_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_fs_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_vfs_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_csi_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_fsi_clay_free_lt2mmbase = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_clay_clay_free_2mm_base = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_25 = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_520 = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_2075 = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_0175 = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_3_inch_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_whole_soil_moist = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_percent_gt_2_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_percent_gt_250_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_75_to_250_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_2_to_75_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_20_to_75_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_5_to_20_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_lt_1_fourth_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_lt_1_tenth_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_lt_5_hundredths = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_size_lt_60_pe = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_size_lt_50_pe = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_size_lt_10_pe = models.TextField(blank=True, null=True)  # This field type is a guess.
    gradiation_uniformity = models.TextField(blank=True, null=True)  # This field type is a guess.
    gradation_curvature = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_third_ovendry_whole_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_third_bar_to_oven_dry_rewet = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_third_fifteen_whole_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    void_ratio_third_bar_lt_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    void_ratio_third_bar_whole_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_difference_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    pores_drained_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    pores_filled_third_bar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_2_to_5_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight_pct_less_than_2_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_gt_2_mm_thirdbar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_gt_250_mm_thirdbar_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_75_to_250_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_2_to_75_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_20_to_75_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_5_to_20_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    volume_pct_2_to_5_mm_third_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_2_inch_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_1_and_1_half = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_1_inch_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_3_quarter_inch = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_3_eights_inch = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_no_4_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_no_10_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_no_40_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_no_200_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_20_micron_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_5_micron_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    percent_passing_2_micron_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_less_than_1mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    cumulative_curve_lt_1_half_mm = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_calculations_including_estimates_and_default_values'


class LabChemicalProperties(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField()
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    ca_nh4_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ca_nh4_ph_7_method = models.TextField(blank=True, null=True)
    mg_nh4_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    mg_nh4_ph_7_method = models.TextField(blank=True, null=True)
    na_nh4_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    na_nh4_ph_7_method = models.TextField(blank=True, null=True)
    k_nh4_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    k_nh4_ph_7_method = models.TextField(blank=True, null=True)
    acidity_bacl2_tea_ph_8_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    acidity_bacl2_tea_ph_82_method = models.TextField(blank=True, null=True)
    aluminum_kcl_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_kcl_extract_method = models.TextField(blank=True, null=True)
    manganese_kcl_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_kcl_extract_method = models.TextField(blank=True, null=True)
    iron_kcl_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_kcl_extractable_method = models.TextField(blank=True, null=True)
    cec_nh4_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    cec_nh4_ph_7_method = models.TextField(blank=True, null=True)
    total_carbon_ncs = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_carbon_ncs_method = models.TextField(blank=True, null=True)
    total_nitrogen_ncs = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_nitrogen_ncs_method = models.TextField(blank=True, null=True)
    total_sulfur_ncs = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_sulfur_ncs_method = models.TextField(blank=True, null=True)
    organic_carbon_walkley_black = models.TextField(blank=True, null=True)  # This field type is a guess.
    oc_walkley_black_method = models.TextField(blank=True, null=True)
    fe_dithionite_citrate_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_dc_extract_method = models.TextField(blank=True, null=True)
    aluminum_dithionite_citrate = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_dc_extract_method = models.TextField(blank=True, null=True)
    manganese_dithionite_citrate = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_dc_extract_method = models.TextField(blank=True, null=True)
    ammoniumoxalate_opticaldensity = models.TextField(blank=True, null=True)  # This field type is a guess.
    ammonium_ox_opt_dens_method = models.TextField(blank=True, null=True)
    fe_ammoniumoxalate_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_ammonium_oxalate_method = models.TextField(blank=True, null=True)
    aluminum_ammonium_oxalate = models.TextField(blank=True, null=True)  # This field type is a guess.
    al_ammonium_oxalate_method = models.TextField(blank=True, null=True)
    silica_ammonium_oxalate = models.TextField(blank=True, null=True)  # This field type is a guess.
    silica_ammonium_oxalate_method = models.TextField(blank=True, null=True)
    manganese_ammonium_oxalate = models.TextField(blank=True, null=True)  # This field type is a guess.
    mn_ammonium_oxalate_method = models.TextField(blank=True, null=True)
    carbon_sodium_pyro_phosphate = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_na_pyro_phosphate_method = models.TextField(blank=True, null=True)
    iron_sodium_pyro_phosphate = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_na_pyro_phosphate_method = models.TextField(blank=True, null=True)
    aluminum_na_pyro_phosphate = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_na_pyro_phosphate_method = models.TextField(blank=True, null=True)
    manganese_na_pyro_phosphate = models.TextField(blank=True, null=True)  # This field type is a guess.
    mn_na_pyro_phosphate_method = models.TextField(blank=True, null=True)
    ph_kcl = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_kcl_method = models.TextField(blank=True, null=True)
    ph_cacl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_cacl2_method = models.TextField(blank=True, null=True)
    ph_h2o = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_h2o_method = models.TextField(blank=True, null=True)
    ph_saturated_paste = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_saturated_paste_method = models.TextField(blank=True, null=True)
    ph_oxidized = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_oxidized_initial = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_oxidized_method = models.TextField(blank=True, null=True)
    ph_naf = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_naf_method = models.TextField(blank=True, null=True)
    ph_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    ph_water_extract_method = models.TextField(blank=True, null=True)
    caco3_lt_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    caco3_lt_2_mm_method = models.TextField(blank=True, null=True)
    corrected_gypsum_lt_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    corrected_gyp_lt_2_mm_method = models.TextField(blank=True, null=True)
    resistivity_saturated_paste = models.TextField(blank=True, null=True)  # This field type is a guess.
    resistivity_sp_method = models.TextField(blank=True, null=True)
    ca_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    ca_satx_method = models.TextField(blank=True, null=True)
    mg_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    mg_satx_method = models.TextField(blank=True, null=True)
    ca_plus_mg_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    ca_plus_mg_satx_method = models.TextField(blank=True, null=True)
    na_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    na_satx_method = models.TextField(blank=True, null=True)
    k_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    k_satx_method = models.TextField(blank=True, null=True)
    co3_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    co3_satx_method = models.TextField(blank=True, null=True)
    hco3_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    hco3_satx_method = models.TextField(blank=True, null=True)
    co3_plus_hco3_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    co3_plus_hco3_satx_method = models.TextField(blank=True, null=True)
    cl_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    cl_satx_method = models.TextField(blank=True, null=True)
    f_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_satx_method = models.TextField(blank=True, null=True)
    po4_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    po4_satx_method = models.TextField(blank=True, null=True)
    br_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    br_satx_method = models.TextField(blank=True, null=True)
    oac_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    oac_satx_method = models.TextField(blank=True, null=True)
    so4_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    so4_satx_method = models.TextField(blank=True, null=True)
    no2_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    no2_satx_method = models.TextField(blank=True, null=True)
    no3_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    no3_satx_method = models.TextField(blank=True, null=True)
    h20_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    h20_satx_method = models.TextField(blank=True, null=True)
    electrical_conductivity_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    electrical_cond_satx_method = models.TextField(blank=True, null=True)
    ec_predict_one_to_two = models.TextField(blank=True, null=True)  # This field type is a guess.
    ec_predict_one_to_two_method = models.TextField(blank=True, null=True)
    melanic_index = models.TextField(blank=True, null=True)  # This field type is a guess.
    melanic_index_method = models.TextField(blank=True, null=True)
    new_zealand_phosphorus_retent = models.TextField(blank=True, null=True)  # This field type is a guess.
    new_zealand_phos_retent_method = models.TextField(blank=True, null=True)
    phosphorus_ammonium_oxalate = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_ammonium_oxalate_method = models.TextField(blank=True, null=True)
    phosphorus_anion_resin_one_hr = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_anion_resin_24_hr = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_anion_resin_method = models.TextField(blank=True, null=True)
    phosphorus_bray1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_bray1_method = models.TextField(blank=True, null=True)
    phosphorus_bray2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_bray2_method = models.TextField(blank=True, null=True)
    phosphorus_citric_acid = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_citric_acid_method = models.TextField(blank=True, null=True)
    phosphorus_mehlich_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_mehlich_3_method = models.TextField(blank=True, null=True)
    phosphorus_olsen = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_olsen_method = models.TextField(blank=True, null=True)
    phosphorus_water = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_water_method = models.TextField(blank=True, null=True)
    nitrate_1m_kcl = models.TextField(blank=True, null=True)  # This field type is a guess.
    nitrate_1m_kcl_method = models.TextField(blank=True, null=True)
    water_extract_method = models.TextField(blank=True, null=True)
    acetate_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    arsenic_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    barium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    boron_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    bromide_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    cadmium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    calcium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    chloride_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    chromium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    cobalt_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    copper_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    ec_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    fluoride_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    lead_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    magnesium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    molybdenum_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    nickel_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    nitrate_n_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    nitrate_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    nitrite_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphate_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    potassium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    selenium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    silicon_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    sodium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    strontium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    sulfate_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    vanadium_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    zinc_water_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    mehlich_3_extractable_method = models.TextField(blank=True, null=True)
    aluminum_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    arsenic_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    barium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    cadmium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    calcium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    chromium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    cobalt_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    copper_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    lead_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    magnesium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    molybdenum_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    nickel_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    potassium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    selenium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    silicon_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    sodium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    strontium_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    zinc_mehlich3_extractable = models.TextField(blank=True, null=True)  # This field type is a guess.
    sum_of_nh4_ph_7_ext_bases = models.TextField(db_column='sum_of_nh4_ph_7_Ext_bases', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sum_of_cations_cec_ph_8_2 = models.TextField(db_column='sum_of_cations_cec_pH_8_2', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ecec_base_plus_aluminum = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_saturation = models.TextField(blank=True, null=True)  # This field type is a guess.
    base_sat_sum_of_cations_ph_8_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    base_sat_nh4oac_ph_7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_organic_carbon = models.TextField(blank=True, null=True)  # This field type is a guess.
    carbon_to_nitrogen_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_plus_half_iron_oxalate = models.TextField(blank=True, null=True)  # This field type is a guess.
    caco3_lt_20_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    gypsum_lt_20_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ca_to_mg_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_estimated_salts_satx = models.TextField(blank=True, null=True)  # This field type is a guess.
    exchangeable_sodium = models.TextField(blank=True, null=True)  # This field type is a guess.
    sodium_absorption_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_anion_resin_capacity = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_chemical_properties'


class LabCombineNasisNcss(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    shape = models.TextField(db_column='Shape')  # Field name made lowercase. This field type is a guess.
    objectid_1 = models.TextField()  # This field type is a guess.
    pedon_key = models.TextField()  # This field type is a guess.
    site_key = models.TextField()  # This field type is a guess.
    pedlabsampnum = models.TextField()
    peiid = models.TextField(blank=True, null=True)  # This field type is a guess.
    upedonid = models.TextField()
    labdatadescflag = models.TextField(blank=True, null=True)  # This field type is a guess.
    priority = models.TextField(blank=True, null=True)
    priority2 = models.TextField(blank=True, null=True)
    samp_name = models.TextField(blank=True, null=True)
    samp_class_type = models.TextField(blank=True, null=True)
    samp_classdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    samp_classification_name = models.TextField(blank=True, null=True)
    samp_taxorder = models.TextField(blank=True, null=True)
    samp_taxsuborder = models.TextField(blank=True, null=True)
    samp_taxgrtgroup = models.TextField(blank=True, null=True)
    samp_taxsubgrp = models.TextField(blank=True, null=True)
    samp_taxpartsize = models.TextField(blank=True, null=True)
    samp_taxpartsizemod = models.TextField(blank=True, null=True)
    samp_taxceactcl = models.TextField(blank=True, null=True)
    samp_taxreaction = models.TextField(blank=True, null=True)
    samp_taxtempcl = models.TextField(blank=True, null=True)
    samp_taxmoistscl = models.TextField(blank=True, null=True)
    samp_taxtempregime = models.TextField(blank=True, null=True)
    samp_taxminalogy = models.TextField(blank=True, null=True)
    samp_taxother = models.TextField(blank=True, null=True)
    samp_osdtypelocflag = models.TextField(blank=True, null=True)  # This field type is a guess.
    corr_name = models.TextField(blank=True, null=True)
    corr_class_type = models.TextField(blank=True, null=True)
    corr_classdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    corr_classification_name = models.TextField(blank=True, null=True)
    corr_taxorder = models.TextField(blank=True, null=True)
    corr_taxsuborder = models.TextField(blank=True, null=True)
    corr_taxgrtgroup = models.TextField(blank=True, null=True)
    corr_taxsubgrp = models.TextField(blank=True, null=True)
    corr_taxpartsize = models.TextField(blank=True, null=True)
    corr_taxpartsizemod = models.TextField(blank=True, null=True)
    corr_taxceactcl = models.TextField(blank=True, null=True)
    corr_taxreaction = models.TextField(blank=True, null=True)
    corr_taxtempcl = models.TextField(blank=True, null=True)
    corr_taxmoistscl = models.TextField(blank=True, null=True)
    corr_taxtempregime = models.TextField(blank=True, null=True)
    corr_taxminalogy = models.TextField(blank=True, null=True)
    corr_taxother = models.TextField(blank=True, null=True)
    corr_osdtypelocflag = models.TextField(blank=True, null=True)  # This field type is a guess.
    ssl_name = models.TextField(db_column='SSL_name', blank=True, null=True)  # Field name made lowercase.
    ssl_class_type = models.TextField(db_column='SSL_class_type', blank=True, null=True)  # Field name made lowercase.
    ssl_classdate = models.TextField(db_column='SSL_classdate', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ssl_classification_name = models.TextField(db_column='SSL_classification_name', blank=True, null=True)  # Field name made lowercase.
    ssl_taxorder = models.TextField(db_column='SSL_taxorder', blank=True, null=True)  # Field name made lowercase.
    ssl_taxsuborder = models.TextField(db_column='SSL_taxsuborder', blank=True, null=True)  # Field name made lowercase.
    ssl_taxgrtgroup = models.TextField(db_column='SSL_taxgrtgroup', blank=True, null=True)  # Field name made lowercase.
    ssl_taxsubgrp = models.TextField(db_column='SSL_taxsubgrp', blank=True, null=True)  # Field name made lowercase.
    ssl_taxpartsize = models.TextField(db_column='SSL_taxpartsize', blank=True, null=True)  # Field name made lowercase.
    ssl_taxpartsizemod = models.TextField(db_column='SSL_taxpartsizemod', blank=True, null=True)  # Field name made lowercase.
    ssl_taxceactcl = models.TextField(db_column='SSL_taxceactcl', blank=True, null=True)  # Field name made lowercase.
    ssl_taxreaction = models.TextField(db_column='SSL_taxreaction', blank=True, null=True)  # Field name made lowercase.
    ssl_taxtempcl = models.TextField(db_column='SSL_taxtempcl', blank=True, null=True)  # Field name made lowercase.
    ssl_taxmoistscl = models.TextField(db_column='SSL_taxmoistscl', blank=True, null=True)  # Field name made lowercase.
    ssl_taxtempregime = models.TextField(db_column='SSL_taxtempregime', blank=True, null=True)  # Field name made lowercase.
    ssl_taxminalogy = models.TextField(db_column='SSL_taxminalogy', blank=True, null=True)  # Field name made lowercase.
    ssl_taxother = models.TextField(db_column='SSL_taxother', blank=True, null=True)  # Field name made lowercase.
    ssl_osdtypelocflag = models.TextField(db_column='SSL_osdtypelocflag', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    siteiid = models.TextField(blank=True, null=True)  # This field type is a guess.
    usiteid = models.TextField()
    site_obsdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude_decimal_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_decimal_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    country_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    state_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    county_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    mlra_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    ssa_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    npark_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    nforest_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    note = models.TextField(blank=True, null=True)
    samp_taxfamhahatmatcl = models.TextField(blank=True, null=True)
    corr_taxfamhahatmatcl = models.TextField(blank=True, null=True)
    ssl_taxfamhahatmatcl = models.TextField(db_column='SSL_taxfamhahatmatcl', blank=True, null=True)  # Field name made lowercase.
    pedobjupdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    siteobjupdate = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_combine_nasis_ncss'


class LabLayer(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField()
    project_key = models.TextField()  # This field type is a guess.
    site_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    pedon_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    layer_sequence = models.TextField(blank=True, null=True)  # This field type is a guess.
    layer_type = models.TextField(blank=True, null=True)
    layer_field_label_1 = models.TextField(blank=True, null=True)
    layer_field_label_2 = models.TextField(blank=True, null=True)
    layer_field_label_3 = models.TextField(blank=True, null=True)
    hzn_top = models.TextField(blank=True, null=True)  # This field type is a guess.
    hzn_bot = models.TextField(blank=True, null=True)  # This field type is a guess.
    hzn_desgn_old = models.TextField(blank=True, null=True)
    hzn_desgn = models.TextField(blank=True, null=True)
    hzn_discontinuity = models.TextField(blank=True, null=True)  # This field type is a guess.
    hzn_master = models.TextField(blank=True, null=True)
    hzn_prime = models.TextField(blank=True, null=True)
    hzn_vert_subdvn = models.TextField(blank=True, null=True)  # This field type is a guess.
    hzn_desgn_other = models.TextField(blank=True, null=True)
    non_hzn_desgn = models.TextField(blank=True, null=True)
    stratified_textures_flag = models.TextField(blank=True, null=True)  # This field type is a guess.
    texture_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_layer'


class LabMajorAndTraceElementsAndOxides(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField(blank=True, null=True)
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    major_element_method = models.TextField(blank=True, null=True)
    aluminum_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    calcium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    potassium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    magnesium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    sodium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    silicon_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    strontium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    titanium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    zirconium_major_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    trace_element_method = models.TextField(blank=True, null=True)
    silver_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    arsenic_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    barium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    beryllium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    cadmium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    cobalt_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    chromium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    copper_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    mercury_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    manganese_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    molybdenum_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    nickel_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    phosphorus_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    lead_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    antimony_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    selenium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    tin_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    strontium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    thallium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    vanadium_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    tungsten_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    zinc_trace_element = models.TextField(blank=True, null=True)  # This field type is a guess.
    iron_oxide_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    aluminum_oxide_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    potassium_oxide_total = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_major_and_trace_elements_and_oxides'


class LabMethodCode(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    mcid = models.TextField()  # This field type is a guess.
    procedure_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    requested_anal_name = models.TextField(blank=True, null=True)
    proced_name = models.TextField(blank=True, null=True)
    proced_abbrev = models.TextField(blank=True, null=True)
    proced_desc = models.TextField(blank=True, null=True)
    proced_code = models.TextField(blank=True, null=True)
    source_system_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    source_system_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_method_code'


class LabMineralogyGlassCount(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField(blank=True, null=True)
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    analyzed_size_frac = models.TextField(blank=True, null=True)
    glass_count_method = models.TextField(db_column='Glass_Count_Method', blank=True, null=True)  # Field name made lowercase.
    bg_basic_glass_count = models.TextField(db_column='BG_Basic_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    di_diatoms_glass_count = models.TextField(db_column='DI_Diatoms_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ga_glass_aggregates_glass_count = models.TextField(db_column='GA_Glass_Aggregates_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gs_glass_glass_count = models.TextField(db_column='GS_Glass_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fg_glass_coated_feldspar_glass_count = models.TextField(db_column='FG_Glass_Coated_Feldspar_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gc_glass_coated_grain_glass_count = models.TextField(db_column='GC_Glass_Coated_Grain_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hg_glass_coated_hornblende_glass_count = models.TextField(db_column='HG_Glass_Coated_Hornblende_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    og_glass_coated_opaques_glass_count = models.TextField(db_column='OG_Glass_Coated_Opaques_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qg_glass_coated_quartz_glass_count = models.TextField(db_column='QG_Glass_Coated_Quartz_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gm_glassy_materials_glass_count = models.TextField(db_column='GM_Glassy_Materials_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ot_other_glass_count = models.TextField(db_column='OT_Other_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    po_plant_opal_glass_count = models.TextField(db_column='PO_Plant_Opal_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ss_sponge_spicule_glass_count = models.TextField(db_column='SS_Sponge_Spicule_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ar_weatherable_aggregates_glass_count = models.TextField(db_column='AR_Weatherable_Aggregates_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pa_palagonite_glass_count = models.TextField(db_column='PA_Palagonite_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pm_pumice_glass_count = models.TextField(db_column='PM_Pumice_Glass_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    petro_count_method = models.TextField(db_column='Petro_Count_Method', blank=True, null=True)  # Field name made lowercase.
    ac_actinolite_petro_count = models.TextField(db_column='AC_Actinolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fb_albite_petro_count = models.TextField(db_column='FB_Albite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    am_amphibole_petro_count = models.TextField(db_column='AM_Amphibole_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ae_anatase_petro_count = models.TextField(db_column='AE_Anatase_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    an_andalusite_petro_count = models.TextField(db_column='AN_andalusite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fa_andesite_petro_count = models.TextField(db_column='FA_andesite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ay_anhydrite_petro_count = models.TextField(db_column='AY_Anhydrite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fn_anorthite_petro_count = models.TextField(db_column='FN_Anorthite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fh_anorthoclase_petro_count = models.TextField(db_column='FH_Anorthoclase_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ah_anthophyllite_petro_count = models.TextField(db_column='AH_Anthophyllite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ag_antigorite_petro_count = models.TextField(db_column='AG_Antigorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ap_apatite_petro_count = models.TextField(db_column='AP_Apatite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ao_aragonite_petro_count = models.TextField(db_column='AO_Aragonite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    af_arfvedsonite_petro_count = models.TextField(db_column='AF_Arfvedsonite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    au_augite_petro_count = models.TextField(db_column='AU_Augite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ba_barite_petro_count = models.TextField(db_column='BA_Barite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bg_basic_glass_petro_count = models.TextField(db_column='BG_Basic_Glass_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    by_beryl_petro_count = models.TextField(db_column='BY_Beryl_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bt_biotite_petro_count = models.TextField(db_column='BT_Biotite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bc_biotite_chlorite_petro_count = models.TextField(db_column='BC_Biotite_Chlorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    be_bohmite_petro_count = models.TextField(db_column='BE_Bohmite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bz_bronzite_petro_count = models.TextField(db_column='BZ_Bronzite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bk_brookite_petro_count = models.TextField(db_column='BK_Brookite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    br_brucite_petro_count = models.TextField(db_column='BR_Brucite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ca_calcite_petro_count = models.TextField(db_column='CA_Calcite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cb_carbonate_aggregates_petro_count = models.TextField(db_column='CB_Carbonate_Aggregates_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ct_cassiterite_petro_count = models.TextField(db_column='CT_Cassiterite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cd_chert_chalcedony_jasper_agate_onyx_petro_count = models.TextField(db_column='CD_Chert_Chalcedony_Jasper_Agate_Onyx_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cl_chlorite_petro_count = models.TextField(db_column='CL_Chlorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cm_chlorite_mica_petro_count = models.TextField(db_column='CM_Chlorite_Mica_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cy_chrysotile_petro_count = models.TextField(db_column='CY_Chrysotile_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qc_clay_coated_quartz_petro_count = models.TextField(db_column='QC_Clay_Coated_Quartz_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ch_cliachite_bauxite_petro_count = models.TextField(db_column='CH_Cliachite_Bauxite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cz_clinozoisite_petro_count = models.TextField(db_column='CZ_Clinozoisite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cc_coal_petro_count = models.TextField(db_column='CC_Coal_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    co_collophane_petro_count = models.TextField(db_column='CO_Collophane_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cn_corundum_petro_count = models.TextField(db_column='CN_Corundum_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cr_cristobalite_petro_count = models.TextField(db_column='CR_Cristobalite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    di_diatoms_petro_count = models.TextField(db_column='DI_Diatoms_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dp_diopside_petro_count = models.TextField(db_column='DP_Diopside_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dl_dolomite_petro_count = models.TextField(db_column='DL_Dolomite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    du_dumortierite_petro_count = models.TextField(db_column='DU_Dumortierite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    en_enstatite_petro_count = models.TextField(db_column='EN_Enstatite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_epidote_petro_count = models.TextField(db_column='EP_Epidote_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fd_feldspar_petro_count = models.TextField(db_column='FD_Feldspar_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fz_feldspathoids_petro_count = models.TextField(db_column='FZ_Feldspathoids_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fm_ferromagnesium_petro_count = models.TextField(db_column='FM_Ferromagnesium_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fu_fluorite_petro_count = models.TextField(db_column='FU_Fluorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ff_foraminifera_petro_count = models.TextField(db_column='FF_Foraminifera_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gg_galena_petro_count = models.TextField(db_column='GG_Galena_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gn_garnet_petro_count = models.TextField(db_column='GN_Garnet_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gi_gibbsite_petro_count = models.TextField(db_column='GI_Gibbsite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ga_glass_aggregates_petro_count = models.TextField(db_column='GA_Glass_Aggregates_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fg_glass_coated_feldspar_petro_count = models.TextField(db_column='FG_Glass_Coated_Feldspar_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gc_glass_coated_grain_petro_count = models.TextField(db_column='GC_Glass_Coated_Grain_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hg_glass_coated_hornblende_petro_count = models.TextField(db_column='HG_Glass_Coated_Hornblende_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    og_glass_coated_opaque_petro_count = models.TextField(db_column='OG_Glass_Coated_Opaque_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qg_glass_coated_quartz_petro_count = models.TextField(db_column='QG_Glass_Coated_Quartz_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gs_glass_petro_count = models.TextField(db_column='GS_Glass_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gm_glassy_matrials_petro_count = models.TextField(db_column='GM_Glassy_Matrials_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gl_glauconite_petro_count = models.TextField(db_column='GL_Glauconite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    go_glaucophane_petro_count = models.TextField(db_column='GO_Glaucophane_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ge_goethite_petro_count = models.TextField(db_column='GE_Goethite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gd_gold_petro_count = models.TextField(db_column='GD_Gold_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gy_gypsum_petro_count = models.TextField(db_column='GY_Gypsum_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kh_halloysite_petro_count = models.TextField(db_column='KH_Halloysite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    he_hematite_petro_count = models.TextField(db_column='HE_Hematite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hn_hornblende_petro_count = models.TextField(db_column='HN_Hornblende_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hb_hydrobiotite_petro_count = models.TextField(db_column='HB_Hydrobiotite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    id_iddingsite_petro_count = models.TextField(db_column='ID_Iddingsite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qi_iron_oxide_coated_quartz_petro_count = models.TextField(db_column='QI_Iron_Oxide_Coated_Quartz_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fe_iron_oxides_geothite_magnetite_hematite_li_petro_count = models.TextField(db_column='FE_Iron_Oxides_Geothite_Magnetite_Hematite_Li_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    jo_jarosite_petro_count = models.TextField(db_column='JO_Jarosite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kk_kaolinite_petro_count = models.TextField(db_column='KK_Kaolinite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ky_kyanite_petro_count = models.TextField(db_column='KY_Kyanite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fl_labradorite_petro_count = models.TextField(db_column='FL_Labradorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    la_lamprobolite_petro_count = models.TextField(db_column='LA_Lamprobolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lp_lepidolite_petro_count = models.TextField(db_column='LP_Lepidolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lo_lepidomelane_petro_count = models.TextField(db_column='LO_Lepidomelane_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lu_leucoxene_petro_count = models.TextField(db_column='LU_Leucoxene_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lm_limonite_petro_count = models.TextField(db_column='LM_Limonite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lt_lithiophorite_petro_count = models.TextField(db_column='LT_Lithiophorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    me_magnesite_petro_count = models.TextField(db_column='ME_Magnesite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mg_magnetite_petro_count = models.TextField(db_column='MG_Magnetite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mr_marcasite_petro_count = models.TextField(db_column='MR_Marcasite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ml_melilite_petro_count = models.TextField(db_column='ML_Melilite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mi_mica_petro_count = models.TextField(db_column='MI_Mica_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fc_microcline_petro_count = models.TextField(db_column='FC_Microcline_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mz_monazite_petro_count = models.TextField(db_column='MZ_Monazite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mt_montmorillonite_petro_count = models.TextField(db_column='MT_Montmorillonite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ms_muscovite_petro_coun = models.TextField(db_column='MS_Muscovite_Petro_Coun', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ne_nepheline_petro_count = models.TextField(db_column='NE_Nepheline_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    nx_non_crystalline_petro_count = models.TextField(db_column='NX_Non_Crystalline_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fo_oligoclase_petro_count = models.TextField(db_column='FO_Oligoclase_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ov_olivine_petro_count = models.TextField(db_column='OV_Olivine_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    op_opaques_petro_count = models.TextField(db_column='OP_Opaques_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fr_orthoclase_petro_count = models.TextField(db_column='FR_Orthoclase_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    or_other_resistant_minerals_petro_count = models.TextField(db_column='OR_Other_Resistant_Minerals_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ow_other_weatherable_minerals_petro_count = models.TextField(db_column='OW_Other_Weatherable_Minerals_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ot_other_petro_count = models.TextField(db_column='OT_Other_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pk_perovskite_petro_count = models.TextField(db_column='PK_Perovskite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pl_phlogophit_petro_count = models.TextField(db_column='PL_Phlogophit_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pd_piemontite_petro_count = models.TextField(db_column='PD_Piemontite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fp_plagioclase_feldspar_petro_count = models.TextField(db_column='FP_Plagioclase_Feldspar_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    po_plant_opal_petro_count = models.TextField(db_column='PO_Plant_Opal_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pj_plumbojarosite_petro_count = models.TextField(db_column='PJ_Plumbojarosite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pn_pollen_petro_count = models.TextField(db_column='PN_Pollen_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fk_potassium_feldspar_petro_count = models.TextField(db_column='FK_Potassium_Feldspar_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pi_pyrite_petro_count = models.TextField(db_column='PI_Pyrite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pu_pyrolusite_petro_count = models.TextField(db_column='PU_Pyrolusite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    py_pyrophyllite_petro_count = models.TextField(db_column='PY_Pyrophyllite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pr_pyroxene_petro_count = models.TextField(db_column='PR_Pyroxene_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qz_quartz_petro_count = models.TextField(db_column='QZ_Quartz_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ra_resistant_aggregates_petro_count = models.TextField(db_column='RA_Resistant_Aggregates_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    md_resistant_mineraloids_petro_count = models.TextField(db_column='MD_Resistant_Mineraloids_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    re_resistant_minerals_petro_count = models.TextField(db_column='RE_Resistant_Minerals_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ro_rhodochrosite_petro_count = models.TextField(db_column='RO_Rhodochrosite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    rb_riebeckite_blue_amphibole_pero_count = models.TextField(db_column='RB_Riebeckite_Blue_Amphibole_Pero_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ru_rutile_petro_count = models.TextField(db_column='RU_Rutile_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fs_sanidine_petro_count = models.TextField(db_column='FS_Sanidine_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sr_sericite_petro_count = models.TextField(db_column='SR_Sericite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    si_siderite_petro_count = models.TextField(db_column='SI_Siderite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sa_siliceous_aggregates_petro_count = models.TextField(db_column='SA_Siliceous_Aggregates_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sl_sillimanite_petro_count = models.TextField(db_column='SL_Sillimanite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sg_sphalerite_petro_count = models.TextField(db_column='SG_Sphalerite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sp_sphene_petro_count = models.TextField(db_column='SP_Sphene_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sn_spinel_petro_count = models.TextField(db_column='SN_Spinel_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ss_sponge_spicule_petro_count = models.TextField(db_column='SS_Sponge_Spicule_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    so_staurolite_petro_count = models.TextField(db_column='SO_Staurolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    st_stilbite_petro_count = models.TextField(db_column='ST_Stilbite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    su_sulfur_petro_count = models.TextField(db_column='SU_Sulfur_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ta_talc_petro_count = models.TextField(db_column='TA_Talc_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tp_topaz_petro_count = models.TextField(db_column='TP_Topaz_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tm_tourmaline_petro_count = models.TextField(db_column='TM_Tourmaline_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    te_tremolite_petro_count = models.TextField(db_column='TE_Tremolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vr_vermiculite_petro_count = models.TextField(db_column='VR_Vermiculite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vc_vermiculite_chlorite_petro_count = models.TextField(db_column='VC_Vermiculite_Chlorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vh_vermiculite_hydrobiotite_petro_count = models.TextField(db_column='VH_Vermiculite_Hydrobiotite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vm_vermiculite_mica_petro_count = models.TextField(db_column='VM_Vermiculite_Mica_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vi_vivianite_petro_count = models.TextField(db_column='VI_Vivianite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    wv_wavellite_petro_count = models.TextField(db_column='WV_Wavellite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ar_weatherable_aggregates_petro_count = models.TextField(db_column='AR_Weatherable_Aggregates_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    we_weatherable_mineral_petro_count = models.TextField(db_column='WE_Weatherable_Mineral_petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ze_zeolite_petro_count = models.TextField(db_column='ZE_Zeolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    zr_zircon_petro_count = models.TextField(db_column='ZR_Zircon_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    zo_zoisite_petro_count = models.TextField(db_column='ZO_Zoisite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ai_aegirine_augite_petro_count = models.TextField(db_column='AI_Aegirine_Augite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    al_allophane_petro_count = models.TextField(db_column='AL_Allophane_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ce_cobaltite_petro_count = models.TextField(db_column='CE_Cobaltite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ha_halite_petro_count = models.TextField(db_column='HA_Halite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    il_illite_hydromuscovite_petro_count = models.TextField(db_column='IL_Illite_Hydromuscovite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_analcime_petro_count = models.TextField(db_column='LC_Analcime_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    le_lepidocrocite_petro_count = models.TextField(db_column='LE_Lepidocrocite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    li_leucite_petro_count = models.TextField(db_column='LI_Leucite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mc_montmorillonite_chlorite_petro_count = models.TextField(db_column='MC_Montmorillonite_Chlorite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mh_maghemite_petro_count = models.TextField(db_column='MH_Maghemite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mm_montmorillonite_mica_petro_count = models.TextField(db_column='MM_Montmorillonite_Mica_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mv_montmorillonite_vermiculite_petro_count = models.TextField(db_column='MV_Montmorillonite_Vermiculite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pa_palagonite_petro_count = models.TextField(db_column='PA_Palagonite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pg_palygorskite_petro_count = models.TextField(db_column='PG_Palygorskite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sc_scapolite_petro_count = models.TextField(db_column='SC_Scapolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    se_sepiolite_petro_count = models.TextField(db_column='SE_Sepiolite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sm_smectite_petro_count = models.TextField(db_column='SM_Smectite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    td_tridymite_petro_count = models.TextField(db_column='TD_Tridymite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    th_thenardite_petro_count = models.TextField(db_column='TH_thenardite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hy_hypersthene_petro_count = models.TextField(db_column='HY_Hypersthene_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hs_hydroxy_interlayer_smectite_petro_count = models.TextField(db_column='HS_Hydroxy_Interlayer_Smectite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hv_hydroxy_interlayer_vermiculite_petro_count = models.TextField(db_column='HV_Hydroxy_Interlayer_Vermiculite_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pm_pumice_petro_count = models.TextField(db_column='PM_Pumice_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sz_serpentine_petro_count = models.TextField(db_column='SZ_Serpentine_Petro_Count', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    total_grains_counted = models.TextField(db_column='Total_Grains_Counted', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    resistant_minerals_total_mineral_soil = models.TextField(db_column='Resistant_Minerals_Total_Mineral_Soil', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    glass_count_mineral_interpretation = models.TextField(db_column='Glass_Count_Mineral_Interpretation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lab_mineralogy_glass_count'


class LabMir(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    id = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField(blank=True, null=True)
    layer_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    smp_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    rep_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    lab_proj_name = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    absorbance = models.TextField(blank=True, null=True)
    d_wavelength_array_id = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_mir'


class LabMirWavelength(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    d_wavelength_array_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField()
    wavelength_string = models.TextField()

    class Meta:
        managed = False
        db_table = 'lab_mir_wavelength'


class LabPedon(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    pedon_key = models.TextField()  # This field type is a guess.
    pedlabsampnum = models.TextField(blank=True, null=True)
    observation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_pedon_id = models.TextField()
    pedon_seq_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    cntrl_depth_to_top = models.TextField(blank=True, null=True)  # This field type is a guess.
    cntrl_depth_to_bot = models.TextField(blank=True, null=True)  # This field type is a guess.
    fldsyb = models.TextField(blank=True, null=True)
    mapsyb = models.TextField(blank=True, null=True)
    site_key = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_pedon'


class LabPhysicalProperties(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField(blank=True, null=True)
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    texture_lab = models.TextField(blank=True, null=True)
    particle_size_method = models.TextField(blank=True, null=True)
    clay_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    clay_fine = models.TextField(blank=True, null=True)  # This field type is a guess.
    clay_caco3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_fine = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_coarse = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_very_fine = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_fine = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_medium = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_coarse = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_very_coarse = models.TextField(blank=True, null=True)  # This field type is a guess.
    frag_2_5_mm_wt_pct_lt_75 = models.TextField(blank=True, null=True)  # This field type is a guess.
    frag_2_20_mm_wt_pct_lt_75 = models.TextField(db_column='frag__2_20_mm_wt_pct_lt_75', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. This field type is a guess.
    frag_5_20_mm_wt_pct_lt_75 = models.TextField(blank=True, null=True)  # This field type is a guess.
    frag_20_75_mm_wt_pct_lt_75 = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_frag_wt_pct_gt_2_mm_ws = models.TextField(blank=True, null=True)  # This field type is a guess.
    wt_pct_1_tenth_to_75_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_tenth_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_tenth_bar_method = models.TextField(blank=True, null=True)
    bulk_density_third_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_third_bar_method = models.TextField(blank=True, null=True)
    bulk_density_oven_dry = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_oven_dry_method = models.TextField(blank=True, null=True)
    bulk_density_lt_2_mm_air_dry = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_air_dry_method = models.TextField(blank=True, null=True)
    bd_third_bar_lt2_reconstituted = models.TextField(blank=True, null=True)  # This field type is a guess.
    bd_thirdbar_reconstituted_method = models.TextField(blank=True, null=True)
    bulk_den_ovendry_reconstituted = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_odreconstituted_method = models.TextField(blank=True, null=True)
    bulk_density_field_moist = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_field_moist_method = models.TextField(blank=True, null=True)
    particle_density_less_than_2mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    particle_density_lt_2mm_method = models.TextField(blank=True, null=True)
    particle_density_gt_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    particle_density_gt_2mm_method = models.TextField(blank=True, null=True)
    cole_whole_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    cole_whole_soil_method = models.TextField(blank=True, null=True)
    le_third_fifteen_lt2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_third_fifteen_lt2_method = models.TextField(blank=True, null=True)
    le_third_ovendry_lt_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_third_ovendry_lt_2_mm_method = models.TextField(blank=True, null=True)
    le_field_moist_to_oben_dry = models.TextField(blank=True, null=True)  # This field type is a guess.
    le_fm_to_od_method = models.TextField(blank=True, null=True)
    water_retention_0_bar_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_0_bar_method = models.TextField(blank=True, null=True)
    water_retention_6_hundredths = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_6_hund_method = models.TextField(blank=True, null=True)
    water_retention_10th_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_10th_bar_method = models.TextField(blank=True, null=True)
    water_retention_third_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_thirdbar_method = models.TextField(blank=True, null=True)
    water_retention_1_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_1_bar_method = models.TextField(blank=True, null=True)
    water_retention_2_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_2_bar_method = models.TextField(blank=True, null=True)
    water_retention_3_bar_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_3_bar_method = models.TextField(blank=True, null=True)
    water_retention_5_bar_sieve = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_5_bar_method = models.TextField(blank=True, null=True)
    water_retention_15_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_15_bar_method = models.TextField(blank=True, null=True)
    water_retention_field_state = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_retention_field_state_me = models.TextField(blank=True, null=True)
    airdry_ovendry_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    atterberg_liquid_limit = models.TextField(blank=True, null=True)
    atterberg_liquid_limit_method = models.TextField(blank=True, null=True)
    atterberg_plasticity_index = models.TextField(blank=True, null=True)
    plastic_limit = models.TextField(blank=True, null=True)
    plastic_limit_method = models.TextField(blank=True, null=True)
    aggregate_stability_05_2_mm = models.TextField(blank=True, null=True)  # This field type is a guess.
    aggregate_stability_05_2_method = models.TextField(blank=True, null=True)
    le_to_clay_third_bar_to_ovendry = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_15_bar_to_clay_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    cec7_clay_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    effective_cec_to_clay_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    psda_ethanol_dispersion_method = models.TextField(blank=True, null=True)
    sand_total_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_total_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    clay_total_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_very_fine_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_fine_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_medium_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_coarse_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_very_coarse_ethanol_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    water_dispersible_fraction_method = models.TextField(blank=True, null=True)
    clay_tot_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    clay_fine_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    clay_co3_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_total_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_fine_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    silt_coarse_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_total_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_vf_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_fine_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_medium_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_coarse_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    sand_vc_h2o_dispersible = models.TextField(blank=True, null=True)  # This field type is a guess.
    color_pyrophosphate_extractable = models.TextField(blank=True, null=True)
    color_pyrophosphate_method = models.TextField(blank=True, null=True)
    bd_thirdbar_before_rewet_organ = models.TextField(blank=True, null=True)  # This field type is a guess.
    bd_before_rewet_organic_method = models.TextField(blank=True, null=True)
    bd_thirdbar_rewet_organic_soil = models.TextField(blank=True, null=True)  # This field type is a guess.
    bd_third_rewet_organic_method = models.TextField(blank=True, null=True)
    bulk_den_rewet_oven_dry = models.TextField(blank=True, null=True)  # This field type is a guess.
    bulk_density_rewet_oven_dry_method = models.TextField(blank=True, null=True)
    mineral_content_loss_on_ignition = models.TextField(blank=True, null=True)  # This field type is a guess.
    mineral_content_loss_ignition_method = models.TextField(blank=True, null=True)
    estimated_organic_matter = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_om_plus_mineral = models.TextField(blank=True, null=True)  # This field type is a guess.
    fiber_analysis_method = models.TextField(blank=True, null=True)
    fiber_unrubbed = models.TextField(blank=True, null=True)  # This field type is a guess.
    fiber_rubbed = models.TextField(blank=True, null=True)  # This field type is a guess.
    decomposition_state = models.TextField(blank=True, null=True)
    limnic_material_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_physical_properties'


class LabPreparation(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    prep_key = models.TextField()  # This field type is a guess.
    prep_code = models.TextField()
    prep_abbrev = models.TextField()
    moisture_state = models.TextField(blank=True, null=True)
    orig_size_frac = models.TextField(blank=True, null=True)
    final_size_frac = models.TextField(blank=True, null=True)
    prep_desc = models.TextField(blank=True, null=True)
    prep_rpt_sort_order = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_preparation'


class LabRosettaKey(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    rosetta_key = models.TextField()  # This field type is a guess.
    result_source_key = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    theta_r = models.TextField(blank=True, null=True)  # This field type is a guess.
    theta_s = models.TextField(blank=True, null=True)  # This field type is a guess.
    alpha = models.TextField(blank=True, null=True)  # This field type is a guess.
    npar = models.TextField(blank=True, null=True)  # This field type is a guess.
    usedmodel = models.TextField(blank=True, null=True)  # This field type is a guess.
    wlupdated = models.TextField(blank=True, null=True)  # This field type is a guess.
    ks = models.TextField(db_column='Ks', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ko = models.TextField(db_column='Ko', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lpar = models.TextField(db_column='Lpar', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_rosetta_key'


class LabSite(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    site_key = models.TextField()  # This field type is a guess.
    user_site_id = models.TextField()
    horizontal_datum_name = models.TextField(blank=True, null=True)
    latitude_direction = models.TextField(blank=True, null=True)
    latitude_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude_minutes = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude_seconds = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_direction = models.TextField(blank=True, null=True)
    longitude_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_minutes = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_seconds = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude_std_decimal_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_std_decimal_degrees = models.TextField(blank=True, null=True)  # This field type is a guess.
    msrepl_tran_version = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_site'


class LabWebmap(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    wmiid = models.TextField()  # This field type is a guess.
    series = models.TextField(db_column='Series', blank=True, null=True)  # Field name made lowercase.
    user_pedon_id = models.TextField(db_column='User_pedon_ID', blank=True, null=True)  # Field name made lowercase.
    pedon_key = models.TextField(db_column='pedon_Key')  # Field name made lowercase. This field type is a guess.
    peiid = models.TextField(blank=True, null=True)  # This field type is a guess.
    soil_classification = models.TextField(db_column='Soil_Classification', blank=True, null=True)  # Field name made lowercase.
    primary_lab_report = models.TextField(db_column='Primary_Lab_Report', blank=True, null=True)  # Field name made lowercase.
    taxonomy_report = models.TextField(db_column='Taxonomy_Report', blank=True, null=True)  # Field name made lowercase.
    supplementary_lab_report = models.TextField(db_column='Supplementary_Lab_Report', blank=True, null=True)  # Field name made lowercase.
    water_retention_report = models.TextField(db_column='Water_Retention_Report', blank=True, null=True)  # Field name made lowercase.
    correlation_report = models.TextField(db_column='Correlation_Report', blank=True, null=True)  # Field name made lowercase.
    pedon_description_report = models.TextField(db_column='pedon_Description_Report', blank=True, null=True)  # Field name made lowercase.
    soil_profile = models.TextField(db_column='Soil_Profile', blank=True, null=True)  # Field name made lowercase.
    soil_web = models.TextField(db_column='Soil_web', blank=True, null=True)  # Field name made lowercase.
    lat = models.TextField(blank=True, null=True)  # This field type is a guess.
    long = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_webmap'


class LabXrayAndThermal(models.Model):
    objectid = models.AutoField(db_column='OBJECTID', primary_key=True)  # Field name made lowercase.
    objectid_1 = models.TextField()  # This field type is a guess.
    layer_key = models.TextField()  # This field type is a guess.
    labsampnum = models.TextField()
    result_source_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code = models.TextField(blank=True, null=True)
    analyzed_size_frac = models.TextField(blank=True, null=True)
    x_ray_method = models.TextField(db_column='X_Ray_Method', blank=True, null=True)  # Field name made lowercase.
    am_amphibole_x_ray = models.TextField(db_column='AM_Amphibole_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_anacime_x_ray = models.TextField(db_column='LC_Anacime_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ae_anatase_x_ray = models.TextField(db_column='AE_Anatase_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ag_antigoite_x_ray = models.TextField(db_column='AG_Antigoite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ao_aragonite_x_ray = models.TextField(db_column='AO_Aragonite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bt_biotite_x_ray = models.TextField(db_column='BT_Biotite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bc_biotite_chlorite_x_ray = models.TextField(db_column='BC_Biotite_Chlorite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    br_brucite_x_ray = models.TextField(db_column='BR_Brucite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ca_calcite_x_ray = models.TextField(db_column='CA_Calcite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cl_chlorite_x_ray = models.TextField(db_column='CL_Chlorite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cm_chlorite_mica_x_ray = models.TextField(db_column='CM_Chlorite_Mica_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cr_cristobalite_x_ray = models.TextField(db_column='CR_Cristobalite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dl_dolomite_x_ray = models.TextField(db_column='DL_Dolomite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    en_enstatite_x_ray = models.TextField(db_column='EN_Enstatite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fd_feldspar_x_ray = models.TextField(db_column='FD_Feldspar_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gi_gibbsite_x_ray = models.TextField(db_column='GI_Gibbsite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gl_glauconite_x_ray = models.TextField(db_column='GL_Glauconite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ge_geothite_x_ray = models.TextField(db_column='GE_Geothite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gy_gypsum_x_ray = models.TextField(db_column='GY_Gypsum_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kh_halloysite_x_ray = models.TextField(db_column='KH_Halloysite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    he_hematite_x_ray = models.TextField(db_column='HE_Hematite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hn_hornblende_x_ray = models.TextField(db_column='HN_Hornblende_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hb_hydrobiotite_x_ray = models.TextField(db_column='HB_Hydrobiotite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    il_illite_hydromuscovite_x_ray = models.TextField(db_column='IL_Illite_Hydromuscovite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kk_kaolinite_x_ray = models.TextField(db_column='KK_Kaolinite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fl_labradorite_x_ray = models.TextField(db_column='FL_Labradorite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    le_lepidocrocite_x_ray = models.TextField(db_column='LE_Lepidocrocite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mh_maghemite_x_ray = models.TextField(db_column='MH_Maghemite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mg_magnetite_x_ray = models.TextField(db_column='MG_Magnetite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mi_mica_x_ray = models.TextField(db_column='MI_Mica_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mt_montmorillonite_x_ray = models.TextField(db_column='MT_Montmorillonite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mc_montmorillonite_chlorite_x_ray = models.TextField(db_column='MC_Montmorillonite_Chlorite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mm_montmorillonite_mica_x_ray = models.TextField(db_column='MM_Montmorillonite_Mica_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mv_montmorillonite_vermiculite_x_ray = models.TextField(db_column='MV_Montmorillonite_Vermiculite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ms_muscovite_x_ray = models.TextField(db_column='MS_Muscovite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    nx_non_crystalline_x_ray = models.TextField(db_column='NX_Non_Crystalline_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fo_oligoclase_x_ray = models.TextField(db_column='FO_Oligoclase_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fr_orthoclase_x_ray = models.TextField(db_column='FR_Orthoclase_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pg_palygorskite_x_ray = models.TextField(db_column='PG_Palygorskite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pl_phlogophite_x_ray = models.TextField(db_column='PL_Phlogophite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fp_plagioclase_feldspar_x_ray = models.TextField(db_column='FP_Plagioclase_Feldspar_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fk_potassium_feldspar_x_ray = models.TextField(db_column='FK_Potassium_Feldspar_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    py_pyrophyllite_x_ray = models.TextField(db_column='PY_Pyrophyllite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qz_quartz_x_ray = models.TextField(db_column='QZ_Quartz_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    re_resistant_minerals_x_ray = models.TextField(db_column='RE_Resistant_Minerals_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    se_sepiolite_x_ray = models.TextField(db_column='SE_Sepiolite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ta_talc_x_ray = models.TextField(db_column='TA_Talc_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    th_thenardite_x_ray = models.TextField(db_column='TH_thenardite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    td_tridymite_x_ray = models.TextField(db_column='TD_Tridymite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vr_vermiculite_x_ray = models.TextField(db_column='VR_Vermiculite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vc_vermiculite_chlorite_x_ray = models.TextField(db_column='VC_Vermiculite_Chlorite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vh_vermiculite_hydrobiotite_x_ray = models.TextField(db_column='VH_Vermiculite_Hydrobiotite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vm_vermiculite_mica_x_ray = models.TextField(db_column='VM_Vermiculite_Mica_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ze_zeolite_x_ray = models.TextField(db_column='ZE_Zeolite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ha_halite_x_ray = models.TextField(db_column='HA_Halite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hs_hydroxy_interlayered_smectite_x_ray = models.TextField(db_column='HS_Hydroxy_Interlayered_Smectite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hv_hydroxy_interlayered_vermiculite_x_ray = models.TextField(db_column='HV_Hydroxy_Interlayered_Vermiculite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ft_fluorapatite_x_ray = models.TextField(db_column='FT_Fluorapatite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    nu_natrojarosite_x_ray = models.TextField(db_column='NU_Natrojarosite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ha_pt_paragonite_x_ray = models.TextField(db_column='HA_PT_Paragonite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    na_natron_x_ray = models.TextField(db_column='NA_Natron_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    jo_jarosite_x_ray = models.TextField(db_column='JO_Jarosite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sz_serpentine_x_ray = models.TextField(db_column='SZ_Serpentine_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    be_boehmite_x_ray = models.TextField(db_column='BE_Boehmite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bd_beidellite_x_ray = models.TextField(db_column='BD_Beidellite_X_Ray', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    clay_mineral_interpretation = models.TextField(db_column='Clay_Mineral_Interpretation', blank=True, null=True)  # Field name made lowercase.
    coarse_silt_mineral_interpretation = models.TextField(db_column='Coarse_Silt_Mineral_Interpretation', blank=True, null=True)  # Field name made lowercase.
    fine_sand_mineral_interpretation = models.TextField(db_column='Fine_Sand_Mineral_Interpretation', blank=True, null=True)  # Field name made lowercase.
    very_fine_sand_mineral_interpretation = models.TextField(db_column='Very_Fine_Sand_Mineral_Interpretation', blank=True, null=True)  # Field name made lowercase.
    differential_scanning_calorimeter_method = models.TextField(db_column='Differential_Scanning_Calorimeter_Method', blank=True, null=True)  # Field name made lowercase.
    gi_gibbsite_differential_scanning_calorimetry = models.TextField(db_column='GI_Gibbsite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kk_kaolinite_differential_scanning_calorimetry = models.TextField(db_column='KK_Kaolinite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ge_geothite_differential_scanning_calorimetry = models.TextField(db_column='GE_Geothite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gy_gypsum_differential_scanning_calorimetry = models.TextField(db_column='GY_Gypsum_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    at_alunite_differential_scanning_calorimetry = models.TextField(db_column='AT_Alunite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sm_smectite_differential_scanning_calorimetry = models.TextField(db_column='SM_Smectite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kh_halloysite_differential_scanning_calorimetry = models.TextField(db_column='KH_Halloysite_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qz_quartz_differential_scanning_calorimetry = models.TextField(db_column='QZ_Quartz_Differential_Scanning_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    vr_vermiculite_differential_calorimetry = models.TextField(db_column='VR_Vermiculite_Differential_Calorimetry', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    thermal_gravimetric_method = models.TextField(db_column='thermal_Gravimetric_Method', blank=True, null=True)  # Field name made lowercase.
    ag_gypsum_thermal_gravimetric_analysis = models.TextField(db_column='AG_Gypsum_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gi_gibbsite_thermal_gravimetric_analysis = models.TextField(db_column='GI_Gibbsite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ge_kaolinite_differential_thermal_analysis = models.TextField(db_column='GE_Kaolinite_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kk_kaolinite_thermal_gravimetric_analysis = models.TextField(db_column='KK_Kaolinite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ag_antigorite_thermal_gravimetric_analysis = models.TextField(db_column='AG_Antigorite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kh_halloysite_thermal_gravimetric_analysis = models.TextField(db_column='KH_Halloysite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mt_montmorillonite_thermal_gravimetric_analysis = models.TextField(db_column='MT_Montmorillonite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pg_palygorskite_thermal_gravimetric_analysis = models.TextField(db_column='PG_Palygorskite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ca_calcite_thermal_gravimetric_analysis = models.TextField(db_column='CA_Calcite_thermal_Gravimetric_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    differential_thermal_analysis_method = models.TextField(db_column='Differential_thermal_Analysis_Method', blank=True, null=True)  # Field name made lowercase.
    gi_gibbsite_differential_thermal_analysis = models.TextField(db_column='GI_Gibbsite_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kk_kaolinite_differential_thermal_analysis = models.TextField(db_column='KK_Kaolinite_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ge_geothite_differential_thermal_analysis = models.TextField(db_column='GE_Geothite_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    kh_halloysite_differential_thermal_analysis = models.TextField(db_column='KH_Halloysite_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qz_quartz_differential_thermal_analysis = models.TextField(db_column='QZ_Quartz_Differential_thermal_Analysis', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lab_xray_and_thermal'


class StAuxSpatialReferenceSystems(models.Model):
    srid = models.AutoField(primary_key=True)
    auth_name = models.TextField(blank=True, null=True)
    auth_srid = models.TextField(blank=True, null=True)  # This field type is a guess.
    srtext = models.TextField(blank=True, null=True)
    falsex = models.TextField()  # This field type is a guess.
    falsey = models.TextField()  # This field type is a guess.
    xyunits = models.TextField()  # This field type is a guess.
    falsez = models.TextField(blank=True, null=True)  # This field type is a guess.
    zunits = models.TextField(blank=True, null=True)  # This field type is a guess.
    falsem = models.TextField(blank=True, null=True)  # This field type is a guess.
    munits = models.TextField(blank=True, null=True)  # This field type is a guess.
    xycluster_tol = models.TextField(blank=True, null=True)  # This field type is a guess.
    zcluster_tol = models.TextField(blank=True, null=True)  # This field type is a guess.
    mcluster_tol = models.TextField(blank=True, null=True)  # This field type is a guess.
    object_flags = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'st_aux_spatial_reference_systems'
