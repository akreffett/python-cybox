# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

__version__ = "2.0.0b2"

import collections
import json
from StringIO import StringIO

from cybox.utils import NamespaceParser, META


def get_xmlns_string(ns_set):
    """Build a string with 'xmlns' definitions for every namespace in ns_set.

    Arguments:
    - ns_set: a set (or other iterable) of Namespace objects
    """
    xmlns_format = 'xmlns:{0.prefix}="{0.name}"'
    return "\n\t".join([xmlns_format.format(x) for x in ns_set])


def get_schemaloc_string(ns_set):
    """Build a "schemaLocation" string for every namespace in ns_set.

    Arguments:
    - ns_set: a set (or other iterable) of Namespace objects
    """
    schemaloc_format = '{0.name} {0.schema_location}'
    # Only include schemas that have a schema_location defined (for instance,
    # 'xsi' does not.
    return " ".join([schemaloc_format.format(x) for x in ns_set
                     if x.schema_location])


class Entity(object):
    """Base class for all classes in the Cybox SimpleAPI."""

    # By default (unless a particular subclass states otherwise), try to "cast"
    # invalid objects to the correct class using the constructor. Entity
    # subclasses should either provide a "sane" constructor or set this to
    # False.
    _try_cast = True

    # No vars on the base Entity class
    __vars__ = []

    @classmethod
    def _get_vars(cls):
        var_list = []
        var_list.extend(cls.__vars__)
        for baseclass in cls.__bases__:
            var_list.extend(baseclass.__vars__)

        return var_list

    def to_obj(self):
        """Default implementation of a to_obj function.

        Subclasses can override this function."""

        entity_obj = self._binding_class()

        for field in self.__class__._get_vars():
            val = getattr(self, field.attr_name)

            if isinstance(val, Entity):
                val = val.to_obj()

            setattr(entity_obj, field.name, val)

        self._finalize_obj(entity_obj)

        return entity_obj

    def _finalize_obj(self, entity_obj):
        """Subclasses can define additional items in the binding object.

        `entity_obj` should be modified in place.
        """
        pass

    def to_dict(self):
        """Default implementation of a to_dict function.

        Subclasses can override this function."""

        entity_dict = {}

        for field in self.__class__._get_vars():
            val = getattr(self, field.attr_name)

            if isinstance(val, EntityList):
                val = val.to_list()

            elif isinstance(val, Entity):
                val = val.to_dict()

            # Only return non-None objects
            if val is not None:
                entity_dict[field.key_name] = val

        self._finalize_dict(entity_dict)

        return entity_dict

    def _finalize_dict(self, entity_dict):
        """Subclasses can define additional items in the dictionary.

        `entity_dict` should be modified in place.
        """
        pass

    @classmethod
    def from_obj(cls, cls_obj=None):
        if not cls_obj:
            return None

        entity = cls()

        for field in cls._get_vars():
            val = getattr(cls_obj, field.name)
            if field.type_:
                val = field.type_.from_obj(val)
            setattr(entity, field.attr_name, val)

        return entity

    @classmethod
    def from_dict(cls, cls_dict=None):
        if cls_dict is None:
            return None

        entity = cls()

        # Shortcut if an actual dict is not provided:
        if not isinstance(cls_dict, dict):
            value = cls_dict
            # Call the class's constructor
            return cls(value)

        for field in cls._get_vars():
            val = cls_dict.get(field.key_name)
            if field.type_:
                if issubclass(field.type_, EntityList):
                    val = field.type_.from_list(val)
                else:
                    val = field.type_.from_dict(val)
            setattr(entity, field.attr_name, val)

        return entity

    def to_xml(self, include_namespaces=False):
        """Export an object as an XML String"""

        if include_namespaces:
            namespace_def = self._get_namespace_def()
        else:
            namespace_def = ""

        s = StringIO()
        self.to_obj().export(s, 0, namespacedef_=namespace_def)
        return s.getvalue()

    def to_json(self):
        return json.dumps(self.to_dict())

    def _get_namespace_def(self):
        # copy necessary namespaces
        namespaces = self._get_namespaces()

        # if there are any other namepaces, include xsi for "schemaLocation"
        if namespaces:
            namespaces.update([META.lookup_prefix('xsi')])

        if not namespaces:
            return ""

        return ('\n\t' + get_xmlns_string(namespaces) +
                '\n\txsi:schemaLocation="' + get_schemaloc_string(namespaces) +
                '"')

    def _get_namespaces(self, recurse=True):
        ns = set()

        try:
            ns.update([META.lookup_namespace(self._namespace)])
        # TODO: Remove this 'except' once every class has defined a _namespace
        except AttributeError:
            pass

        #In case of recursive relationships, don't process this item twice
        self.touched = True
        if recurse:
            for x in self._get_children():
                if not hasattr(x, 'touched'):
                    ns.update(x._get_namespaces())

        del self.touched

        #print self.__class__, "-", ns
        return ns

    def _get_children(self):
        for k, v in vars(self).items():
            if isinstance(v, Entity):
                yield v
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, Entity):
                        yield item

    @classmethod
    def istypeof(cls, obj):
        """Check if `cls` is the type of `obj`

        In the normal case, as implemented here, a simple isinstance check is
        used. However, there are more complex checks possible. For instance,
        EmailAddress.istypeof(obj) checks if obj is an Address object with
        a category of Address.CAT_EMAIL
        """
        return isinstance(obj, cls)

    @classmethod
    def object_from_dict(cls, entity_dict):
        """Convert from dict representation to object representation."""
        return cls.from_dict(entity_dict).to_obj()

    @classmethod
    def dict_from_object(cls, entity_obj):
        """Convert from object representation to dict representation."""
        return cls.from_obj(entity_obj).to_dict()


