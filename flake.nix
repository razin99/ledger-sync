{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          uv
          python314Packages.uv
          trufflehog
        ];
        shellHook = ''
          if [ -f .env ]; then
            source .env
          fi
        '';
      };
    }
  );
}
