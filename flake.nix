{
  description = "Simple Python-based Nix Flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };
  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python310;  # or pkgs.python312
          pythonPackages = python.pkgs;
        in
        {
          default = pythonPackages.buildPythonApplication {
            pname = "my-app";
            version = "0.1.0";
            src = ./.;
            propagatedBuildInputs = [
              pythonPackages.click
              pythonPackages.requests
            ];
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python310;
          pythonPackages = python.pkgs;
        in
        {
          default = pkgs.mkShell {
            nativeBuildInputs = [
              python
              pythonPackages.click
              pythonPackages.requests
            ];
          };
        });
    };
}