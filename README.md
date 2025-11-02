# JAMS
> JAMS Auto-Mute Sometimes

JAMS pause your music when you're watching a video on your browser.

## Why?
This is a rewrite of an old bash script I had, I'm no bash fan and I didn't like working on it but at least it got the job done for a while.

## Installation and use

### From the AUR
```bash 
yay -S jams
```

### For NixOS
Add it to your NixOS `flake.nix`

```nix
inputs = {
	jams = {
		url = "github:nevimmu/JAMS";
		inputs.nixpkgs.follows = "nixpkgs";
	};
	# ...
}
```

Then enable it in your home-manager configuration:

```nix
{
	programs.jams = {
		enable = true; # Enable jams
		autostart = true; # Autostart jams
		musicPlayer = "spotify" # Default music player
		browser = "firefox" # Default browser
	};
}
```

### From source
```bash
git clone https://github.com/nevimmu/jams
cd jams
pipx install .

jams -s # To setup the tool
jams # To run the tool
```