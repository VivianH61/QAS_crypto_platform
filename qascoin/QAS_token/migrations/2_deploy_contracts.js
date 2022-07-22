var QASToken = artifacts.require("./QASToken.sol");
var QASTokenSale = artifacts.require("./QASTokenSale.sol");

module.exports = function (deployer) {
  deployer.deploy(QASToken, 1000000).then(function() {
    // Token price is 0.001 Ether
    var tokenPrice = 1000000000000000;
    return deployer.deploy(QASTokenSale, QASToken.address, tokenPrice);
  });
};
