#HTML parser into XML.

#Links to be parsed:
#https://apps.umsl.edu/webapps/ITS/CourseSchedule/index.cfm?subject=CMP%20SCI&term=SP2024
#Spring_semester_2024.htm
#https://apps.umsl.edu/webapps/ITS/CourseSchedule/index.cfm?subject=CMP%20SCI&term=SS2024
#Summer_semester_2024.htm
#https://apps.umsl.edu/webapps/ITS/CourseSchedule/index.cfm?subject=CMP%20SCI&term=FS2024
#Fall_semester_2024.htm
#These could possibly be automated for a scraper in the future.

import pandas as pd


# Read in the file
#with open('Fall_semester_2024.htm', 'r') as file:
#  filedata = file.read()

#Formatting definition. Converts HTML to csv readable format. 
#Note: Gets a little hazy in the last few columns, order may need to be reworked. 
def reformat_html(file):
    with open(file, 'r') as new:
        filedata = new.read()
    filedata = filedata.replace('<td>', '')
    filedata = filedata.replace('</td>', ',')
    filedata = filedata.replace('<tr>', '')
    filedata = filedata.replace(' ', '')
    filedata = filedata.replace('\t', '')
    filedata = filedata.replace('\r', '')
    filedata = filedata.replace('\n', '')
    filedata = filedata.replace('CRANK', '')
    filedata = filedata.replace('</tr>', '\n')
    filedata = filedata.replace('</tbody></table></body></html>', '')
    filedata = filedata.replace('<tbody>', '\n')
    return filedata

#Stores HTML as CSV for listed semester (Fall 2024, Spring 2024, Summer 2024)
springcsv=reformat_html('Spring_semester_2024.htm')
with open('spring.csv','w') as file:
    file.write(springcsv)
fallcsv=reformat_html('Fall_semester_2024.htm')
with open('fall.csv','w') as file:
    file.write(fallcsv)
summercsv=reformat_html('Summer_semester_2024.htm')
with open('summer.csv','w') as file:
    file.write(summercsv)

#Converts CSV to Pandas then drops duplicate Catalog numbers. 
summ=pd.read_csv("summer.csv", skiprows=1,index_col=False).drop_duplicates(subset=['CatalogNumber'])
fall=pd.read_csv("fall.csv", skiprows=1,index_col=False).drop_duplicates(subset=['CatalogNumber'])
spri=pd.read_csv("spring.csv", skiprows=1, index_col=False).drop_duplicates(subset=['CatalogNumber'])

#Double merge between the summ, fall, and spring data frames using a tmp dataframe.
tmp=pd.merge(spri,summ, how='outer', suffixes=("_sp","_su"), on=['CatalogNumber'])
merged_catalog=pd.merge(tmp,fall, how='outer', on=['CatalogNumber']).rename(columns={"TERM":"TERM_fa"})

#For loop that converts the 3 terms into a new singlur list column and resets Subject across all coures to CMPSCI
new_list=[]
for i in range(len(merged_catalog["CatalogNumber"])):
    new_list.append(["NA","NA","NA"])
    print(new_list)
    if isinstance(merged_catalog['TERM_sp'].loc[i],str):
        new_list[i][0]='SP'
    if isinstance(merged_catalog['TERM_su'].loc[i],str):
        new_list[i][1]='SU'
    if isinstance(merged_catalog['TERM_fa'].loc[i],str):
        new_list[i][2]='FA'
    merged_catalog["Subject"].iloc[i]="CMPSCI"

#Attaching the list to the new format
merged_catalog['TERMS']=new_list

#Final dataframe.
final_catalog=merged_catalog[["Subject","CatalogNumber","TERMS"]]
print(final_catalog)

#Testing for future object generation to be inserted here 


