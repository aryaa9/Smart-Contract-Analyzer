require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.0",
  paths: {
    sources: "./venv/contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};
