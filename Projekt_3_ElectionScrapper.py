
# Třetí projekt do Engeto Online Python Akademie

# autor: Radovan Krejčíř
# email: krejcir.rad@gmail.com
# discord: Radovan K.#3299


# imported libraries
import bs4.element
from requests import get
from bs4 import BeautifulSoup as BSoup
import csv

# imported data
import dict_template

# default objects
address_lev1 = 'https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'


# FUNCTION: acquire parsed data from the website ('city_names')

def get_city_names(address_lev1: str) -> bs4.element.ResultSet:

    """
    Get parsed data for further use by 'check_input' and 'city_to_villages' functions.
    """

    address_data = get(address_lev1)
    data_parsed = BSoup(address_data.content, features="html.parser")
    city_names = data_parsed.find_all('td')

    return city_names


# FUNCTION: check validity of the main function arguments

def check_input(city_choice: str, city_names: bs4.element.ResultSet, output_name: str) -> bool:

    """
    Function returns 'False', stop the code and alerts user if the main function arguments are not valid.
    """

    input_ok = False

    for i in city_names:
        if city_choice in i:
            input_ok = True

    if type(output_name) is not str or output_name == '':
        input_ok = False

    if input_ok is False:
        print('Main function arguments are not valid.')

    return input_ok


# FUNCTION: generates access to individual municipalities

def city_to_villages(city_names, city_choice: str) -> str:

    """
    Returns a link providing access to individual municipalities.
    """

    reference = ''

    for i in city_names:
        if city_choice in i:
            reference = (i.parent.find_all('a')[2])['href']

    address_lev2 = f'https://www.volby.cz/pls/ps2017nss/{reference}'

    return address_lev2


# Acquire data about individual municipalities ('code', 'location')

    # FUNCTION: acquire 'code' for each municipality

def get_codes(address_lev2: str) -> list:

    """
    Returns a list of dictionaries with 'codes'.

    Example of output:
    [{'code': '552356'}, {'code': '500526'} ...]
    """

    address_data = get(address_lev2)
    data_parsed = BSoup(address_data.content, features="html.parser")
    codes = data_parsed.find_all("td", {'class': 'cislo'})

    codes_output = []
    codes_dicts = []

    for i in codes:
        codes_output.append(i.string)

    pocet = range(0, len(codes_output))

    for i in pocet:
        dict = {'code': codes_output[i]}
        codes_dicts.append(dict)

    return codes_dicts


    # FUNCTION: acquire 'location' for each municipality

def get_locations(address_lev2: str) -> list:

    """
    Returns a list of dictionaries with 'locations'.

    Example of output:
    [{'location': 'Babice'}, {'location': 'Bělkovice-Lašťany'} ... ]
    """

    address_data = get(address_lev2)
    data_parsed = BSoup(address_data.content, features="html.parser")
    locations = data_parsed.find_all("td", {'class': 'overflow_name'})

    locations_output = []
    locations_dicts = []

    for i in locations:
        locations_output.append(i.string)

    pocet = range(0, len(locations_output))

    for i in pocet:
        dict = {'location': locations_output[i]}
        locations_dicts.append(dict)

    return locations_dicts


# FUNCTION: generates access to election results data for all municipalities within our choice

def get_village_links(adress_lev2: str) -> list:

    """
    Returns a list of strings - links providing access to election results data.
    """

    villages = []
    villages_links = []

    page_city = get(adress_lev2)
    city_parsed = BSoup(page_city.content, features="html.parser")
    city_links = city_parsed.find_all('a')

    city_iter_length = len(city_links)
    city_iter = range(5, city_iter_length - 2, 2)

    for i in city_iter:
        villages.append(city_links[i])

    for village in villages:
        extract = village['href']
        villages_links.append(f'https://www.volby.cz/pls/ps2017nss/{extract}')

    return villages_links


# Acquire election results data

    # FUNCTION: acquire 'registered', 'envelopes' and 'valid' data for each municipality

def get_village_info(address_lev3: str) -> list:

    """
    Returns a list with 'registered', 'envelopes' and 'valid' data.

    Example of output:
    ['370', '256', '254']
    """

    village_page = get(address_lev3)
    village_parsed = BSoup(village_page.content, features="html.parser", from_encoding='UTF-8')

    tables_lev3_head_registered = village_parsed.body.contents[3].contents[1].find_all('td', {'class': 'cislo'})[3].text
    tables_lev3_head_envelopes = village_parsed.body.contents[3].contents[1].find_all('td', {'class': 'cislo'})[6].text
    tables_lev3_head_valid = village_parsed.body.contents[3].contents[1].find_all('td', {'class': 'cislo'})[7].text

    village_info = [tables_lev3_head_registered, tables_lev3_head_envelopes, tables_lev3_head_valid]

    return village_info


    # FUNCTION: acquire number of votes for each party

