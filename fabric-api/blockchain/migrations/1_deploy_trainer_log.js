
const TrainerLog = artifacts.require("TrainerLog");

module.exports = function (deployer) {
  deployer.deploy(TrainerLog);
};
