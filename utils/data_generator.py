import random

def generate_plate() -> str:
    return str(random.randint(10000000, 99999999))

def generate_slot() -> str:
    return str(random.randint(500, 999))