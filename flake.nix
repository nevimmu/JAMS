{
	description = "JAMS Auto-Mute Sometimes - Pauses your music when watching videos in browsers";

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
		pyproject-nix = {
			url = "github:nix-community/pyproject.nix";
			inputs.nixpkgs.follows = "nixpkgs";
		};
	};

	outputs = { self, nixpkgs, pyproject-nix, ... }:
		let
			inherit (nixpkgs) lib;

			# Define supported systems
			systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
			
			# Helper to generate attributes for each system
			forAllSystems = f: lib.genAttrs systems (system: f {
				pkgs = nixpkgs.legacyPackages.${system};
				inherit system;
			});

			project = pyproject-nix.lib.project.loadPyproject {
				# Read & unmarshal pyproject.toml relative to this project root.
				# projectRoot is also used to set `src` for renderers such as buildPythonPackage.
				projectRoot = ./.;
			};

		in
		{
			# Build our package using `buildPythonPackage` for all systems
			packages = forAllSystems ({ pkgs, system }: {
				default = 
					let
						python = pkgs.python3;
						# Returns an attribute set that can be passed to `buildPythonPackage`.
						attrs = project.renderers.buildPythonPackage { inherit python; };
					in
					# Pass attributes to buildPythonPackage with additional native dependencies
					python.pkgs.buildPythonPackage (attrs // {
						# dbus-python requires pkg-config and dbus development files
						nativeBuildInputs = (attrs.nativeBuildInputs or []) ++ (with pkgs; [
							pkg-config
						]);
						buildInputs = (attrs.buildInputs or []) ++ (with pkgs; [
							dbus
							glib
						]);
						
						meta = with lib; {
							description = "JAMS Auto-Mute Sometimes - Pauses your music when watching videos in browsers";
							homepage = "https://github.com/nevimmu/jams";
							license = licenses.mit;
							maintainers = [ ];
							platforms = platforms.linux; # JAMS uses D-Bus, likely Linux-specific
						};
					});
			});

			# Home Manager module for JAMS
			homeManagerModules.default = { config, lib, pkgs, ... }:
				let
					cfg = config.programs.jams;
				in
				{
					options.programs.jams = {
						enable = lib.mkEnableOption "JAMS Auto-Mute Sometimes";
						
						package = lib.mkOption {
							type = lib.types.package;
							default = self.packages.${pkgs.system}.default;
							description = "The JAMS package to use";
						};

						autostart = lib.mkOption {
							type = lib.types.bool;
							default = false;
							description = "Whether to autostart JAMS on login";
						};

						musicPlayer = lib.mkOption {
							type = lib.types.nullOr lib.types.str;
							default = null;
							description = "Default music player to use";
						};

						browser = lib.mkOption {
							type = lib.types.nullOr lib.types.str;
							default = null;
							description = "Default browser to use";
						};
					};

					config = lib.mkIf cfg.enable {
						home.packages = [ cfg.package ];

						# Create systemd user service for autostart
						systemd.user.services.jams = lib.mkIf cfg.autostart {
							Unit = {
								Description = "JAMS Auto-Mute Sometimes";
								After = [ "graphical-session-pre.target" ];
								PartOf = [ "graphical-session.target" ];
							};
							
							Install = {
								WantedBy = [ "graphical-session.target" ];
							};
							
							Service = {
								ExecStart = "${cfg.package}/bin/jams";
								Restart = "on-failure";
								RestartSec = 5;
								Type = "simple";
							};
						};

						# Pre-configure JAMS if settings are provided - create a template that will be copied
						home.file.".config/jams/jams.json.template" = lib.mkIf (cfg.musicPlayer != null && cfg.browser != null) {
							text = builtins.toJSON {
								music = cfg.musicPlayer;
								browser = cfg.browser;
								was_playing = false;
							};
						};
					};
				};

			# Development shell for working on the project
			devShells = forAllSystems ({ pkgs, system }: {
				default = 
					let
						python = pkgs.python3;
						# Get project dependencies from pyproject.toml
						attrs = project.renderers.buildPythonPackage { inherit python; };
					in
					pkgs.mkShell {
						buildInputs = with pkgs; [
							python3
							pkg-config
							dbus
							glib
							# Development tools
							python3Packages.black
							python3Packages.isort
							python3Packages.mypy
							python3Packages.pytest
							commitizen
							# Project dependencies
							python3Packages.questionary
							python3Packages.argcomplete
							python3Packages.dbus-python
							# Type stubs for better type checking
							python3Packages.types-setuptools
						];
						
						shellHook = ''
							echo "JAMS development environment"
							echo "Run 'nix run . -- -s' to setup the tool after installation"
						'';
					};
			});
		};
}
