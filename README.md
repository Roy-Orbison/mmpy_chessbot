# mmpychessbot

[Matthew Dorner's chess plugin][1] for Mattermost makes it easy to play against your friends and colleagues, but has no built-in machine opponent.
This simple service built upon [Alex Tzonko's bot][2] and [Niklas Fiekas' chess library][3] allows you to add any machine opponent that uses the Universal Chess Interface.

## Installation

1. Create a system user on any machine that is always on, and has network access to your Mattermost service.
	This can be the same server that Mattermost is on. E.g.:
	```sh
	DHOME=/srv sudo adduser --system --group --shell /bin/bash chessbot
	```
2. On the same machine, download and install a UCI chess engine, like [Stockfish][4], to a location that user can access. E.g.:
	```sh
	wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar
	tar -xf stockfish-ubuntu-x86-64-avx2.tar --strip-components=1 stockfish/stockfish-ubuntu-x86-64-avx2
	sudo install stockfish-ubuntu-x86-64-avx2 /usr/local/bin/stockfish
	rm stockfish-ubuntu-x86-64-avx2*
	```
	Ensure you choose a version that works on your CPU.
	You may need an [older Stockfish engine][5] for your system.
3.	Switch to your new user:
	```sh
	sudo -u chessbot -i
	cd
	```
4.	Clone this repo:
	```sh
	git clone https://github.com/Roy-Orbison/mmpychessbot.git
	cd mmpychessbot/
	```
5.	Install the python dependencies:
	```sh
	python3 -m venv venv
	. venv/bin/activate
	pip3 install chess mmpy-bot
	```
6.	Copy the example app config file and open it for editing, e.g.:
	```sh
	cp mmpychessbot.conf{.example,}
	vim mmpychessbot.conf
	```
	Change the URL to your Mattermost server's, and copy the team's slug from a URL in its main interface, e.g. the `your-team` in `https://mattermost.your-domain.example/your-team/channels/town-square`.
7.	In Mattermost's main interface, open the _Integrations_ panel from the **⋮⋮⋮** menu, and add a bot account.
	It does not require any elevated privileges.
	Copy the access token it provides you back into the config file, and then save it and close your editor.
8.	Test the bot by sourcing the environment variables from the config, and running it (assuming the venv is still active), e.g.:
	```sh
	set -a && . mmpychessbot.conf && set +a
	python3	mm_chess_bot.py
	```
	If it starts running okay, switch to Mattermost, and challenge the bot account to a new game.
	<kbd>Ctrl</kbd> + <kbd>C</kbd> to terminate the script.
	Address any config issues until it works.
9.	Exit the bot account's shell.
10.	Copy the example service file to `/usr/local/lib/systemd/system/mmpychessbot.service`, adjusting the `User=` and/or file paths in that copy if you chose values different to the above.
11.	Enable and start the service:
	```sh
	sudo systemctl enable --now mmpychessbot
	```

## Play

Start games with the bot as you would any other team member.
If you can't see the bot account's icon to access its user menu, thus the _Challenge User to Chess_ link, create a DM channel with it.

You can “nudge” it into responding by `@`-mentioning its username in a game channel.

[1]: https://github.com/MatthewDorner/mattermost-plugin-chess
[2]: https://github.com/attzonko/mmpy_bot
[3]: https://github.com/niklasf/python-chess
[4]: https://stockfishchess.org/download/linux/
[5]: https://drive.google.com/drive/folders/1nzrHOyZMFm4LATjF5ToRttCU0rHXGkXI
