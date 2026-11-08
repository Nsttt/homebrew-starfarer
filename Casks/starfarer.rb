# notarized: false
cask "starfarer" do
  version "0.6.1"
  sha256 "fce01564cc7bc8bc90dedd390d1fb3153ac5c7789ed5418abf6f3d8de466e6e8"

  url "https://downloads.starfarer.ai/releases/v#{version}/Starfarer-aarch64.dmg"
  name "Starfarer"
  desc "Interplanetary coding agent harness"
  homepage "https://starfarer.ai/"

  livecheck do
    url "https://downloads.starfarer.ai/latest.json"
    strategy :json do |json|
      json.dig("macos", "tag")&.delete_prefix("v")
    end
  end

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "Starfarer.app"

  zap trash: [
    "~/Library/Application Support/Starfarer",
    "~/Library/Caches/com.nstlopez.starfarer",
    "~/Library/Preferences/com.nstlopez.starfarer.plist",
    "~/Library/Saved Application State/com.nstlopez.starfarer.savedState",
    "~/Library/WebKit/com.nstlopez.starfarer",
  ]

  caveats <<~EOS
    This preview is not notarized by Apple. If macOS blocks it, use
    System Settings > Privacy & Security > Open Anyway.

    Open Starfarer to install and start the bundled local planet daemon.
    Linux moons require Rosetta: softwareupdate --install-rosetta

    The daemon and sessions continue after closing or uninstalling the desktop.
    Upgrades keep the installed daemon runtime until you explicitly replace it.
    Planet data in ~/.local/share/starfarer is retained, including with --zap.
    Service and runtime upgrade instructions:
      https://github.com/nsttt/homebrew-starfarer#readme
  EOS
end
