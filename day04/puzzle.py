from typing import Dict


def birth_year(bzr: str):
    return bzr.isnumeric() and 1920 <= int(bzr) <= 2002


def issue_year(iyr: str):
    return iyr.isnumeric() and 2010 <= int(iyr) <= 2020


def expiration_year(eyr: str):
    return eyr.isnumeric() and 2020 <= int(eyr) <= 2030


def height(hgt: str):
    ranges = {
        'cm': (150, 193),
        'in': (59, 76)
    }
    try:
        unit = hgt[-2:]
        num = int(hgt[:-2])
        _min, _max = ranges[unit]
        return _min <= num <= _max
    except Exception as e:
        return False


def hair_color(hcl: str):
    def is_hex(str):
        return all(
            s in [c for c in '0123456789abcdef']
            for s in str
        )

    return len(hcl) == 7 and \
           hcl[0] == '#' and \
           is_hex(hcl[1:])


def eye_color(ecl: str):
    return ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def passport_id(pid: str):
    return len(pid) == 9 and pid.isnumeric()


required_fields = {
    "byr": birth_year,
    "iyr": issue_year,
    "eyr": expiration_year,
    "hgt": height,
    "hcl": hair_color,
    "ecl": eye_color,
    "pid": passport_id,
    # "cid": "Country ID",
}


def passports(file):
    passport = {}
    for line in file:
        line = line.strip()
        if not line:
            yield passport
            passport = {}
        else:
            elems = [elem for elem in line.split()]
            fields = dict([
                tuple(elem.split(':'))
                for elem in elems
            ])
            passport |= fields

    if passport:
        yield passport


def is_valid_passport(passport: Dict[str, str]) -> bool:
    return all(
        required_field in passport.keys() and is_valid(passport[required_field])
        for required_field, is_valid in required_fields.items()
    )


if __name__ == '__main__':
    with open('input.txt', 'rt') as puzzle:
        valid_passports = [
            1
            for passport
            in passports(puzzle)
            if is_valid_passport(passport)
        ]

    print('valid passports: ', sum(valid_passports))
