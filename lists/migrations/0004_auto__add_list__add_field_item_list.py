# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'List'
        db.create_table('lists_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['List'])

        # Adding field 'Item.list'
        db.add_column('lists_item', 'list',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.List'], default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'List'
        db.delete_table('lists_list')

        # Deleting field 'Item.list'
        db.delete_column('lists_item', 'list_id')


    models = {
        'lists.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.List']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'lists.list': {
            'Meta': {'object_name': 'List'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['lists']