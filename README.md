# ENGETO_Python_project_3
This is my third and final project for the ENGETO Python Academy.

Author:
RadoVan-K (https://github.com/RadoVan-K)

Purpose:
This code was created as a project for Python Academy by ENGETO.

The code is a web scrapper that acquires data about parliamentary elections in Czechia in 2017.
It enables user to automatically create an Excel table with election results for each municipality 
within area of user´s interest.

Requirements:
The code was created for Python 3.10 an requires following extensions.

requests~=2.28.1
bs4~=0.0.1
beautifulsoup4~=4.11.1

How to use it:
Main function requires two arguments: a name of the city of interest and a name of the output csv file.

The first argument is to be picked from https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ, 'územní úroveň' - 'název'.
The second argument only allows non-empty string.

By default, 'Olomouc' is set as the first argument and 'Volby2017_Olomouc' as the second argument.

if __name__ == '__main__':
    main('Olomouc', 'Volby2017_Olomouc')
    

The code is freely available for anyone who might find it useful. Have fun!

    
