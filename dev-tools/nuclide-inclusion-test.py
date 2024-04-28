import json
import radioactivedecay as rd

data = json.load(open('common-nuclides.json','r'))
#print(data)

i = 0
for isotope in data['radioactive_isotopes']:
    try:
        nuc = rd.Nuclide(isotope['symbol'])
        print(f'found {isotope}')
    except:
        print(f'\tisotope not available: {isotope}')
        i += 1
print(f'not found: {i}')