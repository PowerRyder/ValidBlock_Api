
from src.utilities.utils import execute_query


def save_message(name: str, email: str, type: str, subject: str, message: str):
    res = execute_query("call usp_save_contact_us_message(_name => %s, _email => %s, _type => %s, _subject => %s, _message => %s)", (name, email, type, subject, message))
    return res