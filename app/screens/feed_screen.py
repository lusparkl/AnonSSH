from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Label, ListView, ListItem

from app.db.services import get_messages

# Screen where users see all posts
class FeedScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]

    def action_back(self):
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("LATEST POSTS", classes="screen-title")
        yield Label("No one sent a message yet:(", id="empty")
        yield ListView(id="messages")
        yield Footer()

    async def on_mount(self):
        await self.refresh_messages()

    async def on_screen_resume(self):
        await self.refresh_messages()

    async def refresh_messages(self):
        messages = get_messages()
        message_list = self.query_one("#messages", ListView)
        empty = self.query_one("#empty", Label)

        await message_list.clear()
        empty.display = not messages
        message_list.display = bool(messages)

        if messages:
            await message_list.extend([
                ListItem(Label(f"{message.author_id}  -  {message.created:%d %b, %H:%M}\n{message.text}", markup=False), classes="message")
                for message in messages
            ])
