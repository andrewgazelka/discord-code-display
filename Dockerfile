FROM nixos/nix:2.16.1

# Create a working directory
WORKDIR /app

# Copy your Nix configuration or default.nix (if you’re using flakes, copy flake.nix)
COPY flake.nix .
COPY pyproject.toml uv.lock ./

# Install dependencies with Nix
RUN nix build .#devShellPackages -o /result
# Or if you use default.nix instead of a flake, something like:
# RUN nix-build --attr yourAttribute -o /result

# Activate the environment:
ENV PATH=/result/bin:$PATH

COPY . .

CMD ["python", "hello.py"]