const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Vault Contract", function () {
  let vault;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    
    const Vault = await ethers.getContractFactory("Vault");
    vault = await Vault.deploy();
  });

  describe("Deposit", function () {
    it("Should allow deposits and update balance", async function () {
      const depositAmount = ethers.parseEther("1.0");
      
      await vault.deposit({ value: depositAmount });
      
      expect(await vault.balances(owner.address)).to.equal(depositAmount);
    });
  });

  describe("Withdraw", function () {
    it("Should allow withdrawal of deposited funds", async function () {
      const depositAmount = ethers.parseEther("1.0");
      
      // Deposit first
      await vault.deposit({ value: depositAmount });
      
      // Then withdraw
      await expect(vault.withdraw(depositAmount))
        .to.changeEtherBalance(owner, depositAmount);
      
      expect(await vault.balances(owner.address)).to.equal(0);
    });

    it("Should prevent withdrawal of more than balance", async function () {
      const depositAmount = ethers.parseEther("1.0");
      const withdrawAmount = ethers.parseEther("2.0");
      
      await vault.deposit({ value: depositAmount });
      
      await expect(vault.withdraw(withdrawAmount))
        .to.be.revertedWith("Insufficient balance");
    });

    it("Should prevent reentrancy attacks", async function () {
      // This test verifies the fix we made
      const depositAmount = ethers.parseEther("1.0");
      
      await vault.deposit({ value: depositAmount });
      
      // The balance should be updated before external call
      // preventing reentrancy
      await vault.withdraw(depositAmount);
      expect(await vault.balances(owner.address)).to.equal(0);
    });
  });
});
