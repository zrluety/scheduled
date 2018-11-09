from .session import Session

def read(source, profile):
    s = Session(profile)
    return s.read(source)

def format(transaction_data, profile):
    s = Session(profile)
    return s.format(transaction_data)

def save(transaction_data, dest, profile):
    s = Session(profile)
    return s.save(transaction_data, dest)
