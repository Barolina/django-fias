#coding: utf-8
from __future__ import unicode_literals, absolute_import
from django.db.models import Min
from fias.config import FIAS_TABLES, FIAS_DELETED_TABLES
from fias.importer.log import log
from fias.importer.table import Table
from fias.models import Status, Version
import rarfile
from urllib import urlretrieve


class Archive(object):
    field_name = 'complete_xml_url'

    def __init__(self, version=None, path=None):
        assert version is not None or path is not None, 'Необходимо указать версию или путь к скачанному архиву'
        if version is not None:
            assert isinstance(version, Version), '`{0}` - это не объект типа {1}'.format(repr(version), type(Version))

        self._version = None
        self._tables = None
        self._archive = None
        self._date = None
        self._retrieve(version, path)

    def _retrieve(self, version=None, path=None):
        if path is None:
            path = urlretrieve(getattr(version, self.field_name))[0]
        self._archive = rarfile.RarFile(path)

        if self._version is None:
            self._version = self._get_version()

        return self._archive

    @property
    def tables(self):
        if self._tables is None:
            self._tables = {}
            for filename in self._archive.namelist():
                table = Table(archive=self, filename=filename)
                self._tables[table.full_name] = table
        
        return self._tables

    @property
    def dump_date(self):
        if self._date is None:
            table = self.tables.items()[0][1]
            self._date = table.date
        return self._date

    def _get_version(self):
        try:
            return Version.objects.filter(dumpdate=self.dump_date).latest('dumpdate')
        except Version.DoesNotExist:
            return Version.objects.filter(dumpdate__lte=self.dump_date).latest('dumpdate')

    def open(self, filename):
        return self._archive.open(filename)

    def load(self, truncate=False):
        for table_name in FIAS_TABLES:
            try:
                table = self.tables[table_name]
            except KeyError:
                log.debug('Table `{0}` not found in archive'.format(table_name))
                continue

            try:
                status = Status.objects.get(table=table_name)
            except Status.DoesNotExist:
                table.load()

                status = Status(table=table.full_name, ver=self._version)
                status.save()

                self._process_deleted_table(table_name)
            else:
                log.warning('Table `{0}` has version `{1}`. '
                            'Please use --force-replace for replace '
                            'all tables. Skipping...'.format(status.table, status.ver))

    def _process_deleted_table(self, table_name):
        if table_name in FIAS_DELETED_TABLES:
            try:
                table = self.tables['del_' + table_name]
            except KeyError:
                return

            #TODO: дописать обработчик


class DeltaArchive(Archive):
    field_name = 'delta_xml_url'

    def load(self, truncate=False):
        min_version = Status.objects.aggregate(Min('ver'))['ver__min']
        if min_version is not None:
            for version in Version.objects.filter(ver__gt=min_version).order_by('ver'):

                for table_name in FIAS_TABLES:
                    try:
                        table = self.tables[table_name]
                    except KeyError:
                        log.debug('Table `{0}` not found in archive'.format(table_name))
                        continue

                    try:
                        status = Status.objects.get(table=table)
                    except Status.DoesNotExist:
                        log.warning('Can`t update table `{0}`. Status is unknown!'.format(table))
                    else:
                        if self._version.ver < version.ver:
                            table.load(update=True)

                            status.ver = version
                            status.save()

                            self._process_deleted_table(table_name)
                        else:
                            log.info('Table `{0}` is up to date. Version: {1}'.format(table_name, status.ver))
        else:
            log.error('Not available. Please import the data before updating')
