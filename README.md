# AnonSSH

Anonymous SSH is simple anonymous forum/social media in your SSH. There is no logins, names or any data about user. I made it for fun, so don't judge it hard.

I learned how to work with SSH and discovered Textual python lib, idk how I created TUI's without it. This library makes TUI creation so easy and efficient!

![Screenshot](/assets/Screenshot.png)

---

## Stack 📚

**What I used:**

- [Python](https://www.python.org/) to **write everything!**
- [AsyncSSH](https://github.com/ronf/asyncssh) to **handle server part.**
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) to **work with database.**
- [Textual](https://github.com/textualize/textual) to **create pretty TUI.**
- [Rich](https://github.com/textualize/rich) to **make texts look good.**

---

## How to connect 🤝

Just run it from your terminal, and you're in!

```bash
ssh -p 8022 anonymous@79.76.38.187
```

---

## How to setup 🔧

To setup AnonSSH you need to clone repository into your machine, enter database connection string into .env as DB_LINK, and then run this command:

```bash
pip install -r requirements.txt
python main.py
```

After this you can connect using:

```bash
ssh -p 8022 anonymous@localhost
```

---

## How to run interface localy 📍

To run it locally you'll have to do setup and then run:

```bash
python -m app.app
```

---

## How to contribute 🛠️

I don't intent to continue this project because it was just one day hitter. But if you're willing to improve AnonSSH - post your pull request and I'll definetely check it out!

---

Thats it. Thank you for visiting!🩷
