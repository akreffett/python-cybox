# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import cybox
import cybox.bindings.cybox_common as common_binding
from cybox.common.baseobjectattribute import Base_Object_Attribute
from cybox.common import HashList, Integer


class ByteRun(cybox.Entity):
    _binding = common_binding
    _binding_class = common_binding.ByteRunType

    offset = cybox.TypedField("Offset", Integer)
    file_system_offset = cybox.TypedField("File_System_Offset", Integer)
    image_offset = cybox.TypedField("Image_Offset", Integer)
    length = cybox.TypedField("Length", Integer)
    hashes = cybox.TypedField("Hashes", HashList)
    byte_run_data = cybox.TypedField("Byte_Run_Data")

    __vars__ = (offset, file_system_offset, image_offset, length, hashes,
                byte_run_data)


class ByteRuns(cybox.EntityList):
    _binding_class = common_binding.ByteRunsType
    _contained_type = ByteRun
    _list_name = "Byte_Run"
