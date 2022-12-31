
# region [Practice]Install custom exception handlers [1]
# [1]: https://fastapi.tiangolo.com/ko/tutorial/handling-errors/#install-custom-exception-handlers
# from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import JSONResponse

class FormatInvalidateException(Exception):
    def __int__(self, given_value: str, valid_form: str, format_example: str = None):
        self.given_value = given_value
        self.valid_form = valid_form
        self.format_example = format_example
# endregion [Practice]Install custom exception handlers
