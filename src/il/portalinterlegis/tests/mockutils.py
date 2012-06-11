
def return_values(mock, values):
    def f(procedure):
        mock.side_effect = side_effect(values, procedure)
    return f

def side_effect(values, procedure=None):
    values = values[:]
    values.reverse()
    def _side_effect(*args, **kwargs):
        if procedure:
            procedure(*args, **kwargs)
        return values.pop()
    return _side_effect
