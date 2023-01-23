import pandas as pd
Rules = pd.ExcelFile('site_configurations.xlsx')
generalRule = pd.read_excel(Rules, sheet_name='generalRule',index_col = 0).fillna('').to_dict(orient = 'index')
specialSubjectShort = pd.read_excel(Rules, sheet_name='specialSubjectShort',index_col = 0).fillna('').to_dict(orient = 'index')
specialBylinePos = pd.read_excel(Rules, sheet_name='specialBylinePos',index_col = 0).fillna('').to_dict(orient = 'index')
specialTitleTag = pd.read_excel(Rules, sheet_name='specialTitleTag',index_col = 0).fillna('').to_dict(orient = 'index')
specialBannedTag = pd.read_excel(Rules, sheet_name='specialBannedTag',index_col = 0).fillna('').to_dict(orient = 'index')

for x in generalRule.keys(): generalRule[x] = (generalRule[x][0], generalRule[x][1], str(generalRule[x][2]).split(',')) # may need to strip spaces at beginning at end in case someone adds it
for x in specialBylinePos: specialBylinePos[x] = (specialBylinePos[x][0], specialBylinePos[x][1])
for x in [specialSubjectShort,specialTitleTag]:
    for y in x.keys(): x[y] = x[y][0]
for x in specialBannedTag: specialBannedTag[x] = str(specialBannedTag[x][0]).split(',')

print(
    'generalRule =',generalRule,'\n' +
    'specialSubjectShort =',specialSubjectShort,'\n' +
    'specialBylinePos =',specialBylinePos,'\n' +
    'specialTitleTag =',specialTitleTag,'\n' +
    'specialBannedTag =',specialBannedTag,'\n'
)
