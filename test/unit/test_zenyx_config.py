import pytest
import os
import sys
import re

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "../../lib")))
import config
from zenyx_config import ZenyxConfig


def zenyx_conf(**kwargs):
    defaults = {
        "rpcuser": "zenyxrpc",
        "rpcpassword": "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk",
        "rpcport": 14083,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(
        **defaults
    )

    return conf


def test_get_rpc_creds():
    zenyx_config = zenyx_conf()
    creds = ZenyxConfig.get_rpc_creds(zenyx_config)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "zenyxrpc"
    assert creds.get("password") == "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk"
    assert creds.get("port") == 14083

    zenyx_config = zenyx_conf(rpcpassword="s0X0pers33kr1t", rpcport=8000)
    creds = ZenyxConfig.get_rpc_creds(zenyx_config)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "zenyxrpc"
    assert creds.get("password") == "s0X0pers33kr1t"
    assert creds.get("port") == 8000

    no_port_specified = re.sub("\nrpcport=.*?\n", "\n", zenyx_conf(), re.M)
    creds = ZenyxConfig.get_rpc_creds(no_port_specified)

    for key in ("user", "password", "port"):
        assert key in creds
    assert creds.get("user") == "zenyxrpc"
    assert creds.get("password") == "EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk"
    assert creds.get("port") == 22971


def test_slurp_config_file():
    import tempfile

    zenyx_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    expected_stripped_config = """server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    with tempfile.NamedTemporaryFile(mode="w") as temp:
        temp.write(zenyx_config)
        temp.flush()
        conf = ZenyxConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
