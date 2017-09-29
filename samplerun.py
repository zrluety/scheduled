from scheduled.scripts.cli import run_app

src = r"C:\Users\zluety.GPWA\Desktop\2017Q1 7854 Asset Mark-PugiTwo.pdf"
profile = 'AssetMark'
scheduled = 'random.xlsx'
dst = '2017Q1 7854 Asset Mark-PugiTwo.xlsx'
user = 'me'
run_app(False, src, profile, scheduled, dst, user)
