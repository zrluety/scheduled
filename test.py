from scheduled.pdf import get_java_call


filepath = r"G:\!Programs\scheduled\src\python\tests\data\201601 1205-EatonsNeck.pdf"
outfilepath = r"G:\!Programs\scheduled\src\python\tests\data\201601 1205-EatonsNeck.csv"

names = [
    "DATE",
    "ACCOUNT TYPE",
    "TRANSACTION",
    "QUANTITY",
    "DESCRIPTION",
    "PRICE",
    "AMOUNT",
]
stopwords = [
    "Our Cash Sweep program",
    "Total Deposits",
    "Total Income and distributions",
    "Total Securities purchased",
    "Total Other subtractions and fees",
    "Income on non-reportable accounts",
    "Total Securities sold and redeemed",
    "PPR2 PPDY",
]

v_align = "top"

print(get_java_call(filepath, outfilepath, names, stopwords, v_align))