#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2025
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import pytest

from telegram import (
    InlineKeyboardButton,
    KeyboardButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    WebAppInfo,
)
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def keyboard_button():
    return KeyboardButton(
        KeyboardButtonTestBase.text,
        request_location=KeyboardButtonTestBase.request_location,
        request_contact=KeyboardButtonTestBase.request_contact,
        request_poll=KeyboardButtonTestBase.request_poll,
        web_app=KeyboardButtonTestBase.web_app,
        request_chat=KeyboardButtonTestBase.request_chat,
        request_users=KeyboardButtonTestBase.request_users,
    )


class KeyboardButtonTestBase:
    text = "text"
    request_location = True
    request_contact = True
    request_poll = KeyboardButtonPollType("quiz")
    web_app = WebAppInfo(url="https://example.com")
    request_chat = KeyboardButtonRequestChat(1, True)
    request_users = KeyboardButtonRequestUsers(2)


class TestKeyboardButtonWithoutRequest(KeyboardButtonTestBase):
    def test_slot_behaviour(self, keyboard_button):
        inst = keyboard_button
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_expected_values(self, keyboard_button):
        assert keyboard_button.text == self.text
        assert keyboard_button.request_location == self.request_location
        assert keyboard_button.request_contact == self.request_contact
        assert keyboard_button.request_poll == self.request_poll
        assert keyboard_button.web_app == self.web_app
        assert keyboard_button.request_chat == self.request_chat
        assert keyboard_button.request_users == self.request_users

    def test_to_dict(self, keyboard_button):
        keyboard_button_dict = keyboard_button.to_dict()

        assert isinstance(keyboard_button_dict, dict)
        assert keyboard_button_dict["text"] == keyboard_button.text
        assert keyboard_button_dict["request_location"] == keyboard_button.request_location
        assert keyboard_button_dict["request_contact"] == keyboard_button.request_contact
        assert keyboard_button_dict["request_poll"] == keyboard_button.request_poll.to_dict()
        assert keyboard_button_dict["web_app"] == keyboard_button.web_app.to_dict()
        assert keyboard_button_dict["request_chat"] == keyboard_button.request_chat.to_dict()
        assert keyboard_button_dict["request_users"] == keyboard_button.request_users.to_dict()

    @pytest.mark.parametrize("request_user", [True, False])
    def test_de_json(self, request_user):
        json_dict = {
            "text": self.text,
            "request_location": self.request_location,
            "request_contact": self.request_contact,
            "request_poll": self.request_poll.to_dict(),
            "web_app": self.web_app.to_dict(),
            "request_chat": self.request_chat.to_dict(),
            "request_users": self.request_users.to_dict(),
        }
        if request_user:
            json_dict["request_user"] = {"request_id": 2}

        keyboard_button = KeyboardButton.de_json(json_dict, None)
        if request_user:
            assert keyboard_button.api_kwargs == {"request_user": {"request_id": 2}}
        else:
            assert keyboard_button.api_kwargs == {}

        assert keyboard_button.text == self.text
        assert keyboard_button.request_location == self.request_location
        assert keyboard_button.request_contact == self.request_contact
        assert keyboard_button.request_poll == self.request_poll
        assert keyboard_button.web_app == self.web_app
        assert keyboard_button.request_chat == self.request_chat
        assert keyboard_button.request_users == self.request_users

    def test_equality(self):
        a = KeyboardButton("test", request_contact=True)
        b = KeyboardButton("test", request_contact=True)
        c = KeyboardButton("Test", request_location=True)
        d = KeyboardButton("Test", web_app=WebAppInfo(url="https://ptb.org"))
        e = InlineKeyboardButton("test", callback_data="test")
        f = KeyboardButton(
            "test",
            request_contact=True,
            request_chat=KeyboardButtonRequestChat(1, False),
            request_users=KeyboardButtonRequestUsers(2),
        )
        g = KeyboardButton(
            "test",
            request_contact=True,
            request_chat=KeyboardButtonRequestChat(1, False),
            request_users=KeyboardButtonRequestUsers(2),
        )

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)

        assert a != f
        assert hash(a) != hash(f)

        assert f == g
        assert hash(f) == hash(g)
