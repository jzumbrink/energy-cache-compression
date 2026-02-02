# all file sizes are given in MB
file_sizes = {
    "einstein": 629.1,
}

# all compressed text index sizes are given in MB
idx_sizes = {
    "einstein": {
        "move-r": 23.1,
        "move-r-lzend": 26.8,
        "move-r-rlz": 48.3,
    },
}

# all values are given in Joule per 1000 queries
query_energy_usage = {
    "einstein": {
        "move-r": 4.125640869140625,
        "move-r-lzend": 4.353302001953125,
        "move-r-rlz": 0.881256103515625,
    },
}

measured_locate_data = {
    "einstein": {
        "8": {
            "eng": {
                "move-r": 166.96413294474283,
                "move-r-lzend": 166.59228897094727,
                "move-r-rlz": 22.553624471028645,
            },
            "time": {
                "move-r": 17.062243166666423,
                "move-r-lzend": 11.680849649167309,
                "move-r-rlz": 1.4067980725831148,
            },
            "iter": 20_000.0,
        }
    }
}

measured_build_data = {
    "einstein": {
        "eng": {
            "move-r": 301.71971893310547,
            "move-r-lzend": 6128.963981628418,
            "move-r-rlz": 443.0567321777344,
        },
        "time": {
            "move-r": 33.42205178999984,
            "move-r-lzend": 880.8818223425001,
            "move-r-rlz": 46.35676657699969,
        },
    }
}

co2_eq_per_kw = 363 # in g
co2_eq_per_kJ = co2_eq_per_kw / 3600
co2_eq_per_joule = co2_eq_per_kJ / 1000

co2_equiv_per_tb = 209_500 # in g, mean of page 107 GGC Umweltbundesamt
co2_equiv_per_mb = co2_equiv_per_tb / 1024**2

def disk_co2_emissions(size_in_megabyte: float) -> float:
    return size_in_megabyte * co2_equiv_per_mb

def query_co2_emissions(count_queries: int, joule_per_1000_queries: float) -> float:
    return (count_queries / 1000) * joule_per_1000_queries * co2_eq_per_joule

def joule_to_co2(energy_in_joule: float) -> float:
    return energy_in_joule * co2_eq_per_joule

def all_co2_emissions(size_in_megabyte: float, construction_energy: float, joule_per_query, count_queries: int) -> float: # returns in g co2 eq
    return (disk_co2_emissions(size_in_megabyte)
            + joule_to_co2(construction_energy)
            + joule_to_co2(joule_per_query * count_queries))
