import pytest
from brain.client import VoxieClient, AVAILABLE_ROOMS


class TestVoxieClientInit:
    def test_default_state(self):
        client = VoxieClient()
        assert client.active_room is None
        assert client.history == []


class TestEnterRoom:
    def test_enter_valid_room(self):
        client = VoxieClient()
        client.enter_room("astrophysics")
        assert client.active_room == "astrophysics"

    def test_enter_all_available_rooms(self):
        client = VoxieClient()
        for room in AVAILABLE_ROOMS:
            client.enter_room(room)
            assert client.active_room == room

    def test_enter_unknown_room_raises(self):
        client = VoxieClient()
        with pytest.raises(ValueError, match="Unknown room"):
            client.enter_room("underwater_basket_weaving")

    def test_enter_room_switches_room(self):
        client = VoxieClient()
        client.enter_room("astrophysics")
        client.enter_room("languages")
        assert client.active_room == "languages"


class TestLeaveRoom:
    def test_leave_room_clears_active(self):
        client = VoxieClient()
        client.enter_room("engineering")
        client.leave_room()
        assert client.active_room is None

    def test_leave_room_when_none_is_noop(self):
        client = VoxieClient()
        client.leave_room()
        assert client.active_room is None


class TestSend:
    def test_send_returns_response(self):
        client = VoxieClient()
        response = client.send("Hello!")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_send_records_history(self):
        client = VoxieClient()
        client.send("Hello!")
        assert len(client.history) == 2
        assert client.history[0]["role"] == "user"
        assert client.history[1]["role"] == "assistant"

    def test_send_includes_room_in_response(self):
        client = VoxieClient()
        client.enter_room("astrophysics")
        response = client.send("What is a black hole?")
        assert "astrophysics" in response

    def test_send_without_room_uses_general(self):
        client = VoxieClient()
        response = client.send("Hey!")
        assert "general" in response

    def test_send_empty_message_raises(self):
        client = VoxieClient()
        with pytest.raises(ValueError, match="empty"):
            client.send("")

    def test_send_whitespace_only_raises(self):
        client = VoxieClient()
        with pytest.raises(ValueError, match="empty"):
            client.send("   ")

    def test_multiple_sends_accumulate_history(self):
        client = VoxieClient()
        client.send("First")
        client.send("Second")
        assert len(client.history) == 4


class TestClearHistory:
    def test_clear_history_empties_history(self):
        client = VoxieClient()
        client.send("Something")
        client.clear_history()
        assert client.history == []

    def test_clear_history_does_not_affect_room(self):
        client = VoxieClient()
        client.enter_room("digital_art")
        client.send("Inspire me")
        client.clear_history()
        assert client.active_room == "digital_art"
