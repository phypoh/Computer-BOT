# Tool Module:
# Small functions used to make life simpler!

# Return TRUE if INT else FALSE
def isIntTOOL(number):
    try:
        int(number)
        return True
    except ValueError:
        return False