from royal_game_of_ur.src.rgu import RGU


def test_whatsit():
    assert True


def test_failure():
    assert False


def test_rgu_init():
    rgu = RGU()
    assert rgu.player == 0
