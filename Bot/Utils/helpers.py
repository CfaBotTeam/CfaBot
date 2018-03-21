
def get_enum_name(enum_class, enum_value):
    enum_names = {value: name for name, value in vars(enum_class).items() if name.isupper()}
    return enum_names[enum_value]