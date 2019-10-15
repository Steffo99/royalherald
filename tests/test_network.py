import pytest
import uuid
import asyncio
import logging
import royalherald as h


log = logging.root
stream_handler = logging.StreamHandler()
stream_handler.formatter = logging.Formatter("{asctime}\t{name}\t{levelname}\t{message}", style="{")
log.addHandler(stream_handler)
log.setLevel(logging.WARNING)


@pytest.fixture
def async_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def echo_request_handler(message):
    return message


def test_package_serialization():
    pkg = h.Package({"ciao": "ciao"},
                    source=str(uuid.uuid4()),
                    destination=str(uuid.uuid4()),
                    source_conv_id=str(uuid.uuid4()),
                    destination_conv_id=str(uuid.uuid4()))
    assert pkg == h.Package.from_dict(pkg.to_dict())
    assert pkg == h.Package.from_json_string(pkg.to_json_string())
    assert pkg == h.Package.from_json_bytes(pkg.to_json_bytes())


def test_request_creation():
    request = h.Request("pytest", {"testing": "is fun", "bugs": "are less fun"})
    assert request == h.Request.from_dict(request.to_dict())


# Broken!
#
# def test_links(async_loop: asyncio.AbstractEventLoop):
#     address, port = "127.0.0.1", 1234
#     master = h.Server(address, port, "test", loop=async_loop)
#     async_loop.create_task(master.run())
#     async_loop.run_until_complete(asyncio.sleep(5))
#     # Test invalid secret
#     wrong_secret_link = h.Link(f"ws://{address}:{port}", "invalid", "test", echo_request_handler, loop=async_loop)
#     with pytest.raises(h.ConnectionClosedError):
#         async_loop.run_until_complete(wrong_secret_link.run())
#     # Test regular connection
#     link1 = h.Link("ws://127.0.0.1:1235", "test", "one", echo_request_handler, loop=async_loop)
#     async_loop.create_task(link1.run())
#     link2 = h.Link("ws://127.0.0.1:1235", "test", "two", echo_request_handler, loop=async_loop)
#     async_loop.create_task(link2.run())
#     message = {"ciao": "ciao"}
#     response = async_loop.run_until_complete(link1.request(message, "two"))
#     assert message == response