from scheduled.extractor import PdfExtractor
from scheduled.utils import read_profile

filename = r'H:\36538\FPC\Original Data\PAID 9-4-17\ALP AUG 17.pdf'

with open('./profiles/Eric.yaml', 'r') as f:
    y = read_profile(f)
    options = y.get('options')

e = PdfExtractor()
df = e.extract(source=filename, options=options)
print(df)
