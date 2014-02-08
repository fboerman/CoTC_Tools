__author__ = 'williewonka'

#mostly set per kingdom, if kingdom is not listed than its broken down per duchy if that is not listed then its undefined
#these are set by the original rules, for first time generation. religion and culture in an existing file will always take precedence over these lists
cultures_per_region = {
    'Xin Zizhiqu' : 'sino_bianjiangese',
    'Bianjiang' : 'sino_bianjiangese',
    'Orion Reach' : 'hispanic_orion',
    'Orion Nebula' : 'hispanic_orion',
    'Fire Nebula' : 'hispanic_orion',
    'Horsehead Nebula' : 'hispanic_orion',
    'Mukta Duniya' : 'indo_mukta',
    'The Outer Veil' : 'indo_mukta', #part of the Veil Nebula
    'The Remote' : 'indo_tarkan', #part of the Veil Nebula
    'Akkala' : 'indo_tarkan',
    'Avalon' : 'anglo_avalonian',
    'Frontier' : 'anglo_frontiersman',
    'New Frontier' : 'anglo_frontiersman',
    'Core Witch Head' : 'anglo_frontiersman', #part of witch head nebula
    'Lower Witch Head' : 'japanese_tengoku', #part of witch head nebula
    'Upper Witch Head' : 'japanese_tengoku', #part of witch head nebula
    'Sector Tengoku' : 'japanese_tengoku', #part of The Centauri Reach
    'Jion' : 'japanese_tengoku',
    'Strugatsky' : 'russo_strugatskite',
    'Novyy Edem' : 'russo_edemite',
    'Sector Paraiso' : 'arab_samawati',
    'Sector Miltia' : 'hispanic_samawati',
    'Sector New Jerusalem' : 'hispanic_orion'
}
#same for ideology
ideology_per_region = {
    'Orion Reach' : 'colonial_seperatist',
    'Mukta Duniya' : 'colonial_seperatist',
    'Xin Zizhiqu' : 'colonial_seperatist',
    'New Frontier' : 'colonial_seperatist',
    'Bianjiang' : 'colonial_seperatist',
    'Sector Tarka' : 'cyberneticist',
    'Jion' : 'astrist',
    'Novyy Edem' : 'astrist',
    'Strugatsky' : 'neo_socialist',
    'Parasio' : 'pilgrim'
}

# Atmosphere
#  xx_no_atmosphere -> xx_no_atmosphere_domes -> xx_artificial_atmosphere
#  xx_toxic_atmosphere -> xx_toxic_atmosphere_domes -> xx_scrubbed_atmosphere
#  xx_clean_atmosphere
# Temperature
#  xx_frozen -> xx_cold -> xx_cool -> xx_optimal_cold
#  xx_burning -> xx_hot -> xx_warm -> xx_optimal_hot
# Water
#  xx_no_water -> xx_trace_water -> xx_lakes -> xx_seas -> xx_oceans
# Space Station Size
#  xx_space_station_0 -> xx_space_station_1 -> xx_space_station_2 -> xx_space_station_3 -> xx_space_station_4

Atmosphere = [
    'xx_no_atmosphere',
    'xx_no_atmosphere_domes',
    'xx_artificial_atmosphere',
    'xx_toxic_atmosphere',
    'xx_toxic_atmosphere_domes',
    'xx_scrubbed_atmosphere',
    'xx_clean_atmosphere'
]

Temperature = [
    'xx_frozen',
    'xx_cold',
    'xx_cool',
    'xx_optimal_cold',
    'xx_burning',
    'xx_hot',
    'xx_warm',
    'xx_optimal_hot'
]

Water = [
    'xx_no_water',
    'xx_trace_water',
    'xx_lakes',
    'xx_seas',
    'xx_oceans'
]

SpaceStation = [
    'xx_space_station_0',
    'xx_space_station_1',
    'xx_space_station_2',
    'xx_space_station_3',
    'xx_space_station_4'
]

Colony = [
    'xx_colony_0',
    'xx_colony_1',
    'xx_colony_2',
    'xx_colony_3',
    'xx_colony_4'
]

Asteroids = [
    'None',
    'xx_asteroids'
]