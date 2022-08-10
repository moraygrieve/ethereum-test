# script to build artifacts required for running tests 

script_path="$(cd "$(dirname "${0}")" && pwd)"
src_path="${script_path}/../go-obscuro"

# purge artifacts
echo Purging artifacts directory
rm ${script_path}/artifacts/wallet_extension*

# run the build
cd $src_path/tools/walletextension/main
echo Building GOOS=darwin GOARCH=amd64
env GOOS=darwin GOARCH=amd64 go build -o ${script_path}/artifacts/wallet_extension_macos_amd64 .

echo Building GOOS=darwin GOARCH=arm64
env GOOS=darwin GOARCH=arm64 go build -o ${script_path}/artifacts//wallet_extension_macos_arm64 .

echo Building GOOS=windows GOARCH=amd64
env GOOS=windows GOARCH=amd64 go build -o ${script_path}/artifacts//wallet_extension_win_amd64.exe .

echo Building GOOS=linux GOARCH=amd64
env GOOS=linux GOARCH=amd64 go build -o ${script_path}/artifacts//wallet_extension_linux_amd64 .