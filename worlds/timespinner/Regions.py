from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Options import is_option_enabled
from .Locations import LocationData


def create_regions(world: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location], pyramid_keys_unlock: str):
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, location_cache, 'Menu'),
        create_region(world, player, locations_per_region, location_cache, 'Tutorial'),
        create_region(world, player, locations_per_region, location_cache, 'Lake desolation'),
        create_region(world, player, locations_per_region, location_cache, 'Upper lake desolation'),
        create_region(world, player, locations_per_region, location_cache, 'Lower lake desolation'),
        create_region(world, player, locations_per_region, location_cache, 'Eastern lake desolation'),
        create_region(world, player, locations_per_region, location_cache, 'Library'),
        create_region(world, player, locations_per_region, location_cache, 'Library top'),
        create_region(world, player, locations_per_region, location_cache, 'Ifrit\'s Lair'),
        create_region(world, player, locations_per_region, location_cache, 'Varndagroth tower left'),
        create_region(world, player, locations_per_region, location_cache, 'Varndagroth tower right (upper)'),
        create_region(world, player, locations_per_region, location_cache, 'Varndagroth tower right (lower)'),
        create_region(world, player, locations_per_region, location_cache, 'Varndagroth tower right (elevator)'),
        create_region(world, player, locations_per_region, location_cache, 'Sealed Caves (Sirens)'),
        create_region(world, player, locations_per_region, location_cache, 'Military Fortress'),
        create_region(world, player, locations_per_region, location_cache, 'Military Fortress (hangar)'),
        create_region(world, player, locations_per_region, location_cache, 'The lab'),
        create_region(world, player, locations_per_region, location_cache, 'The lab (power off)'),
        create_region(world, player, locations_per_region, location_cache, 'The lab (upper)'),
        create_region(world, player, locations_per_region, location_cache, 'Ravenlord\'s Lair'),
        create_region(world, player, locations_per_region, location_cache, 'Emperors tower'),
        create_region(world, player, locations_per_region, location_cache, 'Skeleton Shaft'),
        create_region(world, player, locations_per_region, location_cache, 'Sealed Caves (upper)'),
        create_region(world, player, locations_per_region, location_cache, 'Sealed Caves (Xarion)'),
        create_region(world, player, locations_per_region, location_cache, 'Refugee Camp'),
        create_region(world, player, locations_per_region, location_cache, 'Forest'),
        create_region(world, player, locations_per_region, location_cache, 'Left Side forest Caves'),
        create_region(world, player, locations_per_region, location_cache, 'Upper Lake Serene'),
        create_region(world, player, locations_per_region, location_cache, 'Lower Lake Serene'),
        create_region(world, player, locations_per_region, location_cache, 'Caves of Banishment (upper)'),
        create_region(world, player, locations_per_region, location_cache, 'Caves of Banishment (Maw)'),
        create_region(world, player, locations_per_region, location_cache, 'Caves of Banishment (Sirens)'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Ramparts'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Keep'),
        create_region(world, player, locations_per_region, location_cache, 'Royal towers (lower)'),
        create_region(world, player, locations_per_region, location_cache, 'Royal towers'),
        create_region(world, player, locations_per_region, location_cache, 'Royal towers (upper)'),
        create_region(world, player, locations_per_region, location_cache, 'Temporal Gyre'),
        create_region(world, player, locations_per_region, location_cache, 'Ancient Pyramid (entrance)'),
        create_region(world, player, locations_per_region, location_cache, 'Ancient Pyramid (left)'),
        create_region(world, player, locations_per_region, location_cache, 'Ancient Pyramid (right)'),
        create_region(world, player, locations_per_region, location_cache, 'Space time continuum')
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())
        
    world.regions += regions

    connectStartingRegion(world, player)

    names: Dict[str, int] = {}

    connect(world, player, names, 'Lake desolation', 'Lower lake desolation', lambda state: state._timespinner_has_timestop(world, player) or state.has('Talaria Attachment', player))
    connect(world, player, names, 'Lake desolation', 'Upper lake desolation', lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Serene', 'Region', player))
    connect(world, player, names, 'Lake desolation', 'Skeleton Shaft', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Lake desolation', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Upper lake desolation', 'Lake desolation')
    connect(world, player, names, 'Upper lake desolation', 'Eastern lake desolation')
    connect(world, player, names, 'Lower lake desolation', 'Lake desolation') 
    connect(world, player, names, 'Lower lake desolation', 'Eastern lake desolation')
    connect(world, player, names, 'Eastern lake desolation', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Eastern lake desolation', 'Library')
    connect(world, player, names, 'Eastern lake desolation', 'Lower lake desolation')
    connect(world, player, names, 'Eastern lake desolation', 'Upper lake desolation', lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Serene', 'Region', player))
    connect(world, player, names, 'Library', 'Eastern lake desolation')
    connect(world, player, names, 'Library', 'Library top', lambda state: state._timespinner_has_doublejump(world, player) or state.has('Talaria Attachment', player)) 
    connect(world, player, names, 'Library', 'Varndagroth tower left', lambda state: state._timespinner_has_keycard_D(world, player))
    connect(world, player, names, 'Library', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Library top', 'Library')
    connect(world, player, names, 'Library top', 'Ifrit\'s Lair', lambda state: state.has('Kobo', player) and state.can_reach('Refugee Camp', 'Region', player))
    connect(world, player, names, 'Ifrit\'s Lair', 'Library top')
    connect(world, player, names, 'Varndagroth tower left', 'Library')
    connect(world, player, names, 'Varndagroth tower left', 'Varndagroth tower right (upper)', lambda state: state._timespinner_has_keycard_C(world, player))
    connect(world, player, names, 'Varndagroth tower left', 'Varndagroth tower right (lower)', lambda state: state._timespinner_has_keycard_B(world, player))
    connect(world, player, names, 'Varndagroth tower left', 'Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connect(world, player, names, 'Varndagroth tower left', 'Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))
    connect(world, player, names, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(world, player, names, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, names, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(world, player, names, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(world, player, names, 'Varndagroth tower right (lower)', 'Varndagroth tower left', lambda state: state._timespinner_has_keycard_B(world, player))
    connect(world, player, names, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, names, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connect(world, player, names, 'Varndagroth tower right (lower)', 'Military Fortress', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connect(world, player, names, 'Varndagroth tower right (lower)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Sealed Caves (Sirens)', 'Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, names, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, names, 'Sealed Caves (Sirens)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Military Fortress', 'Varndagroth tower right (lower)', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connect(world, player, names, 'Military Fortress', 'Temporal Gyre', lambda state: state.has('Timespinner Wheel', player))
    connect(world, player, names, 'Military Fortress', 'Military Fortress (hangar)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Military Fortress (hangar)', 'Military Fortress')
    connect(world, player, names, 'Military Fortress (hangar)', 'The lab', lambda state: state._timespinner_has_keycard_B(world, player) and state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Temporal Gyre', 'Military Fortress')
    connect(world, player, names, 'The lab', 'Military Fortress')
    connect(world, player, names, 'The lab', 'The lab (power off)', lambda state: state._timespinner_has_doublejump_of_npc(world, player))
    connect(world, player, names, 'The lab (power off)', 'The lab')
    connect(world, player, names, 'The lab (power off)', 'The lab (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, names, 'The lab (upper)', 'The lab (power off)')
    connect(world, player, names, 'The lab (upper)', 'Ravenlord\'s Lair', lambda state: state.has('Merchant Crow', player))
    connect(world, player, names, 'The lab (upper)', 'Emperors tower', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, names, 'The lab (upper)', 'Ancient Pyramid (entrance)', lambda state: state.has_all({'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'}, player))
    connect(world, player, names, 'Ravenlord\'s Lair', 'The lab (upper)')
    connect(world, player, names, 'Emperors tower', 'The lab (upper)')
    connect(world, player, names, 'Skeleton Shaft', 'Lake desolation')
    connect(world, player, names, 'Skeleton Shaft', 'Sealed Caves (upper)', lambda state: state._timespinner_has_keycard_A(world, player))
    connect(world, player, names, 'Skeleton Shaft', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Sealed Caves (upper)', 'Skeleton Shaft')
    connect(world, player, names, 'Sealed Caves (upper)', 'Sealed Caves (Xarion)', lambda state: state.has('Twin Pyramid Key', player) or state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Sealed Caves (Xarion)', 'Sealed Caves (upper)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Sealed Caves (Xarion)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Refugee Camp', 'Forest')
    #connect(world, player, names, 'Refugee Camp', 'Library', lambda state: not is_option_enabled(world, player, "Inverted"))
    connect(world, player, names, 'Refugee Camp', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Forest', 'Refugee Camp')
    connect(world, player, names, 'Forest', 'Left Side forest Caves', lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world, player))
    connect(world, player, names, 'Forest', 'Caves of Banishment (Sirens)')
    connect(world, player, names, 'Forest', 'Castle Ramparts')
    connect(world, player, names, 'Left Side forest Caves', 'Forest')
    connect(world, player, names, 'Left Side forest Caves', 'Upper Lake Serene', lambda state: state._timespinner_has_timestop(world, player))
    connect(world, player, names, 'Left Side forest Caves', 'Lower Lake Serene', lambda state: state.has('Water Mask', player))
    connect(world, player, names, 'Left Side forest Caves', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Upper Lake Serene', 'Left Side forest Caves')
    connect(world, player, names, 'Upper Lake Serene', 'Lower Lake Serene', lambda state: state.has('Water Mask', player))
    connect(world, player, names, 'Lower Lake Serene', 'Upper Lake Serene')
    connect(world, player, names, 'Lower Lake Serene', 'Left Side forest Caves')
    connect(world, player, names, 'Lower Lake Serene', 'Caves of Banishment (upper)')
    connect(world, player, names, 'Caves of Banishment (upper)', 'Upper Lake Serene', lambda state: state.has('Water Mask', player))
    connect(world, player, names, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)', lambda state: state.has('Twin Pyramid Key', player) or state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Caves of Banishment (upper)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)', lambda state: state.has('Gas Mask', player))
    connect(world, player, names, 'Caves of Banishment (Maw)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Caves of Banishment (Sirens)', 'Forest')
    connect(world, player, names, 'Castle Ramparts', 'Forest')
    connect(world, player, names, 'Castle Ramparts', 'Castle Keep')
    connect(world, player, names, 'Castle Ramparts', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Castle Keep', 'Castle Ramparts')
    connect(world, player, names, 'Castle Keep', 'Royal towers (lower)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Castle Keep', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Royal towers (lower)', 'Castle Keep')
    connect(world, player, names, 'Royal towers (lower)', 'Royal towers', lambda state: state.has('Timespinner Wheel', player) or state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, names, 'Royal towers (lower)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, names, 'Royal towers', 'Royal towers (lower)')
    connect(world, player, names, 'Royal towers', 'Royal towers (upper)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Royal towers (upper)', 'Royal towers')
    connect(world, player, names, 'Ancient Pyramid (entrance)', 'The lab (upper)', lambda state: not is_option_enabled(world, player, "EnterSandman"))
    connect(world, player, names, 'Ancient Pyramid (entrance)', 'Ancient Pyramid (left)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, names, 'Ancient Pyramid (left)', 'Ancient Pyramid (entrance)')
    connect(world, player, names, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', lambda state: state._timespinner_has_upwarddash(world, player))
    connect(world, player, names, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)', lambda state: state._timespinner_has_upwarddash(world, player))
    connect(world, player, names, 'Space time continuum', 'Lake desolation', lambda state: pyramid_keys_unlock == "GateLakeDesolation")
    connect(world, player, names, 'Space time continuum', 'Lower lake desolation', lambda state: pyramid_keys_unlock == "GateKittyBoss")
    connect(world, player, names, 'Space time continuum', 'Library', lambda state: pyramid_keys_unlock == "GateLeftLibrary")
    connect(world, player, names, 'Space time continuum', 'Varndagroth tower right (lower)', lambda state: pyramid_keys_unlock == "GateMilitairyGate")
    connect(world, player, names, 'Space time continuum', 'Skeleton Shaft', lambda state: pyramid_keys_unlock == "GateSealedCaves")
    connect(world, player, names, 'Space time continuum', 'Sealed Caves (Sirens)', lambda state: pyramid_keys_unlock == "GateSealedSirensCave")
    connect(world, player, names, 'Space time continuum', 'Left Side forest Caves', lambda state: pyramid_keys_unlock == "GateLakeSirineRight")
    connect(world, player, names, 'Space time continuum', 'Refugee Camp', lambda state: pyramid_keys_unlock == "GateAccessToPast")
    connect(world, player, names, 'Space time continuum', 'Castle Ramparts', lambda state: pyramid_keys_unlock == "GateCastleRamparts")
    connect(world, player, names, 'Space time continuum', 'Castle Keep', lambda state: pyramid_keys_unlock == "GateCastleKeep")
    connect(world, player, names, 'Space time continuum', 'Royal towers (lower)', lambda state: pyramid_keys_unlock == "GateRoyalTowers")
    connect(world, player, names, 'Space time continuum', 'Caves of Banishment (Maw)', lambda state: pyramid_keys_unlock == "GateMaw")
    connect(world, player, names, 'Space time continuum', 'Caves of Banishment (upper)', lambda state: pyramid_keys_unlock == "GateCavesOfBanishment")
    connect(world, player, names, 'Space time continuum', 'Ancient Pyramid (entrance)', lambda state: is_option_enabled(world, player, "EnterSandman"))


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception("Timespinner: the following regions are used in locations: {}, but no such region exists".format(regionNames - existingRegions))


def create_location(player: int, location_data: LocationData, region: Region, location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], location_cache: List[Location], name: str) -> Region:
    region = Region(name, RegionType.Generic, name, player)
    region.multiworld = world

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def connectStartingRegion(world: MultiWorld, player: int):
    menu = world.get_region('Menu', player)
    tutorial = world.get_region('Tutorial', player)
    space_time_continuum = world.get_region('Space time continuum', player)

    if is_option_enabled(world, player, "Inverted"):
        starting_region = world.get_region('Refugee Camp', player)
    else:
        starting_region = world.get_region('Lake desolation', player)

    menu_to_tutorial = Entrance(player, 'Tutorial', menu)
    menu_to_tutorial.connect(tutorial)
    menu.exits.append(menu_to_tutorial)

    tutorial_to_start = Entrance(player, 'Start Game', tutorial)
    tutorial_to_start.connect(starting_region)
    tutorial.exits.append(tutorial_to_start)

    teleport_back_to_start = Entrance(player, 'Teleport back to start', space_time_continuum)
    teleport_back_to_start.connect(starting_region)
    space_time_continuum.exits.append(teleport_back_to_start)


def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str, rule: Optional[Callable] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
