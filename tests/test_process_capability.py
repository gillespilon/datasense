import datasense as ds


def test_pp():
    average = 0.11001
    std_devn = 0.868663
    sample_size = 40
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = ds.pp(
        average=average,
        std_devn=std_devn,
        sample_size=sample_size,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (1.5349258956964131, 1.1953921108301047, 1.873778000024199)
    assert result == expected
