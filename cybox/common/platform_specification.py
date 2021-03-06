# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import cybox
import cybox.bindings.cybox_common as common_binding
from cybox.common import String, StructuredText


class PlatformSpecification(cybox.Entity):
    '''CybOX Common PlatformSpecification object representation'''
    _namespace = 'http://cybox.mitre.org/common-2'

    def __init__(self):
        super(PlatformSpecification, self).__init__()
        self.description = None
        self.identifiers = []

    def to_obj(self):
        platform_specification_obj = common_binding.PlatformSpecificationType()
        if self.description is not None : platform_specification_obj.set_Description(self.platform_specification_obj.to_obj())
        if len(self.identifiers) > 0 : 
            for identifier in identifiers: platform_specification_obj.add_Identifier(identifier.to_obj())
        return platform_specification_obj

    def to_dict(self):
        platform_specification_dict = {}
        if self.description is not None : platform_specification_dict['description'] = self.description.to_dict()
        if len(self.identifiers) > 0 : 
            identifier_list = [x.to_dict() for x in self.identifiers]
            platform_specification_dict['identifiers'] = identifier_list
        return platform_specification_obj

    @staticmethod
    def from_dict(platform_specification_dict):
        if not platform_specification_dict:
            return None
        platform_specification_ = PlatformSpecification()
        platform_specification_.description = StructuredText.from_dict(platform_specification_dict.get('description'))
        platform_specification_.identifiers = [PlatformIdentifier.from_dict(x) for x in platform_specification_dict.get('identifiers',[])]
        return platform_specification_

    @staticmethod
    def from_obj(platform_specification_obj):
        if not platform_specification_obj:
            return None
        platform_specification_ = PlatformSpecification()
        platform_specification_.description = StructuredText.from_obj(platform_specification_obj.get_Description())
        platform_specification_.identifiers = [PlatformIdentifier.from_obj(x) for x in platform_specification_obj.get_Identifier()]
        return platform_specification_


class PlatformIdentifier(String):
    _namespace = 'http://cybox.mitre.org/common-2'

    def __init__(self):
        super(PlatformIdentifier, self).__init__()
        self.system = None
        self.system_ref = None

    def _get_binding_class(self):
        return common_binding.PlatformIdentifierType

    def to_obj(self):
        platform_identifier_obj = super(PlatformIdentifier, self).to_obj()
        if self.system is not None: platform_identifier_obj.set_system(self.system)
        if self.system_ref is not None: platform_identifier_obj.set_system_ref(self.system_ref)
        return platform_identifier_obj

    def to_dict(self):
        platform_identifier_dict = super(PlatformIdentifier, self).to_dict()
        if self.system is not None: platform_identifier_dict['system'] = self.system
        if self.system_ref is not None: platform_identifier_dict['system_ref'] = self.system_ref
        return platform_identifier_dict

    @staticmethod
    def from_dict(platform_identifier_dict):
        if not platform_identifier_dict:
            return None
        platform_identifier_ = PlatformIdentifier()
        platform_identifier_.system = platform_identifier_dict.get('system')
        platform_identifier_.system_ref = platform_identifier_dict.get('system_ref')
        return platform_identifier_

    @staticmethod
    def from_obj(platform_identifier_obj):
        if not platform_identifier_obj:
            return None
        platform_identifier_ = PlatformIdentifier()
        platform_identifier_.system = platform_identifier_obj.get_system()
        platform_identifier_.system_ref = platform_identifier_obj.get_system_ref()
        return platform_identifier_
