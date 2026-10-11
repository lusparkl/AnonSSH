from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Label, Static

from app.db.services import create_user
from app.screens.about_screen import AboutScreen
from app.screens.create_screen import CreateScreen
from app.screens.feed_screen import FeedScreen
from app.screens.search_screen import SearchScreen


LOGO = r"""
   ___                    _____ __  __ __  __
  / _ |  ___  ___  ___   / __// /_/ // /_/ /
 / __ | / _ \/ _ \/   \ _\ \ / __  // __  /
/_/ |_|/_//_/\___/_//_//___//_/ /_//_/ /_/
"""


class AnonSHHApp(App):
    TITLE = "AnonSHH"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [("1", "feed", "Latest posts"),
                ("2", "create", "Create a post"),
                ("3", "search_posts", "Search"),
                ("4", "about", "About"),
                ("q", "quit", "Quit")]
    SCREENS = {
        "feed": FeedScreen,
        "create": CreateScreen,
        "search": SearchScreen,
        "about": AboutScreen
    }

    def compose(self) -> ComposeResult:
        with Vertical(id="home"):
            yield Static(LOGO, id="logo")
            yield Label("Say it outloud.", id="tagline")
            yield Label("1-latest   2-post   3-search   4-about", id="menu")
            yield Label("connected as anonymous", id="identity")
        yield Footer()

    def on_mount(self):
        self.user_id = create_user()
        self.query_one("#identity", Label).update(f"joined as {self.user_id}")

    def action_feed(self):
        self.push_screen("feed")

    def action_create(self):
        self.push_screen("create")

    def action_search_posts(self):
        self.push_screen("search")

    def action_about(self):
        self.push_screen("about")

if __name__ == "__main__":
    app = AnonSHHApp()
    app.run()
