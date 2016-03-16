"""
Shows the time on on every in-game hour.
"""
from autostew_back.gameserver.server import Server
from autostew_back.gameserver.session import SessionState

name = "Race clock"

hour = None

def tick(server: Server):
    global hour
    session = server.session
    if session.current_hour.get() != hour and session.session_state.get_nice() == SessionState.race:
        server.api.send_chat("CLOCK {}:{:02d}".format(session.current_hour.get(), session.current_minute.get()))
        hour = session.current_hour.get()