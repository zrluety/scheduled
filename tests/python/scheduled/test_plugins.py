from context import plugins


def test_load_plugin():
    profile = {"plugins": ["dummy_plugin"]}

    funcs = plugins.load_plugin(profile)
    assert len(funcs) == 1

    dummy_plugin = funcs[0]
    assert dummy_plugin("GPW") == "Hello, GPW!"
