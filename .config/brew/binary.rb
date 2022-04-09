# @binaryBrew [ModAnsibleAutodoc](https://github.com/megabyte-labs/mod-ansible-autodoc) - Generate documentation from comments in Ansible YML files
class ModAnsibleAutodoc < Formula
  desc "Generate documentation from comments in Ansible YML files"
  homepage "https://megabyte.space"
  url "https://github.com/megabyte-labs/mod-ansible-autodoc/releases/download/v1.0.0/mod-ansible-autodoc.tar.gz"
  version "1.0.0"
  license "MIT"

  

  def install
    os = OS.kernel_name.downcase
    arch = Hardware::CPU.intel? ? "amd64" : Hardware::CPU.arch.to_s
    bin.install "build/mod-ansible-autodoc-#{os}_#{arch}" => "mod-ansible-autodoc"
  done

  test do
    system bin/"mod-ansible-autodoc", "--version"
  end
end
