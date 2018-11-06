from scheduled.scripts.cli import run_app

src = r"H:\37153\2018\Banking\Quarter 1\Q1 Portfolio VV Statements\csvs\201801 VV RBC Trust Stmt.csv"
profile = 'RBC'
scheduled = r''
dst = r'H:\37153\2018\Banking\Quarter 1\Q1 Portfolio VV Statements\201801 VV RBC Trust Stmt.xlsx'
user = 'me'

# runner = CliRunner()
# result = runner.invoke(run_app, [False, src, profile, scheduled, dst, user])

run_app(False, src, profile, scheduled, dst, user)