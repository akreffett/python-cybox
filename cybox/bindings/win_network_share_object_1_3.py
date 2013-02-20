#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Generated Tue Nov 06 14:04:14 2012 by generateDS.py version 2.7c.
#

import sys
import getopt
import re as re_

import cybox_common_types_1_0

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    if Verbose_import_:
        print 'Error: LXML version 2.3+ required for parsing files'

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# User methods
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError, exp:

    class GeneratedsSuper(object):
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_validate_integer(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_integer_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError), exp:
                    raise_parse_error(node, 'Requires sequence of integers')
            return input_data
        def gds_format_float(self, input_data, input_name=''):
            return '%f' % input_data
        def gds_validate_float(self, input_data, node, input_name=''):
            return input_data
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_float_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError), exp:
                    raise_parse_error(node, 'Requires sequence of floats')
            return input_data
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_validate_double(self, input_data, node, input_name=''):
            return input_data
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_double_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError), exp:
                    raise_parse_error(node, 'Requires sequence of doubles')
            return input_data
        def gds_format_boolean(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean(self, input_data, node, input_name=''):
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in ('true', '1', 'false', '0', ):
                    raise_parse_error(node, 'Requires sequence of booleans ("true", "1", "false", "0")')
            return input_data
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')

#
# Support/utility functions.
#

def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')

def quote_xml(inStr):
    if not inStr:
        return ''
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1

def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text

def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


class GDSParseError(Exception):
    pass

def raise_parse_error(node, msg):
    if XMLParser_import_library == XMLParser_import_lxml:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    else:
        msg = '%s (element %s)' % (msg, node.tag, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace, pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip(): 
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, namespace, name, pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container

def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#

class SharedResourceType(cybox_common_types_1_0.BaseObjectAttributeType):
    """SharedResourceType specifies Windows shared resource types via a
    union of the SharedResourceTypeEnum type and the atomic
    xs:string type. Its base type is the CybOX Core
    cybox_common_types_1_0.BaseObjectAttributeType, for permitting complex (i.e. regular-
    expression based) specifications.This attribute is optional and
    specifies the expected type for the value of the specified
    element."""
    subclass = None
    superclass = cybox_common_types_1_0.BaseObjectAttributeType
    def __init__(self, end_range=None, pattern_type=None, has_changed=None, value_set=None, datatype='String', refanging_transform=None, refanging_transform_type=None, appears_random=None, trend=None, defanging_algorithm_ref=None, is_obfuscated=None, regex_syntax=None, obfuscation_algorithm_ref=None, start_range=None, idref=None, is_defanged=None, id=None, condition=None, valueOf_=None):
        super(SharedResourceType, self).__init__(end_range, pattern_type, has_changed, value_set, datatype, refanging_transform, refanging_transform_type, appears_random, trend, defanging_algorithm_ref, is_obfuscated, regex_syntax, obfuscation_algorithm_ref, start_range, idref, is_defanged, id, condition, valueOf_, )
        self.datatype = _cast(None, datatype)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if SharedResourceType.subclass:
            return SharedResourceType.subclass(*args_, **kwargs_)
        else:
            return SharedResourceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_datatype(self): return self.datatype
    def set_datatype(self, datatype): self.datatype = datatype
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='WinNetworkShareObj:', name_='SharedResourceType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = []
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='SharedResourceType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(str(self.valueOf_).encode(ExternalEncoding))
            self.exportChildren(outfile, level + 1, namespace_, name_, pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespace_='WinNetworkShareObj:', name_='SharedResourceType'):
        super(SharedResourceType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='SharedResourceType')
        if self.datatype is not None and 'datatype' not in already_processed:
            already_processed.append('datatype')
            outfile.write(' datatype=%s' % (quote_attrib(self.datatype), ))
    def exportChildren(self, outfile, level, namespace_='WinNetworkShareObj:', name_='SharedResourceType', fromsubclass_=False, pretty_print=True):
        super(SharedResourceType, self).exportChildren(outfile, level, 'WinNetworkShareObj:', name_, True, pretty_print=pretty_print)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(SharedResourceType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SharedResourceType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.datatype is not None and 'datatype' not in already_processed:
            already_processed.append('datatype')
            showIndent(outfile, level)
            outfile.write('datatype = %s,\n' % (self.datatype,))
        super(SharedResourceType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(SharedResourceType, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('datatype', node)
        if value is not None and 'datatype' not in already_processed:
            already_processed.append('datatype')
            self.datatype = value
        super(SharedResourceType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        pass
# end class SharedResourceType

class WindowsNetworkShareObjectType(cybox_common_types_1_0.DefinedObjectType):
    """he WindowsNetworkShareObjectType type is intended to characterize
    Windows network shares."""
    subclass = None
    superclass = cybox_common_types_1_0.DefinedObjectType
    def __init__(self, object_reference=None, ACCESS_PERM=None, ACCESS_ATRIB=None, ACCESS_ALL=None, ACCESS_READ=None, ACCESS_DELETE=None, ACCESS_WRITE=None, ACCESS_CREATE=None, ACCESS_EXEC=None, Current_Uses=None, Local_Path=None, Max_Uses=None, Netname=None, Type=None):
        super(WindowsNetworkShareObjectType, self).__init__(object_reference, )
        self.ACCESS_PERM = _cast(bool, ACCESS_PERM)
        self.ACCESS_ATRIB = _cast(bool, ACCESS_ATRIB)
        self.ACCESS_ALL = _cast(bool, ACCESS_ALL)
        self.ACCESS_READ = _cast(bool, ACCESS_READ)
        self.ACCESS_DELETE = _cast(bool, ACCESS_DELETE)
        self.ACCESS_WRITE = _cast(bool, ACCESS_WRITE)
        self.ACCESS_CREATE = _cast(bool, ACCESS_CREATE)
        self.ACCESS_EXEC = _cast(bool, ACCESS_EXEC)
        self.Current_Uses = Current_Uses
        self.Local_Path = Local_Path
        self.Max_Uses = Max_Uses
        self.Netname = Netname
        self.Type = Type
    def factory(*args_, **kwargs_):
        if WindowsNetworkShareObjectType.subclass:
            return WindowsNetworkShareObjectType.subclass(*args_, **kwargs_)
        else:
            return WindowsNetworkShareObjectType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_Current_Uses(self): return self.Current_Uses
    def set_Current_Uses(self, Current_Uses): self.Current_Uses = Current_Uses
    def validate_NonNegativeIntegerObjectAttributeType(self, value):
        # Validate type cybox_common_types_1_0.NonNegativeIntegerObjectAttributeType, a restriction on None.
        pass
    def get_Local_Path(self): return self.Local_Path
    def set_Local_Path(self, Local_Path): self.Local_Path = Local_Path
    def validate_StringObjectAttributeType(self, value):
        # Validate type cybox_common_types_1_0.StringObjectAttributeType, a restriction on None.
        pass
    def get_Max_Uses(self): return self.Max_Uses
    def set_Max_Uses(self, Max_Uses): self.Max_Uses = Max_Uses
    def get_Netname(self): return self.Netname
    def set_Netname(self, Netname): self.Netname = Netname
    def get_Type(self): return self.Type
    def set_Type(self, Type): self.Type = Type
    def validate_SharedResourceType(self, value):
        # Validate type SharedResourceType, a restriction on None.
        pass
    def get_ACCESS_PERM(self): return self.ACCESS_PERM
    def set_ACCESS_PERM(self, ACCESS_PERM): self.ACCESS_PERM = ACCESS_PERM
    def get_ACCESS_ATRIB(self): return self.ACCESS_ATRIB
    def set_ACCESS_ATRIB(self, ACCESS_ATRIB): self.ACCESS_ATRIB = ACCESS_ATRIB
    def get_ACCESS_ALL(self): return self.ACCESS_ALL
    def set_ACCESS_ALL(self, ACCESS_ALL): self.ACCESS_ALL = ACCESS_ALL
    def get_ACCESS_READ(self): return self.ACCESS_READ
    def set_ACCESS_READ(self, ACCESS_READ): self.ACCESS_READ = ACCESS_READ
    def get_ACCESS_DELETE(self): return self.ACCESS_DELETE
    def set_ACCESS_DELETE(self, ACCESS_DELETE): self.ACCESS_DELETE = ACCESS_DELETE
    def get_ACCESS_WRITE(self): return self.ACCESS_WRITE
    def set_ACCESS_WRITE(self, ACCESS_WRITE): self.ACCESS_WRITE = ACCESS_WRITE
    def get_ACCESS_CREATE(self): return self.ACCESS_CREATE
    def set_ACCESS_CREATE(self, ACCESS_CREATE): self.ACCESS_CREATE = ACCESS_CREATE
    def get_ACCESS_EXEC(self): return self.ACCESS_EXEC
    def set_ACCESS_EXEC(self, ACCESS_EXEC): self.ACCESS_EXEC = ACCESS_EXEC
    def export(self, outfile, level, namespace_='WinNetworkShareObj:', name_='WindowsNetworkShareObjectType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = []
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='WindowsNetworkShareObjectType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespace_, name_, pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespace_='WinNetworkShareObj:', name_='WindowsNetworkShareObjectType'):
        super(WindowsNetworkShareObjectType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='WindowsNetworkShareObjectType')
        if self.ACCESS_PERM is not None and 'ACCESS_PERM' not in already_processed:
            already_processed.append('ACCESS_PERM')
            outfile.write(' ACCESS_PERM="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_PERM)), input_name='ACCESS_PERM'))
        if self.ACCESS_ATRIB is not None and 'ACCESS_ATRIB' not in already_processed:
            already_processed.append('ACCESS_ATRIB')
            outfile.write(' ACCESS_ATRIB="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_ATRIB)), input_name='ACCESS_ATRIB'))
        if self.ACCESS_ALL is not None and 'ACCESS_ALL' not in already_processed:
            already_processed.append('ACCESS_ALL')
            outfile.write(' ACCESS_ALL="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_ALL)), input_name='ACCESS_ALL'))
        if self.ACCESS_READ is not None and 'ACCESS_READ' not in already_processed:
            already_processed.append('ACCESS_READ')
            outfile.write(' ACCESS_READ="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_READ)), input_name='ACCESS_READ'))
        if self.ACCESS_DELETE is not None and 'ACCESS_DELETE' not in already_processed:
            already_processed.append('ACCESS_DELETE')
            outfile.write(' ACCESS_DELETE="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_DELETE)), input_name='ACCESS_DELETE'))
        if self.ACCESS_WRITE is not None and 'ACCESS_WRITE' not in already_processed:
            already_processed.append('ACCESS_WRITE')
            outfile.write(' ACCESS_WRITE="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_WRITE)), input_name='ACCESS_WRITE'))
        if self.ACCESS_CREATE is not None and 'ACCESS_CREATE' not in already_processed:
            already_processed.append('ACCESS_CREATE')
            outfile.write(' ACCESS_CREATE="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_CREATE)), input_name='ACCESS_CREATE'))
        if self.ACCESS_EXEC is not None and 'ACCESS_EXEC' not in already_processed:
            already_processed.append('ACCESS_EXEC')
            outfile.write(' ACCESS_EXEC="%s"' % self.gds_format_boolean(self.gds_str_lower(str(self.ACCESS_EXEC)), input_name='ACCESS_EXEC'))
    def exportChildren(self, outfile, level, namespace_='WinNetworkShareObj:', name_='WindowsNetworkShareObjectType', fromsubclass_=False, pretty_print=True):
        super(WindowsNetworkShareObjectType, self).exportChildren(outfile, level, 'WinNetworkShareObj:', name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Current_Uses is not None:
            self.Current_Uses.export(outfile, level, 'WinNetworkShareObj:', name_='Current_Uses', pretty_print=pretty_print)
        if self.Local_Path is not None:
            self.Local_Path.export(outfile, level, 'WinNetworkShareObj:', name_='Local_Path', pretty_print=pretty_print)
        if self.Max_Uses is not None:
            self.Max_Uses.export(outfile, level, 'WinNetworkShareObj:', name_='Max_Uses', pretty_print=pretty_print)
        if self.Netname is not None:
            self.Netname.export(outfile, level, 'WinNetworkShareObj:', name_='Netname', pretty_print=pretty_print)
        if self.Type is not None:
            self.Type.export(outfile, level, 'WinNetworkShareObj:', name_='Type', pretty_print=pretty_print)
    def hasContent_(self):
        if (
            self.Current_Uses is not None or
            self.Local_Path is not None or
            self.Max_Uses is not None or
            self.Netname is not None or
            self.Type is not None or
            super(WindowsNetworkShareObjectType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='WindowsNetworkShareObjectType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.ACCESS_PERM is not None and 'ACCESS_PERM' not in already_processed:
            already_processed.append('ACCESS_PERM')
            showIndent(outfile, level)
            outfile.write('ACCESS_PERM = %s,\n' % (self.ACCESS_PERM,))
        if self.ACCESS_ATRIB is not None and 'ACCESS_ATRIB' not in already_processed:
            already_processed.append('ACCESS_ATRIB')
            showIndent(outfile, level)
            outfile.write('ACCESS_ATRIB = %s,\n' % (self.ACCESS_ATRIB,))
        if self.ACCESS_ALL is not None and 'ACCESS_ALL' not in already_processed:
            already_processed.append('ACCESS_ALL')
            showIndent(outfile, level)
            outfile.write('ACCESS_ALL = %s,\n' % (self.ACCESS_ALL,))
        if self.ACCESS_READ is not None and 'ACCESS_READ' not in already_processed:
            already_processed.append('ACCESS_READ')
            showIndent(outfile, level)
            outfile.write('ACCESS_READ = %s,\n' % (self.ACCESS_READ,))
        if self.ACCESS_DELETE is not None and 'ACCESS_DELETE' not in already_processed:
            already_processed.append('ACCESS_DELETE')
            showIndent(outfile, level)
            outfile.write('ACCESS_DELETE = %s,\n' % (self.ACCESS_DELETE,))
        if self.ACCESS_WRITE is not None and 'ACCESS_WRITE' not in already_processed:
            already_processed.append('ACCESS_WRITE')
            showIndent(outfile, level)
            outfile.write('ACCESS_WRITE = %s,\n' % (self.ACCESS_WRITE,))
        if self.ACCESS_CREATE is not None and 'ACCESS_CREATE' not in already_processed:
            already_processed.append('ACCESS_CREATE')
            showIndent(outfile, level)
            outfile.write('ACCESS_CREATE = %s,\n' % (self.ACCESS_CREATE,))
        if self.ACCESS_EXEC is not None and 'ACCESS_EXEC' not in already_processed:
            already_processed.append('ACCESS_EXEC')
            showIndent(outfile, level)
            outfile.write('ACCESS_EXEC = %s,\n' % (self.ACCESS_EXEC,))
        super(WindowsNetworkShareObjectType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(WindowsNetworkShareObjectType, self).exportLiteralChildren(outfile, level, name_)
        if self.Current_Uses is not None:
            showIndent(outfile, level)
            outfile.write('Current_Uses=model_.cybox_common_types_1_0.NonNegativeIntegerObjectAttributeType(\n')
            self.Current_Uses.exportLiteral(outfile, level, name_='Current_Uses')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.Local_Path is not None:
            showIndent(outfile, level)
            outfile.write('Local_Path=model_.cybox_common_types_1_0.StringObjectAttributeType(\n')
            self.Local_Path.exportLiteral(outfile, level, name_='Local_Path')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.Max_Uses is not None:
            showIndent(outfile, level)
            outfile.write('Max_Uses=model_.cybox_common_types_1_0.NonNegativeIntegerObjectAttributeType(\n')
            self.Max_Uses.exportLiteral(outfile, level, name_='Max_Uses')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.Netname is not None:
            showIndent(outfile, level)
            outfile.write('Netname=model_.cybox_common_types_1_0.StringObjectAttributeType(\n')
            self.Netname.exportLiteral(outfile, level, name_='Netname')
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.Type is not None:
            showIndent(outfile, level)
            outfile.write('Type=model_.SharedResourceType(\n')
            self.Type.exportLiteral(outfile, level, name_='Type')
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('ACCESS_PERM', node)
        if value is not None and 'ACCESS_PERM' not in already_processed:
            already_processed.append('ACCESS_PERM')
            if value in ('true', '1'):
                self.ACCESS_PERM = True
            elif value in ('false', '0'):
                self.ACCESS_PERM = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_ATRIB', node)
        if value is not None and 'ACCESS_ATRIB' not in already_processed:
            already_processed.append('ACCESS_ATRIB')
            if value in ('true', '1'):
                self.ACCESS_ATRIB = True
            elif value in ('false', '0'):
                self.ACCESS_ATRIB = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_ALL', node)
        if value is not None and 'ACCESS_ALL' not in already_processed:
            already_processed.append('ACCESS_ALL')
            if value in ('true', '1'):
                self.ACCESS_ALL = True
            elif value in ('false', '0'):
                self.ACCESS_ALL = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_READ', node)
        if value is not None and 'ACCESS_READ' not in already_processed:
            already_processed.append('ACCESS_READ')
            if value in ('true', '1'):
                self.ACCESS_READ = True
            elif value in ('false', '0'):
                self.ACCESS_READ = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_DELETE', node)
        if value is not None and 'ACCESS_DELETE' not in already_processed:
            already_processed.append('ACCESS_DELETE')
            if value in ('true', '1'):
                self.ACCESS_DELETE = True
            elif value in ('false', '0'):
                self.ACCESS_DELETE = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_WRITE', node)
        if value is not None and 'ACCESS_WRITE' not in already_processed:
            already_processed.append('ACCESS_WRITE')
            if value in ('true', '1'):
                self.ACCESS_WRITE = True
            elif value in ('false', '0'):
                self.ACCESS_WRITE = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_CREATE', node)
        if value is not None and 'ACCESS_CREATE' not in already_processed:
            already_processed.append('ACCESS_CREATE')
            if value in ('true', '1'):
                self.ACCESS_CREATE = True
            elif value in ('false', '0'):
                self.ACCESS_CREATE = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('ACCESS_EXEC', node)
        if value is not None and 'ACCESS_EXEC' not in already_processed:
            already_processed.append('ACCESS_EXEC')
            if value in ('true', '1'):
                self.ACCESS_EXEC = True
            elif value in ('false', '0'):
                self.ACCESS_EXEC = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        super(WindowsNetworkShareObjectType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Current_Uses':
            obj_ = cybox_common_types_1_0.NonNegativeIntegerObjectAttributeType.factory()
            obj_.build(child_)
            self.set_Current_Uses(obj_)
        elif nodeName_ == 'Local_Path':
            obj_ = cybox_common_types_1_0.StringObjectAttributeType.factory()
            obj_.build(child_)
            self.set_Local_Path(obj_)
        elif nodeName_ == 'Max_Uses':
            obj_ = cybox_common_types_1_0.NonNegativeIntegerObjectAttributeType.factory()
            obj_.build(child_)
            self.set_Max_Uses(obj_)
        elif nodeName_ == 'Netname':
            obj_ = cybox_common_types_1_0.StringObjectAttributeType.factory()
            obj_.build(child_)
            self.set_Netname(obj_)
        elif nodeName_ == 'Type':
            obj_ = SharedResourceType.factory()
            obj_.build(child_)
            self.set_Type(obj_)
        super(WindowsNetworkShareObjectType, self).buildChildren(child_, node, nodeName_, True)
# end class WindowsNetworkShareObjectType

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)

def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = globals().get(tag)
    return tag, rootClass

def parse(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_Network_Share'
        rootClass = WindowsNetworkShareObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='',
        pretty_print=True)
    return rootObj

def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_Network_Share'
        rootClass = WindowsNetworkShareObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="Windows_Network_Share",
        namespacedef_='')
    return rootObj

def parseLiteral(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_Network_Share'
        rootClass = WindowsNetworkShareObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from temp import *\n\n')
    sys.stdout.write('import temp as model_\n\n')
    sys.stdout.write('rootObj = model_.rootTag(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
    sys.stdout.write(')\n')
    return rootObj

def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()

if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

__all__ = [
    "WindowsNetworkShareObjectType",
    "SharedResourceType"
    ]