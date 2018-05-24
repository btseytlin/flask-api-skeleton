import json
from librarian.models import Kitty


def test_make(client, session):
    assert session.query(Kitty).all() == []
    res = client.post('/make')
    assert res.status_code == 200
    kitties = session.query(Kitty).all()
    assert kitties
    assert len(kitties) == 1
    kitty = kitties[0]
    kitty_data = res.json
    assert kitty.id == kitty_data['id']
    assert kitty.name == kitty_data['name']


def test_list(client, session):
    assert session.query(Kitty).all() == []
    res = client.get('/list')
    assert res.json == []
    assert res.status_code == 200

    res = client.post('/make')
    assert res.status_code == 200
    kitties = session.query(Kitty).all()
    assert kitties
    assert len(kitties) == 1
    kitty = kitties[0]
    kitty_data = res.json
    assert kitty.id == kitty_data['id']
    assert kitty.name == kitty_data['name']

    res = client.get('/list')
    assert res.json
    assert kitty_data in res.json
