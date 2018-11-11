from context import plugins


def test_load_plugin():
    funcs = plugins.load_plugins(["dummy_plugin"])
    assert len(funcs) == 1

    dummy_plugin = funcs[0]
    assert dummy_plugin("GPW") == "Hello, GPW!"
