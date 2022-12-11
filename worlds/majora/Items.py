from .ItemList import item_table
from BaseClasses import Item, ItemClassification


def mm_data_to_ap_id(data, event):
    if event or data[2] is None:
        return None
    if data[0] in ['Item']:
        return MMItem.offset + data[2]
    else:
        raise Exception(f"Unexpected MM item type found {data[0]}")


def ap_id_to_oot_data(ap_id):
    try:
        return list(filter(lambda d: d[1][0] == 'Item' and d[1][2] == ap_id - MMItem.offset, item_table.items()))[0]
    except IndexError:
        raise Exception(f"Could not find desired item ID: {ap_id}")


class MMItem(Item):
    game: str = "Majora's Mask"
    type: str
    offset: int = 24000

    def __init__(self, name, player, data, event, force_not_advancement):
        (type, advancement, index, special) = data
        if force_not_advancement:
            classification = ItemClassification.useful
        elif name == "Ice Trap":
            classification = ItemClassification.trap
        elif advancement:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        super(MMItem, self).__init__(name, classification, mm_data_to_ap_id(data, event), player)
        self.type = type
        self.index = index
        self.special = special or {}
        self.internal = False

    @property
    def dungeonitem(self) -> bool:
        return self.type in ["SmallKey", "BossKey", "Map", "Compass"]
