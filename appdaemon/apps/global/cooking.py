

def are_we_cooking(self, **kwargs):
    """ Check if we are likely to be cooking"""
    if self.get_state("input_boolean.cooking_mode") == 'on' or self.now_is_between("16:00:00", "19:00:00") or self.now_is_between("06:45:00", "08:00:00"):
        return True
    else:
        return False