class EntityList(collections.MutableSequence, Entity):
    _contained_type = object
    # Don't try to cast list types (yet)
    # #TODO: Update __init__ to accept initial items in the List
    _try_cast = False

    def __init__(self):
        self._inner = []

    def __getitem__(self, key):
        return self._inner.__getitem__(key)

    def __setitem__(self, key, value):
        if not self._is_valid(value):
            value = self._fix_value(value)
        self._inner.__setitem__(key, value)

    def __delitem__(self, key):
        self._inner.__delitem__(key)

    def __len__(self):
        return len(self._inner)

    def insert(self, idx, value):
        if not self._is_valid(value):
            value = self._fix_value(value)
        self._inner.insert(idx, value)

    def _is_valid(self, value):
        """Check if this is a valid object to add to the list.

        Subclasses can override this function, but it's probably better to
        modify the istypeof function on the _contained_type.
        """
        return self._contained_type.istypeof(value)

    def _fix_value(self, value):
        """Attempt to coerce value into the correct type.

        Subclasses can override this function.
        """
        try:
            new_value = self._contained_type(value)
        except:
            raise ValueError("Can't put '%s' (%s) into a %s" %
                (value, type(value), self.__class__))
        return new_value

    @staticmethod
    def _set_list(binding_object, list_):
        """Call the proper method on the binding object to set its value.

        In general, these should be of the form:
            binding_object.set_<something>(list_)

        Since <something> differs fromt class to class, this cannot be done
        generically.
        """
        raise NotImplementedError

    @staticmethod
    def _get_list(binding_object):
        """Call the proper method on the binding object to get its value.

        In general, these should be of the form:
            return binding_object.get_<something>()

        Since <something> differs fromt class to class, this cannot be done
        generically.
        """
        raise NotImplementedError

    # The next four functions can be overridden, but otherwise define the
    # default behavior, for EntityList subclasses which define _contained_type,
    # _binding_class, _get_list, and _set_list

    def to_obj(self):
        tmp_list = [x.to_obj() for x in self]

        list_obj = self._binding_class()

        if hasattr(self, '_list_name'):
            setattr(list_obj, self._list_name, tmp_list)
        else:
            self._set_list(list_obj, tmp_list)

        return list_obj

    def to_list(self):
        return [h.to_dict() for h in self]

    @classmethod
    def from_obj(cls, list_obj):
        if not list_obj:
            return None

        list_ = cls()

        if hasattr(list_, '_list_name'):
            tmp_list = getattr(list_obj, list_._list_name)
        else:
            tmp_list = cls._get_list(list_obj)

        for item in tmp_list:
            list_.append(cls._contained_type.from_obj(item))

        return list_

    @classmethod
    def from_list(cls, list_list):
        if not isinstance(list_list, list):
            return None

        list_ = cls()

        for item in list_list:
            list_.append(cls._contained_type.from_dict(item))

        return list_

    @classmethod
    def object_from_list(cls, entitylist_list):
        """Convert from list representation to object representation."""
        return cls.from_list(entitylist_list).to_obj()

    @classmethod
    def list_from_object(cls, entitylist_obj):
        """Convert from object representation to list representation."""
        return cls.from_obj(entitylist_obj).to_list()


