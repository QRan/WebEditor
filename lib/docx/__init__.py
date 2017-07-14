# encoding: utf-8

from lib.docx.api import Document  # noqa

__version__ = '0.8.6'


# register custom Part classes with opc package reader

from lib.docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from lib.docx.opc.part import PartFactory
from lib.docx.opc.parts.coreprops import CorePropertiesPart

from lib.docx.parts.document import DocumentPart
from lib.docx.parts.image import ImagePart
from lib.docx.parts.numbering import NumberingPart
from lib.docx.parts.settings import SettingsPart
from lib.docx.parts.styles import StylesPart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.OPC_CORE_PROPERTIES] = CorePropertiesPart
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_SETTINGS] = SettingsPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart

del (
    CT, CorePropertiesPart, DocumentPart, NumberingPart, PartFactory,
    StylesPart, part_class_selector
)
