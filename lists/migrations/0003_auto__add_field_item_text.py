# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.text'
        db.add_column('lists_item', 'text',
                      self.gf('django.db.models.fields.TextField')(default='default'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.text'
        db.delete_column('lists_item', 'text')


    models = {
        'lists.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['lists']