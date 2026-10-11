from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Label

# Screen with general info about project
class AboutScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]

    def action_back(self):
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("About AnonSHH", classes="screen-title")
        yield Label("A small anonymous forum living inside SSH created for fun.\n\nRead what others wrote, post yourself, or search the archive. No account, profile, or public identity - what a beautiful place!", id="about")
        yield Footer()
