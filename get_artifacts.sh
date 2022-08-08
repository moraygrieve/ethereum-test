# script to build artifacts required for running tests 

script_path="$(cd "$(dirname "${0}")" && pwd)"
src_path="${script_path}/../go-obscuro"

# run the build
cd $src_path/tools/walletextension/main
env GOOS=darwin GOARCH=amd64 go build -o ${script_path}/artifacts/wallet_extension_macos_amd64 .
env GOOS=darwin GOARCH=arm64 go build -o ${script_path}/artifacts//wallet_extension_macos_arm64 .
env GOOS=windows GOARCH=amd64 go build -o ${script_path}/artifacts//wallet_extension_win_amd64.exe .
env GOOS=linux GOARCH=amd64 go build -o ${script_path}/artifacts//wallet_extension_linux_amd64 .