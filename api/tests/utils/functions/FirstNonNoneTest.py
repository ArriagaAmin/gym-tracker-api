import pytest

from api.utils import first_non_none


class FirstNonNoneTest:

    @pytest.mark.parametrize("n_args", list(range(0, 10)))
    def test_failure_none_list(self, n_args: int):
        with pytest.raises(ValueError):
            args = [None] * n_args
            first_non_none(*args)

    @pytest.mark.parametrize("pos", list(range(0, 10)))
    @pytest.mark.parametrize("value", [0, False, "test"])
    def test_success_one_value(self, pos: int, value: int):
        args = [None] * 10
        args[pos] = value

        result = first_non_none(*args)
        
        assert result == value

    @pytest.mark.parametrize("pos", list(range(0, 10)))
    def test_success_multiple_values(self, pos: int):
        value = 0
        args = [None] * 10
        args[pos] = value
        args += list(range(1, 10))

        result = first_non_none(*args)
        
        assert result == value
