from sqlalchemy import *

metadata = MetaData()


def PKColumn(name):
    return Column(name,Integer,primary_key=True)

def FKColumn(name,target,nullable):
    return Column(name,Integer,ForeignKey(target),nullable=nullable)

# Key-value tables - simple tables.

def KVTable(name):
    return Table(name,metadata,
                PKColumn('id'),
                Column('name',String(200),nullable=False)
    )

geology = KVTable('geology')

review_status = KVTable('review_status')

iwi = KVTable('iwi')

marae = KVTable('marae')

site_type = KVTable('site_type')

tla = KVTable('tla')

site_ownership_type = KVTable('site_ownership_type')

region = KVTable('region')

media_type = KVTable('media_type')

petroglyph = KVTable('petroglyph')

pigment = KVTable('pigment')

nztm_source = KVTable('nztm_source')

findable = KVTable('findable')

site = Table('site',metadata,
             PKColumn('id'),
             Column('nzaa_id',String(45),nullable=False),
             Column('nzaa_id_imperial',String(45),nullable=True),
             Column('linz_title_number',String(45),nullable=True),
             Column('srs_updated',Date,nullable=True),
             Column('history',Text,nullable=True),
             Column('file_note',String(400),nullable=True),
             Column('type_short_description',Text,nullable=False),
             FKColumn('type_id','site_type.id',False),
             FKColumn('ownership_type_id','site_ownership_type.id',False),
             Column('nztm_e',Float,nullable=True),
             Column('nztm_n',Float,nullable=True),
             Column('elevation',Float,nullable=True),
             Column('location_1',String(300),nullable=False),
             Column('location_2',String(300),nullable=True),
             FKColumn('region_id','region.id',False),
             FKColumn('tla_id','tla.id',False),
             FKColumn('nztm_source_id','nztm_source.id',False),
             Column('media_folder_url',String(400),nullable=True)
)

site_geology = Table('site_geology',metadata,
                     PKColumn('id'),
                     FKColumn('geology_id','geology.id',False),
                     FKColumn('site_id','site.id',False)
)

site_project_status = Table('site_project_status',metadata,
                            PKColumn('id'),
                            Column('is_file_note_completed',Boolean,nullable=False),
                            Column('is_easy_to_find',Boolean,nullable=False),
                            FKColumn('site_id','site.id',False),
                            FKColumn('status_id','review_status.id',False)
)

site_iwi = Table('site_iwi',metadata,
                 PKColumn('id'),
                 FKColumn('site_id','site.id',False),
                 FKColumn('marae_id','marae.id',False)
)

site_marae = Table('site_marae',metadata,
                   PKColumn('id'),
                   FKColumn('site_id','site.id',False),
                   FKColumn('marae_id','marae.id',False)
)

site_names = Table('site_names',metadata,
                   PKColumn('id'),
                   FKColumn('site_id','site.id',False),
                   Column('name',String(200),nullable=False)
)

site_media_type = Table('site_media_type',metadata,
                        PKColumn('id'),
                        FKColumn('site_id','site.id',False),
                        FKColumn('media_type_id','media_type.id',False)
)

reference = Table('reference',metadata,
                  PKColumn('id'),
                  Column('name',String(200),nullable=False),
                  Column('author',String(200),nullable=False),
                  Column('date',Date,nullable=False),
                  Column('details',Text, nullable=True),
                  Column('url',String(200),nullable=True)
)

site_location_info_source = Table('site_location_info_source',metadata,
                                  PKColumn('id'),
                                  FKColumn('site_id','site.id',False),
                                  FKColumn('location_info_source_id','reference.id',False)
)

site_source = Table('site_source',metadata,
                    PKColumn('id'),
                    FKColumn('site_id','site.id',False),
                    FKColumn('source_id','reference.id',False)
)


panel = Table('panel',metadata,
              PKColumn('id'),
              FKColumn('site_id','site.id',False),
              Column('location',Text,nullable=False),
              Column('condition',Text,nullable=True)
)

element = Table('element',metadata,
                PKColumn('id'),
                FKColumn('site_id','site.id',False),
                FKColumn('panel_id','panel.id',True),
                Column('condition',Text,nullable=True),
                Column('location',Text,nullable=True),
                Column('nztm_n',Float,nullable=True),
                Column('nztm_e',Float,nullable=True),
                Column('elevation',Float,nullable=True)
)

record = Table('record',metadata,
               PKColumn('id'),
               FKColumn('site_id','site.id',False),
               Column('creator',String(150),nullable=False),
               Column('in_situ',Boolean,nullable=False),
               Column('in_situ_comment',Text,nullable=True),
               FKColumn('findable','findable.id',nullable=False),
               Column('findable_comment',Text,nullable=True),
               # A record must either have an exact date when it is recorded,
               # or a comment stating a rough period when it was recorded.
               Column('date_of_record',Date,nullable=True),
               Column('date_of_record_comment',Text,nullable=True),
               Column('archaeological_features',Text,nullable=True),
               Column('subject_description',Text,nullable=True),
               Column('site_condition',Text,nullable=True),
               Column('vegetation',Text,nullable=True),
               Column('waterways',Text,nullable=True),
               Column('features',Text,nullable=True),
               Column('land_use',Text,nullable=True)
)

record_nearby_archaeology = Table('record_nearby_archaeology',metadata,
                                  PKColumn('id'),
                                  FKColumn('site_id','site.id',False),
                                  Column('nearby_archaeology',Text,nullable=False)
)

record_subject = Table('record_subject', metadata,
                       PKColumn('id'),
                       FKColumn('record_id','record.id',False),
                       FKColumn('element_id','element.id',False),
                       # The values in this column needs to be constrained to valid values.
                       Column('subject_name',String(45),nullable=False)
)

record_petroglyph = Table('record_petroglyph',metadata,
                          PKColumn('id'),
                          FKColumn('record_id','record.id',False),
                          FKColumn('element_id','element.id',False),
                          FKColumn('petroglyph_id','petroglyph.id',False)
)

record_pigment = Table('record_pigment',metadata,
                       PKColumn('id'),
                       FKColumn('record_id','record.id',False),
                       FKColumn('element_id','element.id',False),
                       FKColumn('pigment_id','pigment.id',False)
)

media = Table('media',metadata,
              PKColumn('id'),
              FKColumn('media_type_id','media_type.id',False),
              Column('media_file_name',String(400),nullable=True),
              Column('subject',Text,nullable=True),
              Column('date_taken',Date,nullable=False),
              Column('creator',String(150),nullable=False),
              Column('enhancement_comment',Text,nullable=True),
              Column('light_condition_comment',Text,nullable=True),
              Column('url',String(400),nullable=True),
              Column('use_conditions',Text,nullable=True),
              FKColumn('source_id','reference.id',True),
              FKColumn('record_id','record.id',True)
)

media_element = Table('media_element',metadata,
                      PKColumn('id'),
                      FKColumn('media_id','media.id',False),
                      FKColumn('element_id','element.id',False)
)

media_panel = Table('media_panel',metadata,
                      PKColumn('id'),
                      FKColumn('media_id','media.id',False),
                      FKColumn('panel_id','panel.id',False)
)
