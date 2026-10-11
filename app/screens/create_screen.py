from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Input, Label

from app.db.services import send_message

# Screen where users write their posts
class CreateScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]

    def action_back(self):
        self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()

        if not text:
            self.app.notify("You need to write something down.", severity="warning")
            return

        send_message(user_id=self.app.user_id, text=text[:250])
        self.app.notify("Your whisper was posted.")
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("NEW POST", classes="screen-title")
        yield Input(placeholder="What do you want to write about?", max_length=250, id="text")
        yield Label("Press Enter to post", id="post-hint")
        yield Footer()
