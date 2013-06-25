# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import cybox
import cybox.utils


class ObjectProperties(cybox.Entity):
    """The Cybox ObjectProperties base class."""

    object_reference = cybox.TypedField("object_reference")

    def __init__(self):
        self.parent = None

    @property
    def parent(self):
        if not self._parent:
            self._parent = cybox.core.object.Object(self)
        return self._parent

    @parent.setter
    def parent(self, value):
        if value and not isinstance(value, cybox.core.object.Object):
            raise ValueError("Must be an Object")
        self._parent = value

    def add_related(self, related, relationship, inline=True):
        self.parent.add_related(related, relationship, inline)

    def to_obj(self, partial_obj=None):
        # TODO: Hack until all ObjectProperties use TypedField
        if partial_obj is None:
            return super(ObjectProperties, self).to_obj()

        if self.object_reference is not None:
            partial_obj.set_object_reference(self.object_reference)
        self._finalize_obj(partial_obj)

    def _finalize_obj(self, partial_obj=None):
        """Add xsi_type to the binding object."""

        partial_obj.set_xsi_type("%s:%s" % (self._XSI_NS, self._XSI_TYPE))

    def to_dict(self, partial_dict=None):
        # TODO: Hack until all ObjectProperties use TypedField
        if partial_dict is None:
            return super(ObjectProperties, self).to_dict()

        if self.object_reference is not None:
            partial_dict['object_reference'] = self.object_reference
        self._finalize_dict(partial_dict)

    def _finalize_dict(self, partial_dict=None):
        """Add xsi:type to the dictionary."""

        partial_dict['xsi:type'] = self._XSI_TYPE

    @classmethod
    def from_obj(cls, defobj_obj, defobj=None):
        # This is a bit of a hack. If this is being called directly on the
        # ObjectProperties class, then we don't know the xsi_type of the
        # ObjectProperties, so we need to look it up. Otherwise, if this is
        # being called on a particular subclass of ObjectProperties (for
        # example, Address), we can skip directly to the cybox.Entity
        # implementation.
        if cls is not ObjectProperties:
            return super(ObjectProperties, cls()).from_obj(defobj_obj)

        if not defobj_obj:
            return None

        if not defobj:
            xsi_type = defobj_obj.get_xsi_type()
            if not xsi_type:
                raise ValueError("Object has no xsi:type")
            type_value = xsi_type.split(':')[1]

            # Find the class that can parse this type.
            klass = cybox.utils.get_class_for_object_type(type_value)
            defobj = klass.from_obj(defobj_obj)

        defobj.object_reference = defobj_obj.get_object_reference()

        return defobj

    @classmethod
    def from_dict(cls, defobj_dict, defobj=None):
        # Also a hack. See comment on from_obj
        if cls is not ObjectProperties:
            return super(ObjectProperties, cls()).from_dict(defobj_dict)

        if not defobj_dict:
            return None

        if not defobj:
            xsi_type = defobj_dict.get('xsi:type')
            if not xsi_type:
                raise ValueError('dictionary does not have xsi:type key')

            klass = cybox.utils.get_class_for_object_type(xsi_type)
            defobj = klass.from_dict(defobj_dict)

        defobj.object_reference = defobj_dict.get('object_reference')

        return defobj
