# Generated by Django 4.0.7 on 2022-11-29 06:23

from django.db import migrations

CREATE_TRIGGER_SQL = """
CREATE TRIGGER "tgr_{model}_search"
  BEFORE INSERT OR UPDATE
  ON "{db_table}"
  FOR EACH ROW EXECUTE PROCEDURE
  tsvector_update_trigger("search_data", 'pg_catalog.portuguese', {fields})
"""
DROP_TRIGGER_SQL = """
DROP TRIGGER "tgr_{model}_search"
  ON "{db_table}"
"""

def trigger_sql(model, db_table, fields):
    return (
        CREATE_TRIGGER_SQL.format(model=model, db_table=db_table, fields=fields).strip(),
        DROP_TRIGGER_SQL.format(model=model, db_table=db_table).strip(),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('metamemoapp', '0006_memocontext_search_data_memoitem_search_data_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            *trigger_sql(
                model="memoitem",
                db_table="metamemoapp_memoitem",
                fields="title, content",
            ),
        ),
        migrations.RunSQL(
            *trigger_sql(
                model="memomedia",
                db_table="metamemoapp_memomedia",
                fields="transcription",
            ),
        ),
        migrations.RunSQL(
            *trigger_sql(
                model="memocontext",
                db_table="metamemoapp_memocontext",
                fields="context",
            ),
        ),
        migrations.RunSQL(
            *trigger_sql(
                model="newsitem",
                db_table="metamemoapp_newsitem",
                fields="title, text",
            ),
        ),
    ]
