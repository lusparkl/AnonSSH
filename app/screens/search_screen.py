from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView

from app.db.services import search_messages

# Screen where users can search among all posts
class SearchScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]

    def action_back(self):
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("SEARCH POSTS", classes="screen-title")
        yield Input(placeholder="Type anything and press enter", id="query")
        yield Label("Search by words", id="search-status")
        yield ListView(id="results")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted):
        query = event.value.strip()
        results = self.query_one("#results", ListView)
        status = self.query_one("#search-status", Label)

        await results.clear()

        if not query:
            status.update("Search by words")
            return

        messages = search_messages(query)
        status.update(f"{len(messages)} result{'s' if len(messages) != 1 else ''}")

        if messages:
            await results.extend([
                ListItem(Label(f"{message.author_id}  -  {message.created:%d %b, %H:%M}\n{message.text}", markup=False), classes="message")
                for message in messages
            ])
