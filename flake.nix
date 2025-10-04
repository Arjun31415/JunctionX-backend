{
  description = "Python 3.11 development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems = {
      url = "github:nix-systems/default";
    };
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs = {nixpkgs, ...} @ inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];
      perSystem = {system, ...}: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        devShells.default =
          (pkgs.buildFHSEnv {
            name = "junction-shell";
            targetPkgs = pkgs: (with pkgs; [
              linuxPackages.nvidia_x11
              libGLU
              libGL
              xorg.libXi
              xorg.libXmu
              freeglut
              xorg.libXext
              xorg.libX11
              xorg.libXv
              xorg.libXrandr
              zlib
              ncurses5
              stdenv.cc
              binutils
              ffmpeg

              # I daily drive the fish shell
              # you can remove this, the default is bash
              fish
              cudaPackages.cudatoolkit
              cudaPackages.cudnn_8_9
            ]);

            profile = ''
              export LD_LIBRARY_PATH="${pkgs.linuxPackages.nvidia_x11}/lib"
              export CUDA_PATH="${pkgs.cudatoolkit}"
              export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
              export EXTRA_CCFLAGS="-I/usr/include"
            '';

            # again, you can remove this if you like bash
            runScript = "fish";
          }).env;
      };
    };
}
