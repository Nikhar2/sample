import pandas as pd
import glob
import os
import openpyxl

# Directory (check the correct path before execute)
dir = 'workspace/Hybris-sampledata/bb-hybris-sampledata/'

# Define value for file prefix and brand for each folder w.r.t sites
folders = {'bh': { 'fileprefix' : 'BHUS', 'brand' : 'BAL' }, 'bh-au': { 'fileprefix' : 'BHAU', 'brand' : 'BHAU' }, 'bh-de': { 'fileprefix' : 'BHDE', 'brand' : 'BHDE' }, 'bh-fr': { 'fileprefix' : 'BHFR', 'brand' : 'BHFR' }, 'bh-uk': { 'fileprefix' : 'BHUK', 'brand' : 'BHUK' }}

# Create an empty dataframe to append values from all five sites
allRequiredEntites = pd.DataFrame()

for folder in folders:
    # Genrating path of file
    filePath = dir + folder + '/' + folders[folder]['fileprefix'] + 'WebOutbound-AllEntities-StagingDelta_*.xlsx'
    
    # Open the required excel file
    xls_file = pd.ExcelFile(glob.glob(filePath)[0])

    # Get the required sheet from excel file
    entities = pd.read_excel(xls_file, 'Entities')

    # Filter the data where 'Entity Type' is 'SKU'
    requiredEntites = entities[entities["Entity Type"] == "SKU"]

    # Filter required columns
    requiredEntites = requiredEntites[['Initial Merchandising GEN//Product code on website']]

    # Rename columns
    requiredEntites = requiredEntites.rename(columns={'Initial Merchandising GEN//Product code on website':'SKU'})

    # Add columns with value
    # requiredEntites = requiredEntites.assign(BRAND = folders[folder]['brand'] , reconPercentage = None, TotalCartons = 1)
    requiredEntites = requiredEntites.assign(BRAND = folders[folder]['brand'])
    
    # Removing Id values
    # requiredEntites = requiredEntites.assign(Id = None)

    # Append modified data into one dataframe
    allRequiredEntites = allRequiredEntites.append(requiredEntites)
    
# Create an excel file
allRequiredEntites.to_excel('sku_sample_data.xlsx', header=None, index = False)

open('insertSku-Trees.sql','w').close()
open('insertSku-International.sql','w').close()

treesFile = open('insertSku-Trees.sql','a')
internationalFile = open('insertSku-International.sql','a')

wb = openpyxl.load_workbook('sku_sample_data.xlsx')
ws = wb['Sheet1']
for row in ws.iter_rows():
    sku = str(row[0].value)
    brand = str(row[1].value)
    if sku.isnumeric() :
        if brand == 'BAL':
            treesFile.write("insert into temp_SkusToLoad (Sku,Brand) values ('" + sku + "','" + brand + "')\n")
        else:
            internationalFile.write("insert into temp_SkusToLoad (Sku,Brand) values ('" + sku + "','" + brand + "')\n")

treesFile.write('exec GenerateSkusInION')
internationalFile.write('exec GenerateSkusInION')

treesFile.close()
internationalFile.close()

