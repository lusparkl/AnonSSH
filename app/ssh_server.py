import asyncio
import fcntl
import os
import pty
import struct
import sys
import termios
from os import getenv
from pathlib import Path

import asyncssh
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


class AnonSSHServer(asyncssh.SSHServer):
    def begin_auth(self, username: str) -> bool:
        return False


async def handle_client(process: asyncssh.SSHServerProcess):
    if not process.term_type:
        process.stderr.write(b"A terminal is required. Connect with ssh -t.\r\n")
        process.exit(1)
        return

    width, height, _, _ = process.term_size
    master, slave = pty.openpty()
    os.set_inheritable(slave, True)
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", height, width, 0, 0))

    environment = os.environ.copy()
    environment["TERM"] = process.term_type

    app = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "app.app",
        cwd=ROOT,
        env=environment,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        start_new_session=True
    )

    os.close(slave)
    stdin = os.fdopen(os.dup(master), "wb", buffering=0)
    stdout = os.fdopen(os.dup(master), "rb", buffering=0)
    os.close(master)
    try:
        await process.redirect(stdin=stdin, stdout=stdout)
        await app.wait()
    finally:
        stdin.close()
        stdout.close()

        if app.returncode is None:
            app.terminate()
            await app.wait()

    process.exit(app.returncode or 0)


async def run_server():
    host = getenv("SSH_HOST", "0.0.0.0")
    port = int(getenv("SSH_PORT", "8022"))
    key_path = Path(getenv("SSH_HOST_KEY", ROOT / "ssh_host_key"))

    if not key_path.exists():
        asyncssh.generate_private_key("ssh-ed25519").write_private_key(key_path)
        key_path.chmod(0o600)

    server = await asyncssh.create_server(
        AnonSSHServer,
        host,
        port,
        server_host_keys=[key_path],
        process_factory=handle_client,
        encoding=None
    )

    print(f"AnonSHH is listening on {host}:{port}")

    try:
        await asyncio.Future()
    finally:
        server.close()
        await server.wait_closed()
