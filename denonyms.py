#!/usr/bin/env python3


def get_demonym(country_name):
    """
    Return the 'opposite' in the country↔demonym pair.
    Examples:
      - If you pass 'france', it returns 'french'.
      - If you pass 'french', it returns 'france'.
      - If it doesn't exist, returns None.

    NOTE:
    - For collisions (e.g., multiple countries with the same demonym),
      only one key is kept in the reversed dictionary.
    """
    demonym_map = {
        # Europe
        "albania": "albanian",
        "andorra": "andorran",
        "austria": "austrian",
        "belarus": "belarusian",
        "belgium": "belgian",
        "bosnia and herzegovina": "bosnian",
        "bulgaria": "bulgarian",
        "croatia": "croatian",
        "cyprus": "cypriot",
        "czech republic": "czech",
        "denmark": "danish",
        "estonia": "estonian",
        "finland": "finnish",
        "france": "french",
        "germany": "german",
        "greece": "greek",
        "hungary": "hungarian",
        "iceland": "icelandic",
        "ireland": "irish",
        "italy": "italian",
        "kosovo": "kosovar",
        "latvia": "latvian",
        "liechtenstein": "liechtensteiner",
        "lithuania": "lithuanian",
        "luxembourg": "luxembourgish",
        "malta": "maltese",
        "moldova": "moldovan",
        "monaco": "monégasque",
        "montenegro": "montenegrin",
        "netherlands": "dutch",
        "north macedonia": "macedonian",
        "norway": "norwegian",
        "poland": "polish",
        "portugal": "portuguese",
        "romania": "romanian",
        "russia": "russian",
        "san marino": "sammarinese",
        "serbia": "serbian",
        "slovakia": "slovak",
        "slovenia": "slovenian",
        "spain": "spanish",
        "sweden": "swedish",
        "switzerland": "swiss",
        "turkey": "turkish",
        "ukraine": "ukrainian",
        "united kingdom": "british",
        "vatican city": "vatican",
        # Other common
        "brazil": "brazilian",
        "china": "chinese",
        "egypt": "egyptian",
        "honduras": "honduran",
        "japan": "japanese",
        "mexico": "mexican",
        "united states": "american",
        "usa": "american",
        # etc...
    }

    # Build a reversed map, e.g. "french" -> "france"
    reversed_map = {v: k for k, v in demonym_map.items()}

    # Normalize
    normalized = country_name.strip().lower()

    # If it's a known country, return its demonym
    if normalized in demonym_map:
        return demonym_map[normalized]
    # If it's a known demonym, return the country
    elif normalized in reversed_map:
        return reversed_map[normalized]
    # Otherwise, we have no match
    else:
        return None
