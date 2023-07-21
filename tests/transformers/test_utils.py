import pytest
from pydantic import BaseModel

from esmerald import File, ImproperlyConfigured, Param, ValidationErrorException, get
from esmerald.enums import ParamType
from esmerald.transformers.model import ParamSetting
from esmerald.transformers.utils import get_request_params, get_signature


class Test(BaseModel):
    """"""


@get()
async def test() -> None:
    """"""


def test_get_signature_improperly_configured():
    test = Test()
    with pytest.raises(ImproperlyConfigured):
        get_signature(test)


def test_signature_model_is_none():
    handler = get_signature(test)

    assert handler is None


def test_get_request_params_raise_validation_error_exception():
    param = Param(default=None)
    expected_param = File(default=None)
    param_setting = ParamSetting(
        default_value=None,
        field_alias="param",
        field_name="param",
        is_required=True,
        param_type=ParamType.PATH,
        field_info=param,
    )

    expected_param_setting = ParamSetting(
        default_value=None,
        field_alias="test",
        field_name="test",
        is_required=True,
        param_type=ParamType.PATH,
        field_info=expected_param,
    )

    set_params = {param_setting}
    expected_params = {expected_param_setting}

    with pytest.raises(ValidationErrorException):
        get_request_params(
            params=set_params, expected=expected_params, url="http://testserver.com"
        )
