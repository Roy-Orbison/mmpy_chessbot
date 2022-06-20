# mmpychessbot

[Matthew Dorner's chess plugin][1] for Mattermost makes it easy to play against your friends and colleagues, but has no built-in machine opponent.
This simple service built upon [Alex Tzonko's bot][2] and [Niklas Fiekas' chess library][3] allows you to add any machine opponent that uses the Universal Chess Interface.

## Installation

1. Create a system user on any machine that is always on, and has network access to your Mattermost service.
	This can be the same server that Mattermost is on. E.g.:
	```sh
	sudo adduser --system --group --shell /bin/bash chessbot
	```
2. On the same machine, download and install a UCI chess engine, like [Stockfish][4], to a location that user can access. E.g.:
	```sh
	wget https://stockfishchess.org/files/stockfish_15_linux_x64_bmi2.zip
	unzip stockfish_15_linux_x64_bmi2.zip
	sudo install stockfish_15_linux_x64_bmi2/stockfish_15_x64_bmi2 /usr/local/bin/stockfish
	```
	Ensure you choose a version that works on your CPU.
	You may need an [older Stockfish engine][5] for your system.
3.	Switch to your new user:
	```sh
	sudo -u chessbot -i
	cd
	```
4.	Install the python dependencies:
	```sh
	pip install -U chess mmpy-bot
	```
5.	Clone this repo:
	```sh
	git clone https://github.com/Roy-Orbison/mmpychessbot.git
	cd mmpychessbot/
	```
6.	Copy the example service conf file and open it for editing:
	```sh
	cp mmpychessbot.conf{.example,}
	vim mmpychessbot.conf
	```
	Change the URL to your Mattermost server's, and copy the team's slug from a URL in its main interface, e.g. the `your-team` in `https://mattermost.your-domain.example/your-team/channels/town-square`.
7.	In Mattermost's main interface, open the _Integrations_ panel from the **⋮⋮⋮** menu, and add a bot account. It does not require any elevated privileges. Copy the access token it provides you back into the `.conf` file and then save it and close your editor.
8.	If you chose a different username or home directory location in step 1, first make a copy of the example service file (as with the `.conf` example), and edit the `User=` and/or paths to match.
9.	`exit` the service account's shell. Copy the example or move your customised version of the service file to `/usr/local/lib/systemd/system/mmpychessbot.service`
10.	Enable and start the service:
	```sh
	sudo systemctl enable --now mmpychessbot
	```

## Play

Start a game with the bot account's username as you would any other team member. If you can't see the bot account's icon to access its user menu, thus the _Challenge User to Chess_ link, create a DM channel with it.

You can “nudge” it into responding by `@`-mentioning its username in a game channel.

[1]: https://github.com/MatthewDorner/mattermost-plugin-chess
[2]: https://github.com/attzonko/mmpy_bot
[3]: https://github.com/niklasf/python-chess
[4]: https://stockfishchess.org/download/linux/
[5]: https://stockfishchess.org/files/