def get_votes(address_lev3: str) -> list:

    """
    Returns a list of dictionaries with votes for each party.

    Example of output:
    [{'Občanská demokratická strana': '13', 'Řád národa - Vlastenecká unie': '0' ...} ...]
    """

    page_village = (get(address_lev3))
    village_parsed = BSoup(page_village.content, features="html.parser", from_encoding='UTF-8')

    village_tables_votes1 = village_parsed.body.contents[3].contents[1].find_all('td', {'headers': 't1sa2 t1sb3'})
    village_tables_votes2 = village_parsed.body.contents[3].contents[1].find_all('td', {'headers': 't2sa2 t2sb3'})
    village_tables_votes = village_tables_votes1 + village_tables_votes2

    village_tables_names = village_parsed.body.contents[3].contents[1].find_all('td', {'class': 'overflow_name'},{'headers': 't2sa1 t2sb2'})

    parties_names = []
    votes = []

    for i in village_tables_names:
        parties_names.append(i.text)

    for i in parties_names:
        dict = {}
        dict[i] = (village_tables_votes[parties_names.index(i)]).text
        votes.append(dict)

    return votes


    # FUNCTION: acquire election results data ('registered', 'envelopes', 'valid') for all municipal. within our choice

def get_all_info(villages_links: list) -> list:

    """
    Returns a list of lists with 'registered', 'envelopes' and 'valid' data for each municipality.

    Example of output:
    [['370', '256', '254'], ['931', '568', '565'] ...]

    """

    info_all = []

    for i in villages_links:
        info_all.append(get_village_info(i))

    return info_all


    # FUNCTION: acquire election results data (votes) for all municipalities within our choice

def get_all_votes(villages_hyptexts: list) -> list:

    """
    Returns a list of lists containing dictionaries with votes for each party for each municipality.

    Example of output:
    [[{'Občanská demokratická strana': '13'}, {'Řád národa - Vlastenecká unie': '0'} ...] ...]
    """

    votes_all = []

    for i in villages_hyptexts:
        votes_all.append(get_votes(i))

    return votes_all


# Transform election results data

    # FUNCTION: transform data generated by get_all_info function

def get_info_dicts(all_info: list) -> list:

    """
    Transform a list of lists to a list of dictionaries.

    Example of output:
    [{'registered': '370', 'envelopes': '256', 'valid': '254'},
     {'registered': '931', 'envelopes': '568', 'valid': '565'} ...]
    """

    info_dicts = []

    for i in all_info:
        dict = {'registered': i[0], 'envelopes': i[1], 'valid': i[2]}
        info_dicts.append(dict)

    return info_dicts


    # FUNCTION: transform data generated by get_all_votes function

def get_votes_dicts(all_votes: list) -> list:

    """
    Transform a list of lists of dictionaries to a list of dictionaries.

    Example of output:
    [{'Občanská demokratická strana': '13', 'Řád národa - Vlastenecká unie': '0' ...} ...]
    """

    votes_dicts = []

    for i in all_votes:
        dict = {}
        for j in i:
            dict = {**dict, **j}

        votes_dicts.append(dict)

    return votes_dicts


# FUNCTION: merge datasets

def merge_dicts(dicts1: list, dicts2: list) -> list:

    """
    Using two lists of dictionaries, take dictionaries with the same index within each list and merge them in a single
    dictionary containing all the values. Output is a list of merged dictionaries.

    Example of input:
    [{'code': '552356'}, {'code': '500526'}]
    [{'location': 'Babice'}, {'location': 'Bělkovice-Lašťany'}]

    Example of output:
    [{'code': '552356', 'location': 'Babice'}, {'code': '500526', 'location': 'Bělkovice-Lašťany'}]
    """

    merged = []

    for i in dicts1:
        dicts = {**i, **dicts2[dicts1.index(i)]}
        merged.append(dicts)

    return merged


# FUNCTION: create an excel table using acquired data

def make_table(slovnik0: dict, all_info: list, output_name: str) -> csv:

    """
    Generates a csv file using a dictionary (a table head) and a list of dictionaries (source of data).
    """

    make_me_table = open(output_name, mode='w', newline='')

    head = slovnik0.keys()
    writer = csv.DictWriter(make_me_table, fieldnames=head, dialect='excel-tab')

    writer.writeheader()
    writer.writerows(all_info)

    make_me_table.close()


# MAIN FUNCTION

def main(city_choice: str, output_name: str) -> csv:

    """
    Generates a csv file (formatted for Excel) with election results data using two arguments:
    a name of the city of interest and a name of the output csv.
    """

    city_names = get_city_names(address_lev1)

    input_ok = check_input(city_choice, city_names, output_name)

    while input_ok:

        address_lev2 = city_to_villages(city_names, city_choice)

        codes = get_codes(address_lev2)
        locations = get_locations(address_lev2)

        villages_links = get_village_links(address_lev2)

        all_votes = get_all_votes(villages_links)
        all_info = get_all_info(villages_links)

        info_dicts = get_info_dicts(all_info)
        votes_dicts = get_votes_dicts(all_votes)

        merged_step1 = merge_dicts(codes, locations)
        merged_step2 = merge_dicts(merged_step1, info_dicts)
        merged_step3 = merge_dicts(merged_step2, votes_dicts)

        make_table(dict_template.template, merged_step3, output_name)

        input_ok = False

        return input_ok


if __name__ == '__main__':
    main('Olomouc', 'Volby2017_Olomouc')