class ObjectReference(Entity):
    _binding_class = None

    def __init__(self, object_reference=None):
        self.object_reference = object_reference

    def to_obj(self):
        obj = self._binding_class()

        obj.set_object_reference(self.object_reference)

        return obj

    def to_dict(self):
        return {'object_reference': self.object_reference}

    @classmethod
    def from_obj(cls, ref_obj):
        if not ref_obj:
            return None

        ref = cls()
        ref.object_reference = ref_obj.get_object_reference()

        return ref

    @classmethod
    def from_dict(cls, ref_dict):
        if not ref_dict:
            return None

        ref = cls()
        ref.object_reference = ref_dict.get('object_reference')

        return ref


class ReferenceList(EntityList):

    def _fix_value(self, value):
        if isinstance(value, basestring):
            return self._contained_type(value)


class TypedField(object):

    def __init__(self, name, type_=None, callback_hook=None, key_name=None):
        """
        Create a new field.

        - `name` is the name of the field in the Binding class
        - `type_` is the type that objects assigned to this field must be.
          If `None`, no type checking is performed.
        - `key_name` is only needed if the desired key for the dictionary
          representation is differen than the lower-case version of `name`
        """
        self.name = name
        self.type_ = type_
        self.callback_hook = callback_hook
        self._key_name = key_name

    def __get__(self, instance, owner):
        # If we are calling this on a class, we want the actual Field, not its
        # value
        if not instance:
            return self

        # TODO: move this to cybox.Entity constructor
        if not hasattr(instance, "_fields"):
            instance._fields = {}
        return instance._fields.get(self.name)

    def __set__(self, instance, value):
        # TODO: move this to cybox.Entity constructor
        if not hasattr(instance, "_fields"):
            instance._fields = {}

        if ((value is not None) and (self.type_ is not None) and
                (not self.type_.istypeof(value))):
            if self.type_._try_cast:
                value = self.type_(value)
            else:
                raise ValueError("%s must be a %s, not a %s" %
                                    (self.__name__, self.type_, type(value)))
        instance._fields[self.name] = value

        if self.callback_hook:
            self.callback_hook(instance)

    def __str__(self):
        return self.attr_name

    @property
    def key_name(self):
        if self._key_name:
            return self._key_name
        else:
            return self.name.lower()

    @property
    def attr_name(self):
        """The name of this field as an attribute name.

        This is identical to the key_name, unless the key name conflicts with
        a builtin Python keyword, in which case a single underscore is
        appended.

        This should match the name given to the TypedField class variable (see
        examples below), but this is not enforced.

        Examples:
            data = cybox.TypedField("Data", String)
            from_ = cybox.TypedField("From", String)
        """

        attr = self.key_name
        # TODO: expand list with other Python keywords
        if attr in ('from', 'class', 'type', 'with', 'for', 'id'):
            attr = attr + "_"
        return attr
