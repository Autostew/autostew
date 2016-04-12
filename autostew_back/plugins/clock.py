"""
Shows the time on on every in-game hour.
"""
from autostew_web_session.models.server import Server

name = "Race clock"

hour = None

def tick(server: Server):
    global hour
    session = server.session_api
    if session.current_hour.get() != hour and session.session_state.get_nice() == SessionState.race:
        server.api.send_chat("")
        server.api.send_chat("CLOCK {}:{:02d}".format(session.current_hour.get(), session.current_minute.get()))
        hour = session.current_hour.get